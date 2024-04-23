from pydantic import BaseModel, Field

class EnumValue(BaseModel):
    enum_name : str = Field(..., title="",description="枚举类型的名称",examples=['国家'])
    enum_value : str = Field(..., title="", description="枚举的具体值",examples=['韩国','中国'])
    description : str = Field(..., title="", description="枚举值的描述或标签",examples=[''])
    sort_number: int = Field(0, title="", description="排序序号",examples=[ 2])
    parent_id: str = Field('', title="", description="父级ID",examples=[''])


