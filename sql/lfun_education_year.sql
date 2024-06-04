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

 Date: 04/06/2024 15:18:55
*/
CREATE SEQUENCE lfun_education_year_id_seq
START WITH 1
INCREMENT BY 1
NO MINVALUE
NO MAXVALUE
CACHE 1;

-- ----------------------------
-- Table structure for lfun_education_year
-- ----------------------------
DROP TABLE IF EXISTS "public"."lfun_education_year";
CREATE TABLE "public"."lfun_education_year" (
  "id" int4 NOT NULL DEFAULT nextval('lfun_education_year_id_seq'::regclass),
  "school_type" varchar(24) COLLATE "pg_catalog"."default",
  "education_year" int4 NOT NULL,
  "city" varchar(64) COLLATE "pg_catalog"."default",
  "district" varchar(64) COLLATE "pg_catalog"."default",
  "is_deleted" bool NOT NULL,
  "created_at" timestamp(6)
)
;
COMMENT ON COLUMN "public"."lfun_education_year"."id" IS '年级ID';
COMMENT ON COLUMN "public"."lfun_education_year"."school_type" IS '学校类型（小学/初中）';
COMMENT ON COLUMN "public"."lfun_education_year"."education_year" IS '学制年限（如：6年/3年）';
COMMENT ON COLUMN "public"."lfun_education_year"."city" IS '城市';
COMMENT ON COLUMN "public"."lfun_education_year"."is_deleted" IS '删除态';
COMMENT ON COLUMN "public"."lfun_education_year"."created_at" IS '创建时间';
COMMENT ON TABLE "public"."lfun_education_year" IS '学制表';

-- ----------------------------
-- Records of lfun_education_year
-- ----------------------------
INSERT INTO "public"."lfun_education_year" VALUES (2, '小学', 6, '沈阳市', NULL, 'f', '2024-06-04 15:17:52');
INSERT INTO "public"."lfun_education_year" VALUES (4, '初中', 3, '沈阳市', NULL, 'f', '2024-06-04 15:18:23');

-- ----------------------------
-- Primary Key structure for table lfun_education_year
-- ----------------------------
ALTER TABLE "public"."lfun_education_year" ADD CONSTRAINT "lfun_education_year_pkey" PRIMARY KEY ("id");
