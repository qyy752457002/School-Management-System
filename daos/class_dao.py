from sqlalchemy import select, func, update, and_, or_, alias

from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest
from sqlalchemy.orm import aliased

from models.classes import Classes
from models.grade import Grade
from models.school import School
from models.students import Student
from models.students_base_info import StudentBaseInfo
from models.teachers import Teacher
from models.teachers_info import TeacherInfo


class ClassesDAO(DAOBase):

    async def get_classes_by_id(self, classes_id):
        classes_id = int(classes_id)
        session = await self.slave_db()
        result = await session.execute(select(Classes).where(Classes.id == classes_id))
        return result.scalar_one_or_none()

    async def get_classes_by_classes_name(self, classes_name, school_id=None, classes=None):
        session = await self.slave_db()
        query = select(Classes).where(Classes.class_name == classes_name).where(Classes.is_deleted == False)
        if school_id:
            school_id = int(school_id)

            query = query.where(Classes.school_id == school_id)
            # result = await session.execute(select(Classes).where(and_(Classes.class_name == classes_name,Classes.school_id==school_id)))
        else:
            pass
        if classes.session_id:
            classes.session_id = int(classes.session_id)

            query = query.where(Classes.session_id == classes.session_id)
        if classes.grade_id:
            classes.grade_id = int(classes.grade_id)

            query = query.where(Classes.grade_id == classes.grade_id)

        result = await session.execute(query)
        return result.first()

    async def add_classes(self, classes):
        session = await self.master_db()
        session.add(classes)
        await session.commit()
        await session.refresh(classes)
        return classes

    async def update_classes(self, classes, ctype=1):
        session = await self.master_db()
        # session.add(classes)
        if ctype == 1:
            classes.id = int(classes.id)

            update_stmt = update(Classes).where(Classes.id == classes.id).values(
                classes_id=classes.classes_id,
                grade_id=classes.grade_id,
                grade_no=classes.grade_no,
                is_att_class=classes.is_att_class,
                att_class_type=classes.att_class_type,
                class_name=classes.class_name,
                class_number=classes.class_number,
                year_established=classes.year_established,
                teacher_id_card=classes.teacher_id_card,
                teacher_name=classes.teacher_name,
                education_stage=classes.education_stage,
                classes_system=classes.classes_system,
                monitor=classes.monitor,
                class_type=classes.class_type,
                is_bilingual_class=classes.is_bilingual_class,
                major_for_vocational=classes.major_for_vocational,
                bilingual_teaching_mode=classes.bilingual_teaching_mode,
                ethnic_language=classes.ethnic_language,

            )
        else:
            pass

        await session.execute(update_stmt)
        await session.commit()
        return classes

    async def softdelete_classes(self, classes):
        session = await self.master_db()
        deleted_status = True
        classes.id = int(classes.id)

        update_stmt = update(Classes).where(Classes.id == classes.id).values(
            is_deleted=deleted_status,
        )
        await session.execute(update_stmt)
        # await session.delete(classes)
        await session.commit()
        return classes

    async def get_classes_count(self):
        session = await self.slave_db()
        result = await session.execute(select(func.count()).select_from(Classes))
        return result.scalar()

    async def query_classes_with_page(self, borough, block, school_id, grade_id, class_name,
                                      page_request: PageRequest,school_no=None) -> Paging:
        teacher_alias = aliased(Teacher, name='teacher_alias')
        teacherinfo_alias = aliased(TeacherInfo, name='teacherinfo_alias')
        query = (select(School.block, School.borough, School.school_name, Classes.id, Classes.class_name,
                        Classes.class_number, Classes.year_established,
                        Classes.session_id,
                        Classes.created_at,
                        Classes.class_index,
                        Classes.education_stage, Classes.school_system,
                        Classes.class_type, Classes.is_bilingual_class, Classes.major_for_vocational,
                        Classes.bilingual_teaching_mode, Classes.ethnic_language, Classes.is_att_class,
                        Classes.att_class_type, Classes.grade_no, Classes.grade_id, Classes.is_deleted,
                        Classes.school_id,
                        Classes.teacher_id,
                        Classes.monitor_id,
                        Classes.care_teacher_id,
                        Grade.grade_type,
                        Classes.created_at, Classes.updated_at,
                        Classes.created_uid, Classes.updated_uid,
                        Teacher.teacher_id_number,
                        Teacher.teacher_name,
                        Teacher.teacher_id_type,
                        Teacher.mobile,

                        func.coalesce(Teacher.teacher_id_number, '').label('teacher_id_card'),
                        func.coalesce(Teacher.teacher_id_type, '').label('teacher_card_type'),
                        func.coalesce(Teacher.mobile, '').label('teacher_phone'),
                        func.coalesce(TeacherInfo.teacher_number, '').label('teacher_job_number'),
                        func.coalesce(Student.student_name, '').label('monitor'),
                        func.coalesce(StudentBaseInfo.student_number, '').label('monitor_student_number'),

                        func.coalesce(teacher_alias.teacher_id_number, '').label('care_teacher_id_card'),
                        func.coalesce(teacher_alias.teacher_id_type, '').label('care_teacher_card_type'),
                        func.coalesce(teacher_alias.mobile, '').label('care_teacher_phone'),
                        func.coalesce(teacherinfo_alias.teacher_number, '').label('care_teacher_job_number'),
                        func.coalesce(teacher_alias.teacher_name, '').label('care_teacher_name'),
                        # func.coalesce(teacher_alias.teacher_name, '').label('care_teacher_name'),

                        ).select_from(Classes).join(School, School.id == Classes.school_id, isouter=True)
                 .join(Grade, Grade.id == Classes.grade_id, isouter=True)
                 .join(Teacher, Teacher.teacher_id == Classes.teacher_id, isouter=True)
                 .join(TeacherInfo, Teacher.teacher_id == TeacherInfo.teacher_id, isouter=True)
                 .join(teacher_alias, teacher_alias.teacher_id == Classes.care_teacher_id, isouter=True)
                 .join(teacherinfo_alias, teacher_alias.teacher_id == teacherinfo_alias.teacher_id, isouter=True)

                 .join(Student, Student.student_id == Classes.monitor_id, isouter=True)
                 .join(StudentBaseInfo, Student.student_id == StudentBaseInfo.student_id, isouter=True)

                 .where(Classes.is_deleted == False)
                 .order_by(Classes.id.desc()))

        if school_id:
            query = query.where(Classes.school_id == int(school_id))
            pass
        if school_no is not None:
            query = query.where(School.school_no == school_no )
            pass
        if grade_id and int(grade_id) > 0:
            print(grade_id)
            query = query.where(Classes.grade_id == int(grade_id))
        if class_name:
            # query = query.where(Classes.classes_no == class_name)
            query = query.where(Classes.class_name.like(f'%{class_name}%'))

            # pass
        if borough and block:
            cond1 = School.borough == borough
            cond2 = School.block == block
            mcond = or_(cond1, cond2)

            query = query.filter(and_(
                Classes.is_deleted == False,  # a=1
                or_(
                    mcond
                )
            ))
        elif borough or block:
            if block:
                query = query.where(School.block == block)
            if borough:
                query = query.where(School.borough == borough)

        paging = await self.query_page(query, page_request)

        return paging

    async def update_classes_byargs(self, classes: Classes, *args, is_commit: bool = True):
        session = await self.master_db()
        if classes.id:
            classes.id = int(classes.id)
        if classes.school_id:
            classes.school_id = int(classes.school_id)
        if classes.grade_id:
            classes.grade_id = int(classes.grade_id)
        if classes.session_id:
            classes.session_id = int(classes.session_id)
        update_contents = get_update_contents(classes, *args)
        query = update(Classes).where(Classes.id == classes.id).values(**update_contents)
        return await self.update(session, query, classes, update_contents, is_commit=is_commit)

    async def get_all_class(self):
        session = await self.slave_db()
        result = await session.execute(select(Classes))
        return result.scalars().all()
