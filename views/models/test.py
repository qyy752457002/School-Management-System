from pydantic import BaseModel, Field


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
