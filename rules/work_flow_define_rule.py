from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from views.models.work_flow_define import WorkFlowDefineModel
from daos.work_flow_node_define_dao import WorkFlowNodeDefineDAO
from daos.work_flow_define_dao import WorkFlowDefineDAO
from daos.work_flow_node_depend_dao import WorkFlowNodeDependDAO
from daos.work_flow_node_depend_strategy_dao import WorkFlowNodeDependStrategyDAO
from models.work_flow_node_define import WorkFlowNodeDefine
from models.work_flow_node_depend import WorkFlowNodeDepend
from models.work_flow_define import WorkFlowDefine
from models.work_flow_node_depend_strategy import WorkFlowNodeDependStrategy
from mini_framework.databases.entities import BaseDBModel, to_dict


@dataclass_inject
class WorkFlowNodeDefineRule(object):
    work_flow_node_define_dao: WorkFlowNodeDefineDAO
    work_flow_define_dao: WorkFlowDefineDAO
    work_flow_node_depend_dao: WorkFlowNodeDependDAO
    work_flow_node_depend_strategy_dao: WorkFlowNodeDependStrategyDAO

    async def add_transfer_node(self, process_code, is_transfer, is_transfer_external, **kwargs):

        # 定义调出时，由系统内向外发起节点信息映射
        out_transfer_out_nodes = {
            'is_transfer_out_area_approval': ('由内向外调出调出区审批节点', 'out_out_tf_out_area_approval'),
            'is_transfer_city_approval': ('由内向外调出调动市审批节点', 'out_out_tf_lc_city_approval'),
            'start': ('调出之调出校发起节点', 'out_out_tf_start_node'),
            'success': ('由内向外调出调动成功节点', 'out_out_tf_success_end'),
            'fail': ('由内向外调出调动失败节点', 'out_out_tf_fail_end')
        }

        # # 定义调出时调入校发起节点信息映射
        # out_transfer_in_nodes = {
        #     'is_transfer_out_school_approval': ('调出之调入发起调出校审批节点', 'out_in_tf_out_school_approval'),
        #     'is_transfer_in_area_approval': ('调出之调入发起调入区审批节点', 'out_in_tf_in_area_approval'),
        #     'is_transfer_out_area_approval': ('调出之调入发起调出区审批节点', 'out_in_tf_out_area_approval'),
        #     'is_transfer_city_approval': ('调出之调入发起调动市审批节点', 'out_in_tf_lc_city_approval'),
        #     'start': ('调出之调入发起调入校发起节点', 'out_in_tf_start_node'),
        #     'success': ('调出之调入发起调动成功节点', 'out_in_tf_success_end'),
        #     'fail': ('调出之调入发起调动失败节点', 'out_in_tf_fail_end')
        # }

        # 定义调入校发起调入时，由系统外向系统内节点信息映射
        in_transfer_out_nodes = {
            'is_transfer_in_area_approval': ('由外向内调入调入区审批节点', 'in_out_tf_in_area_approval'),
            'is_transfer_city_approval': ('由外向内调入调动市审批节点', 'in_out_tf_lc_city_approval'),
            'start': ('调入之调出校发起节点', 'in_out_tf_start_node'),
            'success': ('由外向内调入调动成功节点', 'in_out_tf_success_end'),
            'fail': ('由外向内调入调动失败节点', 'in_out_tf_fail_end')
        }

        # 定义调入校发起调入时，由系统内向系统内发起节点信息映射
        in_transfer_in_nodes = {
            'is_transfer_out_school_approval': ('由内向内调入调出校审批节点', 'in_in_tf_out_school_approval'),
            'is_transfer_in_area_approval': ('由内向内调入调入区审批节点', 'in_in_tf_in_area_approval'),
            'is_transfer_out_area_approval': ('由内向内调入调出区审批节点', 'in_in_tf_out_area_approval'),
            'is_transfer_city_approval': ('由内向内调入调动市审批节点', 'in_in_tf_lc_city_approval'),
            'start': ('由内向内调入调入校发起节点', 'in_in_tf_start_node'),
            'success': ('由内向内调入调动成功节点', 'in_in_tf_success_end'),
            'fail': ('由内向内调入调动失败节点', 'in_in_tf_fail_end')
        }

        # 初始化节点定义表
        nodes_list = []
        # 根据是调入流程还是调出流程分别处理
        if is_transfer:  # 代表是调出流程
            nodes_info = out_transfer_out_nodes

        else:  # 代表是调入流程
            if is_transfer_external:
                nodes_info = in_transfer_out_nodes
            else:
                nodes_info = in_transfer_in_nodes

        # 添加发起节点
        nodes_list.append({
            'process_code': process_code,
            'node_name': nodes_info['start'][0],
            'node_code': nodes_info['start'][1]
        })

        # 遍历检查条件，判断是否需要新增节点
        for key, value in kwargs.items():
            if value and key in nodes_info:
                nodes_list.append({
                    'process_code': process_code,
                    'node_name': nodes_info[key][0],
                    'node_code': nodes_info[key][1]
                })

        # 添加成功和失败节点
        nodes_list.append({
            'process_code': process_code,
            'node_name': nodes_info['success'][0],
            'node_code': nodes_info['success'][1]
        })
        nodes_list.append({
            'process_code': process_code,
            'node_name': nodes_info['fail'][0],
            'node_code': nodes_info['fail'][1]
        })
        print("增加的列表节点-----------------------开始")
        print(nodes_list)
        print("增加的列表节点-----------------------结束")
        print("\n")
        db_records = []
        for node in nodes_list:
            record = create_model_instance(WorkFlowNodeDefine, node)
            db_records.append(record)
        print("增加的节点-----------------------开始")
        print([to_dict(item) for item in db_records])
        print("增加的节点-----------------------结束")
        print("\n")

        return db_records

    async def add_depend(self, node_list, process_type, **kwargs):
        """
        添加依赖
        """
        process_type = process_type
        if process_type == "transfer":
            is_transfer = kwargs.get('is_transfer')
            is_transfer_external = kwargs.get('is_transfer_external')
            if is_transfer:
                if is_transfer_external:
                    pre = "ootf"  # 调出时，由系统内向外发起节点
            else:
                if is_transfer_external:
                    pre = "iotf"  # 调入时，由系统外向内调入节点
                else:
                    pre = "iitf"  # 调入时，由系统内向系统内发起节点
        elif process_type == "borrow":
            pass

        elif process_type == "entry":
            pass

        elif process_type == "info":
            pass

        elif process_type == "change":
            pass

        depend_data = []
        num_nodes = len(node_list)
        if num_nodes <= 3:
            raise Exception("节点数量构不成流程")

        for i in range(1, num_nodes - 2):
            current_node = node_list[i]
            previous_node = node_list[i - 1]
            next_node = node_list[i + 1]
            fail_node = node_list[-1]
            success_node = node_list[-2]

            if i == 1:
                # First approval node
                depend_data.append({
                    "depend_code": generate_depend_code(pre, process_type, node_list[0].node_code,
                                                        current_node.node_code),
                    "source_node": node_list[0].node_code,
                    "next_node": current_node.node_code
                })
                depend_data.append({
                    "depend_code": generate_depend_code(pre, process_type, current_node.node_code,
                                                        node_list[0].node_code),
                    "source_node": current_node.node_code,
                    "next_node": node_list[0].node_code
                })
                depend_data.append({
                    "depend_code": generate_depend_code(pre, process_type, current_node.node_code,
                                                        fail_node.node_code),
                    "source_node": current_node.node_code,
                    "next_node": fail_node.node_code
                })
                depend_data.append({
                    "depend_code": generate_depend_code(pre, process_type, current_node.node_code,
                                                        next_node.node_code),
                    "source_node": current_node.node_code,
                    "next_node": next_node.node_code
                })

            elif i == num_nodes - 3:
                # Last approval node
                depend_data.append({
                    "depend_code": generate_depend_code(pre, process_type, current_node.node_code,
                                                        previous_node.node_code),
                    "source_node": current_node.node_code,
                    "next_node": previous_node.node_code
                })
                depend_data.append({
                    "depend_code": generate_depend_code(pre, process_type, current_node.node_code,
                                                        fail_node.node_code),
                    "source_node": current_node.node_code,
                    "next_node": fail_node.node_code
                })
                depend_data.append({
                    "depend_code": generate_depend_code(pre, process_type, current_node.node_code,
                                                        success_node.node_code),
                    "source_node": current_node.node_code,
                    "next_node": success_node.node_code
                })

            else:
                # Intermediate approval nodes
                depend_data.append({
                    "depend_code": generate_depend_code(pre, process_type, current_node.node_code,
                                                        previous_node.node_code),
                    "source_node": current_node.node_code,
                    "next_node": previous_node.node_code
                })
                depend_data.append({
                    "depend_code": generate_depend_code(pre, process_type, current_node.node_code,
                                                        fail_node.node_code),
                    "source_node": current_node.node_code,
                    "next_node": fail_node.node_code
                })
                depend_data.append({
                    "depend_code": generate_depend_code(pre, process_type, current_node.node_code,
                                                        next_node.node_code),
                    "source_node": current_node.node_code,
                    "next_node": next_node.node_code
                })
        depends_list = []
        for depend in depend_data:
            record = create_model_instance(WorkFlowNodeDepend, depend)
            depends_list.append(record)
        return depends_list

    async def add_strategy(self, depends_list, node_list):
        """
        添加依赖策略
        """
        print("获取的测试依赖节点-----------------------开始")
        print([to_dict(item) for item in depends_list])
        print("获取的测试依赖节点-----------------------结束")
        print("\n")

        print("获取的测试节点-----------------------开始")
        print([to_dict(item) for item in node_list])
        print("获取的测试节点-----------------------结束")
        print("\n")
        node_priority = {node.node_code: idx for idx, node in enumerate(node_list)}
        strategy_data = []
        for depend in depends_list:
            source_node = depend.source_node
            next_node = depend.next_node
            depend_code = depend.depend_code
            # 一条依赖关系除了开始节点，审批节点的写入的顺序是：审批节点->失败节点，审批节点->下一个审批节点，审批节点->上一个审批节点
            if "start" in source_node:
                strategy_data.append({
                    "depend_code": depend_code,
                    "parameter_name": "action",
                    "parameter_value": "create",
                    "operation": "="
                })
                continue
            source_priority = node_priority[source_node]
            next_priority = node_priority[next_node]
            if "fail" in next_node:
                strategy_data.append({
                    "depend_code": depend_code,
                    "parameter_name": "action",
                    "parameter_value": "rejected",
                    "operation": "="
                })
            elif source_priority < next_priority:
                strategy_data.append({
                    "depend_code": depend_code,
                    "parameter_name": "action",
                    "parameter_value": "approved",
                    "operation": "="
                })
            elif source_priority > next_priority:
                strategy_data.append({
                    "depend_code": depend_code,
                    "parameter_name": "action",
                    "parameter_value": "revoke",
                    "operation": "="
                })
                strategy_data.append({
                    "depend_code": depend_code,
                    "parameter_name": "node_status",
                    "parameter_value": "pending",
                    "operation": "="
                })
        print("策略列表节点-----------------------开始")
        print(strategy_data)
        print("策略列表节点-----------------------结束")
        print("\n")
        strategy_list = []
        for strategy in strategy_data:
            record = create_model_instance(WorkFlowNodeDependStrategy, strategy)
            strategy_list.append(record)
        return strategy_list

    async def add_work_flow_define(self, work_flow_define: WorkFlowDefineModel):

        process_type = work_flow_define.process_type
        process_code = work_flow_define.process_code
        is_borrow = work_flow_define.is_borrow
        is_borrow_external = work_flow_define.is_borrow_external
        is_borrow_in_school_approval = work_flow_define.is_borrow_in_school_approval
        is_borrow_out_school_approval = work_flow_define.is_borrow_out_school_approval
        is_borrow_in_area_approval = work_flow_define.is_borrow_in_area_approval
        is_borrow_out_area_approval = work_flow_define.is_borrow_out_area_approval
        is_borrow_city_approval = work_flow_define.is_borrow_city_approval

        is_transfer = work_flow_define.is_transfer
        is_transfer_external = work_flow_define.is_transfer_external
        is_transfer_in_school_approval = work_flow_define.is_transfer_in_school_approval
        is_transfer_out_school_approval = work_flow_define.is_transfer_out_school_approval
        is_transfer_in_area_approval = work_flow_define.is_transfer_in_area_approval
        is_transfer_out_area_approval = work_flow_define.is_transfer_out_area_approval
        is_transfer_city_approval = work_flow_define.is_transfer_city_approval

        is_info_school_approval = work_flow_define.is_info_school_approval
        is_info_area_approval = work_flow_define.is_info_area_approval
        is_info_city_approval = work_flow_define.is_info_city_approval

        is_change_school_approval = work_flow_define.is_change_school_approval
        is_change_area_approval = work_flow_define.is_change_area_approval
        is_change_city_approval = work_flow_define.is_change_city_approval

        is_entry_school_approval = work_flow_define.is_entry_school_approval
        is_entry_area_approval = work_flow_define.is_entry_area_approval
        is_entry_city_approval = work_flow_define.is_entry_city_approval

        work_flow_define_db = view_model_to_orm_model(work_flow_define, WorkFlowDefine)
        # work_flow_define_db = await self.work_flow_define_dao.add_work_flow_define(work_flow_define_db)
        # work_flow_define_db = orm_model_to_view_model(work_flow_define_db, WorkFlowDefineModel)

        if process_type == "transfer":

            work_flow_node_list = await self.add_transfer_node(process_code, is_transfer, is_transfer_external,
                                                               is_transfer_in_school_approval=is_transfer_in_school_approval,
                                                               is_transfer_out_school_approval=is_transfer_out_school_approval,
                                                               is_transfer_in_area_approval=is_transfer_in_area_approval,
                                                               is_transfer_out_area_approval=is_transfer_out_area_approval,
                                                               is_transfer_city_approval=is_transfer_city_approval)

            # work_flow_node_list_db = await self.work_flow_node_define_dao.add_work_flow_node_define(
            #     work_flow_node_list)  # 添加节点
            # print("获取的数据库节点-----------------------开始")
            # print([to_dict(item) for item in work_flow_node_list_db])
            # print("获取的数据库节点-----------------------结束")
            # print("\n")
            work_flow_node_depends_list = await self.add_depend(work_flow_node_list, process_type,
                                                                is_transfer=is_transfer,
                                                                transfer_initiate=is_transfer_external)  # 获得依赖节点
            print("获取的依赖节点-----------------------开始")
            print([to_dict(item) for item in work_flow_node_list])
            # print([to_dict(item) for item in work_flow_node_list_db])
            print([to_dict(item) for item in work_flow_node_depends_list])
            print("获取的依赖节点-----------------------结束")
            print("\n")

            # work_flow_node_depends_db = await self.work_flow_node_depend_dao.add_work_flow_node_depend(
            #     work_flow_node_depends_list)  # 获取数据库依赖节点
            # print("获取的数据库依赖节点-----------------------开始")
            # print([to_dict(item) for item in work_flow_node_depends_db])
            # print("获取的数据库依赖节点-----------------------结束")
            # print("\n")

            print("获取的测试-----------------------开始")
            print(work_flow_node_list)
            # print(work_flow_node_list_db)
            print([to_dict(item) for item in work_flow_node_list])
            print("获取的测试-----------------------结束")
            print("\n")

            # print("获取的测试-----------------------开始")
            # print([to_dict(item) for item in work_flow_node_list_db])
            # print("获取的测试-----------------------结束")
            # print("\n")

            work_flow_node_depends_strategy_list = await self.add_strategy(work_flow_node_depends_list,
                                                                           work_flow_node_list)
            print("获取的依赖策略-----------------------开始")
            print([to_dict(item) for item in work_flow_node_depends_strategy_list])
            print("获取的依赖策略-----------------------结束")
            print("\n")
            await self.work_flow_node_depend_strategy_dao.add_work_flow_process(
                work_flow_define_db, work_flow_node_list, work_flow_node_depends_list,
                work_flow_node_depends_strategy_list)
            print("获取的数据库依赖策略-----------------------开始")
            # print([to_dict(item) for item in work_flow_node_depends_strategy_db])
            print("获取的数据库依赖策略-----------------------结束")
            print("\n")

        elif process_type == "borrow":
            pass
        elif process_type == "entry":
            pass
        elif process_type == "info":
            pass
        elif process_type == "change":
            pass


def create_model_instance(model, element):
    """
    根据给定的字典元素创建数据库模型对象实例。

    Args:
    - model: 数据库模型类
    - element: 字典元素，包含模型对象的字段值

    Returns:
    - 创建的数据库模型对象实例
    """
    instance = model()
    for key, value in element.items():
        setattr(instance, key, value)
    return instance


def generate_depend_code(pre, process_type, source, target):
    """生成depend的主键"""

    if process_type == "transfer" or process_type == "borrow":
        source_keywords = "_".join([word for word in source.split('_')][3:5])
        target_keywords = "_".join([word for word in target.split('_')][3:5])
        return f"{pre}_{source_keywords}_to_{target_keywords}"
    elif process_type == "entry" or process_type == "info" or process_type == "change":
        source_keywords = "_".join([word for word in source.split('_')][1:3])
        target_keywords = "_".join([word for word in target.split('_')][1:3])
        return f"{pre}_{source_keywords}_to_{target_keywords}"
