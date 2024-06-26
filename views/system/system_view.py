from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.web.views import BaseView

from rules.education_year_rule import EducationYearRule
from rules.sub_system_rule import SubSystemRule
from rules.system_config_rule import SystemConfigRule
from rules.system_rule import SystemRule
from views.models.planning_school import PlanningSchool, PlanningSchoolBaseInfo
from views.models.school import School, SchoolKeyAddInfo
# from fastapi import Field
from fastapi import Query, Depends
from pydantic import BaseModel, Field
from mini_framework.web.std_models.page import PageRequest
from mini_framework.web.std_models.page import PaginatedResponse
from views.models.sub_system import SubSystem
from views.models.system import SystemConfig

# 当前工具包里支持get  patch前缀的 方法的自定义使用
class SystemView(BaseView):
    def __init__(self):
        super().__init__()
        self.system_config_rule = get_injector(SystemConfigRule)
        self.system_rule = get_injector(SystemRule)
        self.education_year_rule = get_injector(EducationYearRule)

    async def page_menu(self,
                   page_request=Depends(PageRequest),
                   role_id: int = Query(None, title="", description="角色id",
                                                 example='1'),
                   unit_type :str= Query(None, title="单位类型 例如学校 市/区", description="",min_length=1,max_length=20,example='city'),
                   edu_type :str= Query(None, title="教育阶段类型 例如幼儿园 中小学 职高", description="",min_length=1,max_length=20,example='kg'),
                   system_type :str= Query(None, title="系统类型 例如老师 单位 学生", description="",min_length=1,max_length=20,example='unit'),
                   ):
        print(page_request)
        items = []
        title=''
        if system_type=='teacher' or system_type=='student':
            # title='学校版'
            unit_type=''
            edu_type=''
        res ,title= await self.system_rule.query_system_with_kwargs( role_id, unit_type, edu_type, system_type )
        # res,title  = await self.system_rule.query_system_with_page(page_request, role_id, unit_type, edu_type, system_type )
        return {'app_name':title,
                'menu':list(res.values())
                }

    async def get_education_year(self,
                        # page_request=Depends(PageRequest),


                                 school_type :str= Query(None, title="", description="",min_length=1,max_length=20,example=''),
                                 city :str= Query(None, title="", description="",min_length=1,max_length=20,example=''),
                                 district :str= Query(None, title="", description="",min_length=1,max_length=20,example=''),

                        ):
        # print(page_request)
        items = []
        title=''
        res = await self.education_year_rule.get_education_year_all( school_type, city, district,  )
        # res,title  = await self.system_rule.query_system_with_page(page_request, role_id, unit_type, edu_type, system_type )
        return res
    # 系统配置的新增接口 
    async def post_system_config(self, system_config: SystemConfig):
        res = await self.system_config_rule.add_system_config(system_config)
        print(res)
        return res
    async def page_system_config(self,
                        page_request=Depends(PageRequest),
                                 config_name :str= Query(None, title="", description="",min_length=1,max_length=50,example=''),
                                 school_id: int = Query(0, description="学校id", example='1'),

                        ):
        print(page_request)
        items = []
        title=''
        res= await self.system_config_rule.query_system_config_with_page( config_name,school_id,page_request  )
        return  res

    async def get_system_config_detail(self,
                  config_id: int = Query(0, description="", example='1'),
                  ):
        res  = await self.system_config_rule.get_system_config_by_id(config_id)

        return res


    async def put_system_config(self,
                                system_config: SystemConfig

                          ):
        res = await self.system_config_rule.update_system_config(system_config)
        return res
