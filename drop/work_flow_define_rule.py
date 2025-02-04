from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from mini_framework.design_patterns.depend_inject import dataclass_inject
from views.models.work_flow_define import WorkFlowDefineModel
from daos.work_flow_node_define_dao import WorkFlowNodeDefineDAO
from daos.work_flow_define_dao import WorkFlowDefineDAO
from daos.work_flow_node_depend_dao import WorkFlowNodeDependDAO
from daos.work_flow_node_depend_strategy_dao import WorkFlowNodeDependStrategyDAO
from drop.work_flow_node_define import WorkFlowNodeDefine
from drop.work_flow_node_depend import WorkFlowNodeDepend
from drop.work_flow_define import WorkFlowDefine
from drop.work_flow_node_depend_strategy import WorkFlowNodeDependStrategy


@dataclass_inject
class WorkFlowNodeDefineRule(object):
    work_flow_node_define_dao: WorkFlowNodeDefineDAO
    work_flow_define_dao: WorkFlowDefineDAO
    work_flow_node_depend_dao: WorkFlowNodeDependDAO
    work_flow_node_depend_strategy_dao: WorkFlowNodeDependStrategyDAO

    async def add_node(self, process_type, process_code, **kwargs):
        """
        对流程增加节点
        """

        # 定义调出时，由系统内向外开始节点信息映射
        out_transfer_out_nodes = {
            'is_transfer_out_area_approval': ('由内向外调出调出区审批节点', 'out_out_tf_out_area_approval'),
            'is_transfer_city_approval': ('由内向外调出调动市审批节点', 'out_out_tf_lc_city_approval'),
            'start': ('调出之调出校开始节点', 'out_out_tf_start_node'),
            'success': ('由内向外调出调动成功节点', 'out_out_tf_success_end'),
            'fail': ('由内向外调出调动失败节点', 'out_out_tf_fail_end')
        }

        # 定义调入校发起调入时，由系统外向系统内节点信息映射
        in_transfer_out_nodes = {
            'is_transfer_in_area_approval': ('由外向内调入调入区审批节点', 'in_out_tf_in_area_approval'),
            'is_transfer_city_approval': ('由外向内调入调动市审批节点', 'in_out_tf_lc_city_approval'),
            'start': ('调入之调出校开始节点', 'in_out_tf_start_node'),
            'success': ('由外向内调入调动成功节点', 'in_out_tf_success_end'),
            'fail': ('由外向内调入调动失败节点', 'in_out_tf_fail_end')
        }

        # 定义调入校发起调入时，由系统内向系统内开始节点信息映射
        in_transfer_in_nodes = {
            'is_transfer_out_school_approval': ('由内向内调入调出校审批节点', 'in_in_tf_out_school_approval'),
            'is_transfer_in_area_approval': ('由内向内调入调入区审批节点', 'in_in_tf_in_area_approval'),
            'is_transfer_out_area_approval': ('由内向内调入调出区审批节点', 'in_in_tf_out_area_approval'),
            'is_transfer_city_approval': ('由内向内调入调动市审批节点', 'in_in_tf_lc_city_approval'),
            'start': ('由内向内调入调入校开始节点', 'in_in_tf_start_node'),
            'success': ('由内向内调入调动成功节点', 'in_in_tf_success_end'),
            'fail': ('由内向内调入调动失败节点', 'in_in_tf_fail_end')
        }

        # 定义借出时，由系统内向外开始节点信息映射
        out_borrow_out_nodes = {
            'is_borrow_out_area_approval': ('由内向外借出借出区审批节点', 'out_out_br_out_area_approval'),
            'is_borrow_city_approval': ('由内向外借出借动市审批节点', 'out_out_br_lc_city_approval'),
            'start': ('借出之借出校开始节点', 'out_out_br_start_node'),
            'success': ('由内向外借出借动成功节点', 'out_out_br_success_end'),
            'fail': ('由内向外借出借动失败节点', 'out_out_br_fail_end')
        }

        # 定义借入校发起借入时，由系统外向系统内节点信息映射
        in_borrow_out_nodes = {
            'is_borrow_in_area_approval': ('由外向内借入借入区审批节点', 'in_out_br_in_area_approval'),
            'is_borrow_city_approval': ('由外向内借入借动市审批节点', 'in_out_br_lc_city_approval'),
            'start': ('借入之借出校开始节点', 'in_out_br_start_node'),
            'success': ('由外向内借入借动成功节点', 'in_out_br_success_end'),
            'fail': ('由外向内借入借动失败节点', 'in_out_br_fail_end')
        }

        # 定义借入校发起借入时，由系统内向系统内开始节点信息映射
        in_borrow_in_nodes = {
            'is_borrow_out_school_approval': ('由内向内借入借出校审批节点', 'in_in_br_out_school_approval'),
            'is_borrow_in_area_approval': ('由内向内借入借入区审批节点', 'in_in_br_in_area_approval'),
            'is_borrow_out_area_approval': ('由内向内借入借出区审批节点', 'in_in_br_out_area_approval'),
            'is_borrow_city_approval': ('由内向内借入借动市审批节点', 'in_in_br_lc_city_approval'),
            'start': ('由内向内借入借入校开始节点', 'in_in_br_start_node'),
            'success': ('由内向内借入借动成功节点', 'in_in_br_success_end'),
            'fail': ('由内向内借入借动失败节点', 'in_in_br_fail_end')
        }

        # 定义教师入职时，节点信息映射
        entry_nodes = {
            'is_entry_school_approval': ('入职校审批节点', f'{process_code}_school_approval'),
            'is_entry_area_approval': ('入职区审批节点', f'{process_code}_area_approval'),
            'is_entry_city_approval': ('入职市审批节点', f'{process_code}_city_approval'),
            'start': ('入职开始节点', f'{process_code}_start_node'),
            'success': ('入职成功节点', f'{process_code}_success_end'),
            'fail': ('入职失败节点', f'{process_code}_fail_end')
        }

        # 定义教师信息修改时，节点信息映射
        info_nodes = {
            'is_info_school_approval': ('信息修改校审批节点', f'{process_code}_school_approval'),
            'is_info_area_approval': ('信息修改区审批节点', f'{process_code}_area_approval'),
            'is_info_city_approval': ('信息修改市审批节点', f'{process_code}_city_approval'),
            'start': ('信息修改开始节点', f'{process_code}_start_node'),
            'success': ('信息修改成功节点', f'{process_code}_success_end'),
            'fail': ('信息修改失败节点', f'{process_code}_fail_end')
        }
        # 定义教师变动时，节点信息映射
        change_nodes = {
            'is_change_school_approval': ('变动校审批节点', f'{process_code}_school_approval'),
            'is_change_area_approval': ('变动区审批节点', f'{process_code}_area_approval'),
            'is_change_city_approval': ('变动市审批节点', f'{process_code}_city_approval'),
            'start': ('变动开始节点', f'{process_code}_start_node'),
            'success': ('变动成功节点', f'{process_code}_success_end'),
            'fail': ('变动失败节点', f'{process_code}_fail_end')
        }

        # 初始化节点定义表
        nodes_list = []

        # 根据是调入流程还是调出流程分别处理
        if process_type == "transfer":
            is_transfer = kwargs.get('is_transfer')
            is_transfer_external = kwargs.get('is_transfer_external')
            if is_transfer:  # 代表是调出流程
                nodes_info = out_transfer_out_nodes

            else:  # 代表是调入流程
                if is_transfer_external:
                    nodes_info = in_transfer_out_nodes
                else:
                    nodes_info = in_transfer_in_nodes
        elif process_type == "borrow":
            is_borrow = kwargs.get('is_borrow')
            is_borrow_external = kwargs.get('is_borrow_external')
            if is_borrow:  # 代表是借出流程
                nodes_info = out_borrow_out_nodes
            else:  # 代表是借入流程
                if is_borrow_external:
                    nodes_info = in_borrow_out_nodes
                else:
                    nodes_info = in_borrow_in_nodes
        elif process_type == "entry":
            nodes_info = entry_nodes
        elif process_type == "info":
            nodes_info = info_nodes
        elif process_type == "change":
            nodes_info = change_nodes
        else:
            raise Exception("未知流程类型")

        # 添加开始节点
        nodes_list.append(generate_node(process_code, nodes_info['start'][0], nodes_info['start'][1]))

        # 遍历检查条件，判断是否需要新增节点
        for key, value in kwargs.items():
            if value and key in nodes_info:
                nodes_list.append(generate_node(process_code, nodes_info[key][0], nodes_info[key][1]))

        # 添加成功和失败节点
        nodes_list.append(generate_node(process_code, nodes_info['success'][0], nodes_info['success'][1]))
        nodes_list.append(generate_node(process_code, nodes_info['fail'][0], nodes_info['fail'][1]))

        # 转化为数据库模型
        db_records = []
        for node in nodes_list:
            record = create_model_instance(WorkFlowNodeDefine, node)
            db_records.append(record)
        return db_records

    async def add_depend(self, node_list, process_code, process_type, **kwargs):
        """
        添加依赖
        """
        process_type = process_type
        if process_type == "transfer":
            is_transfer = kwargs.get('is_transfer')
            is_transfer_external = kwargs.get('is_transfer_external')
            if is_transfer:
                if is_transfer_external:
                    pre = "ootf"  # 调出时，由系统内向外开始节点
            else:
                if is_transfer_external:
                    pre = "iotf"  # 调入时，由系统外向内调入节点
                else:
                    pre = "iitf"  # 调入时，由系统内向系统内开始节点
        elif process_type == "borrow":
            is_borrow = kwargs.get('is_borrow')
            is_borrow_external = kwargs.get('is_borrow_external')
            if is_borrow:
                if is_borrow_external:
                    pre = "oobr"
            else:
                if is_borrow_external:
                    pre = "iobr"
                else:
                    pre = "iibr"
        else:
            pre = process_code
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
                depend_data.append(generate_depend(pre, process_type, node_list[0].node_code,
                                                   current_node.node_code))
                depend_data.append(generate_depend(pre, process_type, current_node.node_code,
                                                   node_list[0].node_code))
                depend_data.append(generate_depend(pre, process_type, current_node.node_code,
                                                   fail_node.node_code))
                depend_data.append(generate_depend(pre, process_type, current_node.node_code,
                                                   next_node.node_code))

            elif i == num_nodes - 3:
                # Last approval node
                depend_data.append(generate_depend(pre, process_type, current_node.node_code,
                                                   previous_node.node_code))

                depend_data.append(generate_depend(pre, process_type, current_node.node_code,
                                                   fail_node.node_code))
                depend_data.append(generate_depend(pre, process_type, current_node.node_code,
                                                   success_node.node_code))

            else:
                # Intermediate approval nodes
                depend_data.append(generate_depend(pre, process_type, current_node.node_code,
                                                   previous_node.node_code))
                depend_data.append(generate_depend(pre, process_type, current_node.node_code,
                                                   fail_node.node_code))
                depend_data.append(generate_depend(pre, process_type, current_node.node_code,
                                                   next_node.node_code))
        depends_list = []
        for depend in depend_data:
            record = create_model_instance(WorkFlowNodeDepend, depend)
            depends_list.append(record)
        return depends_list

    async def add_strategy(self, depends_list, node_list):
        """
        添加依赖策略
        """
        node_priority = {node.node_code: idx for idx, node in enumerate(node_list)}
        strategy_data = []
        for depend in depends_list:
            source_node = depend.source_node
            next_node = depend.next_node
            depend_code = depend.depend_code
            # 一条依赖关系除了开始节点，审批节点的写入的顺序是：审批节点->失败节点，审批节点->下一个审批节点，审批节点->上一个审批节点
            if "start" in source_node:
                strategy_data.append(generate_strategy(depend_code, "action", "create", "="))
                continue
            source_priority = node_priority[source_node]
            next_priority = node_priority[next_node]
            if "fail" in next_node:
                strategy_data.append(generate_strategy(depend_code, "action", "rejected", "="))
            elif source_priority < next_priority:
                strategy_data.append(generate_strategy(depend_code, "action", "approved", "="))
            elif source_priority > next_priority:
                strategy_data.append(generate_strategy(depend_code, "action", "revoke", "="))
                strategy_data.append(generate_strategy(depend_code, "node_status", "pending", "="))
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
        exit_flow = await self.work_flow_define_dao.get_work_flow_define_by_process_code(process_code)
        if exit_flow:
            raise Exception("流程已存在")
        work_flow_node_list = await self.add_node(process_type, process_code,
                                                  is_borrow=is_borrow, is_borrow_external=is_borrow_external,
                                                  is_borrow_in_school_approval=is_borrow_in_school_approval,
                                                  is_borrow_out_school_approval=is_borrow_out_school_approval,
                                                  is_borrow_in_area_approval=is_borrow_in_area_approval,
                                                  is_borrow_out_area_approval=is_borrow_out_area_approval,
                                                  is_borrow_city_approval=is_borrow_city_approval,
                                                  is_transfer=is_transfer,
                                                  is_transfer_external=is_transfer_external,
                                                  is_transfer_in_school_approval=is_transfer_in_school_approval,
                                                  is_transfer_out_school_approval=is_transfer_out_school_approval,
                                                  is_transfer_in_area_approval=is_transfer_in_area_approval,
                                                  is_transfer_out_area_approval=is_transfer_out_area_approval,
                                                  is_transfer_city_approval=is_transfer_city_approval,
                                                  is_info_school_approval=is_info_school_approval,
                                                  is_info_area_approval=is_info_area_approval,
                                                  is_info_city_approval=is_info_city_approval,
                                                  is_change_school_approval=is_change_school_approval,
                                                  is_change_area_approval=is_change_area_approval,
                                                  is_change_city_approval=is_change_city_approval,
                                                  is_entry_school_approval=is_entry_school_approval,
                                                  is_entry_area_approval=is_entry_area_approval,
                                                  is_entry_city_approval=is_entry_city_approval
                                                  )
        if process_type == "transfer":
            work_flow_node_depends_list = await self.add_depend(work_flow_node_list, process_code, process_type,
                                                                is_transfer=is_transfer,
                                                                transfer_initiate=is_transfer_external)  # 获得依赖节点
        elif process_type == "borrow":
            work_flow_node_depends_list = await self.add_depend(work_flow_node_list, process_code, process_type,
                                                                is_borrow=is_borrow,
                                                                borrow_initiate=is_borrow_external)
        else:
            work_flow_node_depends_list = await self.add_depend(work_flow_node_list, process_code, process_type)

        work_flow_node_depends_strategy_list = await self.add_strategy(work_flow_node_depends_list,
                                                                       work_flow_node_list)

        work_flow_define_db, work_flow_node_list, work_flow_node_depends_list, work_flow_node_depends_strategy_list = await self.work_flow_node_depend_strategy_dao.add_work_flow_process(
            work_flow_define_db, work_flow_node_list, work_flow_node_depends_list,
            work_flow_node_depends_strategy_list)
        work_flow_define_db = orm_model_to_view_model(work_flow_define_db, WorkFlowDefineModel)
        return work_flow_define_db


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
        source_keywords = [word for word in source.split('_')][-2]
        target_keywords = [word for word in target.split('_')][-2]
        return f"{pre}_{source_keywords}_to_{target_keywords}"


def generate_depend(pre, process_type, current_node_node_code,
                    next_node_node_code):
    """添加单个depend"""

    depend = {"depend_code": generate_depend_code(pre, process_type, current_node_node_code,
                                                  next_node_node_code),
              "source_node": current_node_node_code,
              "next_node": next_node_node_code}
    return depend


def generate_strategy(depend_code, parameter_name, parameter_value, operation):
    """添加单个strategy"""

    strategy = {"depend_code": depend_code,
                "parameter_name": parameter_name,
                "parameter_value": parameter_value,
                "operation": operation}
    return strategy


def generate_node(process_code, node_name, node_code):
    """添加单个node"""

    node = {"process_code": process_code,
            "node_name": node_name,
            "node_code": node_code}
    return node
