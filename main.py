import os

import fire
from mini_framework.context import env


def generate_dao():
    env.sync_type = "sync"
    env.app_root = os.path.dirname(os.path.abspath(__file__))
    model_list = [('models.domestic_training', 'DomesticTraining'), ('models.overseas_study', 'OverseasStudy'),
                  ('models.talent_program', 'TalentProgram'), ('models.annual_review', 'AnnualReview'),
                  ('models.research_achievements', 'ResearchAchievements')]
    dao_files_path = os.path.join(env.app_root, "daos_test")
    # 增加当前目录到sys.path
    from mini_framework.databases.toolkit.dao_generator import generate_dao_files
    generate_dao_files(model_list, dao_files_path)
    print("Generate DAO files successfully!")


def generate_db():
    env.sync_type = "sync"
    env.app_root = os.path.dirname(os.path.abspath(__file__))
    from mini_framework.databases.conn_managers.db_manager import db_connection_manager

    session = db_connection_manager.get_sync_session("default", True)
    from models import metadata
    metadata.create_all(session.bind, checkfirst=True)


def web():
    env.app_root = os.path.dirname(os.path.abspath(__file__))
    env.sync_type = "async"
    from views.router import init_router
    init_router()
    from mini_framework.web.app_context import ApplicationContextManager
    application_context_manager = ApplicationContextManager()
    application_context_manager.initialize()
    application_context_manager.run()


def main(service="web"):
    if service == "web":
        web()
    elif service == "db-init":
        generate_db()
    elif service == "dao-gen":
        generate_dao()
    else:
        raise ValueError(f"Unknown service: {service}")


if __name__ == '__main__':
    fire.Fire(main)
