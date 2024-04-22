from pydantic import BaseModel, Field
from datetime import date

class TeacherLearnExperienceModel(BaseModel):
    """
    教师ID：teacher_id
    获的学历：education_obtained
    获得学历国家/地区：country_or_region_of_education
    获得学历的院校机构：institution_of_education_obtained
    所学妆业：major_learned
    是否师范类专业：is_major_normal
    入学时间：admission_date
    毕业时间：graduation_date
    学位层次：degree_level
    获取学位过家地区：country_or_region_of_degree_obtained
    获得学位院校机构：institution_of_degree_obtained
    学位授予时间：degree_award_date
    学习方式：study_mode
    在学单位类别：type_of_institution
    """
    teacher_id: int = Field(..., title="教师ID", description="教师ID")
    education_obtained: str = Field(..., title="获的学历", description="获的学历")
    country_or_region_of_education: str = Field(..., title="获得学历国家/地区", description="获得学历国家/地区")
    institution_of_education_obtained: str = Field(..., title="获得学历的院校机构", description="获得学历的院校机构")
    major_learned: str = Field(..., title="所学妆业", description="所学妆业")
    is_major_normal: str = Field(..., title="是否师范类专业", description="是否师范类专业")
    admission_date: date = Field(..., title="入学时间", description="入学时间")
    graduation_date: date = Field(..., title="毕业时间", description="毕业时间")
    degree_level: str = Field(..., title="学位层次", description="学位层次")
    country_or_region_of_degree_obtained: str = Field(..., title="获取学位过家地区", description="获取学位过家地区")
    institution_of_degree_obtained: str = Field(..., title="获得学位院校机构", description="获得学位院校机构")
    degree_award_date: str = Field(..., title="学位授予时间", description="学位授予时间")
    study_mode: str = Field(..., title="学习方式", description="学习方式")
    type_of_institution: str = Field(..., title="在学单位类别", description="在学单位类别")


class TeacherLearnExperienceUpdateModel(BaseModel):
    """
    教师ID：teacher_id
    获的学历：education_obtained
    获得学历国家/地区：country_or_region_of_education
    获得学历的院校机构：institution_of_education_obtained
    所学妆业：major_learned
    是否师范类专业：is_major_normal
    入学时间：admission_date
    毕业时间：graduation_date
    学位层次：degree_level
    获取学位过家地区：country_or_region_of_degree_obtained
    获得学位院校机构：institution_of_degree_obtained
    学位授予时间：degree_award_date
    学习方式：study_mode
    在学单位类别：type_of_institution
    """
    teacher_learn_experience_id: int = Field(..., title="教师学习经历ID", description="教师学习经历ID")
    teacher_id: int = Field(..., title="教师ID", description="教师ID")
    education_obtained: str = Field(..., title="获的学历", description="获的学历")
    country_or_region_of_education: str = Field(..., title="获得学历国家/地区", description="获得学历国家/地区")
    institution_of_education_obtained: str = Field(..., title="获得学历的院校机构", description="获得学历的院校机构")
    major_learned: str = Field(..., title="所学妆业", description="所学妆业")
    is_major_normal: str = Field(..., title="是否师范类专业", description="是否师范类专业")
    admission_date: date = Field(..., title="入学时间", description="入学时间")
    graduation_date: date = Field(..., title="毕业时间", description="毕业时间")
    degree_level: str = Field(..., title="学位层次", description="学位层次")
    country_or_region_of_degree_obtained: str = Field(..., title="获取学位过家地区", description="获取学位过家地区")
    institution_of_degree_obtained: str = Field(..., title="获得学位院校机构", description="获得学位院校机构")
    degree_award_date: str = Field(..., title="学位授予时间", description="学位授予时间")
    study_mode: str = Field(..., title="学习方式", description="学习方式")
    type_of_institution: str = Field(..., title="在学单位类别", description="在学单位类别")