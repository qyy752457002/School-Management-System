from datetime import datetime

from sqlalchemy import String, DateTime
from sqlalchemy.orm import mapped_column, Mapped

from mini_framework.databases.entities import BaseDBModel


class CourseSchoolNature(BaseDBModel):
    """
    """
    __tablename__ = 'lfun_course_school_nature'
    __table_args__ = {'comment': '课程和学校关系表模型'}

    id: Mapped[int] = mapped_column(primary_key=True, comment="ID",autoincrement=True)
    course_no: Mapped[str] = mapped_column(String(24), nullable=True,default='', comment="学科编码")
    school_nature: Mapped[str] = mapped_column(String(40), nullable=True,default='', comment="学校性质 2级或者3级")
    created_uid: Mapped[int] = mapped_column(  nullable=True , comment="创建人",default=0)
    updated_uid: Mapped[int] = mapped_column( nullable=True , comment="操作人",default=0)
    created_at = mapped_column(DateTime, default=datetime.now, nullable=False, comment="创建时间")
    updated_at = mapped_column(DateTime, onupdate=datetime.now, default=datetime.now, nullable=False, comment="更新时间")
    is_deleted: Mapped[bool] = mapped_column( nullable=False  , comment="删除态",default=False)

    @staticmethod
    def seed():
        return [
            CourseSchoolNature(
                id=1 ,
                course_no='11',
                school_nature='202',
                created_uid=0,
                updated_uid=0,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                is_deleted=False,
            ),
            CourseSchoolNature( id=2 ,   course_no='13',  school_nature='202',  created_uid=0,  updated_uid=0,   created_at=datetime.now(),    updated_at=datetime.now(),   is_deleted=False,   ),
            CourseSchoolNature( id=3 ,   course_no='14',  school_nature='202',  created_uid=0,  updated_uid=0,   created_at=datetime.now(),    updated_at=datetime.now(),   is_deleted=False,   ),
            CourseSchoolNature( id=4 ,   course_no='15',  school_nature='202',  created_uid=0,  updated_uid=0,   created_at=datetime.now(),    updated_at=datetime.now(),   is_deleted=False,   ),
            CourseSchoolNature( id=5 ,   course_no='22',  school_nature='202',  created_uid=0,  updated_uid=0,   created_at=datetime.now(),    updated_at=datetime.now(),   is_deleted=False,   ),
            CourseSchoolNature( id=6 ,   course_no='23',  school_nature='202',  created_uid=0,  updated_uid=0,   created_at=datetime.now(),    updated_at=datetime.now(),   is_deleted=False,   ),
            CourseSchoolNature( id=7 ,   course_no='24',  school_nature='202',  created_uid=0,  updated_uid=0,   created_at=datetime.now(),    updated_at=datetime.now(),   is_deleted=False,   ),
            CourseSchoolNature( id=8 ,   course_no='25',  school_nature='202',  created_uid=0,  updated_uid=0,   created_at=datetime.now(),    updated_at=datetime.now(),   is_deleted=False,   ),
            CourseSchoolNature( id=9 ,   course_no='40',  school_nature='202',  created_uid=0,  updated_uid=0,   created_at=datetime.now(),    updated_at=datetime.now(),   is_deleted=False,   ),
            CourseSchoolNature( id=10 ,   course_no='60',  school_nature='202',  created_uid=0,  updated_uid=0,   created_at=datetime.now(),    updated_at=datetime.now(),   is_deleted=False,   ),

            CourseSchoolNature( id=11 ,   course_no='12',  school_nature='204',  created_uid=0,  updated_uid=0,   created_at=datetime.now(),    updated_at=datetime.now(),   is_deleted=False,   ),
            CourseSchoolNature( id=12 ,   course_no='13',  school_nature='204',  created_uid=0,  updated_uid=0,   created_at=datetime.now(),    updated_at=datetime.now(),   is_deleted=False,   ),
            CourseSchoolNature( id=13 ,   course_no='14',  school_nature='204',  created_uid=0,  updated_uid=0,   created_at=datetime.now(),    updated_at=datetime.now(),   is_deleted=False,   ),
            CourseSchoolNature( id=14 ,   course_no='15',  school_nature='204',  created_uid=0,  updated_uid=0,   created_at=datetime.now(),    updated_at=datetime.now(),   is_deleted=False,   ),
            CourseSchoolNature( id=15 ,   course_no='16',  school_nature='204',  created_uid=0,  updated_uid=0,   created_at=datetime.now(),    updated_at=datetime.now(),   is_deleted=False,   ),
            CourseSchoolNature( id=16 ,   course_no='17',  school_nature='204',  created_uid=0,  updated_uid=0,   created_at=datetime.now(),    updated_at=datetime.now(),   is_deleted=False,   ),
            CourseSchoolNature( id=17 ,   course_no='18',  school_nature='204',  created_uid=0,  updated_uid=0,   created_at=datetime.now(),    updated_at=datetime.now(),   is_deleted=False,   ),
            CourseSchoolNature( id=18 ,   course_no='19',  school_nature='204',  created_uid=0,  updated_uid=0,   created_at=datetime.now(),    updated_at=datetime.now(),   is_deleted=False,   ),
            CourseSchoolNature( id=19 ,   course_no='20',  school_nature='204',  created_uid=0,  updated_uid=0,   created_at=datetime.now(),    updated_at=datetime.now(),   is_deleted=False,   ),
            CourseSchoolNature( id=20 ,   course_no='22',  school_nature='204',  created_uid=0,  updated_uid=0,   created_at=datetime.now(),    updated_at=datetime.now(),   is_deleted=False,   ),
            CourseSchoolNature( id=21 ,   course_no='23',  school_nature='204',  created_uid=0,  updated_uid=0,   created_at=datetime.now(),    updated_at=datetime.now(),   is_deleted=False,   ),
            CourseSchoolNature( id=22,   course_no='24',  school_nature='204',  created_uid=0,  updated_uid=0,   created_at=datetime.now(),    updated_at=datetime.now(),   is_deleted=False,   ),
            CourseSchoolNature( id=23,   course_no='25',  school_nature='204',  created_uid=0,  updated_uid=0,   created_at=datetime.now(),    updated_at=datetime.now(),   is_deleted=False,   ),
            CourseSchoolNature( id=24,   course_no='40',  school_nature='204',  created_uid=0,  updated_uid=0,   created_at=datetime.now(),    updated_at=datetime.now(),   is_deleted=False,   ),
            CourseSchoolNature( id=25 ,   course_no='60',  school_nature='204',  created_uid=0,  updated_uid=0,   created_at=datetime.now(),    updated_at=datetime.now(),   is_deleted=False,   ),
            CourseSchoolNature( id=44 ,   course_no='21',  school_nature='204',  created_uid=0,  updated_uid=0,   created_at=datetime.now(),    updated_at=datetime.now(),   is_deleted=False,   ),


            CourseSchoolNature( id=26 ,   course_no='12',  school_nature='207',  created_uid=0,  updated_uid=0,   created_at=datetime.now(),    updated_at=datetime.now(),   is_deleted=False,   ),
            CourseSchoolNature( id=27 ,   course_no='13',  school_nature='207',  created_uid=0,  updated_uid=0,   created_at=datetime.now(),    updated_at=datetime.now(),   is_deleted=False,   ),
            CourseSchoolNature( id=28 ,   course_no='14',  school_nature='207',  created_uid=0,  updated_uid=0,   created_at=datetime.now(),    updated_at=datetime.now(),   is_deleted=False,   ),
            CourseSchoolNature( id=30 ,   course_no='16',  school_nature='207',  created_uid=0,  updated_uid=0,   created_at=datetime.now(),    updated_at=datetime.now(),   is_deleted=False,   ),
            CourseSchoolNature( id=31 ,   course_no='17',  school_nature='207',  created_uid=0,  updated_uid=0,   created_at=datetime.now(),    updated_at=datetime.now(),   is_deleted=False,   ),
            CourseSchoolNature( id=32 ,   course_no='18',  school_nature='207',  created_uid=0,  updated_uid=0,   created_at=datetime.now(),    updated_at=datetime.now(),   is_deleted=False,   ),
            CourseSchoolNature( id=33 ,   course_no='21',  school_nature='207',  created_uid=0,  updated_uid=0,   created_at=datetime.now(),    updated_at=datetime.now(),   is_deleted=False,   ),
            CourseSchoolNature( id=34 ,   course_no='20',  school_nature='207',  created_uid=0,  updated_uid=0,   created_at=datetime.now(),    updated_at=datetime.now(),   is_deleted=False,   ),
            CourseSchoolNature( id=35 ,   course_no='22',  school_nature='207',  created_uid=0,  updated_uid=0,   created_at=datetime.now(),    updated_at=datetime.now(),   is_deleted=False,   ),
            CourseSchoolNature( id=36 ,   course_no='23',  school_nature='207',  created_uid=0,  updated_uid=0,   created_at=datetime.now(),    updated_at=datetime.now(),   is_deleted=False,   ),
            CourseSchoolNature( id=37,   course_no='24',  school_nature='207',  created_uid=0,  updated_uid=0,   created_at=datetime.now(),    updated_at=datetime.now(),   is_deleted=False,   ),
            CourseSchoolNature( id=38,   course_no='25',  school_nature='207',  created_uid=0,  updated_uid=0,   created_at=datetime.now(),    updated_at=datetime.now(),   is_deleted=False,   ),
            CourseSchoolNature( id=39,   course_no='40',  school_nature='207',  created_uid=0,  updated_uid=0,   created_at=datetime.now(),    updated_at=datetime.now(),   is_deleted=False,   ),
            CourseSchoolNature( id=40 ,   course_no='60',  school_nature='207',  created_uid=0,  updated_uid=0,   created_at=datetime.now(),    updated_at=datetime.now(),   is_deleted=False,   ),
            CourseSchoolNature( id=41 ,   course_no='19',  school_nature='207',  created_uid=0,  updated_uid=0,   created_at=datetime.now(),    updated_at=datetime.now(),   is_deleted=False,   ),
            CourseSchoolNature( id=42 ,   course_no='26',  school_nature='207',  created_uid=0,  updated_uid=0,   created_at=datetime.now(),    updated_at=datetime.now(),   is_deleted=False,   ),
            CourseSchoolNature( id=43 ,   course_no='27',  school_nature='207',  created_uid=0,  updated_uid=0,   created_at=datetime.now(),    updated_at=datetime.now(),   is_deleted=False,   ),


            CourseSchoolNature( id=45 ,   course_no='12',  school_nature='209',  created_uid=0,  updated_uid=0,   created_at=datetime.now(),    updated_at=datetime.now(),   is_deleted=False,   ),
            CourseSchoolNature( id=46 ,   course_no='13',  school_nature='209',  created_uid=0,  updated_uid=0,   created_at=datetime.now(),    updated_at=datetime.now(),   is_deleted=False,   ),
            CourseSchoolNature( id=47 ,   course_no='14',  school_nature='209',  created_uid=0,  updated_uid=0,   created_at=datetime.now(),    updated_at=datetime.now(),   is_deleted=False,   ),
            CourseSchoolNature( id=48 ,   course_no='16',  school_nature='209',  created_uid=0,  updated_uid=0,   created_at=datetime.now(),    updated_at=datetime.now(),   is_deleted=False,   ),
            CourseSchoolNature( id=49 ,   course_no='17',  school_nature='209',  created_uid=0,  updated_uid=0,   created_at=datetime.now(),    updated_at=datetime.now(),   is_deleted=False,   ),
            CourseSchoolNature( id=50 ,   course_no='18',  school_nature='209',  created_uid=0,  updated_uid=0,   created_at=datetime.now(),    updated_at=datetime.now(),   is_deleted=False,   ),
            CourseSchoolNature( id=51 ,   course_no='21',  school_nature='209',  created_uid=0,  updated_uid=0,   created_at=datetime.now(),    updated_at=datetime.now(),   is_deleted=False,   ),
            CourseSchoolNature( id=52 ,   course_no='20',  school_nature='209',  created_uid=0,  updated_uid=0,   created_at=datetime.now(),    updated_at=datetime.now(),   is_deleted=False,   ),
            CourseSchoolNature( id=53 ,   course_no='22',  school_nature='209',  created_uid=0,  updated_uid=0,   created_at=datetime.now(),    updated_at=datetime.now(),   is_deleted=False,   ),
            CourseSchoolNature( id=54 ,   course_no='23',  school_nature='209',  created_uid=0,  updated_uid=0,   created_at=datetime.now(),    updated_at=datetime.now(),   is_deleted=False,   ),
            CourseSchoolNature( id=55,   course_no='24',  school_nature='209',  created_uid=0,  updated_uid=0,   created_at=datetime.now(),    updated_at=datetime.now(),   is_deleted=False,   ),
            CourseSchoolNature( id=56,   course_no='25',  school_nature='209',  created_uid=0,  updated_uid=0,   created_at=datetime.now(),    updated_at=datetime.now(),   is_deleted=False,   ),
            CourseSchoolNature( id=57,   course_no='40',  school_nature='209',  created_uid=0,  updated_uid=0,   created_at=datetime.now(),    updated_at=datetime.now(),   is_deleted=False,   ),
            CourseSchoolNature( id=58 ,   course_no='60',  school_nature='209',  created_uid=0,  updated_uid=0,   created_at=datetime.now(),    updated_at=datetime.now(),   is_deleted=False,   ),
            CourseSchoolNature( id=59 ,   course_no='19',  school_nature='209',  created_uid=0,  updated_uid=0,   created_at=datetime.now(),    updated_at=datetime.now(),   is_deleted=False,   ),
            CourseSchoolNature( id=60 ,   course_no='26',  school_nature='209',  created_uid=0,  updated_uid=0,   created_at=datetime.now(),    updated_at=datetime.now(),   is_deleted=False,   ),
            CourseSchoolNature( id=61 ,   course_no='27',  school_nature='209',  created_uid=0,  updated_uid=0,   created_at=datetime.now(),    updated_at=datetime.now(),   is_deleted=False,   ),

        ]



