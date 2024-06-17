from datetime import datetime

from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model

from distribute_transaction_lib.data_access.models import TransactionInfo, TransactionProgress, TransactionResults
from distribute_transaction_lib.data_access.transaction_dao import TransactionDAO
from distribute_transaction_lib.data_access.unit_system_dao import UnitSystemDAO
from distribute_transaction_lib.transaction import Transaction, TransactionState, TransactionNode



@dataclass_inject
class TransactionRule(object):
    transaction_dao: TransactionDAO
    unit_system_dao: UnitSystemDAO

    async def create_transaction(self, transaction: Transaction):
        """
        添加任务
        :param transaction: 任务
        :return:
        """
        transaction.created_at = transaction.created_at or datetime.now()
        transaction_info = view_model_to_orm_model(transaction, TransactionInfo)
        transaction_progress = view_model_to_orm_model(transaction, TransactionProgress)
        transaction_results = view_model_to_orm_model(transaction, TransactionResults)

        transaction_info = await self.transaction_dao.add_transaction(transaction_info)
        transaction_process = await self.transaction_dao.add_transaction_progress(transaction_progress)
        transaction_results = await self.transaction_dao.add_transaction_results(transaction_results)
        return transaction_info, transaction_process, transaction_results

    async def progress_change(self, transaction: Transaction, progress: float, desc: str, state: TransactionState, result_extra=None,
                              result_file: str = ""):
        """
        添加任务进度
        :param transaction: 任务
        :param progress: 进度
        :param desc: 描述
        :param state: 状态
        :param result_extra: 额外结果
        :param result_file: 结果文件
        :return:
        """
        if result_extra is None:
            result_extra = {}
        transaction_progress = TransactionProgress()
        transaction_progress.transaction_id = transaction.transaction_id
        transaction_progress.last_updated = datetime.now()
        transaction_progress.process_desc = desc
        transaction_progress.progress = progress
        transaction.progress = progress

        if state != transaction.state:
            transaction.state = state
            transaction_results = TransactionResults()
            transaction_results.transaction_id = transaction.transaction_id
            transaction_results.state = state
            transaction_results.result_extra = result_extra
            transaction_results.result_file = result_file
            transaction_results.last_updated = datetime.now()
            await self.transaction_dao.add_transaction_results(transaction_results)

        return await self.transaction_dao.add_transaction_progress(transaction_progress)

    async def get_unitsystem_by_unitcode(self, unit_codes ):
        #   根据单位的编号 读取各个单位的URL 返回
        return await self.unit_system_dao.get_unit_system_by_unitcodes(unit_codes)
        pass



    def get_transactions_by_workflow(self,workflow_code, )->list[TransactionNode]:
        # todo 读取 workflow_code配置的 事务 列表   路径  和 顺序   返回 data  依赖与 workflow_code的流程表和节点表
        return [
            TransactionNode(transaction_code='1',prepare_url='22',precommit_url='dd',commit_url='cc')


        ]

        pass
