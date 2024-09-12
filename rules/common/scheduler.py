import logging
import traceback

import shortuuid
# from apscheduler.schedulers.asyncio import AsyncIOScheduler
from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.web.request_context import current_request_id

from rules.planning_school_rule import PlanningSchoolRule
import sys

from rules.school_rule import SchoolRule
from views.models.school_and_teacher_sync import SchoolType


def sync_survey_data():
    # supervisor_rule = get_injector(SurveyExtractRule)
    current_request_id.set(shortuuid.uuid())
    # supervisor_rule.sync_survey_data()
    print("sync survey data")


class SchedulerTask(object):

    def __init__(self):
        # logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)
        # self.scheduler = AsyncIOScheduler()
        self.configs = None
        from mini_framework.configurations import config_injection

        manager = config_injection.get_config_manager()
        sync_scheduler_dict = manager.get_domain_config("sync_scheduler")
        self.scheduler_type = sync_scheduler_dict.get("scheduler_type")
        # print("scheduler type:" + self.scheduler_type)
        self.scheduler_unit = sync_scheduler_dict.get("scheduler_unit")
        # print("scheduler unit:" + self.scheduler_unit)
        self.cron_expression = sync_scheduler_dict.get("cron_expression")
        # print("scheduler expression:" + self.cron_expression)
        self.is_enable = bool(sync_scheduler_dict.get("is_enable", False))
        # print("scheduler enable:" + str(self.is_enable))
        # self.supervisor_rule = get_injector(SurveyExtractRule)
        self.planning_school_rule = get_injector(PlanningSchoolRule)
        self.school_rule = get_injector(SchoolRule)

    async def add_job_cron(self):
        # 获取命令行参数
        params= [ ]
        school_no = 0
        school_type = 'planning_school'
        is_repush= False

        for i, arg in enumerate(sys.argv):
            print(f"参数{i}: {arg}")
            params.append(arg)
            if i==2:
                school_no = arg
            if i==3:
                school_type =  'planning_school' if int(arg)==0 else 'school'
            if i==4:
                is_repush =  int(arg) ==1

        print(params,school_no,school_type,is_repush)
        if ',' in school_no:
            planning_school_no_list= school_no.split(',')
        else:
            planning_school_no_list= [ school_no ]
        # planning_school_no_list= [ '2101031118342' ]
        for planning_school_code in planning_school_no_list:
            try:
                departname = '国际交流处'
                if school_type== SchoolType.PLANING_SCHOOL:
                    checked = await self.planning_school_rule.is_sended(planning_school_code)
                    if checked and not is_repush:
                        print(f'编号{planning_school_code}已经发送过')
                        continue
                    await self.planning_school_rule.send_planning_school_to_org_center_by_school_no(planning_school_code,departname)
                else:
                    checked = await self.school_rule.is_sended(planning_school_code)
                    if checked and not is_repush:
                        print(f'编号{planning_school_code}已经发送过')
                        continue
                    await self.school_rule.send_school_to_org_center_by_school_no(planning_school_code,departname)

            except Exception as e:
                print(f'编号{planning_school_code}的发生错误{e}')
                traceback.print_exc()
                return f'编号{planning_school_code}的发生错误{e}'
        return 'success'
        # self.supervisor_rule.sync_survey_data()


    async def add_job_interval(self, func, number: int):
        if self.is_enable:
            print("timer enable=true, add job interval")
            self.scheduler.add_job(func, 'interval', seconds=number)
        else:
            print("timer enable=false, add job interval")

    async def start(self):
        if self.is_enable:
            self.scheduler.start()
            print("Scheduler started")
        else:
            print("Scheduler not started")

    async def stop(self):
        self.scheduler.shutdown()
