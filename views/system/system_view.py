import datetime

# from fastapi import Field
from fastapi import Query, Depends
from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.web.std_models.page import PageRequest
from mini_framework.web.views import BaseView
from starlette.requests import Request

from common.decorators import require_role_permission
from rules.common import common_rule
from rules.common.common_rule import excel_fields_to_enum, get_org_center_userinfo
from rules.education_year_rule import EducationYearRule
from rules.system_config_rule import SystemConfigRule
from rules.system_rule import SystemRule
from rules.teacher_work_flow_instance_rule import TeacherWorkFlowRule
from rules.teachers_info_rule import TeachersInfoRule
from views.common.common_view import system_config, get_extend_params
from views.models.system import SystemConfig
from views.models.teachers import TeacherInfoImportSubmit


# 当前工具包里支持get  patch前缀的 方法的自定义使用
class SystemView(BaseView):
    def __init__(self):
        super().__init__()
        self.system_config_rule = get_injector(SystemConfigRule)
        self.system_rule = get_injector(SystemRule)
        self.education_year_rule = get_injector(EducationYearRule)
        self.teacher_work_flow_instance_rule = get_injector(TeacherWorkFlowRule)
        self.teachers_info_rule = get_injector(TeachersInfoRule)

    async def page_menu(self,
                        request: Request,

                        page_request=Depends(PageRequest),
                        role_id: int | str = Query(None, title="", description="角色id",
                                                   example='1'),
                        unit_type: str = Query(None, title="单位类型 例如学校 市/区", description="", min_length=1,
                                               max_length=20, example='city'),
                        edu_type: str = Query(None, title="教育阶段类型 例如幼儿园 中小学 职高", description="",
                                              min_length=1, max_length=20, example='kg'),
                        system_type: str = Query(None, title="系统类型 例如老师 单位 学生", description="",
                                                 min_length=1, max_length=20, example='unit'),
                        ):
        print(page_request)
        obj = await get_extend_params(request)
        items = []
        title = ''
        if system_type == 'teacher' or system_type == 'student':
            unit_type = ''
            edu_type = ''
        info, resource_codes, resource_codes_actions = await get_org_center_userinfo()
        print('资源和action', resource_codes, resource_codes_actions)
        is_permission_verify = system_config.system_config.get("permission_verify")
        print('permission verify', is_permission_verify)
        if not is_permission_verify:
            resource_codes = None
        res, title = await self.system_rule.query_system_with_kwargs(role_id, unit_type, edu_type, system_type,
                                                                     resource_codes=resource_codes, extend_params=obj)
        return {'app_name': title,
                'menu': list(res.values()),
                'resource_code': resource_codes_actions
                }

    async def page_menu_reset(self,
                              request: Request,
                              page_request=Depends(PageRequest),
                              role_id: int | str = Query(None, title="", description="角色id",
                                                         example='1'),
                              unit_type: str = Query(None, title="单位类型 例如学校 市/区", description="",
                                                     min_length=1,
                                                     max_length=20, example='city'),
                              edu_type: str = Query(None, title="教育阶段类型 例如幼儿园 中小学 职高", description="",
                                                    min_length=1, max_length=20, example='kg'),
                              system_type: str = Query(None, title="系统类型 例如老师 单位 学生", description="",
                                                       min_length=1, max_length=20, example='unit'),
                              ):

        obj = await get_extend_params(request)
        if system_type == 'teacher' or system_type == 'student':
            unit_type = ''
            edu_type = ''
        info, resource_codes, resource_codes_actions = await get_org_center_userinfo()
        print('资源和action', resource_codes, resource_codes_actions)
        is_permission_verify = system_config.system_config.get("permission_verify")
        print('permission verify', is_permission_verify)
        if not is_permission_verify:
            resource_codes = None
        res, title = await self.system_rule.query_system_with_kwargs(role_id, unit_type, edu_type, system_type,
                                                                     resource_codes=resource_codes, extend_params=obj)
        return {'app_name': title,
                'menu': list(res.values()),
                'resource_code': resource_codes_actions
                }

    async def get_education_year(self,
                                 # page_request=Depends(PageRequest),

                                 school_type: str = Query(None, title="", description="", min_length=1, max_length=20,
                                                          example=''),
                                 city: str = Query(None, title="", description="", min_length=1, max_length=20,
                                                   example=''),
                                 district: str = Query(None, title="", description="", min_length=1, max_length=20,
                                                       example=''),

                                 ):
        # print(page_request)
        items = []
        title = ''
        res = await self.education_year_rule.get_education_year_all(school_type, city, district, )
        # res,title  = await self.system_rule.query_system_with_page(page_request, role_id, unit_type, edu_type, system_type )
        return res

    # 系统配置的新增接口
    @require_role_permission("system_config", "add")
    async def post_system_config(self, system_config: SystemConfig):
        res = await self.system_config_rule.add_system_config(system_config)
        print(res)
        return res

    # 系统配置 列表
    @require_role_permission("system_config", "view")
    async def page_system_config(self,
                                 page_request=Depends(PageRequest),
                                 config_name: str = Query(None, title="", description="", min_length=1, max_length=50,
                                                          example=''),
                                 school_id: int = Query(0, description="学校id", example='1'),

                                 ):
        print(page_request)
        items = []
        title = ''
        res = await self.system_config_rule.query_system_config_with_page(config_name, school_id, page_request)
        return res

    # 系统配置详情
    @require_role_permission("system_config", "detail")
    async def get_system_config_detail(self,
                                       config_id: int | str = Query(0, description="", example='1'),
                                       ):
        res = await self.system_config_rule.get_system_config_by_id(config_id)

        return res

    # 修改系统配置
    @require_role_permission("system_config", "edit")
    async def put_system_config(self,
                                system_config: SystemConfig

                                ):
        res = await self.system_config_rule.update_system_config(system_config)
        return res

    async def get_work_flow_node_log(self, process_instance_id: int = Query(..., title="流程实例id",
                                                                            description="流程实例id")):
        res = await self.teacher_work_flow_instance_rule.get_teacher_work_flow_log_by(process_instance_id)
        return res

    async def get_work_flow_define(self, process_instance_id: int = Query(..., title="流程实例id",
                                                                          description="流程实例id")):
        res = await self.teacher_work_flow_instance_rule.get_work_flow_define(process_instance_id)
        return res

    async def get_work_flow_status(self, process_instance_id: int = Query(..., title="流程实例id",
                                                                          description="流程实例id")):
        res = await self.teacher_work_flow_instance_rule.get_work_flow_instance_by_process_instance_id(
            process_instance_id)
        return res.get('approval_status')

    # 测试用例
    async def get_test_case(self, process_instance_id: int = Query(..., title="流程实例id",
                                                                   description="流程实例id")):
        data_dict = {'ethnicity': '汉族', 'nationality': '中国', 'political_status': '中国共产党预备党员',
                     'native_place': '北京', 'birth_place': '新疆维吾尔自治区-自治区直辖县级行政区划-铁门关市',
                     'former_name': '明天中奖100w', 'marital_status': '未婚', 'health_condition': '一般或较弱',
                     'highest_education': '研究生教育-博士研究生毕业', 'institution_of_highest_education': '清华',
                     'special_education_start_time': datetime.date(2022, 2, 3),
                     'start_working_date': datetime.date(2013, 2, 2),
                     'enter_school_time': datetime.date(2013, 2, 2), 'source_of_staff': '招聘-往届毕业生',
                     'staff_category': '其他行政人员', 'in_post': '是', 'employment_form': '劳务派遣',
                     'contract_signing_status': '聘用合同', 'current_post_type': '专任教师-年级主任',
                     'current_post_level': '教师岗位-专业技术岗位一级', 'current_technical_position': '正高级教师',
                     'full_time_special_education_major_graduate': '是', 'received_preschool_education_training': '是',
                     'full_time_normal_major_graduate': '是', 'received_special_education_training': '是',
                     'has_special_education_certificate': '是', 'information_technology_application_ability': '精通',
                     'free_normal_college_student': '否', 'participated_in_basic_service_project': '是',
                     'basic_service_start_date': datetime.date(2022, 2, 3),
                     'basic_service_end_date': datetime.date(2022, 2, 3),
                     'special_education_teacher': '是', 'dual_teacher': '是',
                     'has_occupational_skill_level_certificate': '否',
                     'enterprise_work_experience': '1到2年（含）', 'county_level_backbone': '是',
                     'psychological_health_education_teacher': '否', 'recruitment_method': '招聘-应届毕业生',
                     'teacher_number': '13246546', 'department': '7210061000211566592', 'org_id': '7210061000211566592',
                     'hmotf': '香港同胞', 'hukou_type': '未落常住户口', 'main_teaching_level': '学前教育',
                     'teacher_qualification_cert_num': 'sdrafhrdfc', 'teaching_discipline': '品德与生活（社会）',
                     'language': '英语', 'language_proficiency_level': '精通',
                     'language_certificate_name': '普通话一级甲等 ',
                     'contact_address': '新疆维吾尔自治区-阿勒泰地区-吉木乃县', 'contact_address_details': '上海市',
                     'email': '1491994788@qq.com', 'highest_education_level': '博士',
                     'highest_degree_name': '学士-军事学学士学位', 'is_major_graduate': '是',
                     'other_contact_address_details': '0513-456789', 'teacher_id': 7212656592112717824,
                     'teacher_base_id': 7212656599385640960}
        import_type = "import_teacher"
        data_dict = await excel_fields_to_enum(data_dict, import_type)
        info_model = TeacherInfoImportSubmit(**data_dict)
        user_id = "asgfhjk"
        await self.teachers_info_rule.update_teachers_info_import(info_model, user_id)
        return

    # 退出的接口
    async def get_login_out(self, ):
        res = await common_rule.login_out()
        return {'home_url': res, 'msg': '退出成功'}
