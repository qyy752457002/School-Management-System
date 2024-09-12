from mini_framework.commands.command_base import Command
import asyncio


class TeacherSyncCommand(Command):
    def __init__(self):
        super().__init__()

    def run(self):
        from mini_framework.context import env
        from rules.teacher_import_rule import TeacherSyncRule
        env.sync_type = 'async'
        teacher_import_rule = TeacherSyncRule()
        async def task_run():
            print("TeacherSyncCommand running...")
            await teacher_import_rule.import_teachers_save_test()
            print("TeacherSyncCommand stop...")
        asyncio.run(task_run())




