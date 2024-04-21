from datetime import datetime

from sqlalchemy import String, DateTime
from sqlalchemy.orm import mapped_column, Mapped

from mini_framework.databases.entities import BaseDBModel


class Tasks(BaseDBModel):

    """
    任务表
    任务编号
    任务类型
    任务状态
    创建时间
    进度
    操作者
    完成日期



    """
    __tablename__ = 'lfun_tasks'
    __table_args__ = {'comment': '任务表'}

    id: Mapped[int] = mapped_column(primary_key=True, comment="班级ID",autoincrement=True)
    task_name: Mapped[str] = mapped_column(String(255),  nullable=True, comment="任务名称",default='')
    task_no: Mapped[str] = mapped_column(String(255),  nullable=True, comment="任务编号",default='')
    task_date: Mapped[str] = mapped_column(String(255),  nullable=True, comment="任务日期",default='')

    task_type: Mapped[str] = mapped_column(String(255),  nullable=True, comment="任务类型",default='')
    task_status: Mapped[str] = mapped_column(String(255),  nullable=True, comment="任务状态",default='')
    task_progress: Mapped[str] = mapped_column(String(255),  nullable=True, comment="任务进度",default='')
    task_remark: Mapped[str] = mapped_column(String(255),  nullable=True, comment="任务备注",default='')
    task_result: Mapped[str] = mapped_column(String(255),  nullable=True, comment="任务结果",default='')


    created_uid: Mapped[int] = mapped_column(  nullable=True , comment="创建人",default=0)
    updated_uid: Mapped[int] = mapped_column( nullable=True , comment="操作人",default=0)
    created_at = mapped_column(DateTime, default=datetime.now, nullable=False, comment="创建时间")
    updated_at = mapped_column(DateTime, onupdate=datetime.now, default=datetime.now, nullable=False, comment="更新时间")
    is_deleted: Mapped[bool] = mapped_column( nullable=False  , comment="删除态",default=False)





