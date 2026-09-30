"""Build a new allowlisted value-bearing copy. Never zip a capture directory."""
from collections import Counter
import csv
from datetime import datetime, timezone
import io
import json
import os
from pathlib import Path
import re
import tempfile
import zipfile

from scripts.build_rpc_inventory import classify, collect_field_paths, write_inventory

RULE_VERSION = 'huuuge-v1-1'
# Exact payload type and field paths; unknown fields/types never leave the server.
# Meanings below are intentionally conservative: protocol amounts are not USD or RTP.
RULES = {
    'Casino.JoinGameRequest': {'game_name':'alias','reconnect':'bool'},
    'Casino.JoinGameResponse': {'game_mode':'enum','status':'enum'},
    'Casino.SlotsProto.SpinRequest': {'bet':'integer','auto':'bool','max_bet_btn':'bool'},
    'Casino.SlotsProto.SpinResponse': {
        'cash.value':'integer','legacy_cash':'integer','jackpot':'bool','stop[]':'integer',
        'free_spins.cash.value':'integer','free_spins.legacy_cash':'integer',
        'free_spins.spin_count':'integer','bonus.cash.value':'integer',
        'bonus.legacy_cash':'integer','bonus.result[]':'integer'},
    'Casino.UpdateProgressRequest': {
        'level':'integer','xp':'number','xp_level':'number',
        'mini_game_event_progress.event_id':'integer',
        'mini_game_event_progress.moves':'integer',
        'mini_game_event_progress.current_sum_of_bets.value':'integer',
        'mini_game_event_progress.required_sum_of_bets.value':'integer',
        'rewards_data.reward[].chips_delta':'integer',
        'rewards_data.reward[].big_chips_delta.value':'integer',
        'rewards_data.reward[].loyalty_points':'integer',
        'rewards_data.reward[].charms_trade_token_delta':'integer',
        'rewards_data.reward[].collectibles_box.box_id':'integer',
        'rewards_data.reward[].collectibles_box.box_type':'integer',
        'rewards_data.reward[].collectibles_box.theme_id':'integer'},
}
ENDPOINTS = {
    ('AppServer','JoinGame','REQUEST'):'Casino.JoinGameRequest',
    ('AppServer','JoinGame','RESPONSE'):'Casino.JoinGameResponse',
    ('SlotsGameServer','Spin','REQUEST'):'Casino.SlotsProto.SpinRequest',
    ('SlotsGameServer','Spin','RESPONSE'):'Casino.SlotsProto.SpinResponse',
    ('SlotsGameServer','FreeSpin','RESPONSE'):'Casino.SlotsProto.SpinResponse',
    ('AppClient','UpdateProgress','REQUEST'):'Casino.UpdateProgressRequest',
}
DROP = object()


def sanitize(data, rules, aliases, omitted, prefix=''):
    if isinstance(data,dict):
        result={}
        for key,value in data.items():
            path=f'{prefix}.{key}' if prefix else key
            out=sanitize(value,rules,aliases,omitted,path)
            if out is not DROP: result[key]=out
        return result if result else DROP
    if isinstance(data,list):
        result=[]
        for value in data:
            out=sanitize(value,rules,aliases,omitted,prefix+'[]')
            # Keep array order/positions when some records contain only omitted fields.
            result.append(None if out is DROP else out)
        return result if any(v is not None for v in result) else DROP
    kind=rules.get(prefix)
    if kind=='integer' and type(data) in (int,str) and re.fullmatch(r'-?\d{1,150}',str(data)):
        return str(data)  # lossless even in JavaScript consumers
    if kind=='bool' and type(data) is bool: return data
    if kind=='number' and type(data) in (int,float):
        import math
        if math.isfinite(data): return data
    if kind=='enum' and isinstance(data,str) and re.fullmatch(r'[A-Z][A-Z_0-9]{0,63}',data):
        return data
    if kind=='alias' and isinstance(data,str) and data:
        key=(prefix,data)
        if key not in aliases: aliases[key]='machine-'+str(len(aliases)+1)
        return aliases[key]
    omitted['omitted_or_invalid_scalar_values']+=1
    return DROP


def dump(value): return json.dumps(value,ensure_ascii=False,allow_nan=False,indent=2)


def build(root, research, segments, metadata):
    """Segments are sealed worker records, not request paths. Publishing is atomic."""
    root=Path(root).resolve()
    if metadata['evidence_kind'] not in ('observed-live','synthetic'):
        raise ValueError('explicit evidence kind required')
    if research['desired'] or not research['ended']:
        raise ValueError('Research capture must be stopped and read back')
    sid=research['id']
    if not re.fullmatch(r'research-[0-9a-f]{24}',sid): raise ValueError('invalid research id')
    exports=root/'exports'; exports.mkdir(mode=0o700,exist_ok=True)
    target=exports/(sid+'.zip')
    if target.is_file(): return target  # published snapshot is immutable
    all_rows=[]; records=[]; field_counts=Counter(); omitted=Counter(); aliases={}; pairs={}
    spans=[]
    for n,segment in enumerate(segments,1):
        segment_root=(root/'research'/sid/segment['id']).resolve()
        if not segment_root.is_relative_to(root/'research'/sid): raise ValueError('outside research')
        sealed=json.loads((segment_root/'sealed.json').read_text())
        if sealed['segment_id']!=segment['id'] or sealed['research_id']!=sid:
            raise ValueError('seal ownership mismatch')
        capture=sealed.get('capture_directory')
        messages=[]
        if capture:
            if not re.fullmatch(r'cloud-\d{8}T\d{6}-[0-9a-f]{12}',capture): raise ValueError('invalid capture reference')
            source=segment_root/capture/'messages.jsonl'
            if source.is_symlink(): raise ValueError('symlink input')
            if metadata['evidence_kind']=='observed-live':
                original=json.loads((source.parent/'manifest.json').read_text())
                if (original['game_version']!=metadata['game_version']
                    or original['source_revision']!=metadata['collector_revision']
                    or original['descriptor_sha256']!=metadata['schema_version']):
                    raise ValueError('source/schema version differs from export metadata')
            with source.open(encoding='utf-8') as handle:
                for line in handle:
                    if line.strip(): messages.append(json.loads(line))
        count=len(messages); decoded=sum(r.get('decoded') is True for r in messages)
        if count!=sealed['capture'] or decoded!=sealed['decoded']:
            raise ValueError('sealed counts disagree with saved records')
        spans.append({'segment':f'segment-{n}','capture':count,'decoded':decoded,
                      'failed':count-decoded,'state':sealed['state'],
                      'started':segment['started'],'ended':segment['ended'],
                      'gap_reason':segment['reason']})
        for position,raw in enumerate(messages,1):
            if raw['seq']!=position: raise ValueError('sequence mismatch')
            service=raw.get('service') or 'Unknown'; method=raw.get('method') or 'Unknown'
            payload=raw.get('payload_type') or 'Unknown'
            # Decoder-generated identifiers only; unknown metadata is represented as Unknown.
            service,method,payload=[v if isinstance(v,str) and re.fullmatch(r'[A-Za-z][A-Za-z0-9_.]{0,160}',v)
                                    else 'Unknown' for v in (service,method,payload)]
            rpc=raw.get('rpc_type') if raw.get('rpc_type') in ('REQUEST','RESPONSE') else 'UNKNOWN'
            direction=raw.get('direction') if raw.get('direction') in ('in','out') else 'unknown'
            timestamp=datetime.fromisoformat(raw['time']).isoformat(timespec='milliseconds')
            seq=raw.get('seq_number'); pair=None
            if type(seq) is int:
                key=(n,service,method,seq)
                if key not in pairs: pairs[key]='rpc-'+str(len(pairs)+1)
                pair=pairs[key]
            rules=RULES.get(payload,{}) if ENDPOINTS.get((service,method,rpc))==payload else {}
            data=sanitize(raw.get('data'),rules,aliases,omitted)
            data={} if data is DROP else data
            record={'segment':f'segment-{n}','sequence':position,'time':timestamp,
                    'service':service,'method':method,'rpc_type':rpc,'direction':direction,
                    'payload_type':payload,'pair_alias':pair,'decoded':raw.get('decoded') is True,
                    'evidence':metadata['evidence_kind'],'data':data,'values_omitted':not bool(data)}
            records.append(record)
            for path,kind in collect_field_paths(data):
                field_counts[(service,method,payload,path,kind)]+=1
            size=raw.get('payload_bytes',0)
            all_rows.append(dict(service=service,method=method,payload_type=payload,rpc_type=rpc,
                                 direction=direction,time=timestamp,decoded='1' if record['decoded'] else '0',
                                 payload_bytes=str(size if type(size) is int and size>=0 else 0)))
    if len(records)!=research['capture'] or sum(r['decoded'] for r in records)!=research['decoded']:
        raise ValueError('research counters disagree with sealed segments')
    manifest={
        'package_version':1,'game_key':'huuuge','shared_game_account':True,
        'evidence_kind':metadata['evidence_kind'],
        'research_account_alias':'huuuge-shared-1','research_session_alias':sid,
        'game_version':metadata['game_version'],'collector_revision':metadata['collector_revision'],
        'schema_version':metadata['schema_version'],'timezone':metadata['timezone'],
        'started':research['started'],'ended':research['ended'],
        'capture_count':len(records),'decoded_count':sum(r['decoded'] for r in records),
        'decode_failed_count':sum(not r['decoded'] for r in records),
        'integrity':'finalized' if research['complete'] else 'incomplete',
        'segments':spans,'redaction_rules':RULE_VERSION,'omissions':dict(omitted),
        'coverage':'Only listed segments; preparation and gaps are not captured.',
        'integer_encoding':'decimal strings, exact; protocol amounts are not USD',
        'files':['README_FOR_AI.md','manifest.json','summary.md','rpc_inventory.csv',
                 'field_paths.csv','decoded/messages.jsonl','reference/field_dictionary.json',
                 'reference/module_map.json']}
    with tempfile.TemporaryDirectory(prefix='.export-',dir=exports) as temporary:
        tmp=Path(temporary)
        if all_rows: write_inventory(all_rows,tmp/'rpc_inventory.csv')
        else: (tmp/'rpc_inventory.csv').write_text('service,method,count\n')
        with (tmp/'field_paths.csv').open('w',encoding='utf-8',newline='') as handle:
            writer=csv.writer(handle); writer.writerow(['service','method','payload_type','field_path','value_type','messages_seen'])
            for key,count in sorted(field_counts.items()): writer.writerow([*key,count])
        dictionary={'rules_version':RULE_VERSION,'evidence':'schema-only until observed in field_paths.csv',
                    'fields':RULES,'meaning':{
                        'bet':'Spin请求中的下注值；保留协议原单位，不换算USD。',
                        'cash / legacy_cash':'Spin响应金额字段；具体奖励/余额语义须结合请求和观察，不能仅按名称判定净收益。',
                        'stop[]':'协议中的轮轴停止位置索引。',
                        'jackpot':'本条响应的布尔标记，不代表长期概率。',
                        'free_spins.spin_count':'本条响应记录的免费转次数。',
                        'game_name':'包内机台别名，仅用于区分和关联。',
                        'pair_alias':'按片段、service/method、RPC序号配对；null表示无序号，不猜配对。'}}
        modules={m:classify(m.split('.')[0],m.split('.')[1]) for m in sorted({
            r['service']+'.'+r['method'] for r in records})}
        readme=Path(__file__).with_name('README_FOR_AI.md').read_text(encoding='utf-8')
        if metadata['evidence_kind']=='synthetic':
            readme='> 合成样例：不含真实游戏采集，不能用于V1验收或业务结论。\n\n'+readme
        package=tmp/'package.zip'
        with zipfile.ZipFile(package,'x',compression=zipfile.ZIP_DEFLATED) as z:
            z.writestr('README_FOR_AI.md',readme)
            z.writestr('manifest.json',dump(manifest))
            z.writestr('summary.md',f"# 采集包统计\n\n证据类型：{metadata['evidence_kind']}。\n\n捕获 {manifest['capture_count']}；解码成功 {manifest['decoded_count']}；失败 {manifest['decode_failed_count']}。\n\n完整性：{manifest['integrity']}。共 {len(spans)} 个片段；以 manifest 中的缺口为准。\n\n包内覆盖："+', '.join(modules)+'。\n')
            z.write(tmp/'rpc_inventory.csv','rpc_inventory.csv'); z.write(tmp/'field_paths.csv','field_paths.csv')
            z.writestr('decoded/messages.jsonl',''.join(json.dumps(r,ensure_ascii=False,allow_nan=False)+'\n' for r in records))
            z.writestr('reference/field_dictionary.json',dump(dictionary))
            z.writestr('reference/module_map.json',dump({'evidence':'inferred from endpoint names','modules':modules}))
        with zipfile.ZipFile(package) as z:
            if z.testzip() is not None or len(z.namelist())!=8: raise ValueError('archive readback failed')
            if json.loads(z.read('manifest.json'))!=manifest: raise ValueError('manifest readback failed')
        with package.open('r+b') as handle: os.fsync(handle.fileno())
        os.replace(package,target)
    return target
