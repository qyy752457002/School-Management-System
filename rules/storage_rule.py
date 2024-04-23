from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.storage.manager import storage_manager

from views.models.storage import StorageModel


@dataclass_inject
class StorageRule(object):
    def __init__(self):
        self.storage = storage_manager

    def get_upload_school_info_token_uri(self, filename: str) -> StorageModel:
        """
        查询文件上传路径（带 token）
        :param bucket_key: 桶名称
        :param filename: 文件名
        :param path: 文件路径（不含文件名）,默认根目录
        :return: 文件上传路径
        """
        filename = filename.split("/")[-1]
        uri = self.storage.query_put_object_url_with_token("school", filename)
        return StorageModel(upload_uri=uri)

    def get_upload_student_info_token_uri(self, filename: str) -> StorageModel:
        """
        查询文件上传路径（带 token）
        :param bucket_key: 桶名称
        :param filename: 文件名
        :param path: 文件路径（不含文件名）,默认根目录
        :return: 文件上传路径
        """
        filename = filename.split("/")[-1]
        uri = self.storage.query_put_object_url_with_token("student", filename)
        return StorageModel(upload_uri=uri)

    def get_upload_teacher_info_token_uri(self, filename: str) -> StorageModel:
        """
        查询文件上传路径（带 token）
        :param bucket_key: 桶名称
        :param filename: 文件名
        :param path: 文件路径（不含文件名）,默认根目录
        :return: 文件上传路径
        """
        filename = filename.split("/")[-1]
        uri = self.storage.query_put_object_url_with_token("teacher", filename)
        return StorageModel(upload_uri=uri)
