from fastapi import Query
from pydantic import BaseModel, Field

class FileTask(BaseModel):
    """{'file_name':filename,'bucket':bucket,'scene':scene},"""
    file_name: str = Field('', title="",description="",examples=[' '])
    bucket: str = Field('', title="",description="",examples=[' '])
    scene: str = Field('', title="",description="",examples=[' '])





