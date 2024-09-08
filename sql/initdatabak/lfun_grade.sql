/*
 Navicat PostgreSQL Dump SQL

 Source Server         : 10.0.0.42
 Source Server Type    : PostgreSQL
 Source Server Version : 120001 (120001)
 Source Host           : 10.0.0.42:54321
 Source Catalog        : school_oms_dev
 Source Schema         : public

 Target Server Type    : PostgreSQL
 Target Server Version : 120001 (120001)
 File Encoding         : 65001

 Date: 08/09/2024 13:24:17
*/


-- ----------------------------
-- Table structure for lfun_grade
-- ----------------------------
DROP TABLE IF EXISTS "public"."lfun_grade";
CREATE TABLE "public"."lfun_grade" (
  "id" int8 NOT NULL DEFAULT nextval('lfun_grade_id_seq'::regclass),
  "school_id" int8,
  "grade_no" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "grade_name" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "grade_alias" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "description" varchar(64) COLLATE "pg_catalog"."default",
  "is_deleted" bool NOT NULL,
  "created_at" timestamp(6),
  "city" varchar(64) COLLATE "pg_catalog"."default",
  "district" varchar(64) COLLATE "pg_catalog"."default",
  "sort_number" int4,
  "school_type" varchar(64) COLLATE "pg_catalog"."default",
  "course_no" varchar(24) COLLATE "pg_catalog"."default",
  "course_no_lv2" varchar(24) COLLATE "pg_catalog"."default",
  "course_no_lv3" varchar(24) COLLATE "pg_catalog"."default",
  "grade_type" varchar(64) COLLATE "pg_catalog"."default",
  "class_number" int4 NOT NULL,
  "grade_index" int4,
  "section" varchar(64) COLLATE "pg_catalog"."default",
  "major" varchar(64) COLLATE "pg_catalog"."default",
  "study_section" varchar(64) COLLATE "pg_catalog"."default",
  "is_enabled" bool,
  "is_graduation_grade" bool
)
;
COMMENT ON COLUMN "public"."lfun_grade"."id" IS '年级ID';
COMMENT ON COLUMN "public"."lfun_grade"."school_id" IS '学校ID';
COMMENT ON COLUMN "public"."lfun_grade"."grade_no" IS '年级编号';
COMMENT ON COLUMN "public"."lfun_grade"."grade_name" IS '年级名称/班级名称';
COMMENT ON COLUMN "public"."lfun_grade"."grade_alias" IS '年级别名';
COMMENT ON COLUMN "public"."lfun_grade"."description" IS '简介';
COMMENT ON COLUMN "public"."lfun_grade"."is_deleted" IS '删除态';
COMMENT ON COLUMN "public"."lfun_grade"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."lfun_grade"."city" IS '城市 编码';
COMMENT ON COLUMN "public"."lfun_grade"."district" IS '区 编码';
COMMENT ON COLUMN "public"."lfun_grade"."sort_number" IS '排序序号';
COMMENT ON COLUMN "public"."lfun_grade"."school_type" IS '教育阶段/学校类别 例如 小学 初中';
COMMENT ON COLUMN "public"."lfun_grade"."course_no" IS '学科编码/中职用枚举';
COMMENT ON COLUMN "public"."lfun_grade"."course_no_lv2" IS '学科编码2';
COMMENT ON COLUMN "public"."lfun_grade"."course_no_lv3" IS '学科编码3';
COMMENT ON COLUMN "public"."lfun_grade"."grade_type" IS '年级类型/班级类型 例如 一年级 二年级 三年级,枚举grade';
COMMENT ON COLUMN "public"."lfun_grade"."class_number" IS '本年级班级数量';
COMMENT ON COLUMN "public"."lfun_grade"."grade_index" IS '年级序号,用来判断怎么选择';
COMMENT ON COLUMN "public"."lfun_grade"."section" IS '学段';
COMMENT ON COLUMN "public"."lfun_grade"."major" IS '专业';
COMMENT ON COLUMN "public"."lfun_grade"."study_section" IS '教育阶段';
COMMENT ON COLUMN "public"."lfun_grade"."is_enabled" IS '是否选择';
COMMENT ON COLUMN "public"."lfun_grade"."is_graduation_grade" IS '是否毕业年级';
COMMENT ON TABLE "public"."lfun_grade" IS '年级表模型';

-- ----------------------------
-- Records of lfun_grade
-- ----------------------------
INSERT INTO "public"."lfun_grade" VALUES (1463469243350405122, 0, '11', '幼儿园小班', '排序2', NULL, 'f', '2021-11-24 19:27:12', NULL, '0', 1, '义务', NULL, NULL, NULL, '11', 0, 2, NULL, NULL, '幼儿园', 'f', 'f');
INSERT INTO "public"."lfun_grade" VALUES (1463474614114734082, 0, '12', '幼儿园中班', '排序3', NULL, 'f', '2021-11-24 19:48:32', NULL, '0', 2, '义务', NULL, NULL, NULL, '12', 0, 3, NULL, NULL, '幼儿园', 'f', 'f');
INSERT INTO "public"."lfun_grade" VALUES (1471766925709971458, 0, '23', '幼儿园大班', '9999', NULL, 'f', '2021-12-17 16:59:13', NULL, '0', 9, '义务', NULL, NULL, NULL, '23', 0, 4, NULL, NULL, '幼儿园', 'f', 'f');
INSERT INTO "public"."lfun_grade" VALUES (1473479668888522754, 0, '31', '小学一年级', '9999', NULL, 'f', '2021-12-22 10:25:03', NULL, '0', 10, '高中', NULL, NULL, NULL, '31', 0, 5, NULL, NULL, '小学', 'f', 'f');
INSERT INTO "public"."lfun_grade" VALUES (1473479745426182146, 0, '32', '小学二年级', '9999', NULL, 'f', '2021-12-22 10:25:21', NULL, '0', 11, '高中', NULL, NULL, NULL, '32', 0, 6, NULL, NULL, '小学', 'f', 'f');
INSERT INTO "public"."lfun_grade" VALUES (1473479887789248514, 0, '33', '小学三年级', '9999', NULL, 'f', '2021-12-22 10:25:55', NULL, '0', 12, '高中', NULL, NULL, NULL, '33', 0, 7, NULL, NULL, '小学', 'f', 'f');
INSERT INTO "public"."lfun_grade" VALUES (1476444303656820738, 0, '2015', '小学四年级', '9999', NULL, 'f', '2021-12-30 14:45:27', NULL, '0', 0, '中职', NULL, NULL, NULL, '2015', 0, 8, NULL, NULL, '小学', 'f', 'f');
INSERT INTO "public"."lfun_grade" VALUES (1476444416802365442, 0, '2016', '小学五年级', '9999', NULL, 'f', '2021-12-30 14:45:54', NULL, '0', 0, '中职', NULL, NULL, NULL, '2016', 0, 9, NULL, NULL, '小学', 'f', 'f');
INSERT INTO "public"."lfun_grade" VALUES (1504647486988140546, 0, '2018', '初中一年级', '9999', NULL, 'f', '2022-03-18 10:34:50', NULL, '0', 0, '中职', NULL, NULL, NULL, '2018', 0, 11, NULL, NULL, '初中', 'f', 'f');
INSERT INTO "public"."lfun_grade" VALUES (1543112069020250114, 0, '2019', '初中二年级', '9999', NULL, 'f', '2022-07-02 13:59:21.548000', NULL, '0', 0, '中职', NULL, NULL, NULL, '2019', 0, 12, NULL, NULL, '初中', 'f', 'f');
INSERT INTO "public"."lfun_grade" VALUES (1543112383504969729, 0, '2021', '高中一年级', '9999', NULL, 'f', '2022-07-02 14:00:36.527000', NULL, '0', 0, '中职', NULL, NULL, NULL, '2021', 0, 14, NULL, NULL, '高中', 'f', 'f');
INSERT INTO "public"."lfun_grade" VALUES (1543112383551107074, 0, '2022', '高中二年级', '9999', NULL, 'f', '2022-07-02 14:00:36.538000', NULL, '0', 0, '中职', NULL, NULL, NULL, '2022', 0, 15, NULL, NULL, '高中', 'f', 'f');
INSERT INTO "public"."lfun_grade" VALUES (1471766111234916354, 0, '15', '幼儿园托班', '排序100010022442', NULL, 'f', '2021-12-17 16:55:59', NULL, '0', 5, '义务', NULL, NULL, NULL, '15', 0, 1, NULL, NULL, '幼儿园', 'f', 'f');
INSERT INTO "public"."lfun_grade" VALUES (1476444524818276353, 0, '2017', '小学六年级', '9999', NULL, 'f', '2021-12-30 14:46:20', NULL, '0', 0, '中职', NULL, NULL, NULL, '2017', 0, 10, NULL, NULL, '小学', 'f', 'f');
INSERT INTO "public"."lfun_grade" VALUES (1543112370674593794, 0, '2020', '初中三年级', '9999', NULL, 'f', '2022-07-02 14:00:33.468000', NULL, '0', 0, '中职', NULL, NULL, NULL, '2020', 0, 13, NULL, NULL, '初中', 'f', 'f');
INSERT INTO "public"."lfun_grade" VALUES (1543194815873708033, 0, '2023', '高中三年级', '9999', NULL, 'f', '2022-07-02 19:28:09.935000', NULL, '0', 0, '中职', NULL, NULL, NULL, '2023', 0, 16, NULL, NULL, '高中', 'f', 'f');

-- ----------------------------
-- Primary Key structure for table lfun_grade
-- ----------------------------
ALTER TABLE "public"."lfun_grade" ADD CONSTRAINT "lfun_grade_pkey" PRIMARY KEY ("id");
