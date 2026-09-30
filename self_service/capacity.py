"""Bounded capture/export admission; never delete an existing result."""
from pathlib import Path
import shutil
import time


def size(path):
    path=Path(path)
    if not path.exists(): return 0
    total=0
    for entry in path.rglob('*'):
        if entry.is_symlink(): raise ValueError('Data directory contains a symlink')
        if entry.is_file(): total+=entry.stat().st_size
    return total


def check(config,row=None,export=False):
    root=Path(config['data_root'])
    if shutil.disk_usage(root).free < config.get('min_free_bytes',5*1024**3):
        return '磁盘可用空间不足；停止新增采集，保留已有数据。'
    if size(root)>=config.get('max_data_bytes',8*1024**3):
        return '本任务存储达到上限；保留已有数据，请联系维护者。'
    if row and not export:
        if time.time()-row['started']>=config.get('max_run_seconds',3600):
            return '本轮达到时长上限，正在停止保存。'
        if size(root/'research'/row['id'])>=config.get('max_batch_bytes',64*1024**2):
            return '本轮数据达到容量上限，正在停止保存。'
    if export and size(root/'exports')>=config.get('max_export_bytes',2*1024**3):
        return '导出容量达到上限；原始数据已保留，可维护后重试。'
    return ''
