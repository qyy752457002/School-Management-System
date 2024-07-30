from mini_framework.databases.entities import BaseDBModel
from sqlalchemy import select, func, update, desc

from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.classes import Classes
from models.grade import Grade
from models.major import Major
from models.planning_school import PlanningSchool
from models.school import School
from models.school_communication import SchoolCommunication
from models.students import Student, StudentApprovalAtatus
from models.students_base_info import StudentBaseInfo
from views.models.extend_params import ExtendParams
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

    async def update_students_base_info(self, students_base_info, *args, is_commit: bool = True):
        """
        编辑学生基本信息
        """
        session = await self.master_db()
        update_contents = get_update_contents(students_base_info, *args)
        query = update(StudentBaseInfo).where(StudentBaseInfo.student_id == int(students_base_info.student_id)).values(
            **update_contents)
        return await self.update(session, query, students_base_info, update_contents, is_commit=is_commit)

    async def update_students_class_division(self, class_id, student_ids):
        """
        编辑学生基本信息
        """
        session = await self.master_db()
        # update_contents = get_update_contents(students_base_info, *args)
        if isinstance(student_ids, str) and  ',' in student_ids:
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
        result = await session.execute(select(StudentBaseInfo).where(StudentBaseInfo.student_id == int(students_id)))
        return result.scalar_one_or_none()

    async def get_students_base_info_ext_by_student_id(self, students_id):
        """
        通过学生id获取单个学生基本信息   专业
        """
        session = await self.slave_db()
        query = select(Classes.class_name, Major.major_name, School.school_name, StudentBaseInfo.student_id,
                       func.coalesce(Classes.id, 0).label('class_id'),
                       func.coalesce(School.id, 0).label('school_id'),
                       func.coalesce(Grade.id, 0).label('grade_id'),
                       func.coalesce(Major.id, 0).label('major_id'),
                       func.coalesce(PlanningSchool.province, '').label('province'),
                       func.coalesce(PlanningSchool.city, '').label('city'),
                       func.coalesce(Grade.grade_name, '').label('grade_name'),
                       func.coalesce(PlanningSchool.block, '').label('block'),
                       func.coalesce(PlanningSchool.borough, '').label('borough'),
                       func.coalesce(SchoolCommunication.loc_area, '').label('loc_area'),
                       func.coalesce(SchoolCommunication.loc_area_pro, '').label('loc_area_pro'),
                       StudentBaseInfo.session, ).join(Classes, Classes.id == StudentBaseInfo.class_id,
                                                       isouter=True).join(Grade, Grade.id == StudentBaseInfo.grade_id,
                                                                          isouter=True).join(School,
                                                                                             School.id == StudentBaseInfo.school_id,
                                                                                             isouter=True).join(
            SchoolCommunication, SchoolCommunication.school_id == School.id, isouter=True).join(PlanningSchool,
                                                                                                PlanningSchool.id == School.planning_school_id,
                                                                                                isouter=True).join(
            Major, Major.id == Classes.major_for_vocational, isouter=True).where(
            StudentBaseInfo.student_id == int(students_id))
        result_list = await session.execute(query)
        column_names = query.columns.keys()
        # ret = result.scalar_one_or_none()

        result_items = list(result_list.fetchall())
        items = []
        for item in result_items:
            if issubclass(item[0].__class__, BaseDBModel):
                items.append(item[0])
            else:
                item_dict = dict(zip(column_names, item))
                items.append(item_dict)
        return items

    async def get_students_base_info_by_id(self, student_base_id):
        """
        通过主键获取单个学生基本信息
        """
        session = await self.slave_db()
        result = await session.execute(
            select(StudentBaseInfo).where(StudentBaseInfo.student_base_id == int(student_base_id)))
        return result.scalar_one_or_none()

    async def delete_students_base_info(self, students: Student):
        """
        删除单个学生基本信息
        """
        session = await self.master_db()
        return await self.delete(session, students)

    async def query_students_with_page(self, query_model: NewStudentsQuery, page_request: PageRequest,extend_params:ExtendParams=None) -> Paging:
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
                       Student.enrollment_number, Student.photo, Student.birthday,
                       StudentBaseInfo.session,
                       StudentBaseInfo.edu_number,
                       StudentBaseInfo.enrollment_date,
                       Classes.class_name,
                       Grade.grade_name,
                       PlanningSchool.block,
                       PlanningSchool.borough,
                       Student.student_gender, Student.approval_status, StudentBaseInfo.residence_district,
                       StudentBaseInfo.school, School.block, School.school_name, School.borough,
                       SchoolCommunication.loc_area, SchoolCommunication.loc_area_pro).select_from(Student).join(
            StudentBaseInfo,
            Student.student_id == StudentBaseInfo.student_id, isouter=True).join(School,
                                                                                 School.id == StudentBaseInfo.school_id,
                                                                                 isouter=True).join(SchoolCommunication,
                                                                                                    School.id == SchoolCommunication.school_id,
                                                                                                    isouter=True).join(
            PlanningSchool,
            School.planning_school_id == PlanningSchool.id,
            isouter=True).join(Classes,
                               Classes.id == StudentBaseInfo.class_id,
                               isouter=True).join(Grade,
                                                  Grade.id == StudentBaseInfo.grade_id,
                                                  isouter=True).order_by(desc(Student.student_id))
        query = query.where(Student.is_deleted == False)

        if extend_params is not None and len(query_model.county)==0  :
            if extend_params.county_id:
                query_model.county= extend_params.county_id
            pass
        if extend_params is not None and query_model.school_id==0  :
            if extend_params.school_id:
                query_model.school_id= extend_params.school_id
            pass

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
            query = query.where(StudentBaseInfo.school_id == int(query_model.school_id))
        if query_model.class_id:
            query = query.where(StudentBaseInfo.class_id == int(query_model.class_id))
        if query_model.enrollment_date:
            query = query.where(StudentBaseInfo.enrollment_date == query_model.enrollment_date)
        if query_model.county:
            query = query.where(PlanningSchool.block  == query_model.county)
        if query_model.emporary_borrowing_status:
            query = query.where(StudentBaseInfo.emporary_borrowing_status == query_model.emporary_borrowing_status)
        if query_model.edu_number:
            query = query.where(StudentBaseInfo.edu_number == query_model.edu_number)
        if query_model.approval_status:
            # 多选的处理
            if ',' in query_model.approval_status:
                approval_status = query_model.approval_status.split(',')
                query = query.where(Student.approval_status.in_(approval_status))
            else:
                query = query.where(Student.approval_status == query_model.approval_status)
        if query_model.enrollment_date_range:
            # 多选的处理
            if ',' in query_model.enrollment_date_range:
                enrollment_date_range = query_model.enrollment_date_range.split(',')
                if len(enrollment_date_range) == 2:
                    if enrollment_date_range[0] != '':
                        query = query.where(StudentBaseInfo.enrollment_date >= enrollment_date_range[0])
                    if enrollment_date_range[1] != '':
                        query = query.where(StudentBaseInfo.enrollment_date <= enrollment_date_range[1])
                    # query = query.where(StudentBaseInfo.enrollment_date.between(enrollment_date_range[0],
                    #                                                          enrollment_date_range[1]))
                elif len(enrollment_date_range) == 1:
                    if enrollment_date_range[0] != '':
                        query = query.where(StudentBaseInfo.enrollment_date >= enrollment_date_range[0])
                    else:
                        query = query.where(StudentBaseInfo.enrollment_date <= enrollment_date_range[1])

                    # query = query.where(StudentBaseInfo.enrollment_date == enrollment_date_range[0])
                # query = query.where(Student.enrollment_date_range.in_(approval_status))
            else:
                query = query.where(StudentBaseInfo.enrollment_date >= query_model.enrollment_date_range)

                # query = query.where(Student.approval_status == query_model.approval_status)
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

    async def get_students_base_info_by_param(self, **kwargs):
        """
        获取单个学生信息
        """
        session = await self.slave_db()
        query = select(StudentBaseInfo)
        for key, value in kwargs.items():
            query = query.where(getattr(StudentBaseInfo, key) == value)
        result = await session.execute(query)
        return result.scalar()
