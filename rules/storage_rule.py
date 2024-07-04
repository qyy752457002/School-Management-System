import os
import tempfile
import uuid

import pandas as pd
from mini_framework.data.tasks.excel_tasks import ExcelReader
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.storage.manager import storage_manager
from mini_framework.storage.persistent.file_storage_dao import FileStorageDAO
from mini_framework.storage.view_model import FileStorageResponseModel, FileStorageModel
from views.models.institutions import Institutions, InstitutionsValid
from views.models.planning_school import PlanningSchool, PlanningSchoolImport
from views.models.school import School
from views.models.students import NewStudents
from views.models.system import ImportScene
from views.models.teachers import TeachersCreatModel


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

    #     解析 文件和桶  返回 数据结构
    async def get_file_data(self, filename: str, bucket, sence=''):
        # 下载保存本地
        random_id = str(uuid.uuid4())
        # source='c.xlsx'
        local_filepath = 'planning_school.xlsx'

        # 下载文件到本地
        local_filepath='temp/'+ random_id+filename

        # 根据不同场景 获取不同的模型
        sheetname = 'Sheet1'

        SampleModel = None
        if sence == ImportScene.PLANNING_SCHOOL.value:
            # 暂时调试
            local_filepath = 'planning_school.xlsx'

            SampleModel = PlanningSchoolImport
            sheetname = 'Sheet1'
        else:
            resp =  storage_manager.download_file( bucket_key=bucket, remote_filename=filename,local_filepath=local_filepath)

            if sence == ImportScene.INSTITUTION.value:
                SampleModel = Institutions
            sheetname = 'Sheet1'

            if sence ==ImportScene.SCHOOL.value:
                SampleModel = School
                sheetname = 'Sheet1'
            if sence ==ImportScene.NEWSTUDENT.value:
                SampleModel = NewStudents
                sheetname = 'Sheet1'
            if sence == ImportScene.NEW_TEACHERS.value:
                SampleModel = TeachersCreatModel
                sheetname = 'Sheet1'
            pass



        resdata = TestExcelReader(local_filepath, sheetname, SampleModel).read_valid()
        print(resdata)
        return resdata


class TestExcelReader:
    def __init__(self, filename, sheetname, SampleModel):
        self.reader = ExcelReader()
        self.filename = filename
        self.sheetname = sheetname
        self.reader.register_model(sheetname, SampleModel)

    def read_valid(self):
        # 执行读取操作
        self.reader.set_data(self.filename)
        result = self.reader.execute()
        # print('文件读取器',result)
        # os.remove(self.filename)  # 清理创建的临时文件
        if self.sheetname in result.keys():
            result = result[self.sheetname]
        return result
        #
        # self.assertEqual(len(result['Sheet1']), 2)
        # self.assertIsInstance(result['Sheet1'][0], SampleModel)
        # self.assertEqual(result['Sheet1'][0].name, 'Alice')
        # self.assertEqual(result['Sheet1'][1].id, 2)

    def read_sheet_not_found(self):
        # 创建一个空的临时Excel文件
        with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp:
            with pd.ExcelWriter(tmp.name, engine='xlsxwriter') as writer:
                df = pd.DataFrame({
                    'aaa': [1, 2],
                    'bbb': ['Alice', 'Bob']
                })
                df.to_excel(writer, sheet_name='Sheet1', index=False)

        self.reader.set_data(tmp.name)
        with self.assertRaises(ValueError):
            self.reader.execute()
        os.remove(tmp.name)  # 清理创建的临时文件
