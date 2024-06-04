/*
 Navicat Premium Data Transfer

 Source Server         : 10.0.0.42_54321_schooloms
 Source Server Type    : PostgreSQL
 Source Server Version : 120001 (120001)
 Source Host           : 10.0.0.42:54321
 Source Catalog        : school_oms_dev
 Source Schema         : public

 Target Server Type    : PostgreSQL
 Target Server Version : 120001 (120001)
 File Encoding         : 65001

 Date: 04/06/2024 13:43:28
*/


-- ----------------------------
-- Table structure for lfun_permission_menu
-- ----------------------------
DROP TABLE IF EXISTS "public"."lfun_permission_menu";
CREATE TABLE "public"."lfun_permission_menu" (
  "id" int4 NOT NULL DEFAULT nextval('lfun_permission_menu_id_seq'::regclass),
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
  "sort_order" int4
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
COMMENT ON TABLE "public"."lfun_permission_menu" IS '菜单权限表';

-- ----------------------------
-- Records of lfun_permission_menu
-- ----------------------------
INSERT INTO "public"."lfun_permission_menu" VALUES (6, '课程管理', '/course', '', 'menu', '', '', '3', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'course', 0);
INSERT INTO "public"."lfun_permission_menu" VALUES (12, '职高配置管理', '', '', 'root', '', '', '0', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'config', 0);
INSERT INTO "public"."lfun_permission_menu" VALUES (2, '园所信息管理（学校）', '/school', '', 'menu', '', '', '0', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'school', 0);
INSERT INTO "public"."lfun_permission_menu" VALUES (15, '新教职工入职', '/onboarding', '', 'menu', '', '', '14', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'onboarding', 0);
INSERT INTO "public"."lfun_permission_menu" VALUES (5, '班级管理', '/class', '', 'menu', '', '', '3', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'class', 0);
INSERT INTO "public"."lfun_permission_menu" VALUES (11, '职高信息管理（学校）', '/school', '', 'menu', '', '', '0', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'school', 0);
INSERT INTO "public"."lfun_permission_menu" VALUES (8, '中小学信息管理（学校）', '/school', '', 'menu', '', '', '0', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'school', 0);
INSERT INTO "public"."lfun_permission_menu" VALUES (14, '新教职工管理', '', '', 'root', '', '', '0', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'onboarding', 0);
INSERT INTO "public"."lfun_permission_menu" VALUES (4, '年级管理', '/grade', '', 'menu', '', '', '3', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'grade', 0);
INSERT INTO "public"."lfun_permission_menu" VALUES (17, '在职教职工管理', '', '', 'root', '', '', '0', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'employed', 0);
INSERT INTO "public"."lfun_permission_menu" VALUES (1, '园所信息管理（规划）', '/planning', '', 'menu', '', '', '0', 1, 0, 0, '2024-06-04 10:43:11.169988', '2024-06-04 10:43:11.169988', 'f', 'planning', 0);
INSERT INTO "public"."lfun_permission_menu" VALUES (7, '中小学信息管理（规划）', '/planning', '', 'menu', '', '', '0', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'planning', 0);
INSERT INTO "public"."lfun_permission_menu" VALUES (10, '职高信息管理（规划）', '/planning', '', 'menu', '', '', '0', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'planning', 0);
INSERT INTO "public"."lfun_permission_menu" VALUES (16, '新教职工审批', '/onboarding/approve', '', 'menu', '', '', '14', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'approve', 0);
INSERT INTO "public"."lfun_permission_menu" VALUES (13, '专业管理', '/major', '', 'menu', '', '', '12', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'major', 0);
INSERT INTO "public"."lfun_permission_menu" VALUES (3, '园所配置管理', '', '', 'root', '', '', '0', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'config', 0);
INSERT INTO "public"."lfun_permission_menu" VALUES (9, '中小学配置管理', '', '', 'root', '', '', '0', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'config', 0);
INSERT INTO "public"."lfun_permission_menu" VALUES (21, '年级管理', '/grade', '', 'menu', '', '', '12', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'grade', 0);
INSERT INTO "public"."lfun_permission_menu" VALUES (18, '年级管理', '/grade', '', 'menu', '', '', '9', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'grade', 0);
INSERT INTO "public"."lfun_permission_menu" VALUES (19, '班级管理', '/class', '', 'menu', '', '', '9', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'class', 0);
INSERT INTO "public"."lfun_permission_menu" VALUES (20, '课程管理', '/course', '', 'menu', '', '', '9', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'course', 0);
INSERT INTO "public"."lfun_permission_menu" VALUES (22, '班级管理', '/class', '', 'menu', '', '', '12', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'class', 0);
INSERT INTO "public"."lfun_permission_menu" VALUES (23, '课程管理', '/course', '', 'menu', '', '', '12', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'course', 0);
INSERT INTO "public"."lfun_permission_menu" VALUES (24, '在职教职工管理', '/employed', '', 'menu', '', '', '17', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'employed', 0);
INSERT INTO "public"."lfun_permission_menu" VALUES (25, '新教职工审批', '/employed/approve', '', 'menu', '', '', '17', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'employedapprove', 0);
INSERT INTO "public"."lfun_permission_menu" VALUES (26, '变动管理', '/employed/workchange', '', 'menu', '', '', '17', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'employedworkchange', 0);
INSERT INTO "public"."lfun_permission_menu" VALUES (27, '借入信息管理', '/employed/borrowin', '', 'menu', '', '', '17', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'employedworkborrowin', 0);
INSERT INTO "public"."lfun_permission_menu" VALUES (28, '借出信息管理', '/employed/borrowout', '', 'menu', '', '', '17', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'employedworkborrowout', 0);
INSERT INTO "public"."lfun_permission_menu" VALUES (29, '调入信息管理', '/employed/transferin', '', 'menu', '', '', '17', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'employedworktransferin', 0);
INSERT INTO "public"."lfun_permission_menu" VALUES (30, '调出信息管理', '/employed/transferout', '', 'menu', '', '', '17', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'employedworktransferout', 0);
INSERT INTO "public"."lfun_permission_menu" VALUES (31, '非在职教职工管理', '', '', 'root', '', '', '0', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'nonemployed', 0);
INSERT INTO "public"."lfun_permission_menu" VALUES (32, '系统管理', '', '', 'root', '', '', '0', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'trchsys', 0);
INSERT INTO "public"."lfun_permission_menu" VALUES (33, '系统配置', '/trchsys/config', '', 'menu', '', '', '32', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'trchsysconfig', 0);
INSERT INTO "public"."lfun_permission_menu" VALUES (34, '任务管理', '/trchsys/task', '', 'menu', '', '', '32', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'trchsystask', 0);
INSERT INTO "public"."lfun_permission_menu" VALUES (35, '新学生信息管理', '', '', 'root', '', '', '0', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'newstudent', 0);
INSERT INTO "public"."lfun_permission_menu" VALUES (36, '在校学生信息管理', '', '', 'root', '', '', '0', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'instudent', 0);
INSERT INTO "public"."lfun_permission_menu" VALUES (37, '毕业生信息管理', '/graduation', '', 'menu', '', '', '0', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'graduation', 0);
INSERT INTO "public"."lfun_permission_menu" VALUES (38, '新生入学管理', '/newstudent', '', 'menu', '', '', '35', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'newstudent', 0);
INSERT INTO "public"."lfun_permission_menu" VALUES (39, '分班管理', '/newstudent/classroom', '', 'menu', '', '', '35', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'newstudent_classroom', 0);
INSERT INTO "public"."lfun_permission_menu" VALUES (40, '届别管理', '/newstudent/academia', '', 'menu', '', '', '35', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'newstudent_academia', 0);
INSERT INTO "public"."lfun_permission_menu" VALUES (41, '在校学生信息管理', '/instudent', '', 'menu', '', '', '36', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'instudent', 0);
INSERT INTO "public"."lfun_permission_menu" VALUES (42, '转学管理', '/transfer', '', 'menu', '', '', '36', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'instudent_transfer', 0);
INSERT INTO "public"."lfun_permission_menu" VALUES (43, '转入信息管理', '/transfer/checkin', '', 'menu', '', '', '36', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'instudent_checkin', 0);
INSERT INTO "public"."lfun_permission_menu" VALUES (44, '转出信息管理', '/transfer/checkout', '', 'menu', '', '', '36', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'instudent_checkout', 0);
INSERT INTO "public"."lfun_permission_menu" VALUES (45, '异动管理', '/transfer/innerTransfer', '', 'menu', '', '', '36', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'instudent_innerTransfer', 0);
INSERT INTO "public"."lfun_permission_menu" VALUES (46, '临时就读', '/transfer/emporaryBorrowing', '', 'menu', '', '', '36', 1, 0, 0, '2024-06-04 10:43:11.170994', '2024-06-04 10:43:11.170994', 'f', 'instudent_emporaryBorrowing', 0);

-- ----------------------------
-- Primary Key structure for table lfun_permission_menu
-- ----------------------------
ALTER TABLE "public"."lfun_permission_menu" ADD CONSTRAINT "lfun_permission_menu_pkey" PRIMARY KEY ("id");
