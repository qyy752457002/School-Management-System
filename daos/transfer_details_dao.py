from sqlalchemy import select, func, update
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.transfer_details import TransferDetails
from views.models.teacher_transaction import TeacherTransferQueryModel
from models.teachers_info import TeacherInfo
from models.teachers import Teacher
from models.work_flow_node_instance import WorkFlowNodeInstance
from models.work_flow_instance import WorkFlowInstance
from models.school import School


class TransferDetailsDAO(DAOBase):

    async def add_transfer_details(self, transfer_details: TransferDetails):
        session = await self.master_db()
        session.add(transfer_details)
        await session.commit()
        await session.refresh(transfer_details)
        return transfer_details

    async def get_transfer_details_count(self, ):
        session = await self.slave_db()
        result = await session.execute(select(func.count()).select_from(TransferDetails))
        return result.scalar()

    async def delete_transfer_details(self, transfer_details: TransferDetails):
        session = await self.master_db()
        await session.delete(transfer_details)
        await session.commit()

    async def get_transfer_details_by_transfer_details_id(self, transfer_details_id):
        session = await self.slave_db()
        result = await session.execute(
            select(TransferDetails).where(TransferDetails.transfer_details_id == transfer_details_id))
        return result.scalar_one_or_none()

    async def update_transfer_details(self, teacher_transfer, *args, is_commit=True):
        session = await self.master_db()
        update_contents = get_update_contents(teacher_transfer, *args)
        query = update(TransferDetails).where(
            TransferDetails.transfer_details_id == teacher_transfer.transfer_details_id).values(
            **update_contents)
        return await self.update(session, query, teacher_transfer, update_contents, is_commit=is_commit)

    async def query_transfer_out_launch_with_page(self, query_model: TeacherTransferQueryModel,
                                                  page_request: PageRequest) -> Paging:
        """
        查询条件
        调动审批的查询
        教师姓名：teacher_name
        教职工号：teacher_number
        身份证类型：teacher_id_type
        身份证号：teacher_id_number
        教师性别：teacher_gender
        原行政属地：original_district
        原单位：original_unit
        现行政属地：current_district
        现单位：current_unit
        审批状态：approval_status
        申请时间：operation_time
        审批时间：approval_time
        申请人：operator_name
        审批人：approval_name
        """
        # todo 还缺一个传过来的用户参数，就是筛选出我发起的审批
        subquery = (select(func.max(WorkFlowNodeInstance.operation_time).label("approval_time"),
                           WorkFlowNodeInstance.node_status.label("node_status"),
                           WorkFlowNodeInstance.process_instance_id.label("process_instance_id"),
                           WorkFlowNodeInstance.operator_name.label("approval_name"),
                           WorkFlowNodeInstance.node_code.label("node_code")).group_by(
            WorkFlowNodeInstance.process_instance_id)).alias("subquery")
        query = select(TransferDetails, Teacher.teacher_name, Teacher.teacher_id_type, Teacher.teacher_gender,
                       Teacher.teacher_id_number, Teacher.teacher_employer, School.school_name,
                       TeacherInfo.teacher_number, subquery.c.approval_time, WorkFlowInstance.process_status,
                       subquery.c.approval_name,
                       subquery.c.node_code).join(Teacher, Teacher.teacher_id == TransferDetails.teacher_id,
                                                  isouter=True).join(
            TeacherInfo, TeacherInfo.teacher_id == TransferDetails.teacher_id, isouter=True).join(School,
                                                                                                  School.id == Teacher.teacher_employer,
                                                                                                  isouter=True).join(
            WorkFlowInstance, WorkFlowInstance.process_instance_id == TransferDetails.process_instance_id).join(
            WorkFlowNodeInstance,
            WorkFlowNodeInstance.process_instance_id == WorkFlowInstance.process_instance_id,
            isouter=True).join(subquery,
                               subquery.c.process_instance_id == WorkFlowNodeInstance.process_instance_id,
                               isouter=True).where(TransferDetails.transfer_type == "transfer_out")
        # query=query.where()
        if query_model.teacher_name:
            query = query.where(Teacher.teacher_name.like(f"%{query_model.teacher_name}%"))
        if query_model.teacher_number:
            query = query.where(TeacherInfo.teacher_number == query_model.teacher_number)
        if query_model.teacher_id_type:
            query = query.where(Teacher.teacher_id_type == query_model.teacher_id_type)
        if query_model.teacher_id_number:
            query = query.where(Teacher.teacher_id_number == query_model.teacher_id_number)
        if query_model.teacher_gender:
            query = query.where(Teacher.teacher_gender == query_model.teacher_gender)
        if query_model.original_district:
            query = query.where(TransferDetails.original_district == query_model.original_district)
        if query_model.original_unit:
            query = query.where(TransferDetails.original_unit == query_model.original_unit)
        if query_model.current_district:
            query = query.where(TransferDetails.current_district == query_model.current_district)
        if query_model.current_unit:
            query = query.where(TransferDetails.current_unit == query_model.current_unit)
        if query_model.current_region:
            query = query.where(TransferDetails.current_region == query_model.current_region)
        if query_model.original_region:
            query = query.where(TransferDetails.original_region == query_model.original_region)
        if query_model.approval_status:
            query = query.where(TransferDetails.approval_status == query_model.approval_status)
        if query_model.operation_time:
            query = query.where(func.date(TransferDetails.operation_time) == query_model.operation_time)
        if query_model.approval_time:
            query = query.where(func.date(subquery.c.approval_time) == query_model.approval_time)
        if query_model.approval_name:
            query = query.where(subquery.c.approval_name.like(f"%{query_model.approval_name}%"))
        paging = await self.query_page(query, page_request)
        return paging

    async def query_transfer_out_approval_with_page(self, query_model: TeacherTransferQueryModel,
                                                    page_request: PageRequest) -> Paging:
        """
        查询条件
        调动审批的查询
        教师姓名：teacher_name
        教职工号：teacher_number
        身份证类型：teacher_id_type
        身份证号：teacher_id_number
        教师性别：teacher_gender
        原行政属地：original_district
        原单位：original_unit
        现行政属地：current_district
        现单位：current_unit
        审批状态：approval_status
        申请时间：operation_time
        审批时间：approval_time
        申请人：operator_name
        审批人：approval_name
        """
        subquery = (select(func.max(WorkFlowNodeInstance.operation_time).label("approval_time"),
                           WorkFlowNodeInstance.node_status.label("node_status"),
                           WorkFlowNodeInstance.process_instance_id.label("process_instance_id"),
                           WorkFlowNodeInstance.operator_name.label("approval_name"),
                           WorkFlowNodeInstance.node_code.label("node_code")).group_by(
            WorkFlowNodeInstance.process_instance_id)).alias("subquery")
        query = select(TransferDetails, Teacher.teacher_name, Teacher.teacher_id_type, Teacher.teacher_gender,
                       Teacher.teacher_id_number, Teacher.teacher_employer, School.school_name,
                       TeacherInfo.teacher_number, subquery.c.approval_time, subquery.c.node_status,
                       subquery.c.approval_name,
                       subquery.c.node_code).join(Teacher, Teacher.teacher_id == TransferDetails.teacher_id,
                                                  isouter=True).join(
            TeacherInfo, TeacherInfo.teacher_id == TransferDetails.teacher_id, isouter=True).join(School,
                                                                                                  School.id == Teacher.teacher_employer,
                                                                                                  isouter=True).join(
            WorkFlowInstance, WorkFlowInstance.process_instance_id == TransferDetails.process_instance_id).join(
            WorkFlowNodeInstance,
            WorkFlowNodeInstance.process_instance_id == WorkFlowInstance.process_instance_id,
            isouter=True).join(subquery,
                               subquery.c.process_instance_id == WorkFlowNodeInstance.process_instance_id,
                               isouter=True).where(TransferDetails.transfer_type == "transfer_out")
        if query_model.teacher_name:
            query = query.where(Teacher.teacher_name.like(f"%{query_model.teacher_name}%"))
        if query_model.teacher_number:
            query = query.where(TeacherInfo.teacher_number == query_model.teacher_number)
        if query_model.teacher_id_type:
            query = query.where(Teacher.teacher_id_type == query_model.teacher_id_type)
        if query_model.teacher_id_number:
            query = query.where(Teacher.teacher_id_number == query_model.teacher_id_number)
        if query_model.teacher_gender:
            query = query.where(Teacher.teacher_gender == query_model.teacher_gender)
        if query_model.original_district:
            query = query.where(TransferDetails.original_district == query_model.original_district)
        if query_model.original_unit:
            query = query.where(TransferDetails.original_unit == query_model.original_unit)
        if query_model.current_district:
            query = query.where(TransferDetails.current_district == query_model.current_district)
        if query_model.current_unit:
            query = query.where(TransferDetails.current_unit == query_model.current_unit)
        if query_model.current_region:
            query = query.where(TransferDetails.current_region == query_model.current_region)
        if query_model.original_region:
            query = query.where(TransferDetails.original_region == query_model.original_region)
        if query_model.approval_status:
            query = query.where(TransferDetails.approval_status == query_model.approval_status)
        if query_model.operation_time:
            query = query.where(func.date(TransferDetails.operation_time) == query_model.operation_time)
        if query_model.approval_time:
            query = query.where(func.date(subquery.c.approval_time) == query_model.approval_time)
        if query_model.approval_name:
            query = query.where(subquery.c.approval_name.like(f"%{query_model.approval_name}%"))
        paging = await self.query_page(query, page_request)
        return paging

    async def query_transfer_in_launch_with_page(self, query_model: TeacherTransferQueryModel,
                                                 page_request: PageRequest) -> Paging:
        pass

    async def query_transfer_in_approval_with_page(self, query_model: TeacherTransferQueryModel,
                                                   page_request: PageRequest) -> Paging:
        pass

    async def get_all_transfer_details(self, teacher_id):
        session = await self.slave_db()
        subquery = (select(func.max(WorkFlowNodeInstance.operation_time).label("approval_time"),
                           WorkFlowNodeInstance.node_status.label("node_status"),
                           WorkFlowNodeInstance.process_instance_id.label("process_instance_id"),
                           WorkFlowNodeInstance.operator_name.label("approval_name"),
                           WorkFlowNodeInstance.node_code.label("node_code")).group_by(
            WorkFlowNodeInstance.process_instance_id)).alias("subquery")

        query = (select(TransferDetails, subquery.c.approval_time, subquery.c.node_status, subquery.c.approval_name,
                        subquery.c.node_code, ).join(
            Teacher, TransferDetails.teacher_id == Teacher.teacher_id)).join(WorkFlowNodeInstance,
                                                                             WorkFlowNodeInstance.process_instance_id == TransferDetails.process_instance_id,
                                                                             isouter=True).join(subquery,
                                                                                                subquery.c.process_instance_id == WorkFlowNodeInstance.process_instance_id,
                                                                                                isouter=True)
        query = query.where(
            TransferDetails.teacher_id == teacher_id)
        result = await session.execute(query)
        return result.scalars().all()
