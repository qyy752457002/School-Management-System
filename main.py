import os

from mini_framework.context import env

from router import init_router


def main():
    env.app_root = os.path.dirname(os.path.abspath(__file__))
    init_router()
    from mini_framework.web.app_context import ApplicationContextManager
    application_context_manager = ApplicationContextManager()
    application_context_manager.initialize()
    application_context_manager.run(host="127.0.0.1", port=8000)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
