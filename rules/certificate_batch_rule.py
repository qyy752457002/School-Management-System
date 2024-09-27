from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model

from daos.certificate_batch_dao import CertificateBatchDAO
from views.models.certificate import CertificateBatchField

@dataclass_inject
class CertificateBatchRule(object):
    # 证书批次数据访问对象
    certificate_batch_dao: CertificateBatchDAO

    # 创建新的证书批次
    async def create_new_batch(self, year, batch_name, certification):

        # 创建新的认证批次
        certification_batch_db = await self.certificate_batch_dao.create_new_batch(year, batch_name, certification)
        # 将数据库模型转换为视图模型
        certification_batch = orm_model_to_view_model(certification_batch_db, CertificateBatchField)
        # 返回视图模型
        return certification_batch
    
    # 查询证书批次
    async def query_batches(self, year, batch_name):

        certification_batch_db = await self.certificate_batch_dao.create_new_batch(year, batch_name, certification)
        # 将数据库模型转换为视图模型
        certification_batch = orm_model_to_view_model(certification_batch_db, CertificateBatchField)
        # 返回视图模型
        return certification_batch
