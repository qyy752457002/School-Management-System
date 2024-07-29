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

 Date: 25/07/2024 17:12:35
*/


-- ----------------------------
-- Table structure for lfun_role
-- ----------------------------
DROP TABLE IF EXISTS "public"."lfun_role";
CREATE TABLE "public"."lfun_role" (
  "id" int8 NOT NULL DEFAULT nextval('lfun_role_id_seq'::regclass),
  "system_type" varchar(64) COLLATE "pg_catalog"."default",
  "edu_type" varchar(64) COLLATE "pg_catalog"."default",
  "unit_type" varchar(64) COLLATE "pg_catalog"."default",
  "app_name" varchar(64) COLLATE "pg_catalog"."default",
  "remark" varchar(64) COLLATE "pg_catalog"."default",
  "unit_id" int8,
  "school_id" int8,
  "county_id" int8,
  "created_uid" int4,
  "updated_uid" int4,
  "created_at" timestamp(6),
  "updated_at" timestamp(6),
  "is_deleted" bool NOT NULL
)
;
COMMENT ON COLUMN "public"."lfun_role"."id" IS '角色ID';
COMMENT ON COLUMN "public"."lfun_role"."system_type" IS '系统类型';
COMMENT ON COLUMN "public"."lfun_role"."edu_type" IS '教育类型';
COMMENT ON COLUMN "public"."lfun_role"."unit_type" IS '单位类型';
COMMENT ON COLUMN "public"."lfun_role"."app_name" IS '系统名称';
COMMENT ON COLUMN "public"."lfun_role"."remark" IS '备注';
COMMENT ON COLUMN "public"."lfun_role"."unit_id" IS '单位ID';
COMMENT ON COLUMN "public"."lfun_role"."school_id" IS '学校id';
COMMENT ON COLUMN "public"."lfun_role"."county_id" IS '区id';
COMMENT ON COLUMN "public"."lfun_role"."created_uid" IS '创建人';
COMMENT ON COLUMN "public"."lfun_role"."updated_uid" IS '操作人';
COMMENT ON COLUMN "public"."lfun_role"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."lfun_role"."updated_at" IS '更新时间';
COMMENT ON COLUMN "public"."lfun_role"."is_deleted" IS '删除态';
COMMENT ON TABLE "public"."lfun_role" IS '角色表';

-- ----------------------------
-- Records of lfun_role
-- ----------------------------
INSERT INTO "public"."lfun_role" VALUES (6, 'unit', 'k12', 'county', '中小学信息管理系统', NULL, 0, 0, 0, 1, 1, '2024-06-04 10:43:11.182057', '2024-06-04 10:43:11.182057', 'f');
INSERT INTO "public"."lfun_role" VALUES (2, 'unit', 'k12', 'city', '中小学信息管理系统', NULL, 0, 0, 0, 1, 1, '2024-06-04 10:43:11.182057', '2024-06-04 10:43:11.182057', 'f');
INSERT INTO "public"."lfun_role" VALUES (5, 'unit', 'kg', 'county', '园所信息管理系统', NULL, 0, 0, 0, 1, 1, '2024-06-04 10:43:11.182057', '2024-06-04 10:43:11.182057', 'f');
INSERT INTO "public"."lfun_role" VALUES (11, 'student', '', '', '学生信息管理系统', NULL, 0, 0, 0, 1, 1, '2024-06-04 10:43:11.182057', '2024-06-04 10:43:11.182057', 'f');
INSERT INTO "public"."lfun_role" VALUES (8, 'unit', 'vocational', 'county', '职高信息管理系统', NULL, 0, 0, 0, 1, 1, '2024-06-04 10:43:11.182057', '2024-06-04 10:43:11.182057', 'f');
INSERT INTO "public"."lfun_role" VALUES (4, 'unit', 'kg', 'school', '园所信息管理系统', NULL, 0, 0, 0, 1, 1, '2024-06-04 10:43:11.182057', '2024-06-04 10:43:11.182057', 'f');
INSERT INTO "public"."lfun_role" VALUES (1, 'unit', 'kg', 'city', '园所信息管理系统', NULL, 0, 0, 0, 1, 1, '2024-06-04 10:43:11.182057', '2024-06-04 10:43:11.182057', 'f');
INSERT INTO "public"."lfun_role" VALUES (7, 'unit', 'k12', 'school', '中小学信息管理系统', NULL, 0, 0, 0, 1, 1, '2024-06-04 10:43:11.182057', '2024-06-04 10:43:11.182057', 'f');
INSERT INTO "public"."lfun_role" VALUES (10, 'teacher', '', '', '教职工信息管理系统', NULL, 0, 0, 0, 1, 1, '2024-06-04 10:43:11.182057', '2024-06-04 10:43:11.182057', 'f');
INSERT INTO "public"."lfun_role" VALUES (3, 'unit', 'vocational', 'city', '职高信息管理系统', NULL, 0, 0, 0, 1, 1, '2024-06-04 10:43:11.182057', '2024-06-04 10:43:11.182057', 'f');
INSERT INTO "public"."lfun_role" VALUES (9, 'unit', 'vocational', 'school', '职高信息管理系统', NULL, 0, 0, 0, 1, 1, '2024-06-04 10:43:11.182057', '2024-06-04 10:43:11.182057', 'f');
INSERT INTO "public"."lfun_role" VALUES (14, 'unit', 'institute', 'county', '机构信息管理系统', NULL, 0, 0, 0, 1, 1, '2024-06-04 10:43:11.182057', '2024-06-04 10:43:11.182057', 'f');
INSERT INTO "public"."lfun_role" VALUES (13, 'unit', 'institute', 'city', '机构信息管理系统', NULL, 0, 0, 0, 1, 1, '2024-06-04 10:43:11.182057', '2024-06-04 10:43:11.182057', 'f');
INSERT INTO "public"."lfun_role" VALUES (12, 'unit', 'institute', 'school', '机构信息管理系统', NULL, 0, 0, 0, 1, 1, '2024-06-04 10:43:11.182057', '2024-06-04 10:43:11.182057', 'f');
INSERT INTO "public"."lfun_role" VALUES (15, 'unit', 'institute', 'city', '事业单位系统', NULL, 0, 0, 0, 1, 1, '2024-06-04 10:43:11.182057', '2024-06-04 10:43:11.182057', 'f');
INSERT INTO "public"."lfun_role" VALUES (16, 'unit', 'administration', 'city', '行政单位系统', NULL, 0, 0, 0, 1, 1, '2024-06-04 10:43:11.182057', '2024-06-04 10:43:11.182057', 'f');
INSERT INTO "public"."lfun_role" VALUES (17, 'unit', 'institute', 'school', '事业单位系统', NULL, 0, 0, 0, 1, 1, '2024-06-04 10:43:11.182057', '2024-06-04 10:43:11.182057', 'f');
INSERT INTO "public"."lfun_role" VALUES (18, 'unit', 'institute', 'county', '事业单位系统', NULL, 0, 0, 0, 1, 1, '2024-06-04 10:43:11.182057', '2024-06-04 10:43:11.182057', 'f');
INSERT INTO "public"."lfun_role" VALUES (19, 'unit', 'administration', 'county', '行政单位系统', NULL, 0, 0, 0, 1, 1, '2024-06-04 10:43:11.182057', '2024-06-04 10:43:11.182057', 'f');
INSERT INTO "public"."lfun_role" VALUES (20, 'unit', 'administration', 'school', '行政单位系统', NULL, 0, 0, 0, 1, 1, '2024-06-04 10:43:11.182057', '2024-06-04 10:43:11.182057', 'f');

-- ----------------------------
-- Primary Key structure for table lfun_role
-- ----------------------------
ALTER TABLE "public"."lfun_role" ADD CONSTRAINT "lfun_role_pkey" PRIMARY KEY ("id");
