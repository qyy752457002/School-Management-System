from sqlalchemy import select

from mini_framework.databases.entities.dao_base import DAOBase

from distribute_transaction_lib.data_access.models import TransactionInfo, TransactionProgress, TransactionResults


class TransactionDAO(DAOBase):
    """
    异步事务数据访问对象
    """

    async def add_transaction(self, transaction: TransactionInfo):
        """
        添加事务
        :param transaction: 事务
        :return:
        """
        session = await self.master_db()
        session.add(transaction)
        await session.commit()
        return transaction

    async def add_transaction_progress(self, transaction_progress: TransactionProgress):
        """
        添加事务进度
        :param transaction_progress: 事务
        :return:
        """
        session = await self.master_db()
        session.add(transaction_progress)
        await session.commit()
        return transaction_progress

    async def add_transaction_results(self, transaction_results: TransactionResults):
        """
        添加事务结果
        :param transaction_results: 事务结果
        :return:
        """
        session = await self.master_db()
        session.add(transaction_results)
        await session.commit()
        return transaction_results

    async def get_transaction_by_id(self, transaction_id: int) -> TransactionInfo:
        """
        通过事务ID获取事务
        :param transaction_id: 事务ID
        :return:
        """
        session = await self.slave_db()
        result = await session.execute(select(TransactionInfo).filter(TransactionInfo.transaction_id == transaction_id))
        return result.scalar()
