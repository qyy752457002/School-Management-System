/*
 Navicat PostgreSQL Dump SQL

 Source Server         : 10.0.0.42
 Source Server Type    : PostgreSQL
 Source Server Version : 120001 (120001)
 Source Host           : 10.0.0.42:54321
 Source Catalog        : school_oms_test
 Source Schema         : public

 Target Server Type    : PostgreSQL
 Target Server Version : 120001 (120001)
 File Encoding         : 65001

 Date: 06/09/2024 15:06:10
*/


-- ----------------------------
-- Table structure for lfun_permission_menu
-- ----------------------------
DROP TABLE IF EXISTS "public"."lfun_permission_menu";
CREATE TABLE "public"."lfun_permission_menu" (
  "id" int8 NOT NULL DEFAULT nextval('lfun_permission_menu_id_seq'::regclass),
  "menu_name" varchar(64) COLLATE "pg_catalog"."default",
  "menu_path" varchar(64) COLLATE "pg_catalog"."default",
  "menu_icon" varchar(255) COLLATE "pg_catalog"."default",
  "menu_type" varchar(255) COLLATE "pg_catalog"."default",
  "menu_status" varchar(255) COLLATE "pg_catalog"."default",
  "menu_remark" varchar(255) COLLATE "pg_catalog"."default",
  "parent_id" varchar(255) COLLATE "pg_catalog"."default",
  "permission_id" int4,
  "created_uid" int4,
  "updated_uid" int4,
  "created_at" timestamp(6),
  "updated_at" timestamp(6),
  "is_deleted" bool NOT NULL,
  "menu_code" varchar(255) COLLATE "pg_catalog"."default",
  "sort_order" int4,
  "resource_code" varchar(128) COLLATE "pg_catalog"."default",
  "action" varchar(600) COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "public"."lfun_permission_menu"."id" IS '班级ID';
COMMENT ON COLUMN "public"."lfun_permission_menu"."menu_name" IS '菜单名称';
COMMENT ON COLUMN "public"."lfun_permission_menu"."menu_path" IS '菜单路径';
COMMENT ON COLUMN "public"."lfun_permission_menu"."menu_icon" IS '菜单图标';
COMMENT ON COLUMN "public"."lfun_permission_menu"."menu_type" IS '菜单类型';
COMMENT ON COLUMN "public"."lfun_permission_menu"."menu_status" IS '菜单状态';
COMMENT ON COLUMN "public"."lfun_permission_menu"."menu_remark" IS '菜单备注';
COMMENT ON COLUMN "public"."lfun_permission_menu"."parent_id" IS '父级菜单id';
COMMENT ON COLUMN "public"."lfun_permission_menu"."permission_id" IS '权限ID';
COMMENT ON COLUMN "public"."lfun_permission_menu"."created_uid" IS '创建人';
COMMENT ON COLUMN "public"."lfun_permission_menu"."updated_uid" IS '操作人';
COMMENT ON COLUMN "public"."lfun_permission_menu"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."lfun_permission_menu"."updated_at" IS '更新时间';
COMMENT ON COLUMN "public"."lfun_permission_menu"."is_deleted" IS '删除态';
COMMENT ON COLUMN "public"."lfun_permission_menu"."menu_code" IS '菜单简码';
COMMENT ON COLUMN "public"."lfun_permission_menu"."sort_order" IS '排序 从校到大';
COMMENT ON COLUMN "public"."lfun_permission_menu"."resource_code" IS '资源编码-用于资源和菜单的绑定';
COMMENT ON COLUMN "public"."lfun_permission_menu"."action" IS '允许的资源动作';
COMMENT ON TABLE "public"."lfun_permission_menu" IS '菜单权限表';

-- ----------------------------
-- Records of lfun_permission_menu
-- ----------------------------
INSERT INTO "public"."lfun_permission_menu" VALUES (14, '新教职工管理', '', '', 'root', '', '', '0', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'onboarding', 0, NULL, NULL);
INSERT INTO "public"."lfun_permission_menu" VALUES (17, '在职教职工管理', '', '', 'root', '', '', '0', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'employed', 0, NULL, NULL);
INSERT INTO "public"."lfun_permission_menu" VALUES (31, '非在职教职工管理', '', '', 'root', '', '', '0', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'nonemployed', 0, NULL, NULL);
INSERT INTO "public"."lfun_permission_menu" VALUES (32, '系统管理', '', '', 'root', '', '', '0', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'trchsys', 0, NULL, NULL);
INSERT INTO "public"."lfun_permission_menu" VALUES (34, '任务管理', '/trchsys/task', '', 'menu', '', '', '32', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'trchsystask', 0, NULL, NULL);
INSERT INTO "public"."lfun_permission_menu" VALUES (3, '园所配置管理', '', '', 'root', '', '', '0', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'config', 1, NULL, NULL);
INSERT INTO "public"."lfun_permission_menu" VALUES (9, '中小学配置管理', '', '', 'root', '', '', '0', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'config', 1, NULL, NULL);
INSERT INTO "public"."lfun_permission_menu" VALUES (12, '职高配置管理', '', '', 'root', '', '', '0', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'config', 1, NULL, NULL);
INSERT INTO "public"."lfun_permission_menu" VALUES (52, '借动管理', '', '', 'root', '', '', '17', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'borrow', 0, NULL, NULL);
INSERT INTO "public"."lfun_permission_menu" VALUES (53, '调动管理', '', '', 'root', '', '', '17', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'transfer', 0, NULL, NULL);
INSERT INTO "public"."lfun_permission_menu" VALUES (55, '园所信息审核（学校）', '', '', 'root', '', '', '0', 1, 0, 0, '2024-06-04 10:43:11.169988', '2024-06-04 10:43:11.169988', 'f', 'planning-audit', 0, NULL, NULL);
INSERT INTO "public"."lfun_permission_menu" VALUES (56, '园所信息审核（分校）', '', '', 'root', '', '', '0', 1, 0, 0, '2024-06-04 10:43:11.169988', '2024-06-04 10:43:11.169988', 'f', 'school-audit', 0, NULL, NULL);
INSERT INTO "public"."lfun_permission_menu" VALUES (67, '中小学信息审核（分校）', '', '', 'root', '', '', '0', 1, 0, 0, '2024-06-04 10:43:11.169988', '2024-06-04 10:43:11.169988', 'f', 'school-audit', 0, NULL, NULL);
INSERT INTO "public"."lfun_permission_menu" VALUES (75, '职高信息审核（分校）', '', '', 'root', '', '', '0', 1, 0, 0, '2024-06-04 10:43:11.169988', '2024-06-04 10:43:11.169988', 'f', 'school-audit', 0, NULL, NULL);
INSERT INTO "public"."lfun_permission_menu" VALUES (47, '组织管理', '/org', '', 'menu', '', '', '0', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'org', 5, NULL, NULL);
INSERT INTO "public"."lfun_permission_menu" VALUES (48, '组织管理', '/org', '', 'menu', '', '', '0', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'org', 5, NULL, NULL);
INSERT INTO "public"."lfun_permission_menu" VALUES (49, '组织管理', '/org', '', 'menu', '', '', '0', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'org', 5, NULL, NULL);
INSERT INTO "public"."lfun_permission_menu" VALUES (79, '机构管理', '', '', 'menu', '', '', '0', 1, 0, 0, '2024-06-04 10:43:11.169988', '2024-06-04 10:43:11.169988', 'f', 'institution', 0, NULL, NULL);
INSERT INTO "public"."lfun_permission_menu" VALUES (80, '机构信息审核', '', '', 'menu', '', '', '0', 1, 0, 0, '2024-06-04 10:43:11.169988', '2024-06-04 10:43:11.169988', 'f', 'institution-audit', 0, NULL, NULL);
INSERT INTO "public"."lfun_permission_menu" VALUES (83, '机构开设审核', '/institution-audit/open', '', 'menu', '', '', '80', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'institution-audit-open', 0, NULL, NULL);
INSERT INTO "public"."lfun_permission_menu" VALUES (84, '机构关闭审核', '/institution-audit/close', '', 'menu', '', '', '80', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'institution-audit-close', 0, NULL, NULL);
INSERT INTO "public"."lfun_permission_menu" VALUES (85, '关键信息变更审核', '/institution-audit/changekeyinfo', '', 'menu', '', '', '80', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'institution-audit-changekeyinfo', 0, NULL, NULL);
INSERT INTO "public"."lfun_permission_menu" VALUES (90, '组织管理', '/org', '', 'menu', '', '', '0', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'org', 0, NULL, NULL);
INSERT INTO "public"."lfun_permission_menu" VALUES (95, '组织管理', '/org', '', 'menu', '', '', '0', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'org', 0, NULL, NULL);
INSERT INTO "public"."lfun_permission_menu" VALUES (91, '机构信息审核', '', '', 'menu', '', '', '0', 1, 0, 0, '2024-07-25 13:15:14.000000', '2024-07-25 13:15:12.000000', 'f', 'institution-audit', 0, NULL, NULL);
INSERT INTO "public"."lfun_permission_menu" VALUES (6, '学科管理', '/course', '', 'menu', '', '幼儿园', '3', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'course', 0, 'course', 'add、view');
INSERT INTO "public"."lfun_permission_menu" VALUES (86, '单位信息审核', '', '', 'menu', '', '', '0', 1, 0, 0, '2024-07-25 13:15:14.000000', '2024-07-25 13:15:12.000000', 'f', 'institution-audit', 2, NULL, NULL);
INSERT INTO "public"."lfun_permission_menu" VALUES (18, '年级管理', '/grade', '', 'menu', '', '', '9', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'grade', 0, 'grade', 'add、view、edit、delete');
INSERT INTO "public"."lfun_permission_menu" VALUES (19, '班级管理', '/class', '', 'menu', '', '', '9', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'class', 0, 'class', 'add、view、edit、delete');
INSERT INTO "public"."lfun_permission_menu" VALUES (20, '学科管理', '/course', '', 'menu', '', '中小学', '9', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'course', 0, 'course', 'add、view');
INSERT INTO "public"."lfun_permission_menu" VALUES (13, '专业管理', '/major', '', 'menu', '', '', '12', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'major', 0, 'major', 'add、view、edit、delete');
INSERT INTO "public"."lfun_permission_menu" VALUES (38, '新生入学管理', '/newstudent', '', 'menu', '', '', '35', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'newstudent', 0, 'new_student', 'open、import、view、edit、flowout、sync、formaladmission');
INSERT INTO "public"."lfun_permission_menu" VALUES (39, '分班管理', '/newstudent/classroom', '', 'menu', '', '', '35', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'newstudent_classroom', 0, 'classdivision', 'view、lottery_classdivision、import');
INSERT INTO "public"."lfun_permission_menu" VALUES (46, '临时就读', '/instudent/emporaryBorrowing', '', 'menu', '', '', '36', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'instudent_emporaryBorrowing', 0, 'temporary_study', 'view');
INSERT INTO "public"."lfun_permission_menu" VALUES (28, '借出信息管理', '/employed/borrowout', '', 'menu', '', '', '52', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'employedworkborrowout', 0, NULL, NULL);
INSERT INTO "public"."lfun_permission_menu" VALUES (4, '班级类型管理', '/grade', '', 'menu', '', '', '3', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'grade', 0, 'grade', 'add、view、edit、delete');
INSERT INTO "public"."lfun_permission_menu" VALUES (5, '班级管理', '/class', '', 'menu', '', '', '3', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'class', 0, 'class', 'add、view、edit、delete');
INSERT INTO "public"."lfun_permission_menu" VALUES (15, '新教职工入职', '/onboarding', '', 'menu', '', '', '14', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'onboarding', 0, NULL, NULL);
INSERT INTO "public"."lfun_permission_menu" VALUES (16, '新教职工审批', '/onboarding/approve', '', 'menu', '', '', '14', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'approve', 0, NULL, NULL);
INSERT INTO "public"."lfun_permission_menu" VALUES (21, '年级管理', '/grade', '', 'menu', '', '', '12', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'grade', 0, 'grade', 'add、view、edit、delete');
INSERT INTO "public"."lfun_permission_menu" VALUES (22, '班级管理', '/class', '', 'menu', '', '', '12', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'class', 0, 'class', 'add、view、edit、delete');
INSERT INTO "public"."lfun_permission_menu" VALUES (23, '学科管理', '/course', '', 'menu', '', '职高', '12', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'course', 0, 'course', 'add、view');
INSERT INTO "public"."lfun_permission_menu" VALUES (24, '在职教职工管理', '/employed', '', 'menu', '', '', '17', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'employed', 0, NULL, NULL);
INSERT INTO "public"."lfun_permission_menu" VALUES (25, '教职工信息变更审批', '/employed/approve', '', 'menu', '', '', '17', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'employedapprove', 0, NULL, NULL);
INSERT INTO "public"."lfun_permission_menu" VALUES (26, '变动管理', '/employed/workchange', '', 'menu', '', '', '17', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'employedworkchange', 5, NULL, NULL);
INSERT INTO "public"."lfun_permission_menu" VALUES (27, '借入信息管理', '/employed/borrowin', '', 'menu', '', '', '52', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'employedworkborrowin', 0, NULL, NULL);
INSERT INTO "public"."lfun_permission_menu" VALUES (29, '调入信息管理', '/employed/transferin', '', 'menu', '', '', '53', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'employedworktransferin', 0, NULL, NULL);
INSERT INTO "public"."lfun_permission_menu" VALUES (30, '调出信息管理', '/employed/transferout', '', 'menu', '', '', '53', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'employedworktransferout', 0, NULL, NULL);
INSERT INTO "public"."lfun_permission_menu" VALUES (33, '系统配置', '/trchsys/config', '', 'menu', '', '', '32', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'trchsysconfig', 0, NULL, NULL);
INSERT INTO "public"."lfun_permission_menu" VALUES (37, '毕业生信息管理', '/graduation', '', 'menu', '', '', '0', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'graduation', 0, 'graduation', NULL);
INSERT INTO "public"."lfun_permission_menu" VALUES (54, '离退休信息管理', '/nonemployed/retire', '', 'menu', '', '', '31', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'employedworkretire', 0, NULL, NULL);
INSERT INTO "public"."lfun_permission_menu" VALUES (96, '组织管理', '/org', '', 'menu', '', '', '9', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'org', 0, NULL, NULL);
INSERT INTO "public"."lfun_permission_menu" VALUES (94, '关键信息变更审核', '/institution-audit/changekeyinfo', '', 'menu', '', '', '91', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'institution-audit-changekeyinfo', 0, 'administration_keyinfo_audit', 'start、view、cancel、pass、refuse、approval');
INSERT INTO "public"."lfun_permission_menu" VALUES (93, '关闭审核', '/institution-audit/close', '', 'menu', '', '', '91', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'institution-audit-close', 0, 'administration_close_audit', 'start、view、cancel、pass、refuse、approval');
INSERT INTO "public"."lfun_permission_menu" VALUES (92, '开设审核', '/institution-audit/open', '', 'menu', '', '', '91', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'institution-audit-open', 0, 'administration_open_audit', 'start、view、cancel、pass、refuse、approval');
INSERT INTO "public"."lfun_permission_menu" VALUES (89, '关键信息变更审核', '/institution-audit/changekeyinfo', '', 'menu', '', '', '86', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'institution-audit-changekeyinfo', 2, 'institution_keyinfo_audit', 'start、view、cancel、pass、refuse、approval');
INSERT INTO "public"."lfun_permission_menu" VALUES (88, '单位关闭审核', '/institution-audit/close', '', 'menu', '', '', '86', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'institution-audit-close', 2, 'institution_close_audit', 'start、view、cancel、pass、refuse、approval');
INSERT INTO "public"."lfun_permission_menu" VALUES (87, '单位开设审核', '/institution-audit/open', '', 'menu', '', '', '86', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'institution-audit-open', 2, 'institution_open_audit', 'start、view、cancel、pass、refuse、approval');
INSERT INTO "public"."lfun_permission_menu" VALUES (82, '行政单位管理', '/institution/xz', '', 'menu', '', '', '0', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'institution-xz', 0, 'administration', 'open、import、view、edit、delete、change、close、approval');
INSERT INTO "public"."lfun_permission_menu" VALUES (81, '事业单位管理', '/institution/sy', '', 'menu', '', '', '0', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'institution-sy', 0, 'institution', 'open、import、view、edit、delete、change、close、approval');
INSERT INTO "public"."lfun_permission_menu" VALUES (78, '关键信息变更审核', '/school-audit/changekeyinfo', '', 'menu', '', '', '75', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'school-audit-changekeyinfo', 0, 'school_keyinfo_audit', 'start、view、cancel、pass、refuse、approval');
INSERT INTO "public"."lfun_permission_menu" VALUES (77, '学校关闭审核', '/school-audit/closeschool', '', 'menu', '', '', '75', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'school-audit-closeschool', 0, 'school_close_audit', 'start、view、cancel、pass、refuse、approval');
INSERT INTO "public"."lfun_permission_menu" VALUES (76, '学校开设审核', '/school-audit/openschool', '', 'menu', '', '', '75', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'school-audit-openschool', 0, 'school_open_audit', 'start、view、cancel、pass、refuse、approval');
INSERT INTO "public"."lfun_permission_menu" VALUES (74, '关键信息变更审核', '/planning-audit/changekeyinfo', '', 'menu', '', '', '71', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'planning-audit-changekeyinfo', 0, 'planning_school_keyinfo_audit', 'start、view、cancel、pass、refuse、approval');
INSERT INTO "public"."lfun_permission_menu" VALUES (73, '学校关闭审核', '/planning-audit/closeschool', '', 'menu', '', '', '71', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'planning-audit-closeschool', 0, 'planning_school_close_audit', 'start、view、cancel、pass、refuse、approval');
INSERT INTO "public"."lfun_permission_menu" VALUES (72, '学校开设审核', '/planning-audit/openschool', '', 'menu', '', '', '71', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'planning-audit-openschool', 0, 'planning_school_open_audit', 'open、import、view、edit、delete、change_baseinfo、change_keyinfo、close、relation、approval');
INSERT INTO "public"."lfun_permission_menu" VALUES (71, '职高信息审核（学校）', '', '', 'root', '', '', '0', 1, 0, 0, '2024-06-04 10:43:11.169988', '2024-06-04 10:43:11.169988', 'f', 'planning-audit', 0, 'planning_school_open_audit', 'open、import、view、edit、delete、change_baseinfo、change_keyinfo、close、relation、approval');
INSERT INTO "public"."lfun_permission_menu" VALUES (70, '关键信息变更审核', '/school-audit/changekeyinfo', '', 'menu', '', '', '67', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'school-audit-changekeyinfo', 0, 'school_keyinfo_audit', 'start、view、cancel、pass、refuse、approval');
INSERT INTO "public"."lfun_permission_menu" VALUES (69, '学校关闭审核', '/school-audit/closeschool', '', 'menu', '', '', '67', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'school-audit-closeschool', 0, 'school_close_audit', 'start、view、cancel、pass、refuse、approval');
INSERT INTO "public"."lfun_permission_menu" VALUES (68, '学校开设审核', '/school-audit/openschool', '', 'menu', '', '', '67', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'school-audit-openschool', 0, 'school_open_audit', 'start、view、cancel、pass、refuse、approval');
INSERT INTO "public"."lfun_permission_menu" VALUES (66, '关键信息变更审核', '/planning-audit/changekeyinfo', '', 'menu', '', '', '63', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'planning-audit-changekeyinfo', 0, 'planning_school_keyinfo_audit', 'start、view、cancel、pass、refuse、approval');
INSERT INTO "public"."lfun_permission_menu" VALUES (65, '学校关闭审核', '/planning-audit/closeschool', '', 'menu', '', '', '63', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'planning-audit-closeschool', 0, 'planning_school_close_audit', 'start、view、cancel、pass、refuse、approval');
INSERT INTO "public"."lfun_permission_menu" VALUES (64, '学校开设审核', '/planning-audit/openschool', '', 'menu', '', '', '63', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'planning-audit-openschool', 0, 'planning_school_open_audit', 'open、import、view、edit、delete、change_baseinfo、change_keyinfo、close、relation、approval');
INSERT INTO "public"."lfun_permission_menu" VALUES (63, '中小学信息审核（学校）', '', '', 'root', '', '', '0', 1, 0, 0, '2024-06-04 10:43:11.169988', '2024-06-04 10:43:11.169988', 'f', 'planning-audit', 0, 'planning_school_open_audit', 'open、import、view、edit、delete、change_baseinfo、change_keyinfo、close、relation、approval');
INSERT INTO "public"."lfun_permission_menu" VALUES (62, '关键信息变更审核', '/school-audit/changekeyinfo', '', 'menu', '', '', '56', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'school-audit-changekeyinfo', 0, 'school_keyinfo_audit', 'start、view、cancel、pass、refuse、approval');
INSERT INTO "public"."lfun_permission_menu" VALUES (61, '学校关闭审核', '/school-audit/closeschool', '', 'menu', '', '', '56', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'school-audit-closeschool', 0, 'school_close_audit', 'start、view、cancel、pass、refuse、approval');
INSERT INTO "public"."lfun_permission_menu" VALUES (60, '学校开设审核', '/school-audit/openschool', '', 'menu', '', '', '56', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'school-audit-openschool', 0, 'school_open_audit', 'start、view、cancel、pass、refuse、approval');
INSERT INTO "public"."lfun_permission_menu" VALUES (59, '关键信息变更审核', '/planning-audit/changekeyinfo', '', 'menu', '', '', '55', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'planning-audit-changekeyinfo', 0, 'planning_school_keyinfo_audit', 'start、view、cancel、pass、refuse、approval');
INSERT INTO "public"."lfun_permission_menu" VALUES (58, '学校关闭审核', '/planning-audit/closeschool', '', 'menu', '', '', '55', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'planning-audit-closeschool', 0, 'planning_school_close_audit', 'start、view、cancel、pass、refuse、approval');
INSERT INTO "public"."lfun_permission_menu" VALUES (57, '学校开设审核', '/planning-audit/openschool', '', 'menu', '', '', '55', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'planning-audit-openschool', 0, 'planning_school_open_audit', 'open、import、view、edit、delete、change_baseinfo、change_keyinfo、close、relation、approval');
INSERT INTO "public"."lfun_permission_menu" VALUES (51, '课程管理', '/subject', '', 'menu', '', '职高', '12', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'subject', 0, 'subject', 'add、view、edit、delete、approval');
INSERT INTO "public"."lfun_permission_menu" VALUES (50, '课程管理', '/subject', '', 'menu', '', '中小学', '9', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'subject', 0, 'subject', 'add、view、edit、delete、approval');
INSERT INTO "public"."lfun_permission_menu" VALUES (45, '异动管理', '/instudent/innerTransfer', '', 'menu', '', '', '36', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'instudent_innerTransfer', 0, 'student_inner_transaction', 'start、view、cancel、pass、refuse、approval');
INSERT INTO "public"."lfun_permission_menu" VALUES (44, '转出信息管理', '/instudent/checkout', '', 'menu', '', '', '36', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'instudent_checkout', 0, 'instudent_transfer', 'in_view、in_pass、in_refuse、out_view、out_pass、out_refuse、approval');
INSERT INTO "public"."lfun_permission_menu" VALUES (43, '转入信息管理', '/instudent/checkin', '', 'menu', '', '', '36', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'instudent_checkin', 0, 'instudent_transfer', 'in_view、in_pass、in_refuse、out_view、out_pass、out_refuse、approval');
INSERT INTO "public"."lfun_permission_menu" VALUES (42, '转学信息管理', '/instudent/transfer', '', 'menu', '', '', '36', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'instudent_transfer', 0, 'instudent_transfer', 'in_view、in_pass、in_refuse、out_view、out_pass、out_refuse、approval');
INSERT INTO "public"."lfun_permission_menu" VALUES (41, '在校学生信息管理', '/instudent', '', 'menu', '', '', '36', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'instudent', 0, 'infomanage', 'temporary_study_start、temporary_study_cancel、temporary_study_view、current_student_view、current_student_change、current_student_keyinfo_change、approval');
INSERT INTO "public"."lfun_permission_menu" VALUES (40, '届别管理', '/newstudent/academia', '', 'menu', '', '', '35', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'newstudent_academia', 0, 'student_session', 'add、view、edit、delete、approval');
INSERT INTO "public"."lfun_permission_menu" VALUES (36, '在校学生信息管理', '', '', 'root', '', '', '0', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'instudent', 0, 'infomanage', 'temporary_study_start、temporary_study_cancel、temporary_study_view、current_student_view、current_student_change、current_student_keyinfo_change、approval');
INSERT INTO "public"."lfun_permission_menu" VALUES (35, '新学生信息管理', '', '', 'root', '', '', '0', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'newstudent', 0, 'new_student', 'open、import、view、edit、flowout、sync、formaladmission、approval');
INSERT INTO "public"."lfun_permission_menu" VALUES (11, '职高信息管理（分校）', '/school', '', 'menu', '', '', '0', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'school', 0, 'school', 'open、import、view、edit、delete、change_baseinfo、change_keyinfo、close、approval');
INSERT INTO "public"."lfun_permission_menu" VALUES (10, '职高信息管理（学校）', '/planning', '', 'menu', '', '', '0', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'planning', 0, 'planning_school', 'open、import、view、edit、delete、change_baseinfo、change_keyinfo、close、relation、approval');
INSERT INTO "public"."lfun_permission_menu" VALUES (8, '中小学信息管理（分校）', '/school', '', 'menu', '', '', '0', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'school', 0, 'school', 'open、import、view、edit、delete、change_baseinfo、change_keyinfo、close、approval');
INSERT INTO "public"."lfun_permission_menu" VALUES (7, '中小学信息管理（学校）', '/planning', '', 'menu', '', '', '0', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'planning', 0, 'planning_school', 'open、import、view、edit、delete、change_baseinfo、change_keyinfo、close、relation、approval');
INSERT INTO "public"."lfun_permission_menu" VALUES (2, '园所信息管理（分校）', '/school', '', 'menu', '', '', '0', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'school', 0, 'school', 'open、import、view、edit、delete、change_baseinfo、change_keyinfo、close、approval');
INSERT INTO "public"."lfun_permission_menu" VALUES (1, '园所信息管理（学校）', '/planning', '', 'menu', '', '', '0', 1, 0, 0, '2024-06-04 10:43:11.169988', '2024-06-04 10:43:11.169988', 'f', 'planning', 0, 'planning_school', 'open、import、view、edit、delete、change_baseinfo、change_keyinfo、close、relation、approval');

-- ----------------------------
-- Primary Key structure for table lfun_permission_menu
-- ----------------------------
ALTER TABLE "public"."lfun_permission_menu" ADD CONSTRAINT "lfun_permission_menu_pkey" PRIMARY KEY ("id");
