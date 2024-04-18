def main():
    import os
    from mini_framework.context import env
    env.app_root = os.path.dirname(os.path.abspath(__file__))
    env.sync_type = "async"
    from views.router import init_router
    init_router()
    from mini_framework.web.app_context import ApplicationContextManager
    application_context_manager = ApplicationContextManager()
    application_context_manager.initialize()
    return application_context_manager.app


app = main()
