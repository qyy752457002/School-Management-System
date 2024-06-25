from sqlalchemy import select

from mini_framework.async_task.data_access.models import TaskInfo, TaskProgress, TaskResult
from mini_framework.databases.entities.dao_base import DAOBase


class TaskDAO(DAOBase):
    """
    异步任务数据访问对象
    """

    async def add_task(self, task: TaskInfo, is_commit=False):
        """
        添加任务
        :param task: 任务
        :param is_commit: 是否提交
        :return:
        """
        session = await self.master_db()
        session.add(task)
        if is_commit:
            await session.commit()
        return task

    async def add_task_progress(self, task_progress: TaskProgress, is_commit=False):
        """
        添加任务进度
        :param task_progress: 任务
        :param is_commit: 是否提交
        :return:
        """
        session = await self.master_db()
        session.add(task_progress)
        if is_commit:
            await session.commit()
        return task_progress

    async def add_task_result(self, task_results: TaskResult, is_commit=False):
        """
        添加任务结果
        :param is_commit: 是否提交
        :param task_results: 任务结果
        :return:
        """
        session = await self.master_db()
        session.add(task_results)
        if is_commit:
            await session.commit()
        return task_results

    async def get_task_by_id(self, task_id: int) -> TaskInfo:
        """
        通过任务ID获取任务
        :param task_id: 任务ID
        :return:
        """
        session = await self.slave_db()
        result = await session.execute(select(TaskInfo).filter(TaskInfo.task_id == task_id))
        return result.scalar()
