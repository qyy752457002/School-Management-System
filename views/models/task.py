from datetime import datetime
from enum import Enum
from typing import Final

from mini_framework.async_task.task.task import Task
from pydantic import BaseModel, Field

class TaskActionType(str, Enum):
    """
    """
    START = "start"
    STOP = "stop"
    CANCEL = "cancel"

    @classmethod
    def to_list(cls):
        return [cls.START, cls.STOP, cls.CANCEL]

class TaskModel(Task):
    """
    使用框架里的tasks模型 这儿不使用   扩展2个字段 给前段下载用 每次分页后端去获取得到URL
    download_task_result_url 任务结果文件，download_task_source_file_url 源文件

    """
    download_task_result_url: str|None = Field(None, description="任务结果文件")  # 任务ID
    download_task_source_file_url: str|None = Field(None, description="源文件")  # 任务ID

