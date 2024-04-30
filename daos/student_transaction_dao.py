from sqlalchemy import select, func, update, or_, and_
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.student_transaction import StudentTransaction
from models.students import Student
from models.students_base_info import StudentBaseInfo


class StudentTransactionDAO(DAOBase):

	async def add_studenttransaction(self, studenttransaction: StudentTransaction):
		session = await self.master_db()
		session.add(studenttransaction)
		await session.commit()
		await session.refresh(studenttransaction)
		return studenttransaction

	async def get_studenttransaction_count(self, ):
		session = await self.slave_db()
		result = await session.execute(select(func.count()).select_from(StudentTransaction))
		return result.scalar()

	async def delete_studenttransaction(self, studenttransaction: StudentTransaction):
		session = await self.master_db()
		await session.delete(studenttransaction)
		await session.commit()

	async def get_studenttransaction_by_id(self, id):
		session = await self.slave_db()
		result = await session.execute(select(StudentTransaction).where(StudentTransaction.id == id))
		return result.scalar_one_or_none()

	async def query_studenttransaction_with_page(self, page_request: PageRequest, **kwargs,):
		query = select(
		StudentTransaction.id, StudentTransaction.school_name, StudentTransaction.grade_name, StudentTransaction.classes, StudentTransaction.transfer_time, StudentTransaction.transfer_reason, StudentTransaction.doc_upload, StudentTransaction.student_id, StudentTransaction.student_no,
			# StudentTransaction.student_name,
			StudentTransaction.current_org, StudentTransaction.apply_user, StudentTransaction.apply_time, StudentTransaction.school_id, StudentTransaction.relation_id, StudentTransaction.transaction_type, StudentTransaction.transaction_type_lv2, StudentTransaction.country_no, StudentTransaction.reason, StudentTransaction.province_id, StudentTransaction.city_id, StudentTransaction.district_id, StudentTransaction.area_id, StudentTransaction.direction, StudentTransaction.transfer_in_type, StudentTransaction.session, StudentTransaction.attached_class, StudentTransaction.grade_id, StudentTransaction.class_id, StudentTransaction.major_id, StudentTransaction.major_name, StudentTransaction.remark, StudentTransaction.status, StudentTransaction.is_valid, StudentTransaction.created_uid, StudentTransaction.updated_uid, StudentTransaction.created_at, StudentTransaction.updated_at, StudentTransaction.is_deleted,

			# StudentTransaction.id,StudentTransaction.student_id,StudentTransaction.in_school_id,StudentTransaction.out_school_id,
			Student.student_name.label('student_name'),
			Student.student_gender,
			StudentBaseInfo.edu_number,
					   ).select_from(  StudentTransaction).join(Student, StudentTransaction.student_id == Student.student_id,isouter=True ).join(StudentBaseInfo, StudentBaseInfo.student_id == Student.student_id,isouter=True )
		query = query.order_by(StudentTransaction.id.desc())
		# 过滤掉  入  且 有关联ID的
		# 排除direction为'in'且relation_id大于0的记录  出  且学校ID =0
		query = query.filter(or_( StudentTransaction.direction!='out' ,  StudentTransaction.school_id != 0 ) )

		for key, value in kwargs.items():
			if key == 'student_gender' or key == 'student_name':
				query = query.where(getattr(Student, key) == value)
			# elif key == 'school_id':
			# 	cond1 = StudentTransaction.in_school_id == value
			# 	cond2 = StudentTransaction.out_school_id == value
			# 	mcond = or_(cond1, cond2)
			#
			# 	query = query.filter( and_(
			# 		StudentTransaction.is_deleted == False,  # a=1
			# 		or_(
			# 			mcond
			# 		)
			# 	))
				# query = query.where(getattr(Student, key).like(f'%{value}%'))
			else:
				query = query.where(getattr(StudentTransaction, key) == value)

		paging = await self.query_page(query, page_request)
		return paging

	async def update_studenttransaction(self, studenttransaction, *args, is_commit=True):
		session = await self.master_db()
		update_contents = get_update_contents(studenttransaction, *args)
		query = update(StudentTransaction).where(StudentTransaction.id == studenttransaction.id).values(**update_contents)
		return await self.update(session, query, studenttransaction, update_contents, is_commit=is_commit)
