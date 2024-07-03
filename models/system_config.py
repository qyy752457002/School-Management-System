from datetime import datetime

from sqlalchemy import String, DateTime
from sqlalchemy.orm import mapped_column, Mapped

from mini_framework.databases.entities import BaseDBModel


class SystemConfig(BaseDBModel):
    """
    """
    __tablename__ = 'lfun_system_config'
    __table_args__ = {'comment': '系统配置表'}

    id: Mapped[int] = mapped_column(primary_key=True, comment="ID",autoincrement=True)
    config_name: Mapped[str] = mapped_column(String(255),  nullable=True, comment="配置项",default='')
    config_code: Mapped[str] = mapped_column(String(255),  nullable=True, comment="配置项编码",default='')
    config_value: Mapped[str] = mapped_column(String(1024),  nullable=True, comment="配置项值",default='')
    config_remark: Mapped[str] = mapped_column(String(255),  nullable=True, comment="简述",default='')
    school_id: Mapped[int] = mapped_column(  nullable=True , comment="",default=0)
    created_uid: Mapped[int] = mapped_column(  nullable=True , comment="创建人",default=0)
    updated_uid: Mapped[int] = mapped_column( nullable=True , comment="操作人",default=0)
    created_at = mapped_column(DateTime, default=datetime.now, nullable=False, comment="创建时间")
    updated_at = mapped_column(DateTime, onupdate=datetime.now, default=datetime.now, nullable=False, comment="更新时间")
    is_deleted: Mapped[bool] = mapped_column( nullable=False  , comment="删除态",default=False)
    @staticmethod
    def seed():
        """
        # 填充数据
        :return:
        """
        return [
            SystemConfig(id= 1 ,config_name='学校导入模版', config_code='school_import_template', config_value='https://minio.f123.pub/k8s/%E5%AD%A6%E6%A0%A1%E5%BF%AB%E6%8D%B7%E4%BF%A1%E6%81%AF%E5%AF%BC%E5%85%A5%E6%A8%A1%E7%89%881.xlsx?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=N78DMATPEPLX3900EO4W%2F20240703%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20240703T073331Z&X-Amz-Expires=604800&X-Amz-Security-Token=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NLZXkiOiJONzhETUFUUEVQTFgzOTAwRU80VyIsImV4cCI6MTcxOTk5NTUzNiwicGFyZW50IjoieWFuZ2xqIn0.K9tRoyHVJ0XJkmsCzuVycyBjt76oxXPmDn6mRfyTApUuhCKsXlzboCs8qnSb9atCPc2jBSgmcooA4rc-CraTTA&X-Amz-SignedHeaders=host&versionId=null&X-Amz-Signature=be91582833babbef801f5f81d7a2264e8a14453f96fff87757071e9e692ecad3', config_remark='',
                         school_id=0, created_uid=0, updated_uid=0, is_deleted=False),


        ]





