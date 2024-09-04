from fastapi import Query
from pydantic import BaseModel, Field, model_validator


class Tenant(BaseModel):
    id: int | str = Query(None, title="", description="id", example='1'),
    origin_id: int | str = Field(0, title="学校ID", description="学校ID", examples=['1'])
    tenant_type: str = Field(..., title="", description="", examples=['19'])
    code: str | None = Field('', title="", description="", examples=['19'])
    name: str | None = Field('', title="", description="", examples=['19'])
    description: int | str = Field(0, title="", description="", examples=['1'])
    status: str = Field(..., title="", description="", examples=[''])
    client_id: str | None = Field('', title="", description="", examples=[''])
    client_secret: str | None = Field('', title="", description="", examples=[''])
    home_url: str | None = Field('', title="", description="", examples=[''])
    redirect_url: str | None = Field('', title="", description="", examples=[''])

    @model_validator(mode="before")
    @classmethod
    def check_id_before(self, data: dict):
        _change_list = ["id", "origin_id",  ]
        for _change in _change_list:
            if _change not in data:
                continue
            if isinstance(data[_change], str):
                data[_change] = int(data[_change])
            elif isinstance(data[_change], int):
                # data[_change] = str(data[_change])
                pass
            else:
                pass
        return data
