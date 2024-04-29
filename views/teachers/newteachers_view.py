from datetime import datetime, date

from mini_framework.web.views import BaseView

from models.public_enum import YesOrNo
from views.models.teachers import NewTeacher, TeacherInfo, TeacherInfoCreateModel
from fastapi import Query, Depends

from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.web.std_models.page import PageRequest, PaginatedResponse
from mini_framework.web.views import BaseView
from models.teachers import Teacher
from rules.teachers_rule import TeachersRule
from views.models.teachers import Teachers, TeacherInfo, TeachersCreatModel, CurrentTeacherInfoSaveModel, \
    TeacherInfoSaveModel, TeacherInfoSubmit, CurrentTeacherQuery
from rules.teachers_info_rule import TeachersInfoRule


class NewTeachersView(BaseView):
    def __init__(self):
        super().__init__()
        self.teacher_rule = get_injector(TeachersRule)
        self.teacher_info_rule = get_injector(TeachersInfoRule)

    # 新增教职工登记信息
    async def post_newteacher(self, teachers: TeachersCreatModel):
        print(teachers)
        res = await self.teacher_rule.add_teachers(teachers)

        # 创建一个具体的日期对象，例如2024年4月27日
        specific_date = date(1970, 1, 1)
        print(specific_date)  # 输出：2024-04-27

        # 注意：月份是从1开始计数的，也就是说1代表1月，12代表12月
        #
        # res2 = await self.teacher_info_rule.add_teachers_info(TeacherInfoCreateModel(teacher_id=res.teacher_id,
        #                                                                              special_education_start_time= specific_date,
        #                                                                              start_working_date=specific_date,
        #                                                                              enter_school_time=specific_date,
        #                                                                              in_post=YesOrNo.NO,
        #                                                                              full_time_special_education_major_graduate=YesOrNo.NO,
        #                                                                              received_preschool_education_training=YesOrNo.NO,
        #                                                                              full_time_normal_major_graduate=YesOrNo.NO,
        #                                                                              received_special_education_training=YesOrNo.NO,
        #                                                                              has_special_education_certificate=YesOrNo.NO,
        #                                                                              free_normal_college_student=YesOrNo.NO,
        #                                                                              participated_in_basic_service_project=YesOrNo.NO,
        #                                                                              special_education_teacher=YesOrNo.NO,
        #                                                                              dual_teacher=YesOrNo.NO,
        #                                                                              has_occupational_skill_level_certificate=YesOrNo.NO,
        #                                                                              county_level_backbone=YesOrNo.NO,
        #                                                                              psychological_health_education_teacher=YesOrNo.NO,
        #                                                                              ))

        return res

    async def delete_newteacher(self, teacher_id: int = Query(..., title="教师编号", description="教师编号")):
        """
        删除教师信息
        """
        await self.teacher_rule.delete_teachers(teacher_id)
        return str(teacher_id)

    # 查询单个教职工登记信息
    async def get_newteacher(self, teacher_id: int = Query(..., title="教师编号", description="教师编号")):
        res = await self.teacher_rule.get_teachers_by_id(teacher_id)
        return res

    # 编辑新教职工登记信息
    async def put_newteacher(self, teachers: Teachers):
        print(teachers)
        res = await self.teacher_rule.update_teachers(teachers)
        return res

    # 分页查询

    async def page(self, new_teacher=Depends(NewTeacher), page_request=Depends(PageRequest)):
        """
        分页查询
        """
        paging_result = await self.teacher_info_rule.query_teacher_with_page(new_teacher, page_request)
        return paging_result

    # 新教职工基本信息的功能
    # 新增教职工基本信息
    async def post_newteacherinfosave(self, teacher_info: TeacherInfoSaveModel):
        """
        保存不经过验证
        """
        print(teacher_info)
        res = await self.teacher_info_rule.add_teachers_info(teacher_info)
        return res

    async def get_newteacherinfo(self, teacher_id: int = Query(..., title="教师名称", description="教师名称",
                                                               example=123)):
        # todo:重新获取时需要根据状态判断一下返回的应该是需要进行验证的还是不需要验证的。
        res = await self.teacher_info_rule.get_teachers_info_by_teacher_id(teacher_id)
        return res

    async def put_newteacherinfosubmit(self, teacher_info: TeacherInfoSubmit):
        if teacher_info.teacher_base_id > 0:
            res = await self.teacher_info_rule.update_teachers_info(teacher_info)
        else:
            res = await self.teacher_info_rule.add_teachers_info_valid(teacher_info)
        return res

    async def put_newteacherinforesave(self, teacher_info: CurrentTeacherInfoSaveModel):
        res = await self.teacher_info_rule.update_teachers_info(teacher_info)
        return res

    # 编辑教职工基本信息
    async def put_newteacherinfo(self, teacher_info: TeacherInfo):
        res = await self.teacher_info_rule.update_teachers_info(teacher_info)
        return res

    # 删除教职工基本信息
    # async def delete_newteacherinfo(self,
    #                                 teacher_id: int = Query(..., title="教师编号", description="教师编号",example=123)):
    #     res = await self.teacher_info_rule.delete_teachers_info(teacher_id)
    #     return res

    async def patch_submitting(self,
                               teacher_id: int = Query(..., title="教师编号", description="教师编号", example=123)):
        await self.teacher_rule.submitting(teacher_id)
        return teacher_id

    async def patch_submitted(self,
                              teacher_id: int = Query(..., title="教师编号", description="教师编号", example=123)):
        await self.teacher_rule.submitted(teacher_id)
        return teacher_id

    async def patch_approved(self,
                             teacher_id: int = Query(..., title="教师编号", description="教师编号", example=123)):
        await self.teacher_rule.approved(teacher_id)
        return teacher_id

    async def patch_rejected(self,
                             teacher_id: int = Query(..., title="教师编号", description="教师编号", example=123)):
        await self.teacher_rule.rejected(teacher_id)
        return teacher_id

    async def patch_info_submitting(self,
                                    teacher_base_id: int = Query(..., title="教师基本信息编号",
                                                                 description="教师基本信息编号",
                                                                 example=123)):
        await self.teacher_info_rule.submitting(teacher_base_id)
        return teacher_base_id

    async def patch_info_submitted(self,
                                   teacher_base_id: int = Query(..., title="教师基本信息编号",
                                                                description="教师基本信息编号",
                                                                example=123)):
        await self.teacher_info_rule.submitted(teacher_base_id)
        return teacher_base_id

    async def patch_info_approved(self,
                                  teacher_base_id: int = Query(..., title="教师基本信息编号",
                                                               description="教师基本信息编号",
                                                               example=123)):
        await self.teacher_info_rule.approved(teacher_base_id)
        return teacher_base_id

    async def patch_info_rejected(self,
                                  teacher_base_id: int = Query(..., title="教师基本信息编号",
                                                               description="教师基本信息编号",
                                                               example=123)):
        await self.teacher_info_rule.rejected(teacher_base_id)
        return teacher_base_id
