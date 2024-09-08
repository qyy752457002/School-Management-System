from sqlalchemy import select, func, update
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.classes import Classes
from models.graduation_student import GraduationStudent
from models.student_county_school_archive import CountyGraduationStudent
from models.planning_school import PlanningSchool
from models.school import School
from models.students import Student, StudentApprovalAtatus
from models.students_base_info import StudentBaseInfo


class CountyGraduationStudentDAO(DAOBase):

    async def add_county_school_relation(self, county_school_relation: CountyGraduationStudent):
        session = await self.master_db()
        session.add(county_school_relation)
        await session.commit()
        await session.refresh(county_school_relation)
        return county_school_relation