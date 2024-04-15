from mini_framework.web.views import BaseView

from views.models.grades import Grades

from fastapi import Query


class GradesView(BaseView):
    async def get(self,
                  school_id: str = Query(None, title="学校编号", description="学校编号", min_length=1, max_length=20,
                                         example='SC2032633'),
                  grade_no: str = Query(None, description="年级编号", min_length=1, max_length=20, example='XX小学'),
                  ):
        res = Grades(
            school_id=school_id,
            grade_no=grade_no,
            grade_name="A school management system",
            grade_alias="Lfun technical",
        )
        return res

    async def post(self, grades: Grades):
        print(grades)
        return grades
