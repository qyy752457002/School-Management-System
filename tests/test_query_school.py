import os
import unittest
from unittest.mock import MagicMock, AsyncMock

from mini_framework.context import env
env.app_root = os.path.dirname( os.path.dirname(os.path.abspath(__file__)))
env.sync_type = "async"

from sqlalchemy import select

from models.school import School
from rules.school_rule import SchoolRule
from views.models.school import School as SchoolModel
class TestSchoolRule(unittest.IsolatedAsyncioTestCase):

    async def setUp(self):
        self.mock_db_manager = MagicMock()
        self.mock_session = AsyncMock()
        self.mock_db_manager.get_async_session.return_value = self.mock_session
        self.mock_result = AsyncMock()
        self.mock_session.execute.return_value.scalars.return_value.all.return_value=''
        self.school_rule = SchoolRule()

    async def test_query_schools(self):
        school_data = [
            {"school_id": 1, "school_name": "ABC School"},
            {"school_id": 2, "school_name": "XYZ School"}
        ]

        planning_school_name = "ABC"
        result = await self.school_rule.query_schools(planning_school_name)

        # 验证是否调用了数据库
        self.mock_session.execute.assert_called_once_with(
            select(School).where(School.school_name.like(f'{planning_school_name}%'))
        )

        # 验证转换逻辑
        self.assertEqual(len(result), 2)
        for index, school in enumerate(result):
            self.assertIsInstance(school, SchoolModel)
            self.assertEqual(school.school_name, school_data[index]['school_name'])
            self.assertEqual(school.school_id, school_data[index]['school_id'])

        # 验证是否正确关闭了数据库会话
        self.mock_session.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()
