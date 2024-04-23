from pydantic import BaseModel, Field


class StorageModel(BaseModel):
    upload_uri: str = Field("", title="上传路径", description="上传路径",
                            example="https://minio.f123.pub/k8s/school/fdfsdfds.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&"
                                    "X-Amz-Credential=BeZHOqpqs4u5jjuv%2F20240422%2Fus-east-1%2Fs3%2Faws4_request&"
                                    "X-Amz-Date=20240422T114810Z&X-Amz-Expires=600&X-Amz-SignedHeaders=host&"
                                    "X-Amz-Signature=d1803082255f647888ab72239af209b4220938f41d37e96a8c4d95e004499963")
    download_uri: str = Field("", title="下载路径", description="下载路径",
                              example="https://minio.f123.pub/k8s/school/fdfsdfds.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&"
                                      "X-Amz-Credential=BeZHOqpqs4u5jjuv%2F20240422%2Fus-east-1%2Fs3%2Faws4_request&"
                                      "X-Amz-Date=20240422T114810Z&X-Amz-Expires=600&X-Amz-SignedHeaders=host&"
                                      "X-Amz-Signature=d1803082255f647888ab72239af209b4220938f41d37e96a8c4d95e004499963")
