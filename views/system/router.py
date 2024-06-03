from mini_framework.storage.view_model import FileStorageResponseModel
from mini_framework.web.router import Router

from views.system.enum_value_view import EnumValueView
from views.system.operation_record_view import OperationRecordView
from views.system.storage_view import StorageView
from views.system.sub_system_view import SubSystemView
from views.system.system_view import SystemView


def routers():
    router = Router()
    router.include_api_view_class(OperationRecordView, "/v1/system", description="操作日志管理")

    router.include_api_view_class(SubSystemView, "/v1/subsystem", description="子系统列表")
    router.include_api_view_class(SystemView, "/v1/system", description="系统模块")

    router.include_api_view_class(EnumValueView, "/v1/enums", description="枚举值列表")

    router.include_api_view_class(StorageView, "/v1/storage", description="文件上传下载接口",
                                  response_cls=FileStorageResponseModel)

    return router
