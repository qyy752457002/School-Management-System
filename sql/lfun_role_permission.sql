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

 Date: 04/06/2024 13:43:35
*/


-- ----------------------------
-- Table structure for lfun_role_permission
-- ----------------------------
DROP TABLE IF EXISTS "public"."lfun_role_permission";
CREATE TABLE "public"."lfun_role_permission" (
  "id" int4 NOT NULL DEFAULT nextval('lfun_role_permission_id_seq'::regclass),
  "role_id" int4,
  "menu_id" int4,
  "sort_order" int4,
  "created_uid" int4,
  "updated_uid" int4,
  "created_at" timestamp(6),
  "updated_at" timestamp(6),
  "is_deleted" bool NOT NULL,
  "remark" varchar(64) COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "public"."lfun_role_permission"."id" IS '班级ID';
COMMENT ON COLUMN "public"."lfun_role_permission"."role_id" IS '角色ID';
COMMENT ON COLUMN "public"."lfun_role_permission"."menu_id" IS '菜单ID';
COMMENT ON COLUMN "public"."lfun_role_permission"."sort_order" IS '排序从小到大';
COMMENT ON COLUMN "public"."lfun_role_permission"."created_uid" IS '创建人';
COMMENT ON COLUMN "public"."lfun_role_permission"."updated_uid" IS '操作人';
COMMENT ON COLUMN "public"."lfun_role_permission"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."lfun_role_permission"."updated_at" IS '更新时间';
COMMENT ON COLUMN "public"."lfun_role_permission"."is_deleted" IS '删除态';
COMMENT ON COLUMN "public"."lfun_role_permission"."remark" IS '备注';
COMMENT ON TABLE "public"."lfun_role_permission" IS '角色权限表';

-- ----------------------------
-- Records of lfun_role_permission
-- ----------------------------
INSERT INTO "public"."lfun_role_permission" VALUES (1, 1, 1, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (2, 1, 2, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (3, 1, 3, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (4, 1, 4, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (5, 1, 5, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (6, 1, 6, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 't', '');
INSERT INTO "public"."lfun_role_permission" VALUES (7, 4, 2, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (8, 4, 3, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (9, 4, 4, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (10, 4, 5, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (11, 4, 6, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (12, 5, 2, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (13, 5, 3, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (14, 5, 4, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (15, 5, 5, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (16, 5, 6, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (21, 2, 7, 0, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (17, 2, 8, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (18, 2, 9, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (19, 2, 18, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (20, 2, 19, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (22, 7, 8, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (23, 7, 9, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (24, 7, 18, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (25, 7, 19, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (26, 7, 20, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (27, 6, 8, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (28, 6, 9, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (29, 6, 18, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (30, 6, 19, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (31, 6, 20, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (32, 3, 10, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (33, 3, 11, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (34, 3, 12, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (35, 3, 21, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (36, 3, 22, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (37, 8, 10, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (38, 8, 11, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (39, 8, 12, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (40, 8, 21, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (41, 8, 22, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (42, 9, 11, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (43, 9, 12, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (44, 9, 21, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (45, 9, 22, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (46, 9, 23, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (47, 9, 13, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (48, 10, 14, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (49, 10, 15, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (50, 10, 16, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (51, 10, 17, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (52, 10, 24, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (53, 10, 25, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (54, 10, 26, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (55, 10, 27, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (56, 10, 28, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (57, 10, 29, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (58, 10, 30, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (59, 10, 31, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (60, 10, 32, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (61, 10, 33, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (62, 10, 34, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (63, 11, 35, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (64, 11, 36, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (65, 11, 37, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (66, 11, 38, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (67, 11, 39, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (68, 11, 40, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (69, 11, 41, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (70, 11, 42, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (71, 11, 43, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (72, 11, 44, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (73, 11, 45, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (74, 11, 46, 1, 0, 0, '2024-06-04 10:45:29', '2024-06-04 10:45:33', 'f', '');

-- ----------------------------
-- Primary Key structure for table lfun_role_permission
-- ----------------------------
ALTER TABLE "public"."lfun_role_permission" ADD CONSTRAINT "lfun_role_permission_pkey" PRIMARY KEY ("id");
