import sys
import traceback

# from apscheduler.schedulers.asyncio import AsyncIOScheduler
from mini_framework.design_patterns.depend_inject import get_injector

from rules.planning_school_rule import PlanningSchoolRule
from rules.school_rule import SchoolRule
from views.models.school_and_teacher_sync import SchoolType


class SchoolSyncService(object):

    def __init__(self):
        # logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)
        # self.scheduler = AsyncIOScheduler()
        self.configs = None
        from mini_framework.configurations import config_injection

        manager = config_injection.get_config_manager()
        # sync_scheduler_dict = manager.get_domain_config("sync_scheduler")
        # self.scheduler_type = sync_scheduler_dict.get("scheduler_type")

        # print("scheduler enable:" + str(self.is_enable))
        # self.supervisor_rule = get_injector(SurveyExtractRule)
        self.planning_school_rule = get_injector(PlanningSchoolRule)
        self.school_rule = get_injector(SchoolRule)

    async def service_run(self):
        # 获取命令行参数
        params = []
        school_no = 0
        school_type = 'school'
        is_repush = False

        for i, arg in enumerate(sys.argv):
            print(f"参数{i}: {arg}")
            params.append(arg)
            if i == 2:
                school_no = arg
            if i == 3:
                school_type = 'planning_school' if int(arg) == 1 else 'school'
            if i == 4:
                is_repush = int(arg) == 1

        print(params, school_no, school_type, is_repush)
        if ',' in school_no:
            planning_school_no_list = school_no.split(',')
        else:
            planning_school_no_list = [school_no]
        for planning_school_code in planning_school_no_list:
            try:
                departname = '国际交流'
                if school_type == SchoolType.PLANING_SCHOOL:
                    checked = await self.planning_school_rule.is_sended(planning_school_code)
                    if checked and not is_repush:
                        print(f'编号{planning_school_code}已经发送过')
                        continue
                    await self.planning_school_rule.send_planning_school_to_org_center_by_school_no(
                        planning_school_code, departname)
                else:
                    checked = await self.school_rule.is_sended(planning_school_code)
                    if checked and not is_repush:
                        print(f'编号{planning_school_code}已经发送过')
                        continue
                    await self.school_rule.send_school_to_org_center_by_school_no(planning_school_code, departname)

            except Exception as e:
                print(f'编号{planning_school_code}的发生错误{e} 跳过 继续执行')
                traceback.print_exc()
        return 'success'
