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

from . import classes
from . import enum_value
from . import major
from . import graduation_student

from . import course
from . import operation_record
from . import sub_system

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
from . import tasks

metadata = BaseDBModel.metadata
