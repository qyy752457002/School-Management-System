import os
import warnings

import sqlalchemy
from mini_framework.async_task.async_task_command import AsyncTaskCommand
from mini_framework.commands.cli import CLI
from mini_framework.databases.dao_gen_command import DAOGenerateCommand
from mini_framework.databases.db_init_command import DatabaseInitCommand
from mini_framework.web.web_command import WebCommand
from pydantic import json_schema

from common.scheduler_task_command import SchoolSendCommand
from views.common.teacer_to_org_command import TeacherSyncCommand

warnings.filterwarnings('ignore', category=sqlalchemy.exc.SAWarning)

# 创建一个过滤器来忽略 PydanticJsonSchemaWarning
warnings.filterwarnings("ignore", category=json_schema.PydanticJsonSchemaWarning)


def main():
    root_path = os.path.dirname(os.path.abspath(__file__))
    cli = CLI(root_path)
    cli.register('task', AsyncTaskCommand, router_func_module="views.tasks.router.init_task_router")

    cli.register('db-init', DatabaseInitCommand, metadata_model="models.metadata")
    cli.register('dao-gen', DAOGenerateCommand, model_list=[('models.course_school_nature', 'CourseSchoolNature'),
                                                            ])
    cli.register('web', WebCommand, router_func_module="views.router.init_router")
    cli.register('school-sync', SchoolSendCommand)
    cli.register('teacher-sync', TeacherSyncCommand)
    cli.setup()


if __name__ == '__main__':
    main()
