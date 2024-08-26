from sqlalchemy import select, or_

from mini_framework.databases.entities.dao_base import DAOBase

from models.unit_system import UnitSystem


# from distribute_transaction_lib.data_access.models import UnitSystem


class UnitSystemDAO(DAOBase):
    """
    单位部署系统表  数据访问对象
    """

    async def get_unit_system_by_unitcodes(self, unit_codes: list,return_keys=None) :
        """
        获取单位部署的URL 通过单位编号
        :return:
        """
        session = await self.slave_db()
        result = await session.execute(select(UnitSystem) .filter(or_(UnitSystem.school_id.in_(unit_codes),UnitSystem.institution_id.in_(unit_codes))))
        res =result.scalars().all()
        # 如果定义了返回的key 则返回字典 以key作为字典键
        if return_keys:
            dic = {}
            for row in res:
                dic[getattr(row, return_keys)] = row
            return dic
        else:
            lst = []
            for row in res:
                lst.append(row)
            return lst

