from mini_framework.commands.command_base import Command


class SchoolSendCommand(Command):
    def __init__(self):
        super().__init__()

    async def run(self):
        from mini_framework.context import env

        env.sync_type = 'async'
        from rules.common.scheduler import SchoolSyncService
        async def command_run():
            print("命令开始 running...")

            school_sync_service = SchoolSyncService()
            # 启动

            await school_sync_service.service_run()
            print("命令 end   running...")

        await command_run()
