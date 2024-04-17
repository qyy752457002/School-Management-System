import os

import fire
from mini_framework.context import env


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
    else:
        raise ValueError(f"Unknown service: {service}")


if __name__ == '__main__':
    fire.Fire(main)
