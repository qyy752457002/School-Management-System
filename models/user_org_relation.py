from mini_framework.databases.entities import BaseDBModel
from sqlalchemy import String, BigInteger
from sqlalchemy.orm import mapped_column, Mapped


class UserOrgRelation(BaseDBModel):
    """


    """
    __tablename__ = 'lfun_user_org_relation'
    __table_args__ = {'comment': '组织中心用户关联表'}

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, comment="", autoincrement=False)
    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=False, comment="用户ID", nullable=True, default=0)
    org_id: Mapped[str] = mapped_column(String(255), comment="组织ID", nullable=True, default=0)
