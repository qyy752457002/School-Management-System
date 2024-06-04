from mini_framework.databases.entities import BaseDBModel
from . import grade
from . import planning_school
from . import teachers
from . import teachers_info
from . import students
from . import students_base_info
from . import students_family_info
from . import student_session
from . import planning_school_communication
from . import planning_school_eduinfo
from . import institution
from . import school
from . import school_eduinfo
from . import school_communication
from . import campus
from . import campus_communication
from . import campus_eduinfo

from . import teacher_learn_experience
from . import teacher_work_experience
from . import teacher_qualifications
from . import teacher_job_appointments
from . import teacher_professional_titles
from . import teacher_skill_certificates
from . import teacher_ethic_records
from . import educational_teaching

from . import annual_review
from . import domestic_training
from . import overseas_study
from . import talent_program
from . import research_achievements

from . import classes
from . import enum_value
from . import major
from . import graduation_student

from . import course
from . import operation_record
from . import sub_system
from mini_framework.storage.persistent.models import FileStorage
from mini_framework.authentication.persistent.models import AuthAccount, JWTBlacklist
from mini_framework.async_task.data_access.models import TaskProgress, TaskResults, TaskInfo

from . import attachments
from . import data_sync_records
from . import sub_db_info

from . import attach_relations
from . import permission_menu
from . import upload_records

from . import leader_info

from . import teacher_transaction
from . import transfer_details
from . import class_division_records
from . import student_transaction
from . import student_transaction_flow
from . import student_inner_transaction
from . import students_key_info_change
from . import education_year
from . import role
from . import role_permission

#教师工作流定以相关
from . import work_flow_define
from . import work_flow_node_define
from . import work_flow_node_depend
from . import work_flow_node_depend_strategy


#教师工作流实例相关
from . import work_flow_instance
from . import work_flow_node_instance


metadata = BaseDBModel.metadata
