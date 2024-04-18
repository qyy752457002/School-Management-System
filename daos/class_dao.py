from sqlalchemy import select, func, update

from mini_framework.databases.entities.dao_base import DAOBase
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.classes import Classes


class ClassesDAO(DAOBase):

    async def get_classes_by_id(self, classes_id):
        session = await self.slave_db()
        result = await session.execute(select(Classes).where(Classes.id == classes_id))
        return result.scalar_one_or_none()

    async def add_classes(self, classes):
        session = await self.master_db()
        session.add(classes)
        await session.commit()
        await session.refresh(classes)
        return classes

    async def update_classes(self, classes,ctype=1):
        session = await self.master_db()
        # session.add(classes)
        if ctype == 1:
            update_stmt = update(Classes).where(Classes.id == classes.id).values(
                school_id= classes.school_id,
                grade_id= classes.grade_id,
                grade_no= classes.grade_no,
                is_att_class= classes.is_att_class,
                att_class_type= classes.att_class_type,
                class_name= classes.class_name,
                class_number= classes.class_number,
                year_established= classes.year_established,
                teacher_id_card= classes.teacher_id_card,
                teacher_name= classes.teacher_name,
                education_stage= classes.education_stage,
                school_system= classes.school_system,
                monitor= classes.monitor,
                class_type= classes.class_type,
                is_bilingual_class= classes.is_bilingual_class,
                major_for_vocational= classes.major_for_vocational,
                bilingual_teaching_mode= classes.bilingual_teaching_mode,
                ethnic_language= classes.ethnic_language,



            )
        else:
            pass


        await session.execute(update_stmt)
        await session.commit()
        return classes


    async def softdelete_classes(self, classes):
        session = await self.master_db()
        deleted_status= True
        update_stmt = update(Classes).where(Classes.id == classes.id).values(
            is_deleted= deleted_status,
        )
        await session.execute(update_stmt)
        # await session.delete(classes)
        await session.commit()
        return classes


    async def get_classes_count(self):
        session = await self.slave_db()
        result = await session.execute(select(func.count()).select_from(Classes))
        return result.scalar()

    async def query_classes_with_page(self, classes_name, classes_id, classes_no,
                                              page_request: PageRequest) -> Paging:
        query = select(Classes)
        if classes_name:
            # query = query.where(Classes.classes_name == classes_name)
            pass
        if classes_id:
            query = query.where(Classes.id == classes_id)
        if classes_no:
            # query = query.where(Classes.classes_no == classes_no)
            pass
        paging = await self.query_page(query, page_request)
        return paging

