
from models.students import Student, StudentApprovalAtatus
from models.students_base_info import StudentBaseInfo
from views.models.student_graduate import GraduateStudentQueryModel, CountySchoolArchiveQueryModel
from datetime import datetime

from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.web.std_models.page import PageRequest
from sqlalchemy import literal
from sqlalchemy import select, func, update, case, and_

from daos.grade_dao import GradeDAO
from daos.student_session_dao import StudentSessionDao
from models.classes import Classes
from models.graduation_student import GraduationStudent
from models.planning_school import PlanningSchool
from models.public_enum import Section
from models.school import School
from models.student_county_school_archive import CountyGraduationStudent
from models.student_session import StudentSession

class GraduationStudentDAO(DAOBase):

    async def add_graduationstudent(self, graduationstudent: GraduationStudent):
        session = await self.master_db()
        session.add(graduationstudent)
        await session.commit()
        await session.refresh(graduationstudent)
        return graduationstudent

    async def get_graduationstudent_count(self, ):
        session = await self.slave_db()
        result = await session.execute(select(func.count()).select_from(GraduationStudent))
        return result.scalar()

    async def delete_graduationstudent(self, graduationstudent: GraduationStudent):
        session = await self.master_db()
        await session.delete(graduationstudent)
        await session.commit()

    async def get_graduationstudent_by_id(self, id):
        session = await self.slave_db()
        result = await session.execute(
            select(GraduationStudent).where(GraduationStudent.id == id, GraduationStudent.is_deleted == False))
        return result.scalar_one_or_none()

    async def get_graduationstudent_by_student_id(self, student_id):
        session = await self.slave_db()
        result = await session.execute(select(GraduationStudent).where(GraduationStudent.student_id == student_id,
                                                                       GraduationStudent.is_deleted == False))
        return result.scalar_one_or_none()

    async def get_graduationstudent_by_name(self, name):
        session = await self.slave_db()
        result = await session.execute(select(GraduationStudent).where(GraduationStudent.student_name == name))
        return result.scalar_one_or_none()

    async def query_graduationstudent_with_page(self, page_request: PageRequest, **kwargs):
        query = select(Student.student_id, Student.student_name, Student.student_gender, Student.enrollment_number,
                       Student.id_number, Student.approval_status,

                       StudentBaseInfo.edu_number, StudentBaseInfo.class_id,
                       StudentBaseInfo.school_id, StudentBaseInfo.graduation_type,
                       School.school_name, School.block, School.borough, Classes.class_name,

                       ).select_from(Student).join(StudentBaseInfo,
                                                   Student.student_id == StudentBaseInfo.student_id,
                                                   isouter=True).join(School,
                                                                      School.id == StudentBaseInfo.school_id,
                                                                      isouter=True).join(PlanningSchool,
                                                                                         School.planning_school_id == PlanningSchool.id,
                                                                                         isouter=True).join(Classes,
                                                                                                            Classes.id == StudentBaseInfo.class_id,
                                                                                                            isouter=True)

        query = query.where(Student.approval_status == StudentApprovalAtatus.GRADUATED.value)
        for key, value in kwargs.items():
            if key == 'student_name' or key == 'student_gender':
                query = query.where(getattr(Student, key) == value)
            elif key == 'borough':
                query = query.where(getattr(PlanningSchool, key) == value)
            else:
                query = query.where(getattr(StudentBaseInfo, key) == value)

        paging = await self.query_page(query, page_request)
        return paging

    async def update_graduationstudent(self, graduationstudent, *args, is_commit=True):
        session = await self.master_db()
        update_contents = get_update_contents(graduationstudent, *args)
        query = update(StudentBaseInfo).where(StudentBaseInfo.student_id == graduationstudent.student_id).values(
            **update_contents)
        return await self.update(session, query, graduationstudent, update_contents, is_commit=is_commit)

    async def softdelete_graduationstudent(self, graduationstudent):
        session = await self.master_db()
        deleted_status = True
        update_stmt = update(GraduationStudent).where(GraduationStudent.id == graduationstudent.id).values(
            is_deleted=deleted_status,
        )
        await session.execute(update_stmt)
        await session.commit()
        return graduationstudent

    async def update_graduation_student_archive_status_by_school_id(self, school_id: int, is_commit=True):
        session = await self.master_db()
        current_year = datetime.now().year
        try:
            stmt_select = select(GraduationStudent).where(GraduationStudent.school_id == school_id,
                                                          GraduationStudent.archive_status == False)
            result = await session.execute(stmt_select)
            students_to_update = result.scalars().all()
            if not students_to_update:
                return {"message": "没有符合条件的学校"}
            school = students_to_update[0].school
            borough = students_to_update[0].borough
            for student in students_to_update:
                update_contents = {"archive_status": True, "archive_date": str(current_year)}
                query = update(GraduationStudent).where(GraduationStudent.student_id == student.student_id).values(
                    **update_contents)
                await self.update(session, query, student, update_contents, is_commit=False)
            graduate_student_count = len(students_to_update)
            county_school = CountyGraduationStudent(school_id=school_id, graduate_count=graduate_student_count,
                                                    school=school, borough=borough, year=str(current_year))
            session.add(county_school)
            if is_commit:
                await session.commit()
                return True
        except Exception as e:
            await session.rollback()
            return {"error": f"更新失败，已回滚，错误: {str(e)}"}
        finally:
            await session.close()

    async def update_graduation_student_archive_status_by_school_id(self, school_id: int, is_commit=True):
        session = await self.master_db()
        current_year = datetime.now().year
        try:
            stmt_select = select(GraduationStudent).where(GraduationStudent.school_id == school_id,
                                                          GraduationStudent.archive_status == False)
            result = await session.execute(stmt_select)
            students_to_update = result.scalars().all()
            if not students_to_update:
                return {"message": "没有符合条件的学校"}
            school = students_to_update[0].school
            borough = students_to_update[0].borough
            for student in students_to_update:
                update_contents = {"archive_status": True, "archive_date": str(current_year)}
                query = update(GraduationStudent).where(GraduationStudent.student_id == student.student_id).values(
                    **update_contents)
                await self.update(session, query, student, update_contents, is_commit=False)
            graduate_student_count = len(students_to_update)
            county_school = CountyGraduationStudent(school_id=school_id, graduate_count=graduate_student_count,
                                                    school=school, borough=borough, year=str(current_year))
            session.add(county_school)
            if is_commit:
                await session.commit()
                return True
        except Exception as e:
            await session.rollback()
            return {"error": f"更新失败，已回滚，错误: {str(e)}"}
        finally:
            await session.close()

    async def update_graduation_student_archive_status(self, borough, is_commit=True):
        session = await self.master_db()
        current_year = datetime.now().year
        try:
            stmt_select = select(GraduationStudent).where(GraduationStudent.borough == borough,
                                                          GraduationStudent.archive_status == False)
            result = await session.execute(stmt_select)
            students_to_update = result.scalars().all()
            if not students_to_update:
                return {"message": "没有符合条件的学生"}
            for student in students_to_update:
                update_contents = {"archive_status": True, "archive_date": str(current_year)}
                query = update(GraduationStudent).where(GraduationStudent.student_id == student.student_id).values(
                    **update_contents)
                await self.update(session, query, student, update_contents, is_commit=False)
            if is_commit:
                await session.commit()
                return True
        except Exception as e:
            await session.rollback()
            return {"error": f"更新失败，已回滚，错误: {str(e)}"}
        finally:
            await session.close()

    async def update_graduation_student_by_school_id(self, school_id: int, grade_level: int, is_commit=True):
        session = await self.master_db()
        current_year = datetime.now().year
        school_duration = grade_level  # 根据学校不同的学制，比如小学是6年，初中是3年
        session_year = current_year - school_duration
        try:
            # 1 筛选符合要求的学生
            stmt_select = select(StudentBaseInfo, School, Student).join(StudentSession,
                                                                        StudentSession.session_id == StudentBaseInfo.session_id).join(
                School, School.id == StudentBaseInfo.school_id).join(Student,
                                                                     Student.student_id == StudentBaseInfo.student_id).where(
                StudentBaseInfo.school_id == school_id,
                StudentSession.year == str(session_year),  # 届别为需要毕业的年
                StudentBaseInfo.graduation_type == None,  # 状态为未毕业
                Student.is_deleted == False,
            )
            result = await session.execute(stmt_select)
            students_to_graduate = result.all()
            if not students_to_graduate:
                return {"message": "没有符合条件的学生"}
            # 2 更新学生状态
            for student_base, school, student in students_to_graduate:
                update_contents = {"graduation_type": "graduation"}
                query = await session.update(StudentBaseInfo).where(StudentBaseInfo.student_id == student_base.student_id).values(
                    **update_contents)
                await self.update(session, query, student_base, update_contents, is_commit=False)
                # 3 将学生放入毕业表中
                graduation_student = GraduationStudent(student_id=student_base.student_id,
                                                       student_name=student.student_name, school=school.school_name,
                                                       school_id=student_base.school_id, borough=school.borough,
                                                       edu_number=student_base.edu_number,
                                                       class_id=student_base.class_id, session=student_base.session,
                                                       session_id=student_base.session_id,
                                                       status=student_base.graduation_type,
                                                       graduation_date=datetime.now().date(),
                                                       graduation_year=str(current_year),
                                                       graduation_remark="",
                                                       archive_status=False)
                session.add(graduation_student)
            # 4. 提交所有事务
            if is_commit:
                await session.commit()
                return True
                # return {"message": f"{len(students_to_graduate)} 位学生毕业状态更新成功"}
        except Exception as e:
            # 5. 回滚操作，如果有任何失败
            await session.rollback()
            return {"error": f"更新失败，已回滚，错误: {str(e)}"}
        finally:
            # 6. 关闭会话
            await session.close()

        # todo 中职和特殊教育的学制不一样，这里需要特别说明

        # try:
        #     # 1. 查询需要毕业的学生，根据学校ID、学制和届别
        #     # 假设 StudentBaseInfo 包含 school_id, program_id (专业ID), grade (届别), is_graduated
        #     stmt_select = select(StudentBaseInfo).where(
        #         StudentBaseInfo.school_id == school_id,
        #         StudentBaseInfo.is_graduated == False  # 只选择未毕业的学生
        #     )
        #     result = await session.execute(stmt_select)
        #     students_to_check = result.scalars().all()
        #
        #     if not students_to_check:
        #         return {"message": "没有符合条件的学生"}
        #
        #     # 2. 遍历所有学生，计算他们的学制和届别是否达到毕业条件
        #     graduated_students = []
        #     for student in students_to_check:
        #         # 假设每个学生有 program_id 和 program_duration 表示专业学制
        #         # 查询专业对应的学制
        #         stmt_program = select(ProgramInfo).where(ProgramInfo.program_id == student.program_id)
        #         program_result = await session.execute(stmt_program)
        #         program_info = program_result.scalar_one_or_none()
        #
        #         if not program_info:
        #             continue  # 如果没有查询到对应的专业信息，跳过这个学生
        #
        #         program_duration = program_info.program_duration  # 专业的学制（年数）
        #         graduation_year = student.grade + program_duration  # 计算毕业年份
        #
        #         # 判断该学生是否应当毕业
        #         if current_year >= graduation_year:
        #             # 3. 更新学生的毕业状态
        #             update_contents = {"is_graduated": True, "graduation_year": current_year}
        #             query = update(StudentBaseInfo).where(StudentBaseInfo.student_id == student.student_id).values(
        #                 **update_contents)
        #             await self.update(session, query, student, update_contents, is_commit=False)  # 延迟提交
        #
        #             # 4. 将毕业学生记录添加到毕业表
        #             graduation_record = GraduationRecord(
        #                 student_id=student.student_id,
        #                 school_id=school_id,
        #                 graduation_year=current_year
        #             )
        #             session.add(graduation_record)
        #
        #             graduated_students.append(student)
        #
        #     # 5. 提交所有事务
        #     if is_commit and graduated_students:
        #         await session.commit()
        #         return {"message": f"{len(graduated_students)} 位学生毕业状态更新成功"}
        #
        # except Exception as e:
        #     # 6. 回滚操作，如果有任何失败
        #     await session.rollback()
        #     return {"error": f"更新失败，已回滚，错误: {str(e)}"}
        #
        # finally:
        #     # 7. 关闭会话
        #     await session.close()

    async def query_graduation_student_by_model_with_page(self, page_request: PageRequest,
                                                          query_model: GraduateStudentQueryModel):
        """
        根据条件查询毕业生
        """
        query = select(GraduationStudent.student_id, GraduationStudent.school_id, GraduationStudent.school,
                       GraduationStudent.student_name, GraduationStudent.status, GraduationStudent.archive_status,
                       GraduationStudent.graduation_date, Classes.class_name).join(Classes,
                                                                                   Classes.id == GraduationStudent.class_id).where(
            GraduationStudent.is_deleted == False)
        query = query.order_by(GraduationStudent.created_at.desc())
        if query_model.school_id:
            query = query.where(GraduationStudent.school_id == query_model.school_id)
        if query_model.student_name:
            query = query.where(GraduationStudent.student_name == query_model.student_name)
        if query_model.graduation_date_s and query_model.graduation_date_e:
            query = query.where(GraduationStudent.graduation_date.between(query_model.graduation_date_s,
                                                                          query_model.graduation_date_e))
        if query_model.status:
            query = query.where(GraduationStudent.status == query_model.status)
        if query_model.archive_status is not None:
            query = query.where(GraduationStudent.archive_status == query_model.archive_status)
        if query_model.borough:
            query = query.where(GraduationStudent.borough == query_model.borough)
        paging = await self.query_page(query, page_request)
        return paging

    async def query_school_archive_status_with_page(self, page_request: PageRequest,
                                                    query_model: CountySchoolArchiveQueryModel):
        relationship_count_subquery = (
            select(CountyGraduationStudent.school_id, CountyGraduationStudent.graduate_count.label('graduate_count'),
                   func.count(CountyGraduationStudent.school_id).label(
                       'relation_count')).where(
                CountyGraduationStudent.year == str(datetime.now().year)).group_by(
                CountyGraduationStudent.school_id).subquery())
        archive_status = case((relationship_count_subquery.c.relation_count > 0, True), else_=False).label(
            'archive_status')
        query = select(School.school_name, School.borough, School.id, archive_status,
                       func.coalesce(relationship_count_subquery.c.graduate_count, 0).label("graduate_count")).join(
            relationship_count_subquery,
            School.id == relationship_count_subquery.c.school_id,
            isouter=True).where(
            School.is_deleted == False, School.institution_category == None, School.status == "normal")
        if query_model.borough:
            query = query.where(School.borough == query_model.borough)
        if query_model.school_id:
            query = query.where(School.id == query_model.school_id)
        if query_model.archive_status is not None:
            query = query.where(archive_status == literal(query_model.archive_status))
        query = query.order_by(School.id.desc())
        paging = await self.query_page(query, page_request)
        return paging

    async def get_school_is_graduate(self, query_archive_status=False):
        session = await self.slave_db()
        relationship_count_subquery = (
            select(GraduationStudent.school_id, func.count(GraduationStudent.school_id).label(
                'relation_count')).where(GraduationStudent.graduation_year == str(datetime.now().year)).group_by(
                GraduationStudent.school_id).subquery())
        archive_status = case((relationship_count_subquery.c.relation_count > 0, True), else_=False).label(
            'archive_status')
        query = select(School.school_name, School.id, archive_status).join(
            relationship_count_subquery,
            School.id == relationship_count_subquery.c.school_id,
            isouter=True).where(
            School.is_deleted == False, School.institution_category == None, School.status == "normal")
        query = query.where(archive_status == literal(query_archive_status))
        query = query.order_by(School.id.desc())
        result = await session.execute(query)
        return result.scalars().all()

    async def upgrade_all_student(self, school_id: int):
        session = await self.master_db()
        current_year = datetime.now().year
        # try:
        stmt_select = (
            select(Classes, StudentSession)
            .join(StudentSession, StudentSession.session_id == Classes.session_id)
            .where(
                and_(
                    Classes.school_id == school_id,
                    StudentSession.year < current_year  # 比较届别的年份
                )
            )
        )
        result = await session.execute(stmt_select)
        classes_to_upgrade = result.scalars().all()
        grade_dao = get_injector(GradeDAO)
        session_dao = get_injector(StudentSessionDao)
        for class_obj in classes_to_upgrade:
            session_info = await session_dao.get_student_session_by_id(class_obj.session_id)
            section = session_info.section
            grade_level = Section.get_grade_level(section)
            current_grade = await grade_dao.get_grade_by_id_and_school_id(class_obj.grade_id, school_id,
                                                                          session_info.section)
            if current_grade:
                if grade_level != 0:
                    # 如果学制不是0，代表不是中职学校
                    if current_grade.grade_index < grade_level:
                        # 如果当前年级小于学制年级，升级
                        update_grade = await grade_dao.get_grade_by_index_and_school_id(current_grade.id + 1,
                                                                                        school_id, section)
                        if update_grade:
                            # todo 更新班级的年级
                            update_contents = {"grade_id": update_grade.id}
                            await session.update(Classes).where(Classes.id == class_obj.id).values(**update_contents)
                            # todo 更新同一班级学生的年级
                            await session.update(StudentBaseInfo).where(
                                StudentBaseInfo.class_id == class_obj.id).values(**update_contents)
                        else:
                            continue

        #     if is_commit:
        #         await session.commit()
        #         return True
        # except Exception as e:
        #     await session.rollback()
        #     return {"error": f"更新失败，已回滚，错误: {str(e)}"}
        # finally:
        #     await session.close()