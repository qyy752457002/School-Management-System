from sqlalchemy import select, func, update

from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest
from models.teachers import Teacher
from models.teachers_info import TeacherInfo
from views.models.teacher_transaction import TeacherTransactionQuery
from views.models.teachers import TeacherApprovalQuery
from models.school import School


class TeachersDao(DAOBase):
    # 新增教师关键信息
    async def add_teachers(self, teachers):
        session = await self.master_db()
        session.add(teachers)
        await session.commit()
        await session.refresh(teachers)
        return teachers

    async def update_teachers(self, teachers: Teacher, *args, is_commit: bool = True):
        session = await self.master_db()
        update_contents = get_update_contents(teachers, *args)
        query = update(Teacher).where(Teacher.teacher_id == teachers.teacher_id).values(**update_contents)
        return await self.update(session, query, teachers, update_contents, is_commit=is_commit)

    # 获取单个教师信息
    async def get_teachers_by_id(self, teachers_id):
        session = await self.slave_db()
        result = await session.execute(
            select(Teacher).where(Teacher.teacher_id == teachers_id, Teacher.is_deleted == 0))
        return result.scalar_one_or_none()

    # 删除单个教师信息

    # 删除单个教师信息
    async def delete_teachers(self, teachers: Teacher):
        session = await self.master_db()
        print(teachers.teacher_id, teachers.is_deleted)
        return await self.delete(session, teachers)

    # 获取所有教师信息
    async def get_all_teachers(self):
        session = await self.slave_db()
        result = await session.execute(select(Teacher))
        return result.scalars().all()

    # 获取教师数量
    async def get_teachers_count(self):
        session = await self.slave_db()
        result = await session.execute(select(func.count()).select_from(Teacher))
        return result.scalar()

    async def query_teacher_transfer(self, teacher_transaction: TeacherTransactionQuery):
        session = await self.slave_db()
        query = select(Teacher).where(Teacher.teacher_name == teacher_transaction.teacher_name,
                                      Teacher.teacher_id_type == teacher_transaction.teacher_id_type,
                                      Teacher.teacher_id_number == teacher_transaction.teacher_id_number,
                                      )
        result = await session.execute(query)
        return result.scalar_one_or_none()

    async def query_teacher_launch_with_page(self, query_model: TeacherApprovalQuery,
                                             page_request: PageRequest) -> Paging:
        """
        查询我发起的教师审批
        我发起根据的是流程实例的申请人
        我审批根据的是角色
        查询条件：
            教师姓名：teacher_name
            所属机构：teacher_employer
            教师性别：teacher_gender
            申请人：operator_name
            审核人：approval_name
            身份证号：teacher_id_number
        返回内容：
            teacher_name: str = Field("", title="姓名", description="姓名", example="张三")
            teacher_gender: Gender = Field("male", title="性别", description="性别", example="男")
            school_name: str = Query("", title="任职单位名称", description="任职单位名称", example="xx小学")
            teacher_id_number: str = Field("", title="身份证号", description="身份证号", example="123456789012345678")
            employment_form: str = Field("", title="用人形式", description="用人形式", example="合同")
            teacher_id: int = Field(..., title="教师ID", description="教师ID")
            operator_name: str = Field("", title="申请人", description="申请人", example="张三")
            approval_name: str = Field("", title="审核人", description="审核人", example="张三")
            operation_time: Optional[date] = Field(None, title="申请时间", description="申请时间")
            approval_time: Optional[date] = Field(None, title="审批时间", description="审批时间")
            approval_status: str = Field("pending", title="审批状态", description="审批状态")
            process_instance_id: int = Field(0, title="流程实例id", description="流程实例id")
        """
        # todo 模型还缺一个角色
        query = select(Teacher, TeacherInfo.employment_form, School.school_name).join(School,
                                                                                      School.id == Teacher.teacher_employer,
                                                                                      isouter=True)
