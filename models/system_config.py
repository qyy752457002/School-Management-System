from datetime import datetime

from sqlalchemy import String, DateTime, BigInteger
from sqlalchemy.orm import mapped_column, Mapped

from mini_framework.databases.entities import BaseDBModel


class SystemConfig(BaseDBModel):
    """
    """
    __tablename__ = 'lfun_system_config'
    __table_args__ = {'comment': '系统配置表'}

    id: Mapped[int] = mapped_column(BigInteger,primary_key=True, comment="ID",autoincrement=False)
    config_name: Mapped[str] = mapped_column(String(255),  nullable=True, comment="配置项",default='')
    config_code: Mapped[str] = mapped_column(String(255),  nullable=True, comment="配置项编码",default='')
    config_value: Mapped[str] = mapped_column(String(1024),  nullable=True, comment="配置项值",default='')
    config_remark: Mapped[str] = mapped_column(String(255),  nullable=True, comment="简述",default='')
    school_id: Mapped[int] = mapped_column(  nullable=True , comment="",default=0)
    created_uid: Mapped[int] = mapped_column(  nullable=True , comment="创建人",default=0)
    updated_uid: Mapped[int] = mapped_column( nullable=True , comment="操作人",default=0)
    created_at = mapped_column(DateTime, default=datetime.now, nullable=True, comment="创建时间")
    updated_at = mapped_column(DateTime, onupdate=datetime.now, default=datetime.now, nullable=True, comment="更新时间")
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
            SystemConfig(id= 2 ,config_name='班级导入模版', config_code='class_import_template', config_value='', config_remark='',school_id=0, created_uid=0, updated_uid=0, is_deleted=False),
            SystemConfig(id= 3 ,config_name='学生导入模版', config_code='student_import_template', config_value='', config_remark='',school_id=0, created_uid=0, updated_uid=0, is_deleted=False),
            SystemConfig(id= 4 ,config_name='学生家庭成员导入模版', config_code='student_familyinfo_import_template', config_value='', config_remark='',school_id=0, created_uid=0, updated_uid=0, is_deleted=False),
            SystemConfig(id= 5 ,config_name='教师导入模版', config_code='teacher_import_template', config_value='', config_remark='',school_id=0, created_uid=0, updated_uid=0, is_deleted=False),
            SystemConfig(id= 6 ,config_name='教师快捷信息导入模版', config_code='teacher_fastinfo_import_template', config_value='', config_remark='',school_id=0, created_uid=0, updated_uid=0, is_deleted=False),
            SystemConfig(id= 7 ,config_name='教师处分信息导入模版', config_code='teacher_punishmentinfo_import_template', config_value='', config_remark='',school_id=0, created_uid=0, updated_uid=0, is_deleted=False),
            SystemConfig(id= 8 ,config_name='教师岗位聘任 信息导入模版', config_code='teacher_jobinfo_import_template', config_value='', config_remark='',school_id=0, created_uid=0, updated_uid=0, is_deleted=False),
            SystemConfig(id= 9 ,config_name='教师工作经历 信息导入模版', config_code='teacher_workexperienceinfo_import_template', config_value='', config_remark='',school_id=0, created_uid=0, updated_uid=0, is_deleted=False),
            SystemConfig(id= 10 ,config_name='教师国内培训 信息导入模版', config_code='teacher_interstudyinfo_import_template', config_value='', config_remark='',school_id=0, created_uid=0, updated_uid=0, is_deleted=False),
            SystemConfig(id= 11 ,config_name='教师海外研修 信息导入模版', config_code='teacher_overseastudyinfo_import_template', config_value='', config_remark='',school_id=0, created_uid=0, updated_uid=0, is_deleted=False),
            SystemConfig(id= 12 ,config_name='教师技能证书 信息导入模版', config_code='teacher_skillinfo_import_template', config_value='', config_remark='',school_id=0, created_uid=0, updated_uid=0, is_deleted=False),
            SystemConfig(id= 13 ,config_name='教师奖励 信息导入模版', config_code='teacher_bonusinfo_import_template', config_value='', config_remark='',school_id=0, created_uid=0, updated_uid=0, is_deleted=False),
            SystemConfig(id= 14 ,config_name='教师交流轮岗 信息导入模版', config_code='teacher_rotationinfo_import_template', config_value='', config_remark='',school_id=0, created_uid=0, updated_uid=0, is_deleted=False),
            SystemConfig(id= 15 ,config_name='教师教师资格证 信息导入模版', config_code='teacher_qualificationinfo_import_template', config_value='', config_remark='',school_id=0, created_uid=0, updated_uid=0, is_deleted=False),
            SystemConfig(id= 16 ,config_name='教师教育教学 信息导入模版', config_code='teacher_teachinfo_import_template', config_value='', config_remark='',school_id=0, created_uid=0, updated_uid=0, is_deleted=False),
            SystemConfig(id= 17 ,config_name='教师 竞赛奖励信息导入模版', config_code='teacher_competitionrewardinfo_import_template', config_value='', config_remark='',school_id=0, created_uid=0, updated_uid=0, is_deleted=False),
            SystemConfig(id= 18 ,config_name='教师 科研项目信息导入模版', config_code='teacher_researchinfo_import_template', config_value='', config_remark='',school_id=0, created_uid=0, updated_uid=0, is_deleted=False),
            SystemConfig(id= 19 ,config_name='教师 论文信息导入模版', config_code='teacher_thesisinfo_import_template', config_value='', config_remark='',school_id=0, created_uid=0, updated_uid=0, is_deleted=False),
            SystemConfig(id= 20 ,config_name='教师年度考核 信息导入模版', config_code='teacher_kpiinfo_import_template', config_value='', config_remark='',school_id=0, created_uid=0, updated_uid=0, is_deleted=False),
            SystemConfig(id= 21 ,config_name='教师 人才项目信息导入模版', config_code='teacher_talentprojectinfo_import_template', config_value='', config_remark='',school_id=0, created_uid=0, updated_uid=0, is_deleted=False),
            SystemConfig(id= 22 ,config_name='教师师德 信息导入模版', config_code='teacher_ethicsinfo_import_template', config_value='', config_remark='',school_id=0, created_uid=0, updated_uid=0, is_deleted=False),
            SystemConfig(id= 23 ,config_name='教师 文艺作品信息导入模版', config_code='teacher_literaryinfo_import_template', config_value='', config_remark='',school_id=0, created_uid=0, updated_uid=0, is_deleted=False),
            SystemConfig(id= 24 ,config_name='教师 学习经历信息导入模版', config_code='teacher_learnexperienceinfo_import_template', config_value='', config_remark='',school_id=0, created_uid=0, updated_uid=0, is_deleted=False),
            SystemConfig(id= 25 ,config_name='教师 医药信息导入模版', config_code='teacher_medicineinfo_import_template', config_value='', config_remark='',school_id=0, created_uid=0, updated_uid=0, is_deleted=False),
            SystemConfig(id= 26 ,config_name='教师著作 信息导入模版', config_code='teacher_workinfo_import_template', config_value='', config_remark='',school_id=0, created_uid=0, updated_uid=0, is_deleted=False),
            SystemConfig(id= 27 ,config_name='教师 专利和软著信息导入模版', config_code='teacher_patentinfo_import_template', config_value='', config_remark='',school_id=0, created_uid=0, updated_uid=0, is_deleted=False),
            SystemConfig(id= 28 ,config_name='教师专业技术职务 信息导入模版', config_code='teacher_professionalinfo_import_template', config_value='', config_remark='',school_id=0, created_uid=0, updated_uid=0, is_deleted=False),

        ]
