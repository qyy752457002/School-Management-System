INSERT INTO public.lfun_permission_menu (id,menu_name,menu_path,menu_icon,menu_type,menu_status,menu_remark,parent_id,permission_id,created_uid,updated_uid,created_at,updated_at,is_deleted,menu_code,sort_order) VALUES
	 (2,'园所信息管理（学校）','/school','','menu','','','0',1,0,0,'2024-06-04 10:43:11.170994','2024-06-04 10:43:11.170994',false,'school',0),
	 (15,'新教职工入职','/onboarding','','menu','','','14',1,0,0,'2024-06-04 10:43:11.170994','2024-06-04 10:43:11.170994',false,'onboarding',0),
	 (5,'班级管理','/class','','menu','','','3',1,0,0,'2024-06-04 10:43:11.170994','2024-06-04 10:43:11.170994',false,'class',0),
	 (11,'职高信息管理（学校）','/school','','menu','','','0',1,0,0,'2024-06-04 10:43:11.170994','2024-06-04 10:43:11.170994',false,'school',0),
	 (8,'中小学信息管理（学校）','/school','','menu','','','0',1,0,0,'2024-06-04 10:43:11.170994','2024-06-04 10:43:11.170994',false,'school',0),
	 (14,'新教职工管理','','','root','','','0',1,0,0,'2024-06-04 10:43:11.170994','2024-06-04 10:43:11.170994',false,'onboarding',0),
	 (17,'在职教职工管理','','','root','','','0',1,0,0,'2024-06-04 10:43:11.170994','2024-06-04 10:43:11.170994',false,'employed',0),
	 (1,'园所信息管理（规划）','/planning','','menu','','','0',1,0,0,'2024-06-04 10:43:11.169988','2024-06-04 10:43:11.169988',false,'planning',0),
	 (7,'中小学信息管理（规划）','/planning','','menu','','','0',1,0,0,'2024-06-04 10:43:11.170994','2024-06-04 10:43:11.170994',false,'planning',0),
	 (10,'职高信息管理（规划）','/planning','','menu','','','0',1,0,0,'2024-06-04 10:43:11.170994','2024-06-04 10:43:11.170994',false,'planning',0);
INSERT INTO public.lfun_permission_menu (id,menu_name,menu_path,menu_icon,menu_type,menu_status,menu_remark,parent_id,permission_id,created_uid,updated_uid,created_at,updated_at,is_deleted,menu_code,sort_order) VALUES
	 (16,'新教职工审批','/onboarding/approve','','menu','','','14',1,0,0,'2024-06-04 10:43:11.170994','2024-06-04 10:43:11.170994',false,'approve',0),
	 (13,'专业管理','/major','','menu','','','12',1,0,0,'2024-06-04 10:43:11.170994','2024-06-04 10:43:11.170994',false,'major',0),
	 (21,'年级管理','/grade','','menu','','','12',1,0,0,'2024-06-04 10:43:11.170994','2024-06-04 10:43:11.170994',false,'grade',0),
	 (18,'年级管理','/grade','','menu','','','9',1,0,0,'2024-06-04 10:43:11.170994','2024-06-04 10:43:11.170994',false,'grade',0),
	 (19,'班级管理','/class','','menu','','','9',1,0,0,'2024-06-04 10:43:11.170994','2024-06-04 10:43:11.170994',false,'class',0),
	 (22,'班级管理','/class','','menu','','','12',1,0,0,'2024-06-04 10:43:11.170994','2024-06-04 10:43:11.170994',false,'class',0),
	 (24,'在职教职工管理','/employed','','menu','','','17',1,0,0,'2024-06-04 10:43:11.170994','2024-06-04 10:43:11.170994',false,'employed',0),
	 (25,'新教职工审批','/employed/approve','','menu','','','17',1,0,0,'2024-06-04 10:43:11.170994','2024-06-04 10:43:11.170994',false,'employedapprove',0),
	 (26,'变动管理','/employed/workchange','','menu','','','17',1,0,0,'2024-06-04 10:43:11.170994','2024-06-04 10:43:11.170994',false,'employedworkchange',0),
	 (27,'借入信息管理','/employed/borrowin','','menu','','','17',1,0,0,'2024-06-04 10:43:11.170994','2024-06-04 10:43:11.170994',false,'employedworkborrowin',0);
INSERT INTO public.lfun_permission_menu (id,menu_name,menu_path,menu_icon,menu_type,menu_status,menu_remark,parent_id,permission_id,created_uid,updated_uid,created_at,updated_at,is_deleted,menu_code,sort_order) VALUES
	 (28,'借出信息管理','/employed/borrowout','','menu','','','17',1,0,0,'2024-06-04 10:43:11.170994','2024-06-04 10:43:11.170994',false,'employedworkborrowout',0),
	 (29,'调入信息管理','/employed/transferin','','menu','','','17',1,0,0,'2024-06-04 10:43:11.170994','2024-06-04 10:43:11.170994',false,'employedworktransferin',0),
	 (30,'调出信息管理','/employed/transferout','','menu','','','17',1,0,0,'2024-06-04 10:43:11.170994','2024-06-04 10:43:11.170994',false,'employedworktransferout',0),
	 (31,'非在职教职工管理','','','root','','','0',1,0,0,'2024-06-04 10:43:11.170994','2024-06-04 10:43:11.170994',false,'nonemployed',0),
	 (32,'系统管理','','','root','','','0',1,0,0,'2024-06-04 10:43:11.170994','2024-06-04 10:43:11.170994',false,'trchsys',0),
	 (33,'系统配置','/trchsys/config','','menu','','','32',1,0,0,'2024-06-04 10:43:11.170994','2024-06-04 10:43:11.170994',false,'trchsysconfig',0),
	 (34,'任务管理','/trchsys/task','','menu','','','32',1,0,0,'2024-06-04 10:43:11.170994','2024-06-04 10:43:11.170994',false,'trchsystask',0),
	 (35,'新学生信息管理','','','root','','','0',1,0,0,'2024-06-04 10:43:11.170994','2024-06-04 10:43:11.170994',false,'newstudent',0),
	 (36,'在校学生信息管理','','','root','','','0',1,0,0,'2024-06-04 10:43:11.170994','2024-06-04 10:43:11.170994',false,'instudent',0),
	 (37,'毕业生信息管理','/graduation','','menu','','','0',1,0,0,'2024-06-04 10:43:11.170994','2024-06-04 10:43:11.170994',false,'graduation',0);
INSERT INTO public.lfun_permission_menu (id,menu_name,menu_path,menu_icon,menu_type,menu_status,menu_remark,parent_id,permission_id,created_uid,updated_uid,created_at,updated_at,is_deleted,menu_code,sort_order) VALUES
	 (38,'新生入学管理','/newstudent','','menu','','','35',1,0,0,'2024-06-04 10:43:11.170994','2024-06-04 10:43:11.170994',false,'newstudent',0),
	 (39,'分班管理','/newstudent/classroom','','menu','','','35',1,0,0,'2024-06-04 10:43:11.170994','2024-06-04 10:43:11.170994',false,'newstudent_classroom',0),
	 (40,'届别管理','/newstudent/academia','','menu','','','35',1,0,0,'2024-06-04 10:43:11.170994','2024-06-04 10:43:11.170994',false,'newstudent_academia',0),
	 (41,'在校学生信息管理','/instudent','','menu','','','36',1,0,0,'2024-06-04 10:43:11.170994','2024-06-04 10:43:11.170994',false,'instudent',0),
	 (42,'转学管理','/transfer','','menu','','','36',1,0,0,'2024-06-04 10:43:11.170994','2024-06-04 10:43:11.170994',false,'instudent_transfer',0),
	 (43,'转入信息管理','/transfer/checkin','','menu','','','36',1,0,0,'2024-06-04 10:43:11.170994','2024-06-04 10:43:11.170994',false,'instudent_checkin',0),
	 (44,'转出信息管理','/transfer/checkout','','menu','','','36',1,0,0,'2024-06-04 10:43:11.170994','2024-06-04 10:43:11.170994',false,'instudent_checkout',0),
	 (45,'异动管理','/transfer/innerTransfer','','menu','','','36',1,0,0,'2024-06-04 10:43:11.170994','2024-06-04 10:43:11.170994',false,'instudent_innerTransfer',0),
	 (46,'临时就读','/transfer/emporaryBorrowing','','menu','','','36',1,0,0,'2024-06-04 10:43:11.170994','2024-06-04 10:43:11.170994',false,'instudent_emporaryBorrowing',0),
	 (47,'组织管理','/org','','menu','','','0',1,0,0,'2024-06-04 10:43:11.170994','2024-06-04 10:43:11.170994',false,'org',0);
INSERT INTO public.lfun_permission_menu (id,menu_name,menu_path,menu_icon,menu_type,menu_status,menu_remark,parent_id,permission_id,created_uid,updated_uid,created_at,updated_at,is_deleted,menu_code,sort_order) VALUES
	 (3,'园所配置管理','','','root','','','0',1,0,0,'2024-06-04 10:43:11.170994','2024-06-04 10:43:11.170994',false,'config',1),
	 (4,'班级类型管理','/grade','','menu','','','3',1,0,0,'2024-06-04 10:43:11.170994','2024-06-04 10:43:11.170994',false,'grade',0),
	 (48,'组织管理','/org','','menu','','','0',1,0,0,'2024-06-04 10:43:11.170994','2024-06-04 10:43:11.170994',false,'org',0),
	 (9,'中小学配置管理','','','root','','','0',1,0,0,'2024-06-04 10:43:11.170994','2024-06-04 10:43:11.170994',false,'config',1),
	 (49,'组织管理','/org','','menu','','','0',1,0,0,'2024-06-04 10:43:11.170994','2024-06-04 10:43:11.170994',false,'org',0),
	 (12,'职高配置管理','','','root','','','0',1,0,0,'2024-06-04 10:43:11.170994','2024-06-04 10:43:11.170994',false,'config',1),
	 (6,'学科管理','/course','','menu','','','3',1,0,0,'2024-06-04 10:43:11.170994','2024-06-04 10:43:11.170994',false,'course',0),
	 (20,'学科管理','/course','','menu','','','9',1,0,0,'2024-06-04 10:43:11.170994','2024-06-04 10:43:11.170994',false,'course',0),
	 (23,'学科管理','/course','','menu','','','12',1,0,0,'2024-06-04 10:43:11.170994','2024-06-04 10:43:11.170994',false,'course',0),
	 (50,'课程管理','/subject','','menu','','','9',1,0,0,'2024-06-04 10:43:11.170994','2024-06-04 10:43:11.170994',false,'subject',0);
INSERT INTO public.lfun_permission_menu (id,menu_name,menu_path,menu_icon,menu_type,menu_status,menu_remark,parent_id,permission_id,created_uid,updated_uid,created_at,updated_at,is_deleted,menu_code,sort_order) VALUES
	 (51,'课程管理','/subject','','menu','','','12',1,0,0,'2024-06-04 10:43:11.170994','2024-06-04 10:43:11.170994',false,'subject',0);
