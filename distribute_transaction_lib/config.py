import os

from pydantic import BaseModel, Field
from mini_framework.design_patterns.singleton import singleton

#   接受注册 URL    启服务   这里读取所有的 URL    转入 路径  转出 路径  顺序

PREFIX = "transfer_"
LOCK_PATH = PREFIX + "/transfer_lock"
#   改为读取config

# 异常重试的 配置  回滚失败的补偿的 重试的次数 延迟时间
class RetryConfig(BaseModel):
    max_attempts: int = Field(..., description='最大重试次数')
    delay: float = Field(..., description='重试延迟时间')
    backoff: float = Field(..., description='重试延迟时间的指数')
    jitter: bool = Field(..., description='是否启用抖动')



@singleton
class TransactionServiceConfig:
    def __init__(self):
        from mini_framework.configurations import config_injection
        manager = config_injection.get_config_manager()
        # 读取 配置
        transaction_service_dict = manager.get_domain_config("transaction_service")
        if not transaction_service_dict:
            raise ValueError('transaction_service configuration is required')
        self.retry_config = RetryConfig(**transaction_service_dict.get('retry', {}))
        self.workflow_config =  transaction_service_dict.get('workflow')
        self.zookeeper_host_config =  transaction_service_dict.get('zookeeper_host')



transaction_service_config = TransactionServiceConfig()

"""
{
    "transaction_service": {
        "retry": {
            "max_attempts": 3,
            "delay": 1,
            "backoff": 2,
            "jitter": true
        },
         "workflow":  'fff.cc',
         "zookeeper_host":   "10.0.9.1:2181,10.0.9.2:2181,10.0.9.3:2181",
      
        
    }
}
"""
