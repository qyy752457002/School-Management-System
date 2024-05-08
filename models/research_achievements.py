from sqlalchemy import String, Date
from sqlalchemy.orm import mapped_column, Mapped
from mini_framework.databases.entities import BaseDBModel
from datetime import date

class ResearchAchievements(BaseDBModel):
    """
    research_achievements：research_achievements_id
    教师ID：teacher_id
    科研成果种类：research_achievement_type
    类型：type
    是否代表性成果或项目：representative_or_project
    名称：name
    学科领域：disciplinary_field
    本人角色：role
    日期：date
    批准号：approval_number
    经费额度：funding_amount
    开始年月：start_year_month
    结束日期：end_date
    本人排名：ranking
    委托单位：entrusting_unit
    来源：source
    出版社名称：publisher_name
    出版号：publication_number
    总字数：total_words
    本人撰写字数：self_written_words
    发表刊物名称：journal_name
    卷号：volume_number
    期号：issue_number
    论文收录情况：indexing_status
    起始页码：start_page
    结束页码：end_page
    本人排名：personal_rank
    等级：research_level
    其他等级：other_level
    授权国家：authorized_country
    授权单位：authorized_organization
    完成地点：completion_location
    本人工作描述：work_description
    专利号：patent_number
    委托方：entrusting_party
    证书号：certificate_number
    有效期：validity_period
    标准号：standard_number
    发布单位：publishing_organization
    删除状态：is_deleted
    """
    __tablename__ = 'lfun_research_achievements'
    __table_args__ = {'comment': 'research_achievements信息表'}

    research_achievements_id: Mapped[int] = mapped_column(primary_key=True, comment="research_achievementsID")
    teacher_id: Mapped[int] = mapped_column(nullable=False, comment="教师ID")
    research_achievement_type: Mapped[str] = mapped_column(String(64), nullable=False, comment="科研成果种类")
    type: Mapped[str] = mapped_column(String(64), nullable=True, comment="类型")
    representative_or_project: Mapped[bool] = mapped_column(nullable=True, comment="是否代表性成果或项目")
    name: Mapped[str] = mapped_column(String(64), nullable=True, comment="名称")
    disciplinary_field: Mapped[str] = mapped_column(String(64), nullable=True, comment="学科领域")
    role: Mapped[str] = mapped_column(String(64), nullable=True, comment="本人角色")
    research_date: Mapped[date] = mapped_column(Date, nullable=True, comment="日期")
    approval_number: Mapped[str] = mapped_column(String(64), nullable=True, comment="批准号")
    funding_amount: Mapped[str] = mapped_column(String(64), nullable=True, comment="经费额度")
    start_year_month: Mapped[date] = mapped_column(Date, nullable=True, comment="开始年月")
    end_date: Mapped[date] = mapped_column(Date, nullable=True, comment="结束日期")
    ranking: Mapped[str] = mapped_column(String(64), nullable=True, comment="本人排名")
    entrusting_unit: Mapped[str] = mapped_column(String(64), nullable=True, comment="委托单位")
    source: Mapped[str] = mapped_column(String(64), nullable=True, comment="来源")
    publisher_name: Mapped[str] = mapped_column(String(64), nullable=True, comment="出版社名称")
    publication_number: Mapped[str] = mapped_column(String(64), nullable=True, comment="出版号")
    total_words: Mapped[int] = mapped_column(nullable=True, comment="总字数")
    self_written_words: Mapped[int] = mapped_column(nullable=True, comment="本人撰写字数")
    journal_name: Mapped[str] = mapped_column(String(64), nullable=True, comment="发表刊物名称")
    volume_number: Mapped[int] = mapped_column(nullable=True, comment="卷号")
    issue_number: Mapped[int] = mapped_column(nullable=True, comment="期号")
    indexing_status: Mapped[str] = mapped_column(String(64), nullable=True, comment="论文收录情况")
    start_page: Mapped[int] = mapped_column(nullable=True, comment="起始页码")
    end_page: Mapped[int] = mapped_column(nullable=True, comment="结束页码")
    personal_rank: Mapped[str] = mapped_column(String(64), nullable=True, comment="本人排名")
    research_level: Mapped[str] = mapped_column(String(64), nullable=True, comment="等级")
    other_level: Mapped[str] = mapped_column(String(64), nullable=True, comment="其他等级")
    authorized_country: Mapped[str] = mapped_column(String(64), nullable=True, comment="授权国家")
    authorized_organization: Mapped[str] = mapped_column(String(64), nullable=True, comment="授权单位")
    completion_location: Mapped[str] = mapped_column(String(64), nullable=True, comment="完成地点")
    work_description: Mapped[str] = mapped_column(String(64), nullable=True, comment="本人工作描述")
    patent_number: Mapped[str] = mapped_column(String(64), nullable=True, comment="专利号")
    entrusting_party: Mapped[str] = mapped_column(String(64), nullable=True, comment="委托方")
    certificate_number: Mapped[str] = mapped_column(String(64), nullable=True, comment="证书号")
    validity_period: Mapped[date] = mapped_column(Date, nullable=True, comment="有效期")
    standard_number: Mapped[str] = mapped_column(String(64), nullable=True, comment="标准号")
    publishing_organization: Mapped[str] = mapped_column(String(64), nullable=True, comment="发布单位")
    is_deleted: Mapped[bool] = mapped_column(default=False, comment="是否删除")
    
