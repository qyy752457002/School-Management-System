from datetime import datetime

from sqlalchemy import String, DateTime, BigInteger
from sqlalchemy.orm import mapped_column, Mapped

from mini_framework.databases.entities import BaseDBModel


class LeaderInfo(BaseDBModel):

    """
    领导表

领导姓名
leader_name
职务
position
状态
status
任职开始时间
start_date
任职结束时间
end_date
工作内容
job_content
分管工作
job_responsibility
学校ID
school_id
事业单位ID
institution_id
    """
    __tablename__ = 'lfun_leader_info'
    __table_args__ = {'comment': '领导表'}

    id: Mapped[int] = mapped_column(BigInteger,primary_key=True, comment="班级ID",autoincrement=False)
    planning_school_id: Mapped[int] = mapped_column( BigInteger, nullable=True , comment="规划ID",default=0)
    leader_name: Mapped[str] = mapped_column(String(20),  nullable=True, comment="领导姓名",default='')
    position: Mapped[str] = mapped_column(String(255),  nullable=True, comment="职务",default='')
    status: Mapped[str] = mapped_column(String(255),  nullable=True, comment="状态",default='')
    start_date: Mapped[str] = mapped_column(String(20),default=''  , nullable=False, comment="任职开始时间")
    end_date: Mapped[str] = mapped_column(String(20),default='',   nullable=False, comment="任职结束时间")
    job_content: Mapped[str] = mapped_column(String(255),  nullable=True, comment="工作内容",default='')
    job_responsibility: Mapped[str] = mapped_column(String(255),  nullable=True, comment="分管工作",default='')
    school_id: Mapped[int] = mapped_column(BigInteger,  nullable=True , comment="学校ID",default=0)
    institution_id: Mapped[int] = mapped_column(BigInteger,  nullable=True , comment="事业单位ID",default=0)
    identity: Mapped[str] = mapped_column(String(64), nullable=True, comment="身份",default='')

    created_uid: Mapped[int] = mapped_column(  nullable=True , comment="创建人",default=0)
    updated_uid: Mapped[int] = mapped_column( nullable=True , comment="操作人",default=0)
    created_at = mapped_column(DateTime, default=datetime.now, nullable=False, comment="创建时间")
    updated_at = mapped_column(DateTime, onupdate=datetime.now, default=datetime.now, nullable=False, comment="更新时间")
    is_deleted: Mapped[bool] = mapped_column( nullable=False  , comment="删除态",default=False)





