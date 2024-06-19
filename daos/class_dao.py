from sqlalchemy import select, func, update, and_, or_, alias

from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest
from sqlalchemy.orm import aliased

from models.classes import Classes
from models.grade import Grade
from models.school import School
from models.teachers import Teacher
from models.teachers_info import TeacherInfo


class ClassesDAO(DAOBase):

    async def get_classes_by_id(self, classes_id):
        session = await self.slave_db()
        result = await session.execute(select(Classes).where(Classes.id == classes_id))
        return result.scalar_one_or_none()

    async def get_classes_by_classes_name(self, classes_name,school_id=None,classes=None):
        session = await self.slave_db()
        query =  select(Classes).where(Classes.class_name == classes_name)
        if school_id:
            query = query.where(Classes.school_id == school_id)
            # result = await session.execute(select(Classes).where(and_(Classes.class_name == classes_name,Classes.school_id==school_id)))
        else:
            pass
        if classes.session_id:
            query = query.where(Classes.session_id == classes.session_id)
        if classes.grade_id:
            query = query.where(Classes.grade_id == classes.grade_id)

        result = await session.execute(query )
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
                                      page_request: PageRequest) -> Paging:
        teacher_alias = aliased(Teacher, name='teacher_alias')
        query = (select( School.block, School.borough,School.school_name,Classes.id, Classes.class_name,
                        Classes.class_number, Classes.year_established,
                         # Classes.teacher_id_card,
                        # Classes.teacher_name,
                         Classes.education_stage, Classes.school_system,
                         # Classes.monitor,
                        Classes.class_type, Classes.is_bilingual_class, Classes.major_for_vocational,
                        Classes.bilingual_teaching_mode, Classes.ethnic_language, Classes.is_att_class,
                        Classes.att_class_type, Classes.grade_no, Classes.grade_id, Classes.is_deleted,
                        Classes.school_id,
                        Classes.teacher_id,
                        Classes.care_teacher_id,
                         Grade.grade_type,
                         Classes.created_at, Classes.updated_at,
                         Classes.created_uid, Classes.updated_uid,
                         func.coalesce(Teacher.teacher_id_number, '').label('teacher_id_card'),
                         func.coalesce(Teacher.teacher_name, '').label('teacher_name'),
                         func.coalesce(Teacher.teacher_id_type, '').label('teacher_card_type'),
                         func.coalesce(Teacher.mobile, '').label('teacher_phone'),
                         func.coalesce(TeacherInfo.teacher_number, '').label('teacher_number'),



                         func.coalesce(teacher_alias.teacher_id_number, '').label('care_teacher_id_card'),
                         func.coalesce(teacher_alias.teacher_name, '').label('care_teacher_name'),

                         # teacher_alias.teacher_id_number.label('teacher_id_card'),
                        ).select_from(Classes).join(School, School.id == Classes.school_id)
                 .join(Grade, Grade.id == Classes.grade_id)
                 .join(Teacher, Teacher.teacher_id == Classes.teacher_id)
                 .join(TeacherInfo, Teacher.teacher_id == TeacherInfo.teacher_id)
                 .join(teacher_alias, teacher_alias.teacher_id == Classes.care_teacher_id)
                                    .where(Classes.is_deleted == False)
                 .order_by(Classes.id.desc()))


        if school_id:
            query = query.where(Classes.school_id == school_id)
            pass
        if grade_id:
            query = query.where(Classes.grade_id == grade_id)
        if class_name:
            # query = query.where(Classes.classes_no == class_name)
            query = query.where(Classes.class_name.like(f'%{class_name}%'))

            # pass
        if borough and block:
            cond1 = School.borough == borough
            cond2 = School.block == block
            mcond = or_(cond1, cond2)

            query = query.filter( and_(
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
        update_contents = get_update_contents(classes, *args)
        query = update(Classes).where(Classes.id == classes.id).values(**update_contents)
        return await self.update(session, query, classes, update_contents, is_commit=is_commit)
