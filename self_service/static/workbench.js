'use strict';
const $ = id => document.getElementById(id);
const page = crypto.randomUUID();
let csrf = '', current = null, lastUpdate = 0;
let pendingDownload = null, polling = false, ownsCapturePage = false;
const states = {start:'● 开始采集',collecting:'● 采集中',error:'⚠ 采集错误',ended:'■ 采集结束 · 已保存'};
const phases = {queued:'正在准备',connecting:'正在连接游戏',preflight:'正在检查采集条件',
  starting:'探针准备中；可正常进入大厅，尚未开始记录',active:'采集正常；暂时没有新消息时等待新数据',
  stopping:'正在停止并保存',packaging:'正在打包',saved:'结果已保存，可下载',
  recovery:'正在恢复采集；中断时间将记录为缺口'};
function message(text){$('message').textContent=text || '';}
async function api(path, data){
  const options={credentials:'same-origin',headers:{}};
  if(data !== undefined){options.method='POST';options.headers={'Content-Type':'application/json','X-CSRF-Token':csrf};options.body=JSON.stringify(data);}
  const response=await fetch(path,options);
  const result=await response.json();
  if(!response.ok){if(response.status===401) showLogin();throw new Error(result.error || '请求失败，已有数据保留。');}
  return result;
}
function showLogin(){ownsCapturePage=false;$('login').hidden=false;$('workspace').hidden=true;$('logout').hidden=true;csrf='';}
async function signedIn(){const who=await api('api/me');csrf=who.csrf;$('login').hidden=true;$('workspace').hidden=false;$('logout').hidden=false;message('');await refresh();}
$('login-form').onsubmit=async event=>{event.preventDefault();const form=new FormData(event.target);try{
  const result=await api('api/login',{username:form.get('username'),password:form.get('password'),remember:form.has('remember')});
  csrf=result.csrf;event.target.reset();await signedIn();
}catch(e){message(e.message);}};
$('logout').onclick=async()=>{try{await api('api/logout',{});showLogin();}catch(e){message(e.message);}};
$('start').onclick=async()=>{if($('start').disabled)return;$('start').disabled=true;try{
  const result=await api('api/start',{page});current=result.id;ownsCapturePage=true;await refresh();
}catch(e){message(e.message);}finally{$('start').disabled=false;}};
async function control(action){if(!current)return;return api(`api/session/${current}/${action}`,{page});}
$('restore').onclick=async()=>{try{await control('claim');ownsCapturePage=true;message('已恢复本批采集面板，游戏继续在官方Web操作。');await refresh();}catch(e){message(e.message);}};
$('retry').onclick=async()=>{try{await control('retry');message('已申请重连，旧片段和缺口保留。');}catch(e){message(e.message);}};
$('stop').onclick=async()=>{if(!current)return;$('stop').disabled=true;try{await control('stop');pendingDownload=current;await refresh();}catch(e){message(e.message);}finally{$('stop').disabled=false;}};
function download(sid){const a=document.createElement('a');a.href=`api/download/${sid}`;a.download='';document.body.append(a);a.click();a.remove();}
function render(data){
  const active=data.sessions.find(r=>r.lease);const row=active || data.sessions.find(r=>r.id===current) || data.sessions[0];
  current=row?.id || null;
  const state=row?.state || 'start';$('state').className='badge '+state;$('state').textContent=states[state] || states.error;
  $('detail').textContent=row?.error || phases[row?.phase] || (data.busy?'已有采集任务进行中或正在收尾。':'先在官方Web进入Huuuge大厅，再点击开始采集。');
  if(!data.enabled && !active)$('detail').textContent='服务准备未完成，维护者正在核验使用条件。';
  $('start').disabled=data.busy || !data.enabled;
  $('stop').hidden=!active;$('restore').hidden=!active || ownsCapturePage;
  $('retry').hidden=!active || state!=='error';
  $('download').hidden=!row?.downloadable;
  if(row?.downloadable)$('download').href=`api/download/${row.id}`;
  $('started').textContent=row?new Date(row.started*1000).toLocaleString():'—';
  $('elapsed').textContent=row?Math.max(0,Math.floor(((row.ended || data.server_time)-row.started)/60))+' 分钟':'—';
  $('capture').textContent=row?.capture ?? 0;$('decode').textContent=`${row?.decoded ?? 0} / ${row?.failed ?? 0}`;
  $('updated').textContent=row?.worker_seen?new Date(row.worker_seen*1000).toLocaleTimeString():'—';
  $('history').replaceChildren();
  for(const item of data.sessions){
    const li=document.createElement('li'),text=document.createElement('span');text.textContent=`${new Date(item.started*1000).toLocaleString()} · ${states[item.state]} · ${item.capture} 条${item.complete?'':' · 完整性待确认或含缺口'}`;li.append(text);
    if(item.downloadable){const link=document.createElement('a');link.textContent='下载数据';link.href=`api/download/${item.id}`;li.append(link);}
    else if(item.export_state==='failed'){const button=document.createElement('button');button.textContent='重试导出';button.onclick=async()=>{try{await api(`api/session/${item.id}/export`,{});await refresh();}catch(e){message(e.message);}};li.append(button);}
    $('history').append(li);
  }
  if(pendingDownload && data.sessions.some(r=>r.id===pendingDownload && r.downloadable)){download(pendingDownload);pendingDownload=null;}
  if(!active)ownsCapturePage=false;
  return active;
}
async function refresh(){
  if(polling || !csrf)return;polling=true;
  try{const data=await api('api/status');lastUpdate=Date.now();const active=render(data);
    if(active && ownsCapturePage){try{await control('heartbeat');}catch(e){ownsCapturePage=false;message(e.message);}}
  }catch(e){message(e.message);}finally{polling=false;}
}
setInterval(refresh,2000);
setInterval(()=>{if(csrf && lastUpdate && Date.now()-lastUpdate>10000){$('state').className='badge error';$('state').textContent=states.error;$('detail').textContent='状态连接中断，采集是否继续待确认。';}},1000);
signedIn().catch(()=>showLogin());
