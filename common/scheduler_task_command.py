from venv import logger

from mini_framework.commands.command_base import Command


class SchoolSendCommand(Command):
    def __init__(self):
        super().__init__()

    async def run(self):
        from mini_framework.context import env

        env.sync_type = 'async'
        from rules.common.scheduler import SchedulerTask
        import asyncio
        async def task_run():
            print("命令开始 running...")

            scheduler_task = SchedulerTask()
            await scheduler_task.add_job_cron()
            # 启动调度器
            # await scheduler_task.start()
            print("命令 end   running...")
            # try:
            #     while True:
            #         await asyncio.sleep(5)
            # except KeyboardInterrupt:
            #     logger.info("SchoolSendCommand stop...")
            #     scheduler_task.scheduler.shutdown()
        # asyncio.run(task_run())
        await task_run()
