from typing import List

from mini_framework.web.views import BaseView

from views.models.students import NewStudents, NewStudentsQuery, StudentsKeyinfo, StudentsBaseInfo
# from fastapi import Field
from fastapi import Query, Depends
from pydantic import BaseModel, Field
from mini_framework.web.std_models.page import PageRequest
from mini_framework.web.std_models.page import PaginatedResponse
from datetime import date
from views.models.students import StudentEduInfo, StudentsFamilyInfo


class CurrentStudentsView(BaseView):

    # 在校生流出
    async def patch_flowout(self,    student_id: str = Query(...,   description="学生id",min_length=1,max_length=20,example='SC2032633'),
                            flowout_time    :str= Query(..., description="流出时间" ,min_length=1,max_length=20,example='2020-10-10'),
                            flowout_reason   :str= Query(..., description="流出原因" ,min_length=1,max_length=20,example='家庭搬迁'),
                            ):
        # print(new_students_key_info)
        return student_id

    # 在校生转入  todo 届别 班级
    async def patch_transferin(self,StudentEduInfo:StudentEduInfo

                            ):
        # print(new_students_key_info)
        return StudentEduInfo


    # 在校生转入   审批
    async def patch_transferin_audit(self,transferin_audit_id:str=Query(...,   description="转入申请id",min_length=1,max_length=20,example='SC2032633'),

                               ):
        # print(new_students_key_info)
        return transferin_audit_id



    # 在校生转入   系统外转入
    async def patch_transferin_fromoutside(self,StudentEduInfo:StudentEduInfo,
                                           NewStudents:NewStudents,
                                           StudentoutEduInfo:StudentEduInfo,



                               ):
        # print(new_students_key_info)
        return StudentEduInfo


    # 在校生 系统外转出
    async def patch_transferout_tooutside(self,StudentEduInfo:StudentEduInfo,
                                           NewStudents:NewStudents,
                                           StudentoutEduInfo:StudentEduInfo,



                                           ):
        # print(new_students_key_info)
        return StudentEduInfo



    # 在校生转入   审批同意
    async def patch_transferin_auditpass(self,
                                         transferin_audit_id:str=Query(...,   description="转入申请id",min_length=1,max_length=20,example='SC2032633'),
                                         remark:str=Query(...,   description="备注",min_length=1,max_length=20,example='SC2032633'),
                                     ):
        # print(new_students_key_info)
        return transferin_audit_id

    # 在校生转入   审批拒绝
    async def patch_transferin_auditrefuse(self,
                                         transferin_audit_id:str=Query(...,   description="转入申请id",min_length=1,max_length=20,example='SC2032633'),
                                         remark:str=Query(...,   description="备注",min_length=1,max_length=20,example='SC2032633'),
                                         ):
        # print(new_students_key_info)
        return transferin_audit_id



    # 在校生 发起毕业 todo  支持传入部门学生ID或者  / all年级毕业
    async def patch_graduate(self,
                                           student_id: List[str]=Query(...,   description="学生ID",min_length=1,max_length=20,example='SC2032633'),
                             graduate_status:  str =Query(...,   description="毕业状态",min_length=1,max_length=20,example='结业'),
                             graduate_picture:  str =Query(...,   description="毕业照url",min_length=1,max_length=20,example=''),
                                           ):
        # print(new_students_key_info)
        return student_id


    #在校生 查看关键信息

    async def get_studentkeyinfo(self,
                                    student_name: str = Query(None, title="学生姓名", description="学生姓名",
                                                              example="John Doe"),
                                    enrollment_number: str = Query(None, title="报名号", description="报名号",
                                                                   example="20220001"),
                                    birthday: str = Query(None, title="生日", description="生日",
                                                          example="2000-01-01 00:00:00"),
                                    gender: str = Query(None, title="性别", description="性别", example="Male"),
                                    id_type: str = Query(None, title="证件类别", description="证件类别",
                                                         example="ID Card"),
                                    id_number: str = Query(None, title="证件号码", description="证件号码",
                                                           example="12345678"),
                                    ethnicity: str = Query(None, title="民族", description="民族", example="Han"),
                                    photo: str = Query(None, title="照片", description="照片", example="photo.jpg"),
                                    ):
        res = StudentsKeyinfo(
            student_name=student_name,
            birthday=birthday,
            gender=gender,
            id_type=id_type,
            id_number=id_number,
            photo=photo,
            enrollment_number=enrollment_number,
            ethnicity=ethnicity,
        )
        return res

    # 在校生 查看基本信息
    async def get_studentbaseinfo(self,
                  name_pinyin: str = Query(None, title="姓名拼音", description="姓名拼音", example="john_doe"),
                  session: str = Query(None, title="届别", description="届别", example="2022"),
                  grade: str = Query(None, title="年级", description="年级", example="10"),
                  classroom: str = Query(None, title="班级", description="班级", example="A"),
                  class_number: str = Query(None, title="班号", description="班号", example="1"),
                  school: str = Query(None, title="学校", description="学校", example="ABC School"),
                  registration_date: str = Query(None, title="登记日期", description="登记日期", example="2024-04-16 00:00:00"),
                  residence_district: str = Query(None, title="户口所在行政区", description="户口所在行政区", example="Beijing"),
                  birthplace_district: str = Query(None, title="出生地行政区", description="出生地行政区", example="Shanghai"),
                  native_place_district: str = Query(None, title="籍贯行政区", description="籍贯行政区", example="Shanxi"),
                  religious_belief: str = Query(None, title="宗教信仰", description="宗教信仰", example="Christian"),
                  residence_nature: str = Query(None, title="户口性质", description="户口性质", example="Urban"),
                  enrollment_date: str = Query(None, title="入学日期", description="入学日期", example="2023-09-01 00:00:00"),
                  contact_number: str = Query(None, title="联系电话", description="联系电话", example="12345678901"),
                  health_condition: str = Query(None, title="健康状况", description="健康状况", example="Good"),
                  political_status: str = Query(None, title="政治面貌", description="政治面貌", example="Party Member"),
                  blood_type: str = Query(None, title="血型", description="血型", example="O"),
                  home_phone_number: str = Query(None, title="家庭电话", description="家庭电话", example="1234567890"),
                  email_or_other_contact: str = Query(None, title="电子信箱/其他联系方式", description="电子信箱/其他联系方式", example="johndoe@example.com"),
                  migrant_children: bool = Query(None, title="是否随迁子女", description="是否随迁子女", example="1"),
                  disabled_person: bool = Query(None, title="是否残疾人", description="是否残疾人", example="False"),
                  only_child: bool = Query(None, title="是否独生子女", description="是否独生子女", example="1"),
                  left_behind_children: bool = Query(None, title="是否留守儿童", description="是否留守儿童", example="False"),
                  floating_population: bool = Query(None, title="是否流动人口", description="是否流动人口", example="False"),
                  residence_address_detail: str = Query(None, title="户口所在地（详细）", description="户口所在地（详细）", example="123 Main Street, Beijing"),
                  communication_district: str = Query(None, title="通信地址行政区", description="通信地址行政区", example="Beijing"),
                  postal_code: str = Query(None, title="邮政编码", description="邮政编码", example="100000"),
                  communication_address: str = Query(None, title="通信地址", description="通信地址", example="123 Main Street, Beijing"),
                  photo_upload_time: str = Query(None, title="照片上传时间", description="照片上传时间", example="2024-04-16 00:00:00"),
                  identity_card_validity_period: str = Query(None, title="身份证件有效期", description="身份证件有效期", example="2024-04-16 to 2034-04-16"),
                  remark: str = Query(None, title="备注", description="备注", example="This is a remark"),
                  ):
        res = StudentsBaseInfo(
            name_pinyin=name_pinyin,
            session=session,
            grade=grade,
            classroom=classroom,
            class_number=class_number,
            school=school,
            registration_date=registration_date,
            residence_district=residence_district,
            birthplace_district=birthplace_district,
            native_place_district=native_place_district,
            religious_belief=religious_belief,
            residence_nature=residence_nature,
            enrollment_date=enrollment_date,
            contact_number=contact_number,
            health_condition=health_condition,
            political_status=political_status,
            blood_type=blood_type,
            home_phone_number=home_phone_number,
            email_or_other_contact=email_or_other_contact,
            migrant_children=migrant_children,
            disabled_person=disabled_person,
            only_child=only_child,
            left_behind_children=left_behind_children,
            floating_population=floating_population,
            residence_address_detail=residence_address_detail,
            communication_district=communication_district,
            postal_code=postal_code,
            communication_address=communication_address,
            photo_upload_time=photo_upload_time,
            identity_card_validity_period=identity_card_validity_period,
            remark=remark,
        )

    #在校生 查询家庭信息
    async def page_studentfamilyinfo(self, student_name: str = Query(None, title="学生姓名", description="学生姓名", example="John Doe"),
                   page_request=Depends(PageRequest)):
        print(page_request)
        items = []

        res = StudentsFamilyInfo(
            name="John Doe",
            gender="男",
            relationship="父子",
            is_guardian="True",
            identification_type="身份证",
            identification_number="1234567890",
            phone_number="12345678901",
            ethnicity="汉族",
        )
        for i in range(0, page_request.per_page):
            items.append(res)

        return PaginatedResponse(has_next=True, has_prev=True, page=page_request.page, pages=10,
                                 per_page=page_request.per_page, total=100, items=items)
    #查询新生家庭详细信息
    async def get_studentfamilyinfo(self,
                                    student_name: str = Query(None, title="姓名", description="姓名", example="John Doe")):
        res = StudentsFamilyInfo(
            name="John Doe",
            gender="男",
            relationship="父子",
            is_guardian="True",
            identification_type="身份证",
            identification_number="1234567890",
            birthday="2000-01-01",
            phone_number="12345678901",
            ethnicity="汉族",
            health_status="良好",
            political_status="党员",
            nationality="中国",
            contact_address="北京市朝阳区",
            workplace="ABC公司",
            family_member_occupation="教师"
        )
        return res