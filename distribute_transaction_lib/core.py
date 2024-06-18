import uuid
import requests
import logging

from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.utils.http import HTTPRequest

from .config import  LOCK_PATH,  transaction_service_config
from .data_access.transaction_rule import TransactionRule
from .kazooclient import SafeKazooClient
from .monitoring import Monitor
from .statistics import StatisticsCollector
from .transaction import TransactionNode
import traceback

# 本协调者 部署在市区总部  api调用进入这里


class DistributedTransactionCore:
    def __init__(self):
        # 初始化 各个部分组件  例如 日志 监控 和 统计 组件
        self.logger = logging.Logger('dis_trans')
        self.monitor = Monitor()
        self.statistics = StatisticsCollector()
        self.transaction_rule = get_injector(TransactionRule)

        self.api_urls = []
        self.api_url_workflow =  transaction_service_config.workflow_config
        self.transaction_nodes = []  # 事务节点列表
        self.transaction_node = TransactionNode
        self.data = []  # 事务数据
        # 定义各阶段的url key
        self.baseurl_key_name =  'base_url'
        self.prepare_key_name =  'prepare_url'
        self.precommit_key_name =  'precommit_url'
        self.commit_key_name =  'commit_url'
        self.rollback_key_name =  'rollbacked'
        # 各阶段的成功状态码
        self.prepare_success_code =  'prepared'
        self.precommit_success_code =  'commit_url'
        self.commit_success_code =  'commit_url'
        self.rollback_success_code =  'commit_url'

        self.transaction_id = None
        self.prepare_responses = None
        self.commit_responses = None
        self.rollback_responses = None
        self.pre_commit_responses = None
        self.post_commit_responses = None
        self.pre_rollback_responses = None
        self.post_rollback_responses = None

    def start_transaction(self):
        self.transaction_id = str(uuid.uuid4())
        logging.info(f"Starting transaction with ID: {self.transaction_id}")
        return self.transaction_id
    #  这里改为 框架的 调api的方法
    async def safe_api_call(self, url, data):
        try:
            httpreq= HTTPRequest()
            response =await httpreq.post_json(url, data)

            # response = requests.post(url, json=data, timeout=10)
            # response.raise_for_status()
            logging.info(f"API call succeeded: {url}")
            return response
        except Exception as e:
            logging.error(f"API call failed: {e}")
            return dict()

    async def prepare_transaction(self, data):
        prepare_responses = {}
        for value in self.transaction_nodes:
            # 检查节点是否具有prepare_url字段
            if not hasattr(value,self.prepare_key_name):
                print(value)
                logging.error(f"事务节点缺少字段 :准备 url {value}")
                await self.rollback_transaction(prepare_responses)
                return False
                # continue
            # 检查 各单位 具有基础url
            url = f"{getattr(value,self.baseurl_key_name)}{getattr(value,self.prepare_key_name)}"

            response = await self.safe_api_call(url,  self.data)
            # 检查是否 有状态  且是 成功的状态码
            if response and response["status"] == self.prepare_success_code:
                # response["baseurl"] = self.api_urls[value['url']]
                prepare_responses [  'url'] = response
            else:
                await self.rollback_transaction(prepare_responses)
                return False
        return prepare_responses

    # 以下方法类似地进行优化，主要是使用 self.safe_api_call 和改善错误处理...
    # pre_commit_transaction, commit_transaction, rollback_transaction 方法省略...
    async def pre_commit_transaction(self,prepare_responses):
        for system, response in prepare_responses.items():
            # 要求必须返回 pre_commit_url
            url = f"{response.get(self.baseurl_key_name)}{response.get(self.precommit_key_name)}"
            if not await self.safe_api_call(url, response):
                await self.rollback_transaction(prepare_responses)
                return False
        return True

    async def commit_transaction(self,prepare_responses):
        # 要求必须返回 commit_url
        for system, response in prepare_responses.items():
            url = f"{response.get(self.baseurl_key_name)}{response.get( self.commit_key_name)}"
            if not await self.safe_api_call(url, response):
                await self.rollback_transaction(prepare_responses)
                return False
        logging.info("Transaction committed successfully.")
        return True

    async def rollback_transaction(self,prepare_responses):
        for system, response in prepare_responses.items():
            # 读取各个的 基础URL 和 rollback_url
            url = f"{response.get(self.baseurl_key_name)}{response.get( self.rollback_key_name)}"
            res =await self.safe_api_call(url, response)
            # todo  重试回滚 放入队列 或者提示人工干预
            # 回滚接口要求必须返回 status 为 rollbacked

            if not res or res.get('status') !=  self.rollback_success_code:
                logging.info(f"回滚失败 重试回滚 放入队列 或者提示人工干预{url}{response}")
        logging.info("Transaction rolled back.")
    async def get_workflow_trans(self,workflow_code):
        # 读取 流程
        transactions =await self.transaction_rule.get_transactions_by_workflow(workflow_code, )
        self.transaction_nodes = transactions
        unitcodes = [ ]
        # 各节点的单位code 提取
        for transaction in self.transaction_nodes:
            unitcodes.append(transaction .transaction_code)

        # 读取单位URL
        unit_urls = await  self.transaction_rule.get_unitsystem_by_unitcode( unitcodes)
        self.api_urls = unit_urls

        # 获取 事务id
        self.transaction_id = self.start_transaction()
    async def execute_transaction(self,workflow_code, data):
        try:
            self.logger.info(f"入参 transaction.{data}")

            self.data = data
            await self.get_workflow_trans(workflow_code)

            # 获取 锁
            with SafeKazooClient(   transaction_service_config.zookeeper_host_config) as zk:
                lock = zk.Lock(LOCK_PATH)
                try:
                    # self.start_transaction()
                    # self.get_real_url(data)

                    if lock.acquire(blocking=True, timeout=10):
                        try:
                            # 开启事务流程  准备阶段 依次调用  todo 流程如何处理
                            prepare_responses =await self.prepare_transaction(data)
                            if prepare_responses:
                                pass

                            else:
                                logging.info("Prepare phase failed, transaction rolled back.")
                            # 预提交 中间态

                            precommit =await self.pre_commit_transaction(prepare_responses)
                            if not precommit:
                                logging.info("Pre-commit failed, transaction rolled back.")

                            # 提交 终态

                            ultracommit =await self.commit_transaction(prepare_responses)

                            if not ultracommit :

                                logging.info("Commit failed, transaction rolled back.")
                            else:
                                logging.info("Transaction committed successfully.")
                                self.monitor.handle_success_event()
                                self.statistics.handle_success_event()


                        except Exception as e:
                            # 打印异常 追踪堆栈
                            stack_trace = traceback.format_exc()

                            logging.error(f"Exception occurred: {e} ")
                            logging.error(f"Exception 追踪: {stack_trace} ")
                            #             异常的 触发回滚
                            await self.rollback_transaction(prepare_responses)
                        finally:
                            lock.release()
                    else:
                        logging.info("Failed to acquire lock, transaction aborted.")
                except Exception as e:
                    # 打印异常 追踪堆栈
                    stack_trace = traceback.format_exc()

                    logging.error(f"Exception occurred: {e} ")
                    logging.error(f"Exception 追踪: {stack_trace} ")
                    #             异常的 触发回滚
                    await self.rollback_transaction(prepare_responses)
            pass
        except Exception as e:
            self.logger.exception('事务异常',e)








