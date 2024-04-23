from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.web.views import BaseView

from rules.storage_rule import StorageRule


class StorageView(BaseView):
    def __init__(self):
        super().__init__()
        self._storage_rule: StorageRule = get_injector(StorageRule)

    async def get_school_upload_uri(self, filename: str, file_size: int):
        return await self._storage_rule.get_upload_school_info_token_uri(filename, file_size)

    async def get_student_upload_uri(self, filename: str, file_size: int):
        return await self._storage_rule.get_upload_student_info_token_uri(filename, file_size)

    async def get_teacher_upload_uri(self, filename: str, file_size: int):
        return await self._storage_rule.get_upload_teacher_info_token_uri(filename, file_size)
