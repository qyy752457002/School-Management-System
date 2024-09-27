from sqlalchemy import select
from mini_framework.databases.entities.dao_base import DAOBase
from models.certificate_batch import CertificateBatch

class CertificateBatchDAO(DAOBase):
    async def create_new_batch(self, year, batch_name, certification):
        # 获取从数据库的会话
        session = await self.master_db()
        # 创建一个新的CertificateBatch对象，并设置其属性
        new_batch = CertificateBatch(year=year, batch_name=batch_name, certification=certification)
        # 将新对象添加到会话中
        session.add(new_batch)
        # 提交会话，将新对象保存到数据库中
        await session.commit()

    async def query(self, year, batch_name):
        # 获取从数据库的会话
        session = await self.slave_db()
        # 执行查询，查询CertificateBatch表中year和batch_name等于给定参数的记录
        result = await session.execute(select(CertificateBatch).where(CertificateBatch.year == year and CertificateBatch.batch_name == batch_name)) 
        # 返回查询结果的所有记录
        return result.scalars().all()


    
    


