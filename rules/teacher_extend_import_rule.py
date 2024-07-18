from views.models.teachers import IdentityType
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from datetime import datetime
from views.models.teachers import TeachersCreatModel, TeacherInfoSaveModel, TeacherImportSaveResultModel, \
    TeacherFileStorageModel, CurrentTeacherQuery, CurrentTeacherQueryRe, \
    NewTeacherApprovalCreate, TeachersSaveImportCreatModel, TeacherImportResultModel, \
    TeachersSaveImportRegisterCreatModel, TeacherInfoImportSubmit
from business_exceptions.school import SchoolNotFoundError

import shortuuid
from mini_framework.async_task.data_access.models import TaskResult
from mini_framework.async_task.data_access.task_dao import TaskDAO
from mini_framework.async_task.task.task import Task, TaskState
from mini_framework.data.tasks.excel_tasks import ExcelWriter, ExcelReader
from mini_framework.storage.manager import storage_manager
from mini_framework.utils.logging import logger

from rules.common.common_rule import convert_fields_to_str, excel_fields_to_enum

from rules.teachers_info_rule import TeachersInfoRule
from rules.teachers_rule import TeachersRule
from mini_framework.storage.persistent.file_storage_dao import FileStorageDAO
from daos.organization_dao import OrganizationDAO
@dataclass_inject
class TeacherImportExtendRule:
    file_storage_dao: FileStorageDAO
    task_dao: TaskDAO