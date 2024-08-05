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

 Date: 01/08/2024 18:05:43
*/


-- ----------------------------
-- Table structure for lfun_role_permission
-- ----------------------------
DROP TABLE IF EXISTS "public"."lfun_role_permission";
CREATE TABLE "public"."lfun_role_permission" (
  "id" int8 NOT NULL DEFAULT nextval('lfun_role_permission_id_seq'::regclass),
  "role_id" int8,
  "menu_id" int8,
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
INSERT INTO "public"."lfun_role_permission" VALUES (1, 1, 1, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (2, 1, 2, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (3, 1, 3, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (4, 1, 4, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (5, 1, 5, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (6, 1, 6, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (7, 4, 2, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (9, 4, 4, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (10, 4, 5, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (12, 5, 2, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (13, 5, 3, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (14, 5, 4, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (15, 5, 5, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (21, 2, 7, 0, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (17, 2, 8, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (18, 2, 9, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (19, 2, 18, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (20, 2, 19, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (22, 7, 8, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (24, 7, 18, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (25, 7, 19, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (26, 7, 20, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (27, 6, 8, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (28, 6, 9, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (29, 6, 18, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (30, 6, 19, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (31, 6, 20, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (32, 3, 10, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (33, 3, 11, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (34, 3, 12, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (35, 3, 21, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (36, 3, 22, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (37, 8, 10, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (38, 8, 11, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (39, 8, 12, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (40, 8, 21, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (41, 8, 22, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (42, 9, 11, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (44, 9, 21, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (45, 9, 22, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (46, 9, 23, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (47, 9, 13, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (48, 10, 14, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (49, 10, 15, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (50, 10, 16, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (51, 10, 17, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (52, 10, 24, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (53, 10, 25, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (54, 10, 26, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (55, 10, 27, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (56, 10, 28, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (57, 10, 29, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (58, 10, 30, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (59, 10, 31, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (60, 10, 32, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (61, 10, 33, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (62, 10, 34, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (63, 11, 35, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (64, 11, 36, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (65, 11, 37, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (66, 11, 38, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (67, 11, 39, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (68, 11, 40, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (69, 11, 41, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (73, 11, 45, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (74, 11, 46, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (76, 4, 47, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (79, 7, 48, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (83, 9, 49, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (84, 6, 50, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (85, 7, 50, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (86, 9, 51, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (88, 10, 53, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (87, 10, 52, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (89, 10, 54, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (90, 1, 55, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (92, 5, 55, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (93, 5, 56, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (94, 4, 56, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (95, 1, 56, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (96, 5, 57, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (98, 1, 57, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (99, 5, 58, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (101, 1, 58, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (102, 5, 59, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (104, 1, 59, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (105, 5, 60, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (106, 4, 60, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (107, 1, 60, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (108, 5, 61, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (109, 4, 61, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (110, 1, 61, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (111, 5, 62, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (112, 4, 62, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (113, 1, 62, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (114, 6, 63, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (116, 2, 63, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (117, 6, 64, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (119, 2, 64, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (120, 6, 65, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (122, 2, 65, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (123, 6, 66, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (125, 2, 66, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (126, 6, 67, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (127, 7, 67, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (128, 2, 67, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (129, 6, 68, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (130, 7, 68, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (131, 2, 68, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (132, 6, 69, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (133, 7, 69, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (134, 2, 69, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (135, 6, 70, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (136, 7, 70, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (137, 2, 70, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (139, 8, 71, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (140, 3, 71, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (142, 8, 72, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (143, 3, 72, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (145, 8, 73, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (146, 3, 73, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (148, 8, 74, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (149, 3, 74, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (150, 9, 75, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (151, 8, 75, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (152, 3, 75, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (153, 9, 76, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (154, 8, 76, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (155, 3, 76, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (156, 9, 77, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (157, 8, 77, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (158, 3, 77, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (159, 9, 78, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (160, 8, 78, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (161, 3, 78, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (77, 5, 47, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (75, 1, 47, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (8, 4, 3, 2, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (80, 6, 48, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (78, 2, 48, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (23, 7, 9, 2, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (82, 8, 49, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (81, 3, 49, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (43, 9, 12, 2, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (228, 12, 79, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (229, 13, 79, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (230, 14, 79, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (231, 12, 80, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (232, 13, 80, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (233, 14, 80, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (225, 12, 47, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (206, 9, 79, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (205, 8, 79, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (204, 3, 79, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (185, 7, 79, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (184, 6, 79, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (183, 2, 79, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (164, 5, 79, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (163, 4, 79, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (162, 1, 79, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (209, 9, 80, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (208, 8, 80, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (207, 3, 80, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (188, 7, 80, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (187, 6, 80, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (186, 2, 80, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (167, 5, 80, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (166, 4, 80, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (165, 1, 80, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (227, 14, 47, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (226, 13, 47, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (249, 2, 20, 1, 0, 0, '2024-07-16 11:07:09.000000', '2024-07-16 11:07:13.000000', 'f', NULL);
INSERT INTO "public"."lfun_role_permission" VALUES (250, 2, 50, 1, 0, 0, '2024-07-25 11:28:50.000000', '2024-07-18 11:28:53.000000', 'f', NULL);
INSERT INTO "public"."lfun_role_permission" VALUES (16, 5, 6, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (11, 4, 6, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (251, 15, 81, 1, 0, 0, '2024-07-25 11:28:50.000000', '2024-07-18 11:28:53.000000', 'f', NULL);
INSERT INTO "public"."lfun_role_permission" VALUES (252, 15, 86, 1, 0, 0, '2024-07-25 11:28:50.000000', '2024-07-18 11:28:53.000000', 'f', NULL);
INSERT INTO "public"."lfun_role_permission" VALUES (253, 15, 87, 1, 0, 0, '2024-07-25 11:28:50.000000', '2024-07-18 11:28:53.000000', 'f', NULL);
INSERT INTO "public"."lfun_role_permission" VALUES (254, 15, 88, 1, 0, 0, '2024-07-25 11:28:50.000000', '2024-07-18 11:28:53.000000', 'f', NULL);
INSERT INTO "public"."lfun_role_permission" VALUES (255, 15, 89, 1, 0, 0, '2024-07-25 11:28:50.000000', '2024-07-18 11:28:53.000000', 'f', NULL);
INSERT INTO "public"."lfun_role_permission" VALUES (256, 15, 90, 1, 0, 0, '2024-07-25 11:28:50.000000', '2024-07-18 11:28:53.000000', 'f', NULL);
INSERT INTO "public"."lfun_role_permission" VALUES (257, 16, 82, 1, 0, 0, '2024-07-25 11:28:50.000000', '2024-07-18 11:28:53.000000', 'f', NULL);
INSERT INTO "public"."lfun_role_permission" VALUES (258, 16, 91, 1, 0, 0, '2024-07-25 11:28:50.000000', '2024-07-18 11:28:53.000000', 'f', NULL);
INSERT INTO "public"."lfun_role_permission" VALUES (259, 16, 92, 1, 0, 0, '2024-07-25 11:28:50.000000', '2024-07-18 11:28:53.000000', 'f', NULL);
INSERT INTO "public"."lfun_role_permission" VALUES (260, 16, 93, 1, 0, 0, '2024-07-25 11:28:50.000000', '2024-07-18 11:28:53.000000', 'f', NULL);
INSERT INTO "public"."lfun_role_permission" VALUES (261, 16, 94, 1, 0, 0, '2024-07-25 11:28:50.000000', '2024-07-18 11:28:53.000000', 'f', NULL);
INSERT INTO "public"."lfun_role_permission" VALUES (262, 16, 95, 1, 0, 0, '2024-07-25 11:28:50.000000', '2024-07-18 11:28:53.000000', 'f', NULL);
INSERT INTO "public"."lfun_role_permission" VALUES (168, 1, 81, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (169, 4, 81, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (170, 5, 81, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (171, 1, 82, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (172, 4, 82, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (173, 5, 82, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (174, 1, 83, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (175, 4, 83, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (176, 5, 83, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (177, 1, 84, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (178, 4, 84, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (179, 5, 84, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (180, 1, 85, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (181, 4, 85, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (182, 5, 85, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (189, 2, 81, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (190, 6, 81, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (191, 7, 81, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (192, 2, 82, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (193, 6, 82, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (194, 7, 82, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (195, 2, 83, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (196, 6, 83, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (197, 7, 83, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (198, 2, 84, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (199, 6, 84, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (200, 7, 84, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (201, 2, 85, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (202, 6, 85, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (203, 7, 85, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (210, 3, 81, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (211, 8, 81, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (212, 9, 81, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (213, 3, 82, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (214, 8, 82, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (215, 9, 82, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (216, 3, 83, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (217, 8, 83, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (218, 9, 83, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (219, 3, 84, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (220, 8, 84, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (221, 9, 84, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (222, 3, 85, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (223, 8, 85, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (224, 9, 85, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (234, 12, 81, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (235, 13, 81, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (236, 14, 81, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (237, 12, 82, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (238, 13, 82, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (239, 14, 82, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (240, 12, 83, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (241, 13, 83, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (242, 14, 83, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (243, 12, 84, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (244, 13, 84, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (245, 14, 84, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (246, 12, 85, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (247, 13, 85, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (248, 14, 85, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (263, 17, 81, 1, 0, 0, '2024-07-25 11:28:50.000000', '2024-07-18 11:28:53.000000', 'f', NULL);
INSERT INTO "public"."lfun_role_permission" VALUES (264, 17, 86, 1, 0, 0, '2024-07-25 11:28:50.000000', '2024-07-18 11:28:53.000000', 'f', NULL);
INSERT INTO "public"."lfun_role_permission" VALUES (265, 17, 87, 1, 0, 0, '2024-07-25 11:28:50.000000', '2024-07-18 11:28:53.000000', 'f', NULL);
INSERT INTO "public"."lfun_role_permission" VALUES (266, 17, 88, 1, 0, 0, '2024-07-25 11:28:50.000000', '2024-07-18 11:28:53.000000', 'f', NULL);
INSERT INTO "public"."lfun_role_permission" VALUES (267, 17, 89, 1, 0, 0, '2024-07-25 11:28:50.000000', '2024-07-18 11:28:53.000000', 'f', NULL);
INSERT INTO "public"."lfun_role_permission" VALUES (268, 17, 90, 1, 0, 0, '2024-07-25 11:28:50.000000', '2024-07-18 11:28:53.000000', 'f', NULL);
INSERT INTO "public"."lfun_role_permission" VALUES (269, 18, 81, 1, 0, 0, '2024-07-25 11:28:50.000000', '2024-07-18 11:28:53.000000', 'f', NULL);
INSERT INTO "public"."lfun_role_permission" VALUES (270, 18, 86, 1, 0, 0, '2024-07-25 11:28:50.000000', '2024-07-18 11:28:53.000000', 'f', NULL);
INSERT INTO "public"."lfun_role_permission" VALUES (271, 18, 87, 1, 0, 0, '2024-07-25 11:28:50.000000', '2024-07-18 11:28:53.000000', 'f', NULL);
INSERT INTO "public"."lfun_role_permission" VALUES (272, 18, 88, 1, 0, 0, '2024-07-25 11:28:50.000000', '2024-07-18 11:28:53.000000', 'f', NULL);
INSERT INTO "public"."lfun_role_permission" VALUES (273, 18, 89, 1, 0, 0, '2024-07-25 11:28:50.000000', '2024-07-18 11:28:53.000000', 'f', NULL);
INSERT INTO "public"."lfun_role_permission" VALUES (274, 18, 90, 1, 0, 0, '2024-07-25 11:28:50.000000', '2024-07-18 11:28:53.000000', 'f', NULL);
INSERT INTO "public"."lfun_role_permission" VALUES (275, 19, 95, 1, 0, 0, '2024-07-25 11:28:50.000000', '2024-07-18 11:28:53.000000', 'f', NULL);
INSERT INTO "public"."lfun_role_permission" VALUES (276, 19, 94, 1, 0, 0, '2024-07-25 11:28:50.000000', '2024-07-18 11:28:53.000000', 'f', NULL);
INSERT INTO "public"."lfun_role_permission" VALUES (277, 19, 93, 1, 0, 0, '2024-07-25 11:28:50.000000', '2024-07-18 11:28:53.000000', 'f', NULL);
INSERT INTO "public"."lfun_role_permission" VALUES (278, 19, 92, 1, 0, 0, '2024-07-25 11:28:50.000000', '2024-07-18 11:28:53.000000', 'f', NULL);
INSERT INTO "public"."lfun_role_permission" VALUES (279, 19, 91, 1, 0, 0, '2024-07-25 11:28:50.000000', '2024-07-18 11:28:53.000000', 'f', NULL);
INSERT INTO "public"."lfun_role_permission" VALUES (280, 19, 82, 1, 0, 0, '2024-07-25 11:28:50.000000', '2024-07-18 11:28:53.000000', 'f', NULL);
INSERT INTO "public"."lfun_role_permission" VALUES (281, 20, 95, 1, 0, 0, '2024-07-25 11:28:50.000000', '2024-07-18 11:28:53.000000', 'f', NULL);
INSERT INTO "public"."lfun_role_permission" VALUES (282, 20, 94, 1, 0, 0, '2024-07-25 11:28:50.000000', '2024-07-18 11:28:53.000000', 'f', NULL);
INSERT INTO "public"."lfun_role_permission" VALUES (283, 20, 93, 1, 0, 0, '2024-07-25 11:28:50.000000', '2024-07-18 11:28:53.000000', 'f', NULL);
INSERT INTO "public"."lfun_role_permission" VALUES (284, 20, 92, 1, 0, 0, '2024-07-25 11:28:50.000000', '2024-07-18 11:28:53.000000', 'f', NULL);
INSERT INTO "public"."lfun_role_permission" VALUES (285, 20, 91, 1, 0, 0, '2024-07-25 11:28:50.000000', '2024-07-18 11:28:53.000000', 'f', NULL);
INSERT INTO "public"."lfun_role_permission" VALUES (286, 20, 82, 1, 0, 0, '2024-07-25 11:28:50.000000', '2024-07-18 11:28:53.000000', 'f', NULL);
INSERT INTO "public"."lfun_role_permission" VALUES (288, 2, 96, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (289, 6, 96, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (290, 7, 96, 2, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (291, 7, 7, 0, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (287, 6, 7, 0, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (71, 11, 43, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (70, 11, 42, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');
INSERT INTO "public"."lfun_role_permission" VALUES (72, 11, 44, 1, 0, 0, '2024-06-04 10:45:29.000000', '2024-06-04 10:45:33.000000', 'f', '');

-- ----------------------------
-- Primary Key structure for table lfun_role_permission
-- ----------------------------
ALTER TABLE "public"."lfun_role_permission" ADD CONSTRAINT "lfun_role_permission_pkey" PRIMARY KEY ("id");
