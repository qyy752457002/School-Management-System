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

    async def update_teachers(self, teachers, *args, is_commit: bool = True):
        session = await self.master_db()
        print(dir(teachers))
        update_contents = get_update_contents(teachers, *args)
        query = update(Teacher).where(Teacher.teacher_id == teachers.teacher_id).values(**update_contents)
        return await self.update(session, query, teachers, update_contents, is_commit=is_commit)

    # 获取单个教师信息
    async def get_teachers_by_id(self, teachers_id):
        session = await self.slave_db()
        result = await session.execute(
            select(Teacher).where(Teacher.teacher_id == teachers_id, Teacher.is_deleted == False))
        return result.scalar_one_or_none()

    async def get_teachers_arg_by_id(self, teachers_id):
        session = await self.slave_db()
        query = select(Teacher.teacher_avatar.label("avatar"),
                       Teacher.teacher_date_of_birth.label("birthDate"),
                        Teacher.teacher_name.label("realName"),
                       Teacher.teacher_id_type.label("idCardType"),
                       Teacher.teacher_id_number.label("idCardNumber"),
                       Teacher.teacher_employer.label("currentUnit"),

                       ).outerjoin(TeacherInfo, Teacher.teacher_id == TeacherInfo.teacher_id)
        query = query.where(Teacher.teacher_id == teachers_id,
                            Teacher.is_deleted == False)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    # 根据身份证号获取教师信息

    async def get_teachers_by_teacher_id_number(self, teacher_id_number):
        session = await self.slave_db()
        result = await session.execute(
            select(Teacher).where(Teacher.teacher_id_number == teacher_id_number, Teacher.is_deleted == False))
        return result.scalar_one_or_none()

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
                                      Teacher.is_deleted == False
                                      )
        result = await session.execute(query)
        return result.scalar_one_or_none()

    async def get_teacher_by_params(self, teacher_id_number, teacher_id_type, teacher_name):
        session = await self.slave_db()
        query = select(Teacher).where(Teacher.teacher_id_number == teacher_id_number,
                                      Teacher.teacher_id_type == teacher_id_type,
                                      Teacher.teacher_name == teacher_name,
                                      Teacher.is_deleted == False, Teacher.teacher_main_status == 'employed',
                                      Teacher.is_approval == False)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    async def get_teachers_info_by_prams(self, teacher_id_number, teacher_id_type, teacher_name, teacher_gender):
        session = await self.slave_db()
        query = select(Teacher).where(Teacher.teacher_id_number == teacher_id_number,
                                      Teacher.teacher_id_type == teacher_id_type,
                                      Teacher.teacher_name == teacher_name,
                                      Teacher.teacher_gender == teacher_gender)
        result = await session.execute(query)
        length = len(result.scalars().all())
        return length

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
        # todo 模型还缺一个角色 没做流程的查询,模型是不是还缺一个操作人？
        query = select(Teacher, TeacherInfo.employment_form, School.school_name).join(School,
                                                                                      School.id == Teacher.teacher_employer,
                                                                                      isouter=True)
        if query_model.teacher_name:
            query = query.where(Teacher.teacher_name.like(f"%{query_model.teacher_name}%"))
        if query_model.teacher_id_number:
            query = query.where(Teacher.teacher_id_number == query_model.teacher_id_number)
        if query_model.teacher_gender:
            query = query.where(Teacher.teacher_gender == query_model.teacher_gender)
        if query_model.teacher_employer:
            if query_model.teacher_employer != 0:
                query = query.where(Teacher.teacher_employer == query_model.teacher_employer)
            else:
                pass
        if query_model.operator_name:
            pass
        if query_model.approval_name:
            pass
