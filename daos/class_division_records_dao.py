from datetime import date

from sqlalchemy import select, func, update, and_, or_
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.class_division_records import ClassDivisionRecords
from models.classes import Classes

from models.students import Student, StudentApprovalAtatus


class ClassDivisionRecordsDAO(DAOBase):

    async def add_class_division_records(self, class_division_records: ClassDivisionRecords):
        session = await self.master_db()
        session.add(class_division_records)
        await session.commit()
        await session.refresh(class_division_records)
        return class_division_records

    async def get_class_division_records_count(self, ):
        session = await self.slave_db()
        result = await session.execute(select(func.count()).select_from(ClassDivisionRecords))
        return result.scalar()

    async def delete_class_division_records(self, class_division_records: ClassDivisionRecords):
        session = await self.master_db()
        await session.delete(class_division_records)
        await session.commit()

    async def get_class_division_records_by_id(self, id):
        session = await self.slave_db()
        result = await session.execute(select(ClassDivisionRecords).where(ClassDivisionRecords.id == id))
        return result.scalar_one_or_none()

    async def query_class_division_records_with_page(self, school_id, id_type, student_name, created_at, student_gender,
                                                     class_id, status, enrollment_number, page_request: PageRequest,
                                                     ):
        specific_date = date(1970, 1, 1)
        query = select(
            func.coalesce(Classes.class_name, '').label('class_name') ,
            func.coalesce(Student.student_name, '').label('student_name') ,
            func.coalesce(ClassDivisionRecords.class_id, 0).label('class_id') ,
            func.coalesce(Student.student_id, 0).label('student_id'),
            func.coalesce(ClassDivisionRecords.school_id, 0).label('school_id'),
            func.coalesce(ClassDivisionRecords.id, 0).label('id'),
            func.coalesce(ClassDivisionRecords.created_at, specific_date).label('created_at'),

            Student.approval_status,

            ClassDivisionRecords.status,
            Student.id_number,
            Student.student_id,
            Student.student_name, Student.enrollment_number,
            Student.student_gender,

            Student.id_type,

        ).select_from(Student).join(ClassDivisionRecords, ClassDivisionRecords.student_id == Student.student_id, isouter=True).join(Classes, ClassDivisionRecords.class_id == Classes.id, isouter=True)

        ### 此处填写查询条件
        # query = query.where(ClassDivisionRecords.is_deleted == False)
        query = query.where(Student.is_deleted == False)
        cond1 = ClassDivisionRecords.is_deleted == False
        cond2 = ClassDivisionRecords.id == None
        mcond = or_(cond1, cond2)

        query = query.filter(    mcond)


        if school_id:
            query = query.where(ClassDivisionRecords.school_id == school_id)
        if id_type:
            query = query.where(Student.id_type == id_type)
        if student_name:
            query = query.where(ClassDivisionRecords.student_name == student_name)
        if created_at:
            query = query.where(ClassDivisionRecords.created_at == created_at)
        if student_gender:
            query = query.where(Student.student_gender == student_gender)
        if class_id:
            query = query.where(ClassDivisionRecords.class_id == class_id)
        if status:
            query = query.where(Student.approval_status == status)
        else:
            query = query.where(Student.approval_status != StudentApprovalAtatus.OUT.value)

        if enrollment_number:
            query = query.where(Student.enrollment_number == enrollment_number)

        paging = await self.query_page(query, page_request)
        return paging

    async def update_class_division_records(self, class_division_records, *args, is_commit=True):
        session = await self.master_db()
        update_contents = get_update_contents(class_division_records, *args)
        query = update(ClassDivisionRecords).where(ClassDivisionRecords.id == class_division_records.id).values(
            **update_contents)
        return await self.update(session, query, class_division_records, update_contents, is_commit=is_commit)
