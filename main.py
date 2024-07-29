import os

from mini_framework.async_task.async_task_command import AsyncTaskCommand
from mini_framework.commands.cli import CLI
from mini_framework.databases.dao_gen_command import DAOGenerateCommand
from mini_framework.databases.db_init_command import DatabaseInitCommand
from mini_framework.web.web_command import WebCommand


def main():
    root_path = os.path.dirname(os.path.abspath(__file__))
    cli = CLI(root_path)
    cli.register('task', AsyncTaskCommand, router_func_module="views.tasks.router.init_task_router")

    cli.register('db-init', DatabaseInitCommand, metadata_model="models.metadata")
    cli.register('dao-gen', DAOGenerateCommand, model_list=[('models.evaluation_item_model', 'EvaluationItem'),
                                                            ('models.supervisor_evaluation_model',
                                                             'SupervisorEvaluation'),
                                                            ('models.supervisor_model', 'Supervisor'),
                                                            ('models.supervisor_school_model', 'SupervisorSchool')])
    cli.register('web', WebCommand, router_func_module="views.router.init_router")
    cli.setup()


if __name__ == '__main__':
    main()
