# Historical SDK integration, inactive after User scope revision 2026-09-30.
"""Official Alibaba SDK binding, fixed single target, no browser command arguments.

Current standard-instance Ticket revocation is NOT proven. Admission fails closed.
Do not replace that gate with a UI flag or a successful Disconnect API response.
"""
import json
from pathlib import Path
import time


class SafetyGate(RuntimeError):
    pass


class Wuying:
    def __init__(self, config):
        from alibabacloud_eds_aic20230930.client import Client
        from alibabacloud_tea_openapi.models import Config
        from alibabacloud_credentials.client import Client as Credentials
        from alibabacloud_credentials.models import Config as CredentialConfig
        from alibabacloud_eds_aic20230930 import models
        self.models=models
        self.config=config
        # Explicit dedicated identity only; never fall back to owner OAuth/default profile.
        path=Path(config['credentials_file'])
        if path.is_symlink() or (path.stat().st_mode & 0o077):
            raise SafetyGate('管理身份文件权限不符合要求。')
        credentials=json.loads(path.read_text())
        if set(credentials)!={'access_key_id','access_key_secret'}:
            raise SafetyGate('需要本任务专用的受限云身份。')
        credential=Credentials(CredentialConfig(type='access_key',**credentials))
        self.client=Client(Config(credential=credential,endpoint='eds-aic.cn-shanghai.aliyuncs.com',
                                  region_id='cn-shanghai',protocol='https',
                                  read_timeout=10000,connect_timeout=5000))

    def describe(self):
        request=self.models.DescribeAndroidInstancesRequest(
            android_instance_ids=[self.config['instance_id']])
        rows=self.client.describe_android_instances(request).body.instance_model
        if len(rows)!=1 or rows[0].android_instance_id!=self.config['instance_id']:
            raise SafetyGate('云手机目标核验失败。')
        return rows[0]

    def preflight(self):
        phone=self.describe()
        if phone.android_instance_status!='RUNNING': raise SafetyGate('云手机当前不可用。')
        # Observed 2026-09-30: old Ticket reconnected after Disconnect; later 2507
        # is a gateway error, NOT an invalid-ticket proof. Keep this an implementation
        # gate until a vendor-supported revocation path is implemented and tested.
        raise SafetyGate('厂商旧控制凭证失效机制尚未通过验证，暂停自助开放。')

    def issue(self):
        response=self.client.batch_get_acp_connection_ticket(
            self.models.BatchGetAcpConnectionTicketRequest(instance_ids=[self.config['instance_id']]))
        rows=response.body.instance_connection_models
        if len(rows)!=1 or rows[0].instance_id!=self.config['instance_id']:
            raise SafetyGate('连接凭证目标不一致。')
        item=rows[0]
        if item.task_status!='Finished' or not item.ticket:
            raise SafetyGate('厂商尚未生成连接凭证；保留占用等待核验。')
        return dict(openType='inline',resourceType='local',connectType='app',
                    regionId='cn-hongkong',logDisabled=True,userInfo={'ticket':item.ticket},
                    appInfo=dict(osType='Android',appId='android',appInstanceId=item.app_instance_id,
                                 productType='AndroidCloud',loginRegionId='cn-hongkong',
                                 connectionProperties=json.dumps({'authMode':'Session'})),
                    uiConfig={'toolbar':{'visible':False},'vconsoleVisible':False})

    def revoke(self):
        self.client.disconnect_android_instance(self.models.DisconnectAndroidInstanceRequest(
            instance_ids=[self.config['instance_id']]))
        # Disconnecting an active stream is not equivalent to revoking its credential.
        raise SafetyGate('厂商已收到断连请求，但旧 Ticket 失效未确认；保持手机占用。')

    def prepare_capture(self, directory):
        self.preflight()  # do not start Frida/ADB while management protection is unresolved

    def cleanup_capture(self):
        # No production process is started before the explicit gates above pass.
        self.preflight()
