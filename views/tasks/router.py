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
from views.tasks.new_teacher_extend_task import TeacherWorkExperienceImportExecutor, \
    TeacherLearnExperienceImportExecutor, TeacherJobAppointmentsImportExecutor, TeacherProfessionalTitlesImportExecutor, \
    TeacherQualificationsImportExecutor, TeacherSkillCertificatesImportExecutor, \
    TeacherEthicRecordsRewardsImportExecutor, TeacherEthicRecordsDisciplinaryImportExecutor
from views.tasks.new_teacher_extend_task import EducationalTeachingImportExecutor, TalentProgramsImportExecutor, \
    DomesticTrainingImportExecutor, OverseasStudyImportExecutor, AnnualReviewImportExecutor, \
    ResearchAchievementsProjectImportExecutor, ResearchAchievementsBookImportExecutor, \
    ResearchAchievementsPaperImportExecutor, ResearchAchievementsRewardImportExecutor, \
    ResearchAchievementsArtworkImportExecutor, ResearchAchievementsPatentImportExecutor, \
    ResearchAchievementsCompetitionImportExecutor, ResearchAchievementsMedicineImportExecutor


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
        payload_cls=PlanningSchoolFileStorageModel,
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
    task_router.register(
        code="teacher_work_experience_import",
        consumer_group_id="service",
        topic="teacher_work_experience_import",
        name="教师工作经历导入",
        executor_cls=TeacherWorkExperienceImportExecutor,
        payload_cls=TeacherFileStorageModel,
        payload_is_list=False,
        description="",
    )
    task_router.register(
        code="teacher_learn_experience_import",
        consumer_group_id="service",
        topic="teacher_learn_experience_import",
        name="teacher_learn_experience导入",
        executor_cls=TeacherLearnExperienceImportExecutor,
        payload_cls=TeacherFileStorageModel,
        payload_is_list=False,
        description="",
    )
    task_router.register(
        code="teacher_job_appointments_import",
        consumer_group_id="service",
        topic="teacher_job_appointments_import",
        name="teacher_job_appointments导入",
        executor_cls=TeacherJobAppointmentsImportExecutor,
        payload_cls=TeacherFileStorageModel,
        payload_is_list=False,
        description="",
    )

    task_router.register(
        code="teacher_professional_titles_import",
        consumer_group_id="service",
        topic="teacher_professional_titles_import",
        name="teacher_professional_titles导入",
        executor_cls=TeacherProfessionalTitlesImportExecutor,
        payload_cls=TeacherFileStorageModel,
        payload_is_list=False,
        description="",
    )

    task_router.register(
        code="teacher_qualifications_import",
        consumer_group_id="service",
        topic="teacher_qualifications_import",
        name="teacher_qualifications导入",
        executor_cls=TeacherQualificationsImportExecutor,
        payload_cls=TeacherFileStorageModel,
        payload_is_list=False,
        description="",
    )

    task_router.register(
        code="teacher_skill_certificates_import",
        consumer_group_id="service",
        topic="teacher_skill_certificates_import",
        name="teacher_skill_certificates导入",
        executor_cls=TeacherSkillCertificatesImportExecutor,
        payload_cls=TeacherFileStorageModel,
        payload_is_list=False,
        description="",
    )

    task_router.register(
        code="teacher_ethic_records_rewards_import",
        consumer_group_id="service",
        topic="teacher_ethic_records_rewards_import",
        name="teacher_ethic_records_rewards导入",
        executor_cls=TeacherEthicRecordsRewardsImportExecutor,
        payload_cls=TeacherFileStorageModel,
        payload_is_list=False,
        description="",
    )

    task_router.register(
        code="teacher_ethic_records_disciplinary_import",
        consumer_group_id="service",
        topic="teacher_ethic_records_disciplinary_import",
        name="teacher_ethic_records_disciplinary导入",
        executor_cls=TeacherEthicRecordsDisciplinaryImportExecutor,
        payload_cls=TeacherFileStorageModel,
        payload_is_list=False,
        description="",
    )

    task_router.register(
        code="educational_teaching_import",
        consumer_group_id="service",
        topic="educational_teaching_import",
        name="educational_teaching导入",
        executor_cls=EducationalTeachingImportExecutor,
        payload_cls=TeacherFileStorageModel,
        payload_is_list=False,
        description="",
    )

    task_router.register(
        code="talent_programs_import",
        consumer_group_id="service",
        topic="talent_programs_import",
        name="talent_programs导入",
        executor_cls=TalentProgramsImportExecutor,
        payload_cls=TeacherFileStorageModel,
        payload_is_list=False,
        description="",
    )

    task_router.register(
        code="domestic_training_import",
        consumer_group_id="service",
        topic="domestic_training_import",
        name="domestic_training导入",
        executor_cls=DomesticTrainingImportExecutor,
        payload_cls=TeacherFileStorageModel,
        payload_is_list=False,
        description="",
    )

    task_router.register(
        code="overseas_study_import",
        consumer_group_id="service",
        topic="overseas_study_import",
        name="overseas_study导入",
        executor_cls=OverseasStudyImportExecutor,
        payload_cls=TeacherFileStorageModel,
        payload_is_list=False,
        description="",
    )

    task_router.register(
        code="annual_review_import",
        consumer_group_id="service",
        topic="annual_review_import",
        name="annual_review导入",
        executor_cls=AnnualReviewImportExecutor,
        payload_cls=TeacherFileStorageModel,
        payload_is_list=False,
        description="",
    )

    task_router.register(
        code="research_achievements_project_import",
        consumer_group_id="service",
        topic="research_achievements_project_import",
        name="research_achievements_project导入",
        executor_cls=ResearchAchievementsProjectImportExecutor,
        payload_cls=TeacherFileStorageModel,
        payload_is_list=False,
        description="",
    )

    task_router.register(
        code="research_achievements_book_import",
        consumer_group_id="service",
        topic="research_achievements_book_import",
        name="research_achievements_book导入",
        executor_cls=ResearchAchievementsBookImportExecutor,
        payload_cls=TeacherFileStorageModel,
        payload_is_list=False,
        description="",
    )

    task_router.register(
        code="research_achievements_paper_import",
        consumer_group_id="service",
        topic="research_achievements_paper_import",
        name="research_achievements_paper导入",
        executor_cls=ResearchAchievementsPaperImportExecutor,
        payload_cls=TeacherFileStorageModel,
        payload_is_list=False,
        description="",
    )

    task_router.register(
        code="research_achievements_reward_import",
        consumer_group_id="service",
        topic="research_achievements_reward_import",
        name="research_achievements_reward导入",
        executor_cls=ResearchAchievementsRewardImportExecutor,
        payload_cls=TeacherFileStorageModel,
        payload_is_list=False,
        description="",
    )

    task_router.register(
        code="research_achievements_artwork_import",
        consumer_group_id="service",
        topic="research_achievements_artwork_import",
        name="research_achievements_artwork导入",
        executor_cls=ResearchAchievementsArtworkImportExecutor,
        payload_cls=TeacherFileStorageModel,
        payload_is_list=False,
        description="",
    )

    task_router.register(
        code="research_achievements_patent_import",
        consumer_group_id="service",
        topic="research_achievements_patent_import",
        name="research_achievements_patent导入",
        executor_cls=ResearchAchievementsPatentImportExecutor,
        payload_cls=TeacherFileStorageModel,
        payload_is_list=False,
        description="",
    )

    task_router.register(
        code="research_achievements_competition_import",
        consumer_group_id="service",
        topic="research_achievements_competition_import",
        name="research_achievements_competition导入",
        executor_cls=ResearchAchievementsCompetitionImportExecutor,
        payload_cls=TeacherFileStorageModel,
        payload_is_list=False,
        description="",
    )

    task_router.register(
        code="research_achievements_medicine_import",
        consumer_group_id="service",
        topic="research_achievements_medicine_import",
        name="research_achievements_medicine导入",
        executor_cls=ResearchAchievementsMedicineImportExecutor,
        payload_cls=TeacherFileStorageModel,
        payload_is_list=False,
        description="",
    )
