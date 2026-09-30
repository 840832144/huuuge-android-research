"""Fixed phone over restricted SSH reverse forwarding and pinned Frida TLS.

Tunnel installation is a deployment action. No cloud credentials or Web control.
"""
import hashlib
import os
from pathlib import Path
import re
import secrets
import shlex
import signal
import subprocess
import sys
import time
import uuid

from scripts import cloud_capture as cloud


def process_identity(pid):
    """PID reuse protection; a missing or zombie process is stopped."""
    try:
        fields=Path(f'/proc/{pid}/stat').read_text().rsplit(')',1)[1].split()
        if fields[0]=='Z': return None
        return dict(pid=int(pid),start=fields[19],
                    command=Path(f'/proc/{pid}/cmdline').read_bytes().hex())
    except FileNotFoundError:
        return None


def listeners(port):
    found=[]
    for table in ('tcp','tcp6'):
        for line in Path('/proc/net/'+table).read_text().splitlines()[1:]:
            fields=line.split();address,number=fields[1].split(':')
            if int(number,16)==port and fields[3]=='0A':
                found.append((table,address,int(fields[7])))
    return found


class CaptureRuntime:
    def __init__(self, config):
        self.config=config
        self.root=Path(config['data_root'])/'runtime'
        self.journal=self.root/'active.json'
        self.child=None
        self.log=None

    @property
    def binding(self):
        value=self.config.get('runtime')
        if not isinstance(value,dict): raise RuntimeError('受保护运行配置尚未部署。')
        return value

    def command(self,args,**kwargs):
        p=subprocess.run(args,capture_output=True,text=True,timeout=25,**kwargs)
        if p.returncode: raise RuntimeError('任务命令失败，保留私有运行记录。')
        return p.stdout.strip()

    def environment(self):
        env=os.environ.copy()
        for key in ('ADB_SERVER_SOCKET','ANDROID_ADB_SERVER_PORT','ADB_VENDOR_KEYS','ANDROID_USER_HOME','ANDROID_SDK_HOME'):
            env.pop(key,None)
        env.update(HOME=str(self.root/'home'),ANDROID_USER_HOME=str(Path(self.binding['adb_key']).parent),
                   ANDROID_SDK_HOME=str(self.root/'home'),ADB_VENDOR_KEYS=self.binding['adb_key'],ADB_MDNS_AUTO_CONNECT='')
        return env

    def adb(self,*args):
        c=self.binding['controller']
        return self.command([c['adb'],'-H','127.0.0.1','-P',str(c['adb_server_port']),
                             '-s',c['adb_serial'],*args],env=self.environment())

    def shell(self,script):
        return self.adb('shell','sh','-c',shlex.quote(script))

    def tunnel_ready(self):
        b=self.binding;c=b['controller']
        cloud.endpoint(c['adb_serial'],loopback=True)
        port=int(c['adb_serial'].rsplit(':',1)[1])
        if listeners(port)!=[('tcp','0100007F',b['tunnel_uid'])]:
            raise RuntimeError('限定SSH隧道的回环监听或身份不匹配。')

    def preflight(self):
        if sys.platform!='linux': raise RuntimeError('运行适配只在云端Linux执行。')
        b=self.binding;c=b['controller']
        if c.get('transport',{}).get('kind')!='ssh-adb-frida-tls':
            raise RuntimeError('必须明确使用SSH管理通道和Frida TLS。')
        if os.getuid()==0: raise RuntimeError('服务必须使用独立非root身份。')
        if type(b.get('tunnel_uid')) is not int or b['tunnel_uid'] in (0,os.getuid()):
            raise RuntimeError('隧道必须使用独立受限身份。')
        for path in (Path(b['adb_key']),Path(c['descriptors'])):
            if path.is_symlink() or not path.is_file(): raise RuntimeError('必要私有文件缺失。')
        key=Path(b['adb_key']).stat()
        if key.st_uid!=os.getuid() or key.st_mode & 0o077:
            raise RuntimeError('ADB密钥须为服务身份所有且0600，保留原绑定。')
        if hashlib.sha256(Path(c['descriptors']).read_bytes()).hexdigest()!=b['descriptor_sha256']:
            raise RuntimeError('descriptor与已核验版本不一致。')
        for name in ('phone_tools','phone_runs'):
            if not re.fullmatch(r'/data/local/tmp/task0037/[A-Za-z0-9_/-]+',b[name]) or '..' in b[name]:
                raise RuntimeError('只允许本任务手机目录。')
        if not re.fullmatch(r'[0-9a-f]{64}',b['device_serial_sha256']):
            raise RuntimeError('缺少固定目标校验值。')
        self.tunnel_ready()
        self.root.mkdir(parents=True,mode=0o700,exist_ok=True)
        cloud.cloud_only(dict(result_root=str(self.root)))
        if self.journal.exists(): raise RuntimeError('前轮运行尚未清理，保留采集锁。')
        cloud.write(self.root/'check.json',dict(c,result_root=str(self.root)))
        cloud.load_config(self.root/'check.json')
        for port in (c['adb_server_port'],int(c['frida_endpoint'].rsplit(':',1)[1])):
            if listeners(port): raise RuntimeError('任务端口已有监听，禁止接管。')

    def save(self,record):
        cloud.write(self.journal,record)

    def start_adb(self,record,check_game=True):
        c=self.binding['controller'];port=c['adb_server_port']
        if listeners(port): raise RuntimeError('未知ADB server，禁止接管。')
        (self.root/'home').mkdir(mode=0o700,exist_ok=True)
        self.log=(self.root/'adb.log').open('a',encoding='utf-8')
        self.child=subprocess.Popen([c['adb'],'-L',f'tcp:localhost:{port}','server','nodaemon'],
            env=self.environment(),stdout=self.log,stderr=subprocess.STDOUT,start_new_session=True)
        record['adb_process']=process_identity(self.child.pid)
        if not record['adb_process']: raise RuntimeError('ADB server提前退出。')
        self.save(record)
        for _ in range(50):
            observed=listeners(port)
            if observed==[('tcp','0100007F',os.getuid())]: break
            if observed or self.child.poll() is not None: raise RuntimeError('ADB监听不符合回环要求。')
            time.sleep(.1)
        else: raise RuntimeError('ADB server启动超时。')
        self.adb('connect',c['adb_serial'])
        self.verify_device(check_game)

    def verify_device(self,check_game=True):
        self.tunnel_ready()
        if self.adb('get-state')!='device': raise RuntimeError('ADB未授权或未就绪。')
        serial=self.adb('shell','getprop','ro.serialno')
        if not serial or hashlib.sha256(serial.encode()).hexdigest()!=self.binding['device_serial_sha256']:
            raise RuntimeError('隧道目标与本任务手机不一致。')
        if self.adb('shell','id','-u')!='0': raise RuntimeError('现有Root通道不可用。')
        if not check_game: return
        c=self.binding['controller']
        info=self.adb('shell','dumpsys','package',cloud.PACKAGE)
        for field,label in (('game_version','versionName'),('version_code','versionCode'),('abi','primaryCpuAbi')):
            match=re.search(r'\b'+label+r'=([^\s]+)',info)
            if not match or match[1]!=str(c[field]): raise RuntimeError('游戏版本或ABI变化。')
        if not self.adb('shell','pidof',cloud.PACKAGE).isdigit():
            raise RuntimeError('请在官方Web打开Huuuge并停留大厅。')

    def prepare_capture(self,directory):
        self.preflight()
        directory=Path(directory).resolve()
        if self.root.parent/'research' not in directory.parents: raise RuntimeError('片段目录不属于本任务。')
        b=self.binding;c=dict(b['controller']);run=uuid.uuid4().hex
        remote=b['phone_runs']+'/'+run
        record=dict(run=run,directory=str(directory),remote=remote,adb_process=None,forward=False)
        self.save(record)  # Write intent first. An unknown launch is recovered by cleanup, never replay.
        self.start_adb(record)
        tools=b['phone_tools'];q=shlex.quote
        self.shell(f'''set -eu
umask 077
[ "$(df -k {q(b['phone_runs'])} | awk 'END {{print $4}}')" -ge 262144 ]
mkdir {q(remote)}
export LD_LIBRARY_PATH={q(tools)}
{q(tools+'/openssl')} req -x509 -newkey rsa:2048 -nodes -days 1 -subj /CN=127.0.0.1 -addext subjectAltName=IP:127.0.0.1 -keyout {q(remote+'/key.pem')} -out {q(remote+'/cert.pem')} >{q(remote+'/tls.log')} 2>&1
cat {q(remote+'/key.pem')} {q(remote+'/cert.pem')} > {q(remote+'/server.pem')}
''')
        certificate=directory/'frida.crt';token=directory/'frida.token'
        self.adb('pull',remote+'/cert.pem',str(certificate))
        token.write_text(secrets.token_urlsafe(48),encoding='ascii');token.chmod(0o600)
        self.adb('push',str(token),remote+'/token')
        c['transport']=dict(c['transport'],certificate=str(certificate),token_file=str(token))
        c['result_root']=str(directory)
        launcher=directory/'phone-launch.sh'
        launcher.write_text(f'''#!/system/bin/sh
set -eu
umask 077
cd {q(remote)}
printf '%s ' "$$" > owner
awk '{{print $22}}' /proc/$$/stat >> owner
exec {q(tools+'/frida-server')} --listen=127.0.0.1:{c['transport']['device_port']} --certificate={q(remote+'/server.pem')} --token="$(cat token)" --disable-preload --ignore-crashes
''',encoding='utf-8')
        self.adb('push',str(launcher),remote+'/launch.sh')
        self.shell(f'set -eu; chmod 600 {q(remote)}/*; nohup sh {q(remote+"/launch.sh")} >{q(remote+"/frida.log")} 2>&1 </dev/null &')
        forward='tcp:'+c['frida_endpoint'].rsplit(':',1)[1]
        self.adb('forward','--no-rebind',forward,'tcp:'+str(c['transport']['device_port']))
        record['forward']=True;self.save(record)
        if listeners(int(c['frida_endpoint'].rsplit(':',1)[1]))!=[('tcp','0100007F',os.getuid())]:
            raise RuntimeError('Frida转发没有限定到回环。')
        for _ in range(30):
            try: cloud.verify_tls(c);break
            except (OSError,ValueError): time.sleep(.2)
        else: raise RuntimeError('Frida证书/TLS校验失败。')
        import frida
        if frida.__version__!=b['frida_version']: raise RuntimeError('Frida客户端版本漂移。')
        manager=frida.get_device_manager();endpoint=c['frida_endpoint']
        rejected=False
        try:
            invalid=manager.add_remote_device(endpoint,certificate=str(certificate),token='task0037-negative-token')
            invalid.query_system_parameters()
        except frida.InvalidArgumentError as error:
            rejected=str(error)=='incorrect token'
        finally:
            try: manager.remove_remote_device(endpoint)
            except frida.InvalidArgumentError: pass
        if not rejected: raise RuntimeError('错误令牌拒绝校验未通过。')
        device=manager.add_remote_device(endpoint,certificate=str(certificate),token=token.read_text().strip())
        try: device.query_system_parameters()
        finally: manager.remove_remote_device(endpoint)
        cloud.probe(c)
        cloud.write(directory/'runtime-check.json',dict(management='ssh-reverse-loopback',
                    capture='pinned-frida-tls-token',target_verified=True,checked=cloud.now()))
        return c

    def cleanup_capture(self):
        if not self.journal.exists(): return
        record=cloud.read(self.journal);b=self.binding;c=b['controller']
        if not re.fullmatch(r'[0-9a-f]{32}',record['run']) or record['remote']!=b['phone_runs']+'/'+record['run']:
            raise RuntimeError('运行路径不匹配，禁止清理。')
        expected=record.get('adb_process');actual=process_identity(expected['pid']) if expected else None
        if actual and actual!=expected: raise RuntimeError('ADB PID归属已改变，禁止停止。')
        if not actual:
            self.tunnel_ready();self.start_adb(record,check_game=False)
        self.verify_device(check_game=False)
        remote=record['remote'];q=shlex.quote
        output=self.shell(f'''set -eu
d={q(remote)}
if [ -d "$d" ]; then
 if [ -f "$d/owner" ]; then
  read p tick < "$d/owner"
  case "$p:$tick" in *[!0-9:]*) exit 41;; esac
  if [ -r /proc/$p/stat ]; then
   actual=$(awk '{{print $22}}' /proc/$p/stat)
   if [ "$actual" = "$tick" ] && [ "$(awk '{{print $3}}' /proc/$p/stat)" != Z ]; then
    [ "$(readlink /proc/$p/exe)" = {q(b['phone_tools']+'/frida-server')} ] || exit 42
    tr '\\000' '\\n' < /proc/$p/cmdline | grep -Fx -- {q('--certificate='+remote+'/server.pem')} >/dev/null || exit 43
    kill -TERM "$p"
    n=0
    while [ -r /proc/$p/stat ] && [ "$(awk '{{print $3 ":" $22}}' /proc/$p/stat)" != "Z:$tick" ] && [ "$(awk '{{print $22}}' /proc/$p/stat)" = "$tick" ]; do
     n=$((n+1)); [ "$n" -lt 15 ] || exit 44; sleep 1
    done
   fi
  fi
 fi
 if [ -f "$d/launch.sh" ] && [ ! -f "$d/owner" ]; then exit 45; fi
 rm -f "$d/key.pem" "$d/server.pem" "$d/token"
 [ ! -e "$d/key.pem" ] && [ ! -e "$d/server.pem" ] && [ ! -e "$d/token" ]
fi
printf cleaned
''')
        if output!='cleaned': raise RuntimeError('手机清理回读未确认。')
        forward='tcp:'+c['frida_endpoint'].rsplit(':',1)[1]
        mappings=[line.split() for line in self.adb('forward','--list').splitlines() if forward in line.split()]
        if mappings:
            if mappings!=[[c['adb_serial'],forward,'tcp:'+str(c['transport']['device_port'])]]:
                raise RuntimeError('转发归属不一致，禁止移除。')
            self.adb('forward','--remove',forward)
        self.adb('disconnect',c['adb_serial'])
        expected=record['adb_process'];actual=process_identity(expected['pid'])
        if actual:
            if actual!=expected: raise RuntimeError('ADB进程归属不一致。')
            os.kill(expected['pid'],signal.SIGTERM)
            for _ in range(50):
                if process_identity(expected['pid'])!=expected: break
                time.sleep(.1)
            else: raise RuntimeError('专用ADB server尚未退出。')
        if self.child: self.child.wait(timeout=5);self.child=None
        if self.log: self.log.close();self.log=None
        if listeners(c['adb_server_port']) or listeners(int(c['frida_endpoint'].rsplit(':',1)[1])):
            raise RuntimeError('专用端口仍有监听，保持采集锁。')
        directory=Path(record['directory'])
        if self.root.parent/'research' not in directory.resolve().parents: raise RuntimeError('本地片段路径不匹配。')
        (directory/'frida.token').unlink(missing_ok=True)
        cloud.write(directory/'cleanup.json',dict(verified=True,checked=cloud.now(),
                    phone_secrets_removed=True,owned_processes_stopped=True))
        self.journal.unlink()
