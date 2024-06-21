from sqlalchemy import String, Date, DateTime
from sqlalchemy.orm import mapped_column, Mapped
from mini_framework.databases.entities import BaseDBModel
from datetime import date, datetime


class UnitSystem(BaseDBModel):
    """
    # 各单位部署系统的 模型

    """
    __tablename__ = 'lfun_unit_system'
    __table_args__ = {'comment': '单位部署系统的 模型 '}

    id: Mapped[int] = mapped_column(primary_key=True, comment="",autoincrement=True)
    school_id: Mapped[int] = mapped_column( primary_key=False, comment="学校ID",nullable=True,default=0)
    institution_id: Mapped[int] = mapped_column(  comment="行政单位ID 例如区 市教育局",nullable=True,default=0)
    unit_url: Mapped[str] = mapped_column(String(255),comment="api地址",nullable=True,default='',)
    remark: Mapped[str] = mapped_column(String(40),comment="",nullable=True,default='')
    created_at: Mapped[datetime] = mapped_column(comment="创建时间",default=datetime.now)
    updated_at = mapped_column(DateTime, onupdate=datetime.now, default=datetime.now, nullable=False, comment="更新时间")
    is_deleted: Mapped[bool] = mapped_column( nullable=False  , comment="删除态",default=False)

    @staticmethod
    def seed():
        """
        # 填充数据
        :return:
        """
        return [
            UnitSystem(id=1, school_id=1, institution_id=0, unit_url="xxxx", remark="",created_at=datetime.now),
            UnitSystem(id=2, school_id=2, institution_id=0, unit_url="xxbbxx", remark="",created_at=datetime.now),
            ]