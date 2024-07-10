from sqlalchemy import select, func, update
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.classes import Classes
from models.planning_school import PlanningSchool
from models.school import School
from models.student_inner_transaction import StudentInnerTransaction
from models.students import Student
from models.students_base_info import StudentBaseInfo


class StudentInnerTransactionDAO(DAOBase):

    async def add_student_inner_transaction(self, student_inner_transaction: StudentInnerTransaction):
        session = await self.master_db()
        session.add(student_inner_transaction)
        await session.commit()
        await session.refresh(student_inner_transaction)
        return student_inner_transaction

    async def get_student_inner_transaction_count(self, ):
        session = await self.slave_db()
        result = await session.execute(select(func.count()).select_from(StudentInnerTransaction))
        return result.scalar()

    async def delete_student_inner_transaction(self, student_inner_transaction: StudentInnerTransaction):
        session = await self.master_db()
        await session.delete(student_inner_transaction)
        await session.commit()

    async def get_student_inner_transaction_by_id(self, id):
        session = await self.slave_db()
        result = await session.execute(select(StudentInnerTransaction).where(StudentInnerTransaction.id == int(id)))
        return result.scalar_one_or_none()

    async def query_student_inner_transaction_with_page(self, student_inner_transaction_search,
                                                        page_request: PageRequest):
        query = select(
            # StudentInnerTransaction,
                       StudentInnerTransaction.id, StudentInnerTransaction.student_id, StudentInnerTransaction.school_id, StudentInnerTransaction.class_id, StudentInnerTransaction.transaction_type, StudentInnerTransaction.transaction_reason, StudentInnerTransaction.transaction_remark, StudentInnerTransaction.transaction_time, StudentInnerTransaction.transaction_user, StudentInnerTransaction.transaction_user_id, StudentInnerTransaction.created_uid, StudentInnerTransaction.updated_uid, StudentInnerTransaction.created_at, StudentInnerTransaction.updated_at, Student.approval_status, StudentInnerTransaction.is_deleted,
                       School.school_name,
                       Classes.class_name,
                       PlanningSchool.borough,
                       Student.student_name,
                       Student.student_gender,
                       Student.approval_status,
                       StudentBaseInfo.edu_number,
                       ).select_from(StudentInnerTransaction).join(School,
                                                                   StudentInnerTransaction.school_id == School.id,isouter=True).join(
            PlanningSchool, School.planning_school_id == PlanningSchool.id,isouter=True).join(Student,
                                                                                 StudentInnerTransaction.student_id == Student.student_id,isouter=True).join(
            StudentBaseInfo, StudentBaseInfo.student_id == Student.student_id,isouter=True).join(Classes,
                                                                                    StudentInnerTransaction.class_id == Classes.id,isouter=True)

        ### �˴���д��ѯ����
        if student_inner_transaction_search.student_name:
            query = query.where(Student.student_name.like(f'%{student_inner_transaction_search.student_name}%'))
        if student_inner_transaction_search.student_gender:
            query = query.where(Student.student_gender == student_inner_transaction_search.student_gender)
        if student_inner_transaction_search.edu_number:
            query = query.where(StudentBaseInfo.edu_number == student_inner_transaction_search.edu_number)
        if student_inner_transaction_search.school_id:
            query = query.where(StudentInnerTransaction.school_id == int(student_inner_transaction_search.school_id))
        if student_inner_transaction_search.borough:
            query = query.where(PlanningSchool.borough == student_inner_transaction_search.borough)
        if student_inner_transaction_search.class_id:
            query = query.where(StudentInnerTransaction.class_id == int(student_inner_transaction_search.class_id))

        paging = await self.query_page(query, page_request)
        return paging

    async def update_student_inner_transaction(self, student_inner_transaction, *args, is_commit=True):
        session = await self.master_db()
        update_contents = get_update_contents(student_inner_transaction, *args)
        query = update(StudentInnerTransaction).where(
            StudentInnerTransaction.id == int(student_inner_transaction.id)).values(**update_contents)
        return await self.update(session, query, student_inner_transaction, update_contents, is_commit=is_commit)
