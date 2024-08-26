from pydantic import BaseModel, Field
from mini_framework.utils.json import JsonUtils


class ApplicationInfo(BaseModel):
    name: str = Field(..., title="Application Name", description="Application Description")
    version: str = Field(..., title="Application Version", description="Application Version")
    description: str = Field(..., title="Application Description", description="Application Description")
    author: str = Field(..., title="Application Author", description="Application Author")
    author_email: str = Field(..., title="Application Author Email", description="Application Author Email")
    copyright: str = Field(..., title="Application Copyright", description="Application Copyright")

    class Config:
        schema_extra = {
            "example": {
                "name": "School Management System",
                "version": "1.0.0",
                "description": "A school management system",
                "author": "Lfun technical",
                "author_email": "cloud@lfun.cn",
                "copyright": "Copyright © 2024 Lfun technical"
            }
        }
dict = {'contactEmail': 'j.vyevxiloyy@qq.com', 'displayName': '督导处测试',
        'educateUnit': '1a8f5eae2043832fa2c19375b8aefb61', 'isDeleted': False, 'isEnabled': True, 'isTopGroup': False,
        'key': '', 'manager': '', 'name': 'K9tJcfA7xYeKrhdKssFkb6', 'newCode': 'K9tJcfA7xYeKrhdKssFkb6',
        'newType': 'organization', 'owner': '2314234', 'parentId': '7223133029286416384', 'parentName': '',
        'tags': [''], 'title': '', 'type': ''}

json_str = JsonUtils.dict_to_json_str(dict)
print(json_str)