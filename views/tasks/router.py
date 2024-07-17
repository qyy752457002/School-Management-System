from mini_framework.storage.view_model import FileStorageModel
from mini_framework.web.router import root_router

from views.models.class_division_records import ClassDivisionRecordsSearchRes
from views.models.institutions import InstitutionTask, InstitutionPageSearch
from views.models.planning_school import PlanningSchoolTask, PlanningSchoolPageSearch, PlanningSchoolFileStorageModel
from views.models.school import SchoolTask, SchoolPageSearch
from views.models.students import NewStudentTask, NewStudentsQuery
from views.models.teachers import TeacherFileStorageModel, CurrentTeacherQuery
from views.tasks.class_task import ClassExecutor
from views.tasks.institution_task import InstitutionExecutor, InstitutionExportExecutor
from views.tasks.new_student_task import NewStudentExecutor, NewStudentFamilyInfoImportExecutor, \
    NewStudentExportExecutor
from views.tasks.new_teacher_task import TeacherImportExecutor, TeacherExportExecutor, TeacherSaveImportExecutor
from views.tasks.newstudent_class_division_task import NewStudentClassDivisionExportExecutor
from views.tasks.planning_school_task import PlanningSchoolExecutor, PlanningSchoolExportExecutor
from views.tasks.school_task import SchoolExecutor, SchoolExportExecutor


def init_task_router():


    from mini_framework.async_task.router import task_router


    task_router.register(
        code="institution_import",
        consumer_group_id="service",
        topic="institution_import",
        name="事业单位导入任务",
        executor_cls=InstitutionExecutor,
        payload_cls=PlanningSchoolFileStorageModel,
        payload_is_list=False,
        description="事业单位导入任务",
    )
    task_router.register(
        code="institution_export",
        consumer_group_id="service",
        topic="institution_export",
        name="事业单位导出",
        executor_cls=InstitutionExportExecutor,
        payload_cls=InstitutionPageSearch,
        payload_is_list=False,
        description="事业单位导出",
    )
    task_router.register(
        code="new_student_import",
        consumer_group_id="service",
        topic="new_student_import",
        name="新生导入",
        executor_cls=NewStudentExecutor,
        payload_cls=NewStudentTask,
        payload_is_list=False,
        description="新生导入",
    )
    task_router.register(
        code="newstudent_familyinfo_import",
        consumer_group_id="service",
        topic="newstudent_familyinfo_import",
        name="新生家庭成员信息导入",
        executor_cls=NewStudentFamilyInfoImportExecutor,
        payload_cls=NewStudentTask,
        payload_is_list=False,
        description="新生家庭成员信息导入",
    )
    task_router.register(
        code="school_import",
        consumer_group_id="service",
        topic="school_import",
        name="学校导入",
        executor_cls=SchoolExecutor,
        payload_cls=SchoolTask,
        payload_is_list=False,
        description="学校导入",
    )
    task_router.register(
        code="school_export",
        consumer_group_id="service",
        topic="school_export",
        name="学校导出",
        executor_cls=SchoolExportExecutor,
        payload_cls=SchoolPageSearch,
        payload_is_list=False,
        description="学校导出",
    )
    task_router.register(
        code="planning_school_import",
        consumer_group_id="service",
        topic="planning_school_import",
        name="规划校上传和导入",
        executor_cls=PlanningSchoolExecutor,
        payload_cls=PlanningSchoolFileStorageModel,
        payload_is_list=False,
        description="规划校上传和导入",
    )
    task_router.register(
        code="planning_school_export",
        consumer_group_id="service",
        topic="planning_school_export",
        name="规划校的导出",
        executor_cls=PlanningSchoolExportExecutor,
        payload_cls=PlanningSchoolPageSearch,
        payload_is_list=False,
        description="规划校的导出",
    )

    task_router.register(
        code="student_export",
        consumer_group_id="service",
        topic="student_export",
        name="学生导出",
        executor_cls=NewStudentExportExecutor,
        payload_cls=NewStudentsQuery,
        payload_is_list=False,
        description="学生导出",
    )
    task_router.register(
        code="newstudent_classdivision_export",
        consumer_group_id="service",
        topic="newstudent_classdivision_export",
        name="学生分班记录导出",
        executor_cls=NewStudentClassDivisionExportExecutor,
        payload_cls=ClassDivisionRecordsSearchRes,
        payload_is_list=False,
        description="学生分班记录导出",
    )
    task_router.register(
        code="class_import",
        consumer_group_id="service",
        topic="class_import",
        name="班级导入",
        executor_cls=ClassExecutor,
        payload_cls=SchoolTask,
        payload_is_list=False,
        description="班级导入",
    )
    task_router.register(
        code="teacher_import",
        consumer_group_id="service",
        topic="teacher_import",
        name="教师导入",
        executor_cls=TeacherImportExecutor,
        payload_cls=TeacherFileStorageModel,
        payload_is_list=False,
        description="教师导入",
    )
    task_router.register(
        code="teacher_export",
        consumer_group_id="service",
        topic="teacher_export",
        name="教师导出",
        executor_cls=TeacherExportExecutor,
        payload_cls=CurrentTeacherQuery,
        payload_is_list=False,
        description="教师导出",
    )
    task_router.register(
        code="teacher_save_import",
        consumer_group_id="service",
        topic="teacher_save_import",
        name="教师保存导入",
        executor_cls=TeacherSaveImportExecutor,
        payload_cls=TeacherFileStorageModel,
        payload_is_list=False,
        description="",
    )
