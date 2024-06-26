from datetime import datetime
from enum import Enum
from typing import Final

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

class Task(BaseModel):
    """
    使用框架里的tasks模型 这儿不使用

    """

    id: int = Field(0, title="",description="id",examples=['1'])







