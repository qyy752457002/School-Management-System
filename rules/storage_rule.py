from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.storage.manager import storage_manager
from mini_framework.storage.persistent.file_storage_dao import FileStorageDAO
from mini_framework.storage.view_model import FileStorageResponseModel, FileStorageModel


@dataclass_inject
class StorageRule(object):
    storage_dao: FileStorageDAO

    async def get_upload_school_info_token_uri(self, filename: str, file_size: int) -> FileStorageResponseModel:
        """
        查询文件上传路径（带 token）
        :param filename: 文件名
        :param file_size: 文件大小
        :return: 文件上传路径
        """
        filename = filename.split("/")[-1]
        storage_info = FileStorageModel(file_name=filename, bucket_name="school", file_size=file_size)
        resp = await storage_manager.add_file(self.storage_dao, storage_info)
        return resp

    async def get_upload_student_info_token_uri(self, filename: str, file_size: int) -> FileStorageResponseModel:
        """
        查询文件上传路径（带 token）
        :param filename: 文件名
        :param file_size: 文件大小
        :return: 文件上传路径
        """
        filename = filename.split("/")[-1]
        storage_info = FileStorageModel(file_name=filename, bucket_name="student", file_size=file_size)
        resp = await storage_manager.add_file(self.storage_dao, storage_info)
        return resp

    async def get_upload_teacher_info_token_uri(self, filename: str, file_size: int) -> FileStorageResponseModel:
        """
        查询文件上传路径（带 token）
        :param filename: 文件名
        :param file_size: 文件大小
        :return: 文件上传路径
        """
        filename = filename.split("/")[-1]
        storage_info = FileStorageModel(file_name=filename, bucket_name="teacher", file_size=file_size)
        resp = await storage_manager.add_file(self.storage_dao, storage_info)
        return resp
