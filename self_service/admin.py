"""Cloud operator CLI. Password entry is interactive; no defaults or chat delivery."""
import argparse
from getpass import getpass
import json
import os
from pathlib import Path
import re
from werkzeug.security import generate_password_hash
from .store import Store


def main():
    os.umask(0o077)
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['user','revoke'])
    parser.add_argument('username')
    parser.add_argument('--admin',action='store_true')
    args=parser.parse_args()
    if not re.fullmatch(r'[a-zA-Z0-9_-]{3,40}',args.username): parser.error('Use a workbench alias')
    config=json.loads(Path(os.environ['HUUUGE_WORKBENCH_CONFIG']).read_text())
    store=Store(Path(config['data_root'])/'state.sqlite3')
    if args.action=='user':
        password=getpass('设置工作台密码（不回显）: ')
        again=getpass('再次输入: ')
        if password!=again or len(password)<12: parser.error('两次密码需一致，至少12字符')
        with store.tx() as db:
            db.execute('''INSERT INTO users(name,password_hash,admin) VALUES (?,?,?)
                ON CONFLICT(name) DO UPDATE SET password_hash=excluded.password_hash,
                admin=excluded.admin,enabled=1''',(args.username,generate_password_hash(password),int(args.admin)))
    with store.tx() as db:
        db.execute('DELETE FROM auth WHERE user=?',(args.username,))
        if args.action=='revoke': db.execute('UPDATE users SET enabled=0 WHERE name=?',(args.username,))
        db.execute("UPDATE research SET desired=0,ticket=NULL,phase='stopping',state='start' WHERE owner=? AND lease=1",(args.username,))
    print('工作台身份已更新，旧登录已撤销；活动采集将受控收尾。')


if __name__=='__main__':main()
