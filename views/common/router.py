from mini_framework.web.router import Router

from views.common.storage_view import StorageView
from views.models.storage import StorageModel


def routers():
    router = Router()
    router.include_api_view_class(StorageView, "/v1/storage", description="文件上传下载接口", response_cls=StorageModel)

    return router
