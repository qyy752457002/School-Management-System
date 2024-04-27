from sqlalchemy import select, func, update

from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.school import School
from models.school_communication import SchoolCommunication
from models.students import Student, StudentApprovalAtatus
from models.students_base_info import StudentBaseInfo
from views.models.students import NewStudentsQuery


class StudentsBaseInfoDao(DAOBase):
    async def add_students_base_info(self, students_base_info):
        """
        新增学生基本信息
        """
        session = await self.master_db()
        session.add(students_base_info)
        await session.commit()
        await session.refresh(students_base_info)
        return students_base_info

    async def update_students_base_info(self, students_base_info: Student, *args, is_commit: bool = True):
        """
        编辑学生基本信息
        """
        session = await self.master_db()
        update_contents = get_update_contents(students_base_info, *args)
        query = update(StudentBaseInfo).where(StudentBaseInfo.student_id == students_base_info.student_id).values(
            **update_contents)
        return await self.update(session, query, students_base_info, update_contents, is_commit=is_commit)

    async def update_students_class_division(self, class_id, student_ids):
        """
        编辑学生基本信息
        """
        session = await self.master_db()
        # update_contents = get_update_contents(students_base_info, *args)
        if ',' in student_ids:
            student_ids = student_ids.split(',')
        else:
            student_ids = [student_ids]

        query = update(StudentBaseInfo).where(StudentBaseInfo.student_id.in_(student_ids)).values(
            class_id=class_id)
        query2 = update(Student).where(Student.student_id.in_(student_ids)).values(
            approval_status=StudentApprovalAtatus.ASSIGNMENT.value)
        res = await session.execute(query)
        res3 = await session.execute(query2)

        res2 = await session.commit()
        return student_ids

    async def get_students_base_info_by_student_id(self, students_id):
        """
        通过学生id获取单个学生基本信息
        """
        session = await self.slave_db()
        result = await session.execute(select(StudentBaseInfo).where(StudentBaseInfo.student_id == students_id))
        return result.scalar_one_or_none()

    async def get_students_base_info_by_id(self, student_base_id):
        """
        通过主键获取单个学生基本信息
        """
        session = await self.slave_db()
        result = await session.execute(
            select(StudentBaseInfo).where(StudentBaseInfo.student_base_id == student_base_id))
        return result.scalar_one_or_none()

    async def delete_students_base_info(self, students: Student):
        """
        删除单个学生基本信息
        """
        session = await self.master_db()
        return await self.delete(session, students)

    async def query_students_with_page(self, query_model: NewStudentsQuery, page_request: PageRequest) -> Paging:
        """
        学生姓名：student_name
        报名号：enrollment_number
        性别：student_gender
        证件类别：id_type
        证件号码：id_number
        学校：school
        登记时间：enrollment_date
        区县：county
        状态：status
        """
        query = select(Student.student_id, Student.student_name, Student.id_type, Student.id_number,
                       Student.enrollment_number,
                       Student.student_gender, Student.approval_status, StudentBaseInfo.residence_district,
                       StudentBaseInfo.school, School.block, School.school_name, School.borough,
                       SchoolCommunication.loc_area, SchoolCommunication.loc_area_pro).select_from(Student).join(
            StudentBaseInfo,
            Student.student_id == StudentBaseInfo.student_id, isouter=True).join(School,
                                                                                 School.id == StudentBaseInfo.school_id,
                                                                                 isouter=True).join(SchoolCommunication,
                                                                                                    School.id == SchoolCommunication.school_id,
                                                                                                    isouter=True)

        if query_model.student_name:
            query = query.where(Student.student_name == query_model.student_name)
        if query_model.enrollment_number:
            query = query.where(Student.enrollment_number == query_model.enrollment_number)
        if query_model.id_number:
            query = query.where(Student.id_number == query_model.id_number)
        if query_model.student_gender:
            query = query.where(Student.student_gender == query_model.student_gender.value)
        if query_model.school:
            query = query.where(StudentBaseInfo.school == query_model.school)
        if query_model.school_id:
            query = query.where(StudentBaseInfo.school_id == query_model.school_id)
        if query_model.enrollment_date:
            query = query.where(StudentBaseInfo.enrollment_date == query_model.enrollment_date)
        if query_model.county:
            query = query.where(StudentBaseInfo.county == query_model.county)
        if query_model.approval_status:
            # 多选的处理
            if ',' in query_model.approval_status:
                approval_status = query_model.approval_status.split(',')
                query = query.where(Student.approval_status.in_(approval_status))
            else:
                query = query.where(Student.approval_status == query_model.approval_status)
        paging = await self.query_page(query, page_request)
        return paging

    async def get_all_students_base_info(self):
        session = await self.slave_db()
        result = await session.execute(select(StudentBaseInfo))
        return result.scalars().all()

    async def get_student_base_info_count(self):
        session = await self.slave_db()
        result = await session.execute(select(func.count()).select_from(StudentBaseInfo))
        return result.scalar()
