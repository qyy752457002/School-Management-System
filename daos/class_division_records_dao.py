from sqlalchemy import select, func, update
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.class_division_records import ClassDivisionRecords

from models.students import Student


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
        query = select(ClassDivisionRecords.class_id, ClassDivisionRecords.student_id,
                       # ClassDivisionRecords.student_name,
					   ClassDivisionRecords.created_at, Student.approval_status,
                        ClassDivisionRecords.school_id, ClassDivisionRecords.id,
                       ClassDivisionRecords.class_id,
                       ClassDivisionRecords.student_id,
					   ClassDivisionRecords.student_name, ClassDivisionRecords.created_at, ClassDivisionRecords.status,
					    ClassDivisionRecords.school_id,
                       Student.id_number,


					   Student.student_id,
					   Student.student_name,   Student.enrollment_number,
					    Student.student_gender,

					   Student.id_type,


                       ).select_from(Student ).join(ClassDivisionRecords,
                                                                ClassDivisionRecords.student_id == Student.student_id)

        ### 此处填写查询条件
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
