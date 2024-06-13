from sqlalchemy import select, func, update
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.teacher_borrow import TeacherBorrow
from models.teachers import Teacher
from views.models.teacher_transaction import TeacherBorrowQueryModel
from models.teachers_info import TeacherInfo
from models.teachers import Teacher
from models.work_flow_node_instance import WorkFlowNodeInstance
from models.school import School


class TeacherBorrowDAO(DAOBase):

    async def add_teacher_borrow(self, teacher_borrow: TeacherBorrow):
        session = await self.master_db()
        session.add(teacher_borrow)
        await session.commit()
        await session.refresh(teacher_borrow)
        return teacher_borrow

    async def get_teacher_borrow_count(self, ):
        session = await self.slave_db()
        result = await session.execute(select(func.count()).select_from(TeacherBorrow))
        return result.scalar()

    async def delete_teacher_borrow(self, teacher_borrow: TeacherBorrow):
        session = await self.master_db()
        await session.delete(teacher_borrow)
        await session.commit()

    async def get_teacher_borrow_by_teacher_borrow_id(self, teacher_borrow_id):
        session = await self.slave_db()
        result = await session.execute(
            select(TeacherBorrow).where(TeacherBorrow.teacher_borrow_id == teacher_borrow_id))
        return result.scalar_one_or_none()

    async def update_teacher_borrow(self, teacher_borrow, *args, is_commit=True):
        session = await self.master_db()
        update_contents = get_update_contents(teacher_borrow, *args)
        query = update(TeacherBorrow).where(
            TeacherBorrow.teacher_borrow_id == teacher_borrow.teacher_borrow_id).values(
            **update_contents)
        return await self.update(session, query, teacher_borrow, update_contents, is_commit=is_commit)

    async def query_teacher_borrow_with_page(self, teacher_borrow, *args, is_commit=True):
        session = await self.master_db()
        update_contents = get_update_contents(teacher_borrow, *args)
        query = update(TeacherBorrow).where(
            TeacherBorrow.teacher_borrow_id == teacher_borrow.teacher_borrow_id).values(
            **update_contents)
        return await self.update(session, query, teacher_borrow, update_contents, is_commit=is_commit)

    async def query_borrow_out_launch_with_page(self, query_model: TeacherBorrowQueryModel,
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
        query = select(TeacherBorrow, Teacher.teacher_name, Teacher.teacher_id_type, Teacher.teacher_gender,
                       Teacher.teacher_id_number, Teacher.teacher_employer, School.school_name,
                       TeacherInfo.teacher_number, subquery.c.approval_time, subquery.c.node_status,
                       subquery.c.approval_name,
                       subquery.c.node_code).join(Teacher, Teacher.teacher_id == TeacherBorrow.teacher_id,
                                                  isouter=True).join(
            TeacherInfo, TeacherInfo.teacher_id == TeacherBorrow.teacher_id, isouter=True).join(School,
                                                                                                School.id == Teacher.teacher_employer,
                                                                                                isouter=True).join(
            WorkFlowNodeInstance,
            WorkFlowNodeInstance.process_instance_id == TeacherBorrow.process_instance_id,
            isouter=True).join(subquery,
                               subquery.c.process_instance_id == WorkFlowNodeInstance.process_instance_id,
                               isouter=True).where(TeacherBorrow.borrow_type == "borrow_out")
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
            query = query.where(TeacherBorrow.original_district == query_model.original_district)
        if query_model.original_unit:
            query = query.where(TeacherBorrow.original_unit == query_model.original_unit)
        if query_model.current_district:
            query = query.where(TeacherBorrow.current_district == query_model.current_district)
        if query_model.current_unit:
            query = query.where(TeacherBorrow.current_unit == query_model.current_unit)
        if query_model.current_region:
            query = query.where(TeacherBorrow.current_region == query_model.current_region)
        if query_model.original_region:
            query = query.where(TeacherBorrow.original_region == query_model.original_region)
        if query_model.approval_status:
            query = query.where(TeacherBorrow.approval_status == query_model.approval_status)
        if query_model.operation_time:
            query = query.where(func.date(TeacherBorrow.operation_time) == query_model.operation_time)
        if query_model.approval_time:
            query = query.where(func.date(subquery.c.approval_time) == query_model.approval_time)
        if query_model.approval_name:
            query = query.where(subquery.c.approval_name.like(f"%{query_model.approval_name}%"))
        paging = await self.query_page(query, page_request)
        return paging

    async def query_borrow_out_approval_with_page(self, query_model: TeacherBorrowQueryModel,
                                                  page_request: PageRequest) -> Paging:
        """
        查询条件
        借动审批的查询
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
        query = select(TeacherBorrow, Teacher.teacher_name, Teacher.teacher_id_type, Teacher.teacher_gender,
                       Teacher.teacher_id_number, Teacher.teacher_employer, School.school_name,
                       TeacherInfo.teacher_number, subquery.c.approval_time, subquery.c.node_status,
                       subquery.c.approval_name,
                       subquery.c.node_code).join(Teacher, Teacher.teacher_id == TeacherBorrow.teacher_id,
                                                  isouter=True).join(
            TeacherInfo, TeacherInfo.teacher_id == TeacherBorrow.teacher_id, isouter=True).join(School,
                                                                                                School.id == Teacher.teacher_employer,
                                                                                                isouter=True).join(
            WorkFlowNodeInstance,
            WorkFlowNodeInstance.process_instance_id == TeacherBorrow.process_instance_id,
            isouter=True).join(subquery,
                               subquery.c.process_instance_id == WorkFlowNodeInstance.process_instance_id,
                               isouter=True).where(TeacherBorrow.borrow_type == "borrow_out")
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
            query = query.where(TeacherBorrow.original_district == query_model.original_district)
        if query_model.original_unit:
            query = query.where(TeacherBorrow.original_unit == query_model.original_unit)
        if query_model.current_district:
            query = query.where(TeacherBorrow.current_district == query_model.current_district)
        if query_model.current_unit:
            query = query.where(TeacherBorrow.current_unit == query_model.current_unit)
        if query_model.current_region:
            query = query.where(TeacherBorrow.current_region == query_model.current_region)
        if query_model.original_region:
            query = query.where(TeacherBorrow.original_region == query_model.original_region)
        if query_model.approval_status:
            query = query.where(TeacherBorrow.approval_status == query_model.approval_status)
        if query_model.operation_time:
            query = query.where(func.date(TeacherBorrow.operation_time) == query_model.operation_time)
        if query_model.approval_time:
            query = query.where(func.date(subquery.c.approval_time) == query_model.approval_time)
        if query_model.approval_name:
            query = query.where(subquery.c.approval_name.like(f"%{query_model.approval_name}%"))
        paging = await self.query_page(query, page_request)
        return paging

    async def query_borrow_in_launch_with_page(self, query_model: TeacherBorrowQueryModel,
                                               page_request: PageRequest) -> Paging:
        pass

    async def query_borrow_in_approval_with_page(self, query_model: TeacherBorrowQueryModel,
                                                 page_request: PageRequest) -> Paging:
        pass

    async def get_all_teacher_borrow(self, teacher_id):
        session = await self.slave_db()
        subquery = (select(func.max(WorkFlowNodeInstance.operation_time).label("approval_time"),
                           WorkFlowNodeInstance.node_status.label("node_status"),
                           WorkFlowNodeInstance.process_instance_id.label("process_instance_id"),
                           WorkFlowNodeInstance.operator_name.label("approval_name"),
                           WorkFlowNodeInstance.node_code.label("node_code")).group_by(
            WorkFlowNodeInstance.process_instance_id)).alias("subquery")

        query = (select(TeacherBorrow, subquery.c.approval_time, subquery.c.node_status, subquery.c.approval_name,
                        subquery.c.node_code, ).join(
            Teacher, TeacherBorrow.teacher_id == Teacher.teacher_id)).join(WorkFlowNodeInstance,
                                                                           WorkFlowNodeInstance.process_instance_id == TeacherBorrow.process_instance_id,
                                                                           isouter=True).join(subquery,
                                                                                              subquery.c.process_instance_id == WorkFlowNodeInstance.process_instance_id,
                                                                                              isouter=True)
        query = query.where(
            TeacherBorrow.teacher_id == teacher_id)
        result = await session.execute(query)
        return result.scalars().all()
