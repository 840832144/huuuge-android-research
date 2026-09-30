"""Protected cloud runtime binding still awaiting implementation and verification.

Unlike the historical SDK adapter, this does not create, revoke, or disconnect
official Web phone sessions, and does not load any cloud identity by default.
"""


class CaptureRuntime:
    def __init__(self, config):
        self.config = config

    def preflight(self):
        # Do not substitute the old unencrypted public ADB path or a boolean flag.
        raise RuntimeError('受保护采集连接与云端运行适配尚未完成，暂不启动。')

    def prepare_capture(self, directory):
        self.preflight()

    def cleanup_capture(self):
        # No process can be started by this binding yet; never claim verified cleanup.
        raise RuntimeError('本次采集进程清理尚未核验，保留采集锁。')
