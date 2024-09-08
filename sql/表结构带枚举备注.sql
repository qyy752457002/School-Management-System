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

 Date: 02/09/2024 10:13:24
*/


-- ----------------------------
-- Table structure for lfun_annual_review
-- ----------------------------
DROP TABLE IF EXISTS "public"."lfun_annual_review";
CREATE TABLE "public"."lfun_annual_review" (
  "annual_review_id" int8 NOT NULL DEFAULT nextval('lfun_annual_review_annual_review_id_seq'::regclass),
  "teacher_id" int8 NOT NULL,
  "assessment_year" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "assessment_result" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "assessment_institution_name" varchar(64) COLLATE "pg_catalog"."default",
  "is_deleted" bool NOT NULL,
  "approval_status" varchar(64) COLLATE "pg_catalog"."default" NOT NULL
)
;
COMMENT ON COLUMN "public"."lfun_annual_review"."annual_review_id" IS 'annual_reviewID';
COMMENT ON COLUMN "public"."lfun_annual_review"."teacher_id" IS '教师ID';
COMMENT ON COLUMN "public"."lfun_annual_review"."assessment_year" IS '考核年度';
COMMENT ON COLUMN "public"."lfun_annual_review"."assessment_result" IS '考核结果枚举assessment_result_lv1';
COMMENT ON COLUMN "public"."lfun_annual_review"."assessment_institution_name" IS '考核单位名称';
COMMENT ON COLUMN "public"."lfun_annual_review"."is_deleted" IS '是否删除';
COMMENT ON COLUMN "public"."lfun_annual_review"."approval_status" IS '审批状态';
COMMENT ON TABLE "public"."lfun_annual_review" IS 'annual_review信息表';

-- ----------------------------
-- Table structure for lfun_attach_relations
-- ----------------------------
DROP TABLE IF EXISTS "public"."lfun_attach_relations";
CREATE TABLE "public"."lfun_attach_relations" (
  "id" int4 NOT NULL DEFAULT nextval('lfun_attach_relations_id_seq'::regclass),
  "attach_owner_id" int4,
  "attach_owner" varchar(255) COLLATE "pg_catalog"."default",
  "attach_id" int4,
  "attach_type" varchar(255) COLLATE "pg_catalog"."default",
  "attach_remark" varchar(255) COLLATE "pg_catalog"."default",
  "created_uid" int4,
  "updated_uid" int4,
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL,
  "is_deleted" bool NOT NULL
)
;
COMMENT ON COLUMN "public"."lfun_attach_relations"."id" IS '班级ID';
COMMENT ON COLUMN "public"."lfun_attach_relations"."attach_owner_id" IS '附件主体ID';
COMMENT ON COLUMN "public"."lfun_attach_relations"."attach_owner" IS '附件主体';
COMMENT ON COLUMN "public"."lfun_attach_relations"."attach_id" IS '附件ID';
COMMENT ON COLUMN "public"."lfun_attach_relations"."attach_type" IS '附件类型';
COMMENT ON COLUMN "public"."lfun_attach_relations"."attach_remark" IS '附件备注';
COMMENT ON COLUMN "public"."lfun_attach_relations"."created_uid" IS '创建人';
COMMENT ON COLUMN "public"."lfun_attach_relations"."updated_uid" IS '操作人';
COMMENT ON COLUMN "public"."lfun_attach_relations"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."lfun_attach_relations"."updated_at" IS '更新时间';
COMMENT ON COLUMN "public"."lfun_attach_relations"."is_deleted" IS '删除态';
COMMENT ON TABLE "public"."lfun_attach_relations" IS '附件关系表表模型';

-- ----------------------------
-- Table structure for lfun_attachments
-- ----------------------------
DROP TABLE IF EXISTS "public"."lfun_attachments";
CREATE TABLE "public"."lfun_attachments" (
  "id" int4 NOT NULL DEFAULT nextval('lfun_attachments_id_seq'::regclass),
  "attach_name" varchar(255) COLLATE "pg_catalog"."default",
  "attach_path" varchar(255) COLLATE "pg_catalog"."default",
  "attach_url" varchar(255) COLLATE "pg_catalog"."default",
  "created_uid" int4,
  "updated_uid" int4,
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL,
  "is_deleted" bool NOT NULL
)
;
COMMENT ON COLUMN "public"."lfun_attachments"."id" IS '班级ID';
COMMENT ON COLUMN "public"."lfun_attachments"."attach_name" IS '附件名称';
COMMENT ON COLUMN "public"."lfun_attachments"."attach_path" IS '附件路径';
COMMENT ON COLUMN "public"."lfun_attachments"."attach_url" IS '附件url';
COMMENT ON COLUMN "public"."lfun_attachments"."created_uid" IS '创建人';
COMMENT ON COLUMN "public"."lfun_attachments"."updated_uid" IS '操作人';
COMMENT ON COLUMN "public"."lfun_attachments"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."lfun_attachments"."updated_at" IS '更新时间';
COMMENT ON COLUMN "public"."lfun_attachments"."is_deleted" IS '删除态';
COMMENT ON TABLE "public"."lfun_attachments" IS '附件表模型';

-- ----------------------------
-- Table structure for lfun_campus
-- ----------------------------
DROP TABLE IF EXISTS "public"."lfun_campus";
CREATE TABLE "public"."lfun_campus" (
  "id" int8 NOT NULL DEFAULT nextval('lfun_campus_id_seq'::regclass),
  "school_id" int8,
  "campus_name" varchar(64) COLLATE "pg_catalog"."default",
  "campus_no" varchar(64) COLLATE "pg_catalog"."default",
  "campus_code" varchar(64) COLLATE "pg_catalog"."default",
  "campus_operation_license_number" varchar(64) COLLATE "pg_catalog"."default",
  "block" varchar(64) COLLATE "pg_catalog"."default",
  "borough" varchar(64) COLLATE "pg_catalog"."default",
  "campus_type" varchar(64) COLLATE "pg_catalog"."default",
  "campus_operation_type" varchar(64) COLLATE "pg_catalog"."default",
  "campus_nature" varchar(64) COLLATE "pg_catalog"."default",
  "campus_operation_type_lv2" varchar(64) COLLATE "pg_catalog"."default",
  "campus_operation_type_lv3" varchar(64) COLLATE "pg_catalog"."default",
  "campus_org_type" varchar(64) COLLATE "pg_catalog"."default",
  "campus_level" varchar(64) COLLATE "pg_catalog"."default",
  "status" varchar(64) COLLATE "pg_catalog"."default",
  "kg_level" varchar(64) COLLATE "pg_catalog"."default",
  "campus_short_name" varchar(64) COLLATE "pg_catalog"."default",
  "campus_en_name" varchar(64) COLLATE "pg_catalog"."default",
  "social_credit_code" varchar(64) COLLATE "pg_catalog"."default",
  "founder_type" varchar(64) COLLATE "pg_catalog"."default",
  "founder_type_lv2" varchar(64) COLLATE "pg_catalog"."default",
  "founder_type_lv3" varchar(64) COLLATE "pg_catalog"."default",
  "founder_name" varchar(64) COLLATE "pg_catalog"."default",
  "founder_code" varchar(64) COLLATE "pg_catalog"."default",
  "urban_rural_nature" varchar(64) COLLATE "pg_catalog"."default",
  "campus_org_form" varchar(64) COLLATE "pg_catalog"."default",
  "campus_closure_date" varchar(64) COLLATE "pg_catalog"."default",
  "department_unit_number" varchar(64) COLLATE "pg_catalog"."default",
  "sy_zones" varchar(64) COLLATE "pg_catalog"."default",
  "historical_evolution" varchar(640) COLLATE "pg_catalog"."default",
  "area_code" varchar(64) COLLATE "pg_catalog"."default",
  "campus_leader_name" varchar(64) COLLATE "pg_catalog"."default",
  "campus_leader_position" varchar(64) COLLATE "pg_catalog"."default",
  "location_city" varchar(64) COLLATE "pg_catalog"."default",
  "location_district" varchar(64) COLLATE "pg_catalog"."default",
  "contact_number" varchar(64) COLLATE "pg_catalog"."default",
  "long" varchar(64) COLLATE "pg_catalog"."default",
  "lat" varchar(64) COLLATE "pg_catalog"."default",
  "create_campus_date" varchar(64) COLLATE "pg_catalog"."default",
  "postal_code" varchar(64) COLLATE "pg_catalog"."default",
  "fax_number" varchar(64) COLLATE "pg_catalog"."default",
  "email" varchar(64) COLLATE "pg_catalog"."default",
  "detailed_address" varchar(64) COLLATE "pg_catalog"."default",
  "related_license_upload" varchar(255) COLLATE "pg_catalog"."default",
  "sy_zones_pro" varchar(64) COLLATE "pg_catalog"."default",
  "primary_campus_system" varchar(64) COLLATE "pg_catalog"."default",
  "primary_campus_entry_age" varchar(10) COLLATE "pg_catalog"."default",
  "junior_middle_campus_system" varchar(10) COLLATE "pg_catalog"."default",
  "junior_middle_campus_entry_age" varchar(10) COLLATE "pg_catalog"."default",
  "senior_middle_campus_system" varchar(10) COLLATE "pg_catalog"."default",
  "created_uid" int4,
  "updated_uid" int4,
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL,
  "is_deleted" bool NOT NULL,
  "action_reason" varchar(128) COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "public"."lfun_campus"."id" IS 'ID';
COMMENT ON COLUMN "public"."lfun_campus"."school_id" IS '学校id';
COMMENT ON COLUMN "public"."lfun_campus"."campus_name" IS '校区名称';
COMMENT ON COLUMN "public"."lfun_campus"."campus_no" IS '校区编号';
COMMENT ON COLUMN "public"."lfun_campus"."campus_code" IS '校区标识码';
COMMENT ON COLUMN "public"."lfun_campus"."campus_operation_license_number" IS '办学许可证号';
COMMENT ON COLUMN "public"."lfun_campus"."block" IS '地域管辖区';
COMMENT ON COLUMN "public"."lfun_campus"."borough" IS '行政管辖区';
COMMENT ON COLUMN "public"."lfun_campus"."campus_type" IS '校区类型';
COMMENT ON COLUMN "public"."lfun_campus"."campus_operation_type" IS '办学类型/校区性质';
COMMENT ON COLUMN "public"."lfun_campus"."campus_nature" IS '学校性质';
COMMENT ON COLUMN "public"."lfun_campus"."campus_operation_type_lv2" IS '办学类型二级';
COMMENT ON COLUMN "public"."lfun_campus"."campus_operation_type_lv3" IS '办学类型三级';
COMMENT ON COLUMN "public"."lfun_campus"."campus_org_type" IS '校区办别';
COMMENT ON COLUMN "public"."lfun_campus"."campus_level" IS '校区星级';
COMMENT ON COLUMN "public"."lfun_campus"."status" IS '状态';
COMMENT ON COLUMN "public"."lfun_campus"."kg_level" IS '星级';
COMMENT ON COLUMN "public"."lfun_campus"."campus_short_name" IS '园所简称';
COMMENT ON COLUMN "public"."lfun_campus"."campus_en_name" IS '园所英文名称';
COMMENT ON COLUMN "public"."lfun_campus"."social_credit_code" IS '统一社会信用代码';
COMMENT ON COLUMN "public"."lfun_campus"."founder_type" IS '举办者类型';
COMMENT ON COLUMN "public"."lfun_campus"."founder_type_lv2" IS '举办者类型二级';
COMMENT ON COLUMN "public"."lfun_campus"."founder_type_lv3" IS '举办者类型三级';
COMMENT ON COLUMN "public"."lfun_campus"."founder_name" IS '举办者名称';
COMMENT ON COLUMN "public"."lfun_campus"."founder_code" IS '举办者识别码';
COMMENT ON COLUMN "public"."lfun_campus"."urban_rural_nature" IS '城乡性质';
COMMENT ON COLUMN "public"."lfun_campus"."campus_org_form" IS '办学组织形式';
COMMENT ON COLUMN "public"."lfun_campus"."campus_closure_date" IS '校区关闭日期';
COMMENT ON COLUMN "public"."lfun_campus"."department_unit_number" IS '属地管理行政部门单位号';
COMMENT ON COLUMN "public"."lfun_campus"."sy_zones" IS '属地管理行政部门所在地地区';
COMMENT ON COLUMN "public"."lfun_campus"."historical_evolution" IS '历史沿革';
COMMENT ON COLUMN "public"."lfun_campus"."area_code" IS '电话区号';
COMMENT ON COLUMN "public"."lfun_campus"."campus_leader_name" IS '校区负责人姓名';
COMMENT ON COLUMN "public"."lfun_campus"."campus_leader_position" IS '校区负责人职位';
COMMENT ON COLUMN "public"."lfun_campus"."location_city" IS '校区所在地(省市)';
COMMENT ON COLUMN "public"."lfun_campus"."location_district" IS '校区所在地(区县)';
COMMENT ON COLUMN "public"."lfun_campus"."contact_number" IS '联系电话';
COMMENT ON COLUMN "public"."lfun_campus"."long" IS '所在经度';
COMMENT ON COLUMN "public"."lfun_campus"."lat" IS '所在纬度';
COMMENT ON COLUMN "public"."lfun_campus"."create_campus_date" IS '成立日期';
COMMENT ON COLUMN "public"."lfun_campus"."postal_code" IS '邮政编码';
COMMENT ON COLUMN "public"."lfun_campus"."fax_number" IS '传真电话';
COMMENT ON COLUMN "public"."lfun_campus"."email" IS '单位电子信箱';
COMMENT ON COLUMN "public"."lfun_campus"."detailed_address" IS '园所详细地址';
COMMENT ON COLUMN "public"."lfun_campus"."related_license_upload" IS '相关证照上传';
COMMENT ON COLUMN "public"."lfun_campus"."sy_zones_pro" IS '属地管理教育行政部门所在地（省级）';
COMMENT ON COLUMN "public"."lfun_campus"."primary_campus_system" IS '小学学制';
COMMENT ON COLUMN "public"."lfun_campus"."primary_campus_entry_age" IS '小学入学年龄';
COMMENT ON COLUMN "public"."lfun_campus"."junior_middle_campus_system" IS '初中学制';
COMMENT ON COLUMN "public"."lfun_campus"."junior_middle_campus_entry_age" IS '初中入学年龄';
COMMENT ON COLUMN "public"."lfun_campus"."senior_middle_campus_system" IS '高中学制';
COMMENT ON COLUMN "public"."lfun_campus"."created_uid" IS '创建人';
COMMENT ON COLUMN "public"."lfun_campus"."updated_uid" IS '操作人';
COMMENT ON COLUMN "public"."lfun_campus"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."lfun_campus"."updated_at" IS '更新时间';
COMMENT ON COLUMN "public"."lfun_campus"."is_deleted" IS '删除态';
COMMENT ON TABLE "public"."lfun_campus" IS '校区';

-- ----------------------------
-- Table structure for lfun_campus_communications
-- ----------------------------
DROP TABLE IF EXISTS "public"."lfun_campus_communications";
CREATE TABLE "public"."lfun_campus_communications" (
  "id" int8 NOT NULL DEFAULT nextval('lfun_campus_communications_id_seq'::regclass),
  "campus_id" int8,
  "postal_code" varchar(64) COLLATE "pg_catalog"."default",
  "fax_number" varchar(64) COLLATE "pg_catalog"."default",
  "email" varchar(64) COLLATE "pg_catalog"."default",
  "campus_web_url" varchar(64) COLLATE "pg_catalog"."default",
  "related_license_upload" varchar(64) COLLATE "pg_catalog"."default",
  "detailed_address" varchar(64) COLLATE "pg_catalog"."default",
  "contact_number" varchar(64) COLLATE "pg_catalog"."default",
  "area_code" varchar(64) COLLATE "pg_catalog"."default",
  "long" varchar(64) COLLATE "pg_catalog"."default",
  "lat" varchar(64) COLLATE "pg_catalog"."default",
  "leg_repr_name" varchar(64) COLLATE "pg_catalog"."default",
  "party_leader_name" varchar(64) COLLATE "pg_catalog"."default",
  "party_leader_position" varchar(64) COLLATE "pg_catalog"."default",
  "adm_leader_name" varchar(64) COLLATE "pg_catalog"."default",
  "adm_leader_position" varchar(64) COLLATE "pg_catalog"."default",
  "loc_area" varchar(64) COLLATE "pg_catalog"."default",
  "loc_area_pro" varchar(64) COLLATE "pg_catalog"."default",
  "campus_leader_name" varchar(20) COLLATE "pg_catalog"."default",
  "campus_leader_position" varchar(20) COLLATE "pg_catalog"."default",
  "created_uid" int4,
  "updated_uid" int4,
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL,
  "is_deleted" bool NOT NULL
)
;
COMMENT ON COLUMN "public"."lfun_campus_communications"."id" IS 'ID';
COMMENT ON COLUMN "public"."lfun_campus_communications"."campus_id" IS '校区id';
COMMENT ON COLUMN "public"."lfun_campus_communications"."postal_code" IS '邮政编码';
COMMENT ON COLUMN "public"."lfun_campus_communications"."fax_number" IS '传真电话';
COMMENT ON COLUMN "public"."lfun_campus_communications"."email" IS '单位电子信箱';
COMMENT ON COLUMN "public"."lfun_campus_communications"."campus_web_url" IS '校园网域名';
COMMENT ON COLUMN "public"."lfun_campus_communications"."related_license_upload" IS '相关证照上传';
COMMENT ON COLUMN "public"."lfun_campus_communications"."detailed_address" IS '园所详细地址';
COMMENT ON COLUMN "public"."lfun_campus_communications"."contact_number" IS '联系电话';
COMMENT ON COLUMN "public"."lfun_campus_communications"."area_code" IS '电话区号';
COMMENT ON COLUMN "public"."lfun_campus_communications"."long" IS '所在经度';
COMMENT ON COLUMN "public"."lfun_campus_communications"."lat" IS '所在纬度';
COMMENT ON COLUMN "public"."lfun_campus_communications"."leg_repr_name" IS '法定代表人姓名';
COMMENT ON COLUMN "public"."lfun_campus_communications"."party_leader_name" IS '党组织负责人姓名';
COMMENT ON COLUMN "public"."lfun_campus_communications"."party_leader_position" IS '党组织负责人职务';
COMMENT ON COLUMN "public"."lfun_campus_communications"."adm_leader_name" IS '行政负责人姓名';
COMMENT ON COLUMN "public"."lfun_campus_communications"."adm_leader_position" IS '行政负责人职务';
COMMENT ON COLUMN "public"."lfun_campus_communications"."loc_area" IS '园所所在地区';
COMMENT ON COLUMN "public"."lfun_campus_communications"."loc_area_pro" IS '园所所在地(省级)';
COMMENT ON COLUMN "public"."lfun_campus_communications"."campus_leader_name" IS '校区负责人姓名';
COMMENT ON COLUMN "public"."lfun_campus_communications"."campus_leader_position" IS '校区负责人职位';
COMMENT ON COLUMN "public"."lfun_campus_communications"."created_uid" IS '创建人';
COMMENT ON COLUMN "public"."lfun_campus_communications"."updated_uid" IS '操作人';
COMMENT ON COLUMN "public"."lfun_campus_communications"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."lfun_campus_communications"."updated_at" IS '更新时间';
COMMENT ON COLUMN "public"."lfun_campus_communications"."is_deleted" IS '删除态';
COMMENT ON TABLE "public"."lfun_campus_communications" IS '校区通信表';

-- ----------------------------
-- Table structure for lfun_campus_eduinfo
-- ----------------------------
DROP TABLE IF EXISTS "public"."lfun_campus_eduinfo";
CREATE TABLE "public"."lfun_campus_eduinfo" (
  "id" int8 NOT NULL DEFAULT nextval('lfun_campus_eduinfo_id_seq'::regclass),
  "campus_id" int8,
  "is_ethnic_campus" bool,
  "is_att_class" bool,
  "att_class_type" varchar(64) COLLATE "pg_catalog"."default",
  "is_province_feat" bool,
  "is_bilingual_clas" bool,
  "minority_lang_code" varchar(64) COLLATE "pg_catalog"."default",
  "is_profitable" bool,
  "prof_org_name" varchar(64) COLLATE "pg_catalog"."default",
  "is_prov_demo" bool,
  "is_latest_year" bool,
  "is_town_kinderg" bool,
  "is_incl_kinderg" bool,
  "is_affil_campus" bool,
  "affil_univ_code" varchar(64) COLLATE "pg_catalog"."default",
  "affil_univ_name" varchar(64) COLLATE "pg_catalog"."default",
  "is_last_yr_revok" bool,
  "is_campus_counted" bool,
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL,
  "created_uid" int4,
  "updated_uid" int4,
  "is_deleted" bool NOT NULL
)
;
COMMENT ON COLUMN "public"."lfun_campus_eduinfo"."id" IS 'ID';
COMMENT ON COLUMN "public"."lfun_campus_eduinfo"."campus_id" IS '校区id';
COMMENT ON COLUMN "public"."lfun_campus_eduinfo"."is_ethnic_campus" IS '是否民族校';
COMMENT ON COLUMN "public"."lfun_campus_eduinfo"."is_att_class" IS '是否附设班';
COMMENT ON COLUMN "public"."lfun_campus_eduinfo"."att_class_type" IS '附设班类型';
COMMENT ON COLUMN "public"."lfun_campus_eduinfo"."is_province_feat" IS '是否省特色';
COMMENT ON COLUMN "public"."lfun_campus_eduinfo"."is_bilingual_clas" IS '是否具有双语教学班';
COMMENT ON COLUMN "public"."lfun_campus_eduinfo"."minority_lang_code" IS '少数民族语言编码';
COMMENT ON COLUMN "public"."lfun_campus_eduinfo"."is_profitable" IS '是否营利性';
COMMENT ON COLUMN "public"."lfun_campus_eduinfo"."prof_org_name" IS '营利性机构名称';
COMMENT ON COLUMN "public"."lfun_campus_eduinfo"."is_prov_demo" IS '是否省示范';
COMMENT ON COLUMN "public"."lfun_campus_eduinfo"."is_latest_year" IS '是否最新年份';
COMMENT ON COLUMN "public"."lfun_campus_eduinfo"."is_town_kinderg" IS '是否乡镇幼儿园';
COMMENT ON COLUMN "public"."lfun_campus_eduinfo"."is_incl_kinderg" IS '是否普惠性幼儿园';
COMMENT ON COLUMN "public"."lfun_campus_eduinfo"."is_affil_campus" IS '是否附属校区';
COMMENT ON COLUMN "public"."lfun_campus_eduinfo"."affil_univ_code" IS '附属于高校（机构）标识码';
COMMENT ON COLUMN "public"."lfun_campus_eduinfo"."affil_univ_name" IS '附属于高校（机构）名称';
COMMENT ON COLUMN "public"."lfun_campus_eduinfo"."is_last_yr_revok" IS '是否上年撤销';
COMMENT ON COLUMN "public"."lfun_campus_eduinfo"."is_campus_counted" IS '是否计校数';
COMMENT ON COLUMN "public"."lfun_campus_eduinfo"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."lfun_campus_eduinfo"."updated_at" IS '更新时间';
COMMENT ON COLUMN "public"."lfun_campus_eduinfo"."created_uid" IS '创建人';
COMMENT ON COLUMN "public"."lfun_campus_eduinfo"."updated_uid" IS '操作人';
COMMENT ON COLUMN "public"."lfun_campus_eduinfo"."is_deleted" IS '删除态';
COMMENT ON TABLE "public"."lfun_campus_eduinfo" IS '校区教学信息表';

-- ----------------------------
-- Table structure for lfun_class_division_records
-- ----------------------------
DROP TABLE IF EXISTS "public"."lfun_class_division_records";
CREATE TABLE "public"."lfun_class_division_records" (
  "id" int8 NOT NULL DEFAULT nextval('lfun_class_division_records_id_seq'::regclass),
  "student_id" int8,
  "school_id" int8,
  "grade_id" int8,
  "class_id" int8,
  "student_no" varchar(255) COLLATE "pg_catalog"."default",
  "student_name" varchar(255) COLLATE "pg_catalog"."default",
  "status" varchar(255) COLLATE "pg_catalog"."default",
  "remark" varchar(255) COLLATE "pg_catalog"."default",
  "created_uid" int4,
  "updated_uid" int4,
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL,
  "is_deleted" bool NOT NULL
)
;
COMMENT ON COLUMN "public"."lfun_class_division_records"."id" IS '班级ID';
COMMENT ON COLUMN "public"."lfun_class_division_records"."student_id" IS '学生ID';
COMMENT ON COLUMN "public"."lfun_class_division_records"."school_id" IS '学校ID';
COMMENT ON COLUMN "public"."lfun_class_division_records"."grade_id" IS '年级ID';
COMMENT ON COLUMN "public"."lfun_class_division_records"."class_id" IS '班级ID';
COMMENT ON COLUMN "public"."lfun_class_division_records"."student_no" IS '学号';
COMMENT ON COLUMN "public"."lfun_class_division_records"."student_name" IS '学生姓名';
COMMENT ON COLUMN "public"."lfun_class_division_records"."status" IS '状态';
COMMENT ON COLUMN "public"."lfun_class_division_records"."remark" IS '备注';
COMMENT ON COLUMN "public"."lfun_class_division_records"."created_uid" IS '创建人';
COMMENT ON COLUMN "public"."lfun_class_division_records"."updated_uid" IS '操作人';
COMMENT ON COLUMN "public"."lfun_class_division_records"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."lfun_class_division_records"."updated_at" IS '更新时间';
COMMENT ON COLUMN "public"."lfun_class_division_records"."is_deleted" IS '删除态';
COMMENT ON TABLE "public"."lfun_class_division_records" IS '分班表';

-- ----------------------------
-- Table structure for lfun_classes
-- ----------------------------
DROP TABLE IF EXISTS "public"."lfun_classes";
CREATE TABLE "public"."lfun_classes" (
  "id" int8 NOT NULL DEFAULT nextval('lfun_classes_id_seq'::regclass),
  "school_id" int8 NOT NULL,
  "grade_id" int8,
  "grade_no" varchar(20) COLLATE "pg_catalog"."default",
  "is_att_class" bool,
  "att_class_type" varchar(48) COLLATE "pg_catalog"."default",
  "class_name" varchar(48) COLLATE "pg_catalog"."default",
  "class_number" varchar(48) COLLATE "pg_catalog"."default",
  "year_established" varchar(48) COLLATE "pg_catalog"."default",
  "teacher_id_card" varchar(48) COLLATE "pg_catalog"."default",
  "teacher_name" varchar(48) COLLATE "pg_catalog"."default",
  "education_stage" varchar(48) COLLATE "pg_catalog"."default",
  "school_system" varchar(48) COLLATE "pg_catalog"."default",
  "monitor" varchar(48) COLLATE "pg_catalog"."default",
  "class_type" varchar(48) COLLATE "pg_catalog"."default",
  "is_bilingual_class" bool,
  "major_for_vocational" varchar(48) COLLATE "pg_catalog"."default",
  "bilingual_teaching_mode" varchar(48) COLLATE "pg_catalog"."default",
  "ethnic_language" varchar(48) COLLATE "pg_catalog"."default",
  "created_uid" int4,
  "updated_uid" int4,
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL,
  "is_deleted" bool NOT NULL,
  "session_name" varchar(64) COLLATE "pg_catalog"."default",
  "session_id" int8,
  "teacher_card_type" varchar(48) COLLATE "pg_catalog"."default",
  "teacher_phone" varchar(48) COLLATE "pg_catalog"."default",
  "teacher_job_number" varchar(48) COLLATE "pg_catalog"."default",
  "care_teacher_id_card" varchar(48) COLLATE "pg_catalog"."default",
  "care_teacher_card_type" varchar(48) COLLATE "pg_catalog"."default",
  "care_teacher_name" varchar(48) COLLATE "pg_catalog"."default",
  "care_teacher_phone" varchar(48) COLLATE "pg_catalog"."default",
  "care_teacher_job_number" varchar(48) COLLATE "pg_catalog"."default",
  "monitor_student_number" varchar(48) COLLATE "pg_catalog"."default",
  "class_index" varchar(48) COLLATE "pg_catalog"."default",
  "teacher_id" int8,
  "care_teacher_id" int8,
  "monitor_id" int8,
  "class_standard_name" varchar(48) COLLATE "pg_catalog"."default",
  "status" varchar(64) COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "public"."lfun_classes"."id" IS '班级ID';
COMMENT ON COLUMN "public"."lfun_classes"."school_id" IS '学校ID';
COMMENT ON COLUMN "public"."lfun_classes"."grade_id" IS '年级ID';
COMMENT ON COLUMN "public"."lfun_classes"."grade_no" IS '年级编号';
COMMENT ON COLUMN "public"."lfun_classes"."is_att_class" IS '是否附设班';
COMMENT ON COLUMN "public"."lfun_classes"."att_class_type" IS '附设班类型';
COMMENT ON COLUMN "public"."lfun_classes"."class_name" IS '班级别名';
COMMENT ON COLUMN "public"."lfun_classes"."class_number" IS '班号';
COMMENT ON COLUMN "public"."lfun_classes"."year_established" IS '建班年份';
COMMENT ON COLUMN "public"."lfun_classes"."teacher_id_card" IS '班主任身份证';
COMMENT ON COLUMN "public"."lfun_classes"."teacher_name" IS '班主任姓名';
COMMENT ON COLUMN "public"."lfun_classes"."education_stage" IS '教育阶段';
COMMENT ON COLUMN "public"."lfun_classes"."school_system" IS '学制';
COMMENT ON COLUMN "public"."lfun_classes"."monitor" IS '班长';
COMMENT ON COLUMN "public"."lfun_classes"."class_type" IS '中小学班级类型';
COMMENT ON COLUMN "public"."lfun_classes"."is_bilingual_class" IS '是否少数民族双语教学班';
COMMENT ON COLUMN "public"."lfun_classes"."major_for_vocational" IS '中职班级专业';
COMMENT ON COLUMN "public"."lfun_classes"."bilingual_teaching_mode" IS '双语教学模式';
COMMENT ON COLUMN "public"."lfun_classes"."ethnic_language" IS '少数民族语言';
COMMENT ON COLUMN "public"."lfun_classes"."created_uid" IS '创建人';
COMMENT ON COLUMN "public"."lfun_classes"."updated_uid" IS '操作人';
COMMENT ON COLUMN "public"."lfun_classes"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."lfun_classes"."updated_at" IS '更新时间';
COMMENT ON COLUMN "public"."lfun_classes"."is_deleted" IS '删除态';
COMMENT ON COLUMN "public"."lfun_classes"."session_name" IS '届别名称';
COMMENT ON COLUMN "public"."lfun_classes"."session_id" IS '届别ID';
COMMENT ON COLUMN "public"."lfun_classes"."teacher_card_type" IS '班主任证件类型';
COMMENT ON COLUMN "public"."lfun_classes"."teacher_phone" IS '班主任电话';
COMMENT ON COLUMN "public"."lfun_classes"."teacher_job_number" IS '班主任工号';
COMMENT ON COLUMN "public"."lfun_classes"."care_teacher_id_card" IS '保育员身份证';
COMMENT ON COLUMN "public"."lfun_classes"."care_teacher_card_type" IS '班主任证件类型';
COMMENT ON COLUMN "public"."lfun_classes"."care_teacher_name" IS '保育员姓名';
COMMENT ON COLUMN "public"."lfun_classes"."care_teacher_phone" IS '班主任电话';
COMMENT ON COLUMN "public"."lfun_classes"."care_teacher_job_number" IS '班主任工号';
COMMENT ON COLUMN "public"."lfun_classes"."monitor_student_number" IS '班长学号';
COMMENT ON COLUMN "public"."lfun_classes"."class_index" IS '班级序号';
COMMENT ON COLUMN "public"."lfun_classes"."teacher_id" IS '班主任id';
COMMENT ON COLUMN "public"."lfun_classes"."care_teacher_id" IS '保育员id';
COMMENT ON COLUMN "public"."lfun_classes"."monitor_id" IS '班长的学生id';
COMMENT ON COLUMN "public"."lfun_classes"."class_standard_name" IS '班级名称';
COMMENT ON COLUMN "public"."lfun_classes"."status" IS '状态';
COMMENT ON TABLE "public"."lfun_classes" IS '班级表模型';

-- ----------------------------
-- Table structure for lfun_course
-- ----------------------------
DROP TABLE IF EXISTS "public"."lfun_course";
CREATE TABLE "public"."lfun_course" (
  "id" int8 NOT NULL DEFAULT nextval('lfun_course_id_seq'::regclass),
  "school_id" int8,
  "course_no" varchar(24) COLLATE "pg_catalog"."default",
  "grade_id" int8,
  "course_name" varchar(24) COLLATE "pg_catalog"."default" NOT NULL,
  "created_uid" int4,
  "updated_uid" int4,
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL,
  "is_deleted" bool NOT NULL,
  "city" varchar(64) COLLATE "pg_catalog"."default",
  "district" varchar(64) COLLATE "pg_catalog"."default",
  "school_type" varchar(64) COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "public"."lfun_course"."id" IS 'ID';
COMMENT ON COLUMN "public"."lfun_course"."school_id" IS '学校ID';
COMMENT ON COLUMN "public"."lfun_course"."course_no" IS '学科编码';
COMMENT ON COLUMN "public"."lfun_course"."grade_id" IS '年级ID';
COMMENT ON COLUMN "public"."lfun_course"."course_name" IS '学科名称';
COMMENT ON COLUMN "public"."lfun_course"."created_uid" IS '创建人';
COMMENT ON COLUMN "public"."lfun_course"."updated_uid" IS '操作人';
COMMENT ON COLUMN "public"."lfun_course"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."lfun_course"."updated_at" IS '更新时间';
COMMENT ON COLUMN "public"."lfun_course"."is_deleted" IS '删除态';
COMMENT ON COLUMN "public"."lfun_course"."city" IS '城市';
COMMENT ON COLUMN "public"."lfun_course"."school_type" IS '教育阶段/学校类别 例如 小学 初中 多个逗号隔开';
COMMENT ON TABLE "public"."lfun_course" IS '学科表模型';

-- ----------------------------
-- Table structure for lfun_course_school_nature
-- ----------------------------
DROP TABLE IF EXISTS "public"."lfun_course_school_nature";
CREATE TABLE "public"."lfun_course_school_nature" (
  "id" int8 NOT NULL DEFAULT nextval('lfun_course_school_nature_id_seq'::regclass),
  "course_no" varchar(24) COLLATE "pg_catalog"."default",
  "school_nature" varchar(40) COLLATE "pg_catalog"."default",
  "created_uid" int4,
  "updated_uid" int4,
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL,
  "is_deleted" bool NOT NULL
)
;
COMMENT ON COLUMN "public"."lfun_course_school_nature"."id" IS 'ID';
COMMENT ON COLUMN "public"."lfun_course_school_nature"."course_no" IS '学科编码';
COMMENT ON COLUMN "public"."lfun_course_school_nature"."school_nature" IS '学校性质 2级或者3级';
COMMENT ON COLUMN "public"."lfun_course_school_nature"."created_uid" IS '创建人';
COMMENT ON COLUMN "public"."lfun_course_school_nature"."updated_uid" IS '操作人';
COMMENT ON COLUMN "public"."lfun_course_school_nature"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."lfun_course_school_nature"."updated_at" IS '更新时间';
COMMENT ON COLUMN "public"."lfun_course_school_nature"."is_deleted" IS '删除态';
COMMENT ON TABLE "public"."lfun_course_school_nature" IS '课程和学校关系表模型';

-- ----------------------------
-- Table structure for lfun_domestic_training
-- ----------------------------
DROP TABLE IF EXISTS "public"."lfun_domestic_training";
CREATE TABLE "public"."lfun_domestic_training" (
  "domestic_training_id" int8 NOT NULL DEFAULT nextval('lfun_domestic_training_domestic_training_id_seq'::regclass),
  "teacher_id" int8 NOT NULL,
  "training_year" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "training_type" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "training_project" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "training_institution" varchar(64) COLLATE "pg_catalog"."default",
  "training_mode" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "training_hours" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "training_credits" varchar(64) COLLATE "pg_catalog"."default",
  "is_deleted" bool NOT NULL
)
;
COMMENT ON COLUMN "public"."lfun_domestic_training"."domestic_training_id" IS 'domestic_trainingID';
COMMENT ON COLUMN "public"."lfun_domestic_training"."teacher_id" IS '教师ID';
COMMENT ON COLUMN "public"."lfun_domestic_training"."training_year" IS '培训年度';
COMMENT ON COLUMN "public"."lfun_domestic_training"."training_type" IS '培训类型枚举training_type_lv1';
COMMENT ON COLUMN "public"."lfun_domestic_training"."training_project" IS '培训项目';
COMMENT ON COLUMN "public"."lfun_domestic_training"."training_institution" IS '培训机构';
COMMENT ON COLUMN "public"."lfun_domestic_training"."training_mode" IS '培训方式枚举training_mode_lv1';
COMMENT ON COLUMN "public"."lfun_domestic_training"."training_hours" IS '培训学时';
COMMENT ON COLUMN "public"."lfun_domestic_training"."training_credits" IS '培训学分';
COMMENT ON COLUMN "public"."lfun_domestic_training"."is_deleted" IS '是否删除';
COMMENT ON TABLE "public"."lfun_domestic_training" IS 'domestic_training信息表';

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
-- Table structure for lfun_educational_teaching
-- ----------------------------
DROP TABLE IF EXISTS "public"."lfun_educational_teaching";
CREATE TABLE "public"."lfun_educational_teaching" (
  "educational_teaching_id" int8 NOT NULL DEFAULT nextval('lfun_educational_teaching_educational_teaching_id_seq'::regclass),
  "teacher_id" int8 NOT NULL,
  "academic_year" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "semester" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "teaching_stage" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "course_category" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "subject_category" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "course_name" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "average_weekly_teaching_hours" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "other_responsibilities" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "average_weekly_other_duties_hours" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "concurrent_job" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "concurrent_job_name" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "is_deleted" bool NOT NULL
)
;
COMMENT ON COLUMN "public"."lfun_educational_teaching"."educational_teaching_id" IS 'educational_teachingID';
COMMENT ON COLUMN "public"."lfun_educational_teaching"."teacher_id" IS '教师ID';
COMMENT ON COLUMN "public"."lfun_educational_teaching"."academic_year" IS '学年';
COMMENT ON COLUMN "public"."lfun_educational_teaching"."semester" IS '学期';
COMMENT ON COLUMN "public"."lfun_educational_teaching"."teaching_stage" IS '任教阶段';
COMMENT ON COLUMN "public"."lfun_educational_teaching"."course_category" IS '任课课程类别';
COMMENT ON COLUMN "public"."lfun_educational_teaching"."subject_category" IS '任课学科类别';
COMMENT ON COLUMN "public"."lfun_educational_teaching"."course_name" IS '任课课程';
COMMENT ON COLUMN "public"."lfun_educational_teaching"."average_weekly_teaching_hours" IS '平均每周教学课时';
COMMENT ON COLUMN "public"."lfun_educational_teaching"."other_responsibilities" IS '承担其他工作';
COMMENT ON COLUMN "public"."lfun_educational_teaching"."average_weekly_other_duties_hours" IS '平均每周其他工作折合课时';
COMMENT ON COLUMN "public"."lfun_educational_teaching"."concurrent_job" IS '兼任工作';
COMMENT ON COLUMN "public"."lfun_educational_teaching"."concurrent_job_name" IS '兼任工作名称';
COMMENT ON COLUMN "public"."lfun_educational_teaching"."is_deleted" IS '是否删除';
COMMENT ON TABLE "public"."lfun_educational_teaching" IS 'educational_teaching信息表';

-- ----------------------------
-- Table structure for lfun_enum_value
-- ----------------------------
DROP TABLE IF EXISTS "public"."lfun_enum_value";
CREATE TABLE "public"."lfun_enum_value" (
  "id" int8 NOT NULL DEFAULT nextval('lfun_enum_value_id_seq'::regclass),
  "enum_name" varchar(255) COLLATE "pg_catalog"."default",
  "enum_value" varchar(255) COLLATE "pg_catalog"."default",
  "description" varchar(255) COLLATE "pg_catalog"."default",
  "sort_number" int4,
  "parent_id" varchar(255) COLLATE "pg_catalog"."default",
  "is_enabled" bool NOT NULL,
  "created_uid" int4,
  "updated_uid" int4,
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL,
  "is_deleted" bool NOT NULL
)
;
COMMENT ON COLUMN "public"."lfun_enum_value"."id" IS 'ID';
COMMENT ON COLUMN "public"."lfun_enum_value"."enum_name" IS '枚举类型的名称';
COMMENT ON COLUMN "public"."lfun_enum_value"."enum_value" IS '枚举的具体值';
COMMENT ON COLUMN "public"."lfun_enum_value"."description" IS '枚举值的描述或标签';
COMMENT ON COLUMN "public"."lfun_enum_value"."sort_number" IS '排序序号';
COMMENT ON COLUMN "public"."lfun_enum_value"."parent_id" IS '父级ID';
COMMENT ON COLUMN "public"."lfun_enum_value"."is_enabled" IS '是否启用';
COMMENT ON COLUMN "public"."lfun_enum_value"."created_uid" IS '创建人';
COMMENT ON COLUMN "public"."lfun_enum_value"."updated_uid" IS '操作人';
COMMENT ON COLUMN "public"."lfun_enum_value"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."lfun_enum_value"."updated_at" IS '更新时间';
COMMENT ON COLUMN "public"."lfun_enum_value"."is_deleted" IS '删除态';
COMMENT ON TABLE "public"."lfun_enum_value" IS '枚举表模型';

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
  "class_number" int4 NOT NULL
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
COMMENT ON TABLE "public"."lfun_grade" IS '年级表模型';

-- ----------------------------
-- Table structure for lfun_graduation_student
-- ----------------------------
DROP TABLE IF EXISTS "public"."lfun_graduation_student";
CREATE TABLE "public"."lfun_graduation_student" (
  "id" int4 NOT NULL DEFAULT nextval('lfun_graduation_student_id_seq'::regclass),
  "student_id" varchar(32) COLLATE "pg_catalog"."default" NOT NULL,
  "student_name" varchar(32) COLLATE "pg_catalog"."default",
  "gender" varchar(32) COLLATE "pg_catalog"."default",
  "school" varchar(32) COLLATE "pg_catalog"."default",
  "school_id" varchar(32) COLLATE "pg_catalog"."default",
  "county" varchar(32) COLLATE "pg_catalog"."default",
  "edu_number" varchar(32) COLLATE "pg_catalog"."default",
  "class_id" varchar(32) COLLATE "pg_catalog"."default" NOT NULL,
  "class_name" varchar(32) COLLATE "pg_catalog"."default",
  "status" varchar(32) COLLATE "pg_catalog"."default",
  "graduation_date" varchar(32) COLLATE "pg_catalog"."default",
  "graduation_remark" varchar(200) COLLATE "pg_catalog"."default",
  "photo" varchar(64) COLLATE "pg_catalog"."default",
  "archive_status" varchar(32) COLLATE "pg_catalog"."default",
  "archive_date" varchar(32) COLLATE "pg_catalog"."default",
  "created_uid" int4,
  "updated_uid" int4,
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL,
  "is_deleted" bool NOT NULL
)
;
COMMENT ON COLUMN "public"."lfun_graduation_student"."id" IS '班级ID';
COMMENT ON COLUMN "public"."lfun_graduation_student"."student_id" IS '学生id';
COMMENT ON COLUMN "public"."lfun_graduation_student"."student_name" IS '学生姓名';
COMMENT ON COLUMN "public"."lfun_graduation_student"."gender" IS '性别';
COMMENT ON COLUMN "public"."lfun_graduation_student"."school" IS '学校';
COMMENT ON COLUMN "public"."lfun_graduation_student"."school_id" IS '学校ID';
COMMENT ON COLUMN "public"."lfun_graduation_student"."county" IS '行政属地';
COMMENT ON COLUMN "public"."lfun_graduation_student"."edu_number" IS '学籍号码';
COMMENT ON COLUMN "public"."lfun_graduation_student"."class_id" IS '班级id';
COMMENT ON COLUMN "public"."lfun_graduation_student"."class_name" IS '班级';
COMMENT ON COLUMN "public"."lfun_graduation_student"."status" IS '毕业状态';
COMMENT ON COLUMN "public"."lfun_graduation_student"."graduation_date" IS '毕业年份';
COMMENT ON COLUMN "public"."lfun_graduation_student"."graduation_remark" IS '毕业备注';
COMMENT ON COLUMN "public"."lfun_graduation_student"."photo" IS '照片';
COMMENT ON COLUMN "public"."lfun_graduation_student"."archive_status" IS '归档状态';
COMMENT ON COLUMN "public"."lfun_graduation_student"."archive_date" IS '归档年份';
COMMENT ON COLUMN "public"."lfun_graduation_student"."created_uid" IS '创建人';
COMMENT ON COLUMN "public"."lfun_graduation_student"."updated_uid" IS '操作人';
COMMENT ON COLUMN "public"."lfun_graduation_student"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."lfun_graduation_student"."updated_at" IS '更新时间';
COMMENT ON COLUMN "public"."lfun_graduation_student"."is_deleted" IS '删除态';
COMMENT ON TABLE "public"."lfun_graduation_student" IS '毕业生表模型';

-- ----------------------------
-- Table structure for lfun_institutions
-- ----------------------------
DROP TABLE IF EXISTS "public"."lfun_institutions";
CREATE TABLE "public"."lfun_institutions" (
  "id" int4 NOT NULL DEFAULT nextval('lfun_institutions_id_seq'::regclass),
  "institution_name" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "institution_code" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "institution_en_name" varchar(64) COLLATE "pg_catalog"."default",
  "create_institution_date" varchar(64) COLLATE "pg_catalog"."default",
  "department_unit_number" varchar(64) COLLATE "pg_catalog"."default",
  "sy_zones" varchar(64) COLLATE "pg_catalog"."default",
  "social_credit_code" varchar(64) COLLATE "pg_catalog"."default",
  "postal_code" varchar(64) COLLATE "pg_catalog"."default",
  "urban_rural_nature" varchar(64) COLLATE "pg_catalog"."default",
  "status" varchar(64) COLLATE "pg_catalog"."default",
  "fax_number" varchar(64) COLLATE "pg_catalog"."default",
  "email" varchar(64) COLLATE "pg_catalog"."default",
  "contact_number" varchar(64) COLLATE "pg_catalog"."default",
  "area_code" varchar(64) COLLATE "pg_catalog"."default",
  "leg_repr_name" varchar(64) COLLATE "pg_catalog"."default",
  "party_leader_name" varchar(64) COLLATE "pg_catalog"."default",
  "party_leader_position" varchar(64) COLLATE "pg_catalog"."default",
  "adm_leader_name" varchar(64) COLLATE "pg_catalog"."default",
  "adm_leader_position" varchar(64) COLLATE "pg_catalog"."default",
  "detailed_address" varchar(64) COLLATE "pg_catalog"."default",
  "related_license_upload" varchar(64) COLLATE "pg_catalog"."default",
  "long" varchar(64) COLLATE "pg_catalog"."default",
  "lat" varchar(64) COLLATE "pg_catalog"."default",
  "institution_category" varchar(64) COLLATE "pg_catalog"."default",
  "institution_type" varchar(64) COLLATE "pg_catalog"."default",
  "location_economic_attribute" varchar(64) COLLATE "pg_catalog"."default",
  "leg_repr_certificatenumber" varchar(64) COLLATE "pg_catalog"."default",
  "membership_no" varchar(64) COLLATE "pg_catalog"."default",
  "membership_category" varchar(64) COLLATE "pg_catalog"."default",
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL,
  "created_uid" int4,
  "updated_uid" int4,
  "is_deleted" bool NOT NULL,
  "process_instance_id" int8,
  "workflow_status" varchar(64) COLLATE "pg_catalog"."default",
  "block" varchar(64) COLLATE "pg_catalog"."default",
  "borough" varchar(64) COLLATE "pg_catalog"."default",
  "urban_ethnic_nature" varchar(64) COLLATE "pg_catalog"."default",
  "website_url" varchar(64) COLLATE "pg_catalog"."default",
  "is_entity" bool
)
;
COMMENT ON COLUMN "public"."lfun_institutions"."id" IS 'ID';
COMMENT ON COLUMN "public"."lfun_institutions"."institution_name" IS '单位名称';
COMMENT ON COLUMN "public"."lfun_institutions"."institution_code" IS '机构代码';
COMMENT ON COLUMN "public"."lfun_institutions"."institution_en_name" IS '单位名称英文';
COMMENT ON COLUMN "public"."lfun_institutions"."create_institution_date" IS '成立年月';
COMMENT ON COLUMN "public"."lfun_institutions"."department_unit_number" IS '属地管理行政部门单位号';
COMMENT ON COLUMN "public"."lfun_institutions"."sy_zones" IS '属地管理行政部门所在地地区';
COMMENT ON COLUMN "public"."lfun_institutions"."social_credit_code" IS '统一社会信用代码';
COMMENT ON COLUMN "public"."lfun_institutions"."postal_code" IS '邮政编码';
COMMENT ON COLUMN "public"."lfun_institutions"."urban_rural_nature" IS '城乡性质';
COMMENT ON COLUMN "public"."lfun_institutions"."status" IS '状态';
COMMENT ON COLUMN "public"."lfun_institutions"."fax_number" IS '传真电话';
COMMENT ON COLUMN "public"."lfun_institutions"."email" IS '单位电子信箱';
COMMENT ON COLUMN "public"."lfun_institutions"."contact_number" IS '联系电话';
COMMENT ON COLUMN "public"."lfun_institutions"."area_code" IS '电话区号';
COMMENT ON COLUMN "public"."lfun_institutions"."leg_repr_name" IS '法定代表人姓名';
COMMENT ON COLUMN "public"."lfun_institutions"."party_leader_name" IS '党组织负责人姓名';
COMMENT ON COLUMN "public"."lfun_institutions"."party_leader_position" IS '党组织负责人职务';
COMMENT ON COLUMN "public"."lfun_institutions"."adm_leader_name" IS '行政负责人姓名';
COMMENT ON COLUMN "public"."lfun_institutions"."adm_leader_position" IS '行政负责人职务';
COMMENT ON COLUMN "public"."lfun_institutions"."detailed_address" IS '详细地址';
COMMENT ON COLUMN "public"."lfun_institutions"."related_license_upload" IS '相关证照上传';
COMMENT ON COLUMN "public"."lfun_institutions"."long" IS '所在经度';
COMMENT ON COLUMN "public"."lfun_institutions"."lat" IS '所在纬度';
COMMENT ON COLUMN "public"."lfun_institutions"."institution_category" IS ' 单位分类';
COMMENT ON COLUMN "public"."lfun_institutions"."institution_type" IS '单位类型 公办 民办';
COMMENT ON COLUMN "public"."lfun_institutions"."location_economic_attribute" IS ' 所在地经济属性';
COMMENT ON COLUMN "public"."lfun_institutions"."leg_repr_certificatenumber" IS ' 法人证书号';
COMMENT ON COLUMN "public"."lfun_institutions"."membership_no" IS ' 隶属单位号';
COMMENT ON COLUMN "public"."lfun_institutions"."membership_category" IS ' 隶属单位类型';
COMMENT ON COLUMN "public"."lfun_institutions"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."lfun_institutions"."updated_at" IS '更新时间';
COMMENT ON COLUMN "public"."lfun_institutions"."created_uid" IS '创建人';
COMMENT ON COLUMN "public"."lfun_institutions"."updated_uid" IS '操作人';
COMMENT ON COLUMN "public"."lfun_institutions"."is_deleted" IS '删除态';
COMMENT ON COLUMN "public"."lfun_institutions"."process_instance_id" IS '流程ID';
COMMENT ON COLUMN "public"."lfun_institutions"."workflow_status" IS '工作流审核状态';
COMMENT ON COLUMN "public"."lfun_institutions"."block" IS '地域管辖区';
COMMENT ON COLUMN "public"."lfun_institutions"."borough" IS '行政管辖区';
COMMENT ON COLUMN "public"."lfun_institutions"."urban_ethnic_nature" IS ' 所在地民族属性';
COMMENT ON COLUMN "public"."lfun_institutions"."website_url" IS '网址';
COMMENT ON COLUMN "public"."lfun_institutions"."is_entity" IS ' 是否实体';
COMMENT ON TABLE "public"."lfun_institutions" IS '行政事业单位表';

-- ----------------------------
-- Table structure for lfun_leader_info
-- ----------------------------
DROP TABLE IF EXISTS "public"."lfun_leader_info";
CREATE TABLE "public"."lfun_leader_info" (
  "id" int8 NOT NULL DEFAULT nextval('lfun_leader_info_id_seq'::regclass),
  "planning_school_id" int8,
  "leader_name" varchar(20) COLLATE "pg_catalog"."default",
  "position" varchar(255) COLLATE "pg_catalog"."default",
  "status" varchar(255) COLLATE "pg_catalog"."default",
  "start_date" varchar(20) COLLATE "pg_catalog"."default" NOT NULL,
  "end_date" varchar(20) COLLATE "pg_catalog"."default" NOT NULL,
  "job_content" varchar(255) COLLATE "pg_catalog"."default",
  "job_responsibility" varchar(255) COLLATE "pg_catalog"."default",
  "school_id" int8,
  "institution_id" int8,
  "created_uid" int4,
  "updated_uid" int4,
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL,
  "is_deleted" bool NOT NULL,
  "identity" varchar(64) COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "public"."lfun_leader_info"."id" IS '班级ID';
COMMENT ON COLUMN "public"."lfun_leader_info"."planning_school_id" IS '规划ID';
COMMENT ON COLUMN "public"."lfun_leader_info"."leader_name" IS '领导姓名';
COMMENT ON COLUMN "public"."lfun_leader_info"."position" IS '职务';
COMMENT ON COLUMN "public"."lfun_leader_info"."status" IS '状态';
COMMENT ON COLUMN "public"."lfun_leader_info"."start_date" IS '任职开始时间';
COMMENT ON COLUMN "public"."lfun_leader_info"."end_date" IS '任职结束时间';
COMMENT ON COLUMN "public"."lfun_leader_info"."job_content" IS '工作内容';
COMMENT ON COLUMN "public"."lfun_leader_info"."job_responsibility" IS '分管工作';
COMMENT ON COLUMN "public"."lfun_leader_info"."school_id" IS '学校ID';
COMMENT ON COLUMN "public"."lfun_leader_info"."institution_id" IS '事业单位ID';
COMMENT ON COLUMN "public"."lfun_leader_info"."created_uid" IS '创建人';
COMMENT ON COLUMN "public"."lfun_leader_info"."updated_uid" IS '操作人';
COMMENT ON COLUMN "public"."lfun_leader_info"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."lfun_leader_info"."updated_at" IS '更新时间';
COMMENT ON COLUMN "public"."lfun_leader_info"."is_deleted" IS '删除态';
COMMENT ON COLUMN "public"."lfun_leader_info"."identity" IS '身份';
COMMENT ON TABLE "public"."lfun_leader_info" IS '领导表';

-- ----------------------------
-- Table structure for lfun_major
-- ----------------------------
DROP TABLE IF EXISTS "public"."lfun_major";
CREATE TABLE "public"."lfun_major" (
  "id" int8 NOT NULL DEFAULT nextval('lfun_major_id_seq'::regclass),
  "school_id" int8,
  "major_name" varchar(24) COLLATE "pg_catalog"."default" NOT NULL,
  "major_id" varchar(60) COLLATE "pg_catalog"."default",
  "major_type" varchar(24) COLLATE "pg_catalog"."default",
  "major_id_lv2" varchar(24) COLLATE "pg_catalog"."default",
  "major_id_lv3" varchar(24) COLLATE "pg_catalog"."default",
  "created_uid" int4,
  "updated_uid" int4,
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL,
  "is_deleted" bool NOT NULL,
  "city" varchar(64) COLLATE "pg_catalog"."default",
  "district" varchar(64) COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "public"."lfun_major"."id" IS '班级ID';
COMMENT ON COLUMN "public"."lfun_major"."school_id" IS '学校ID';
COMMENT ON COLUMN "public"."lfun_major"."major_name" IS '专业名称';
COMMENT ON COLUMN "public"."lfun_major"."major_id" IS '专业code,枚举major';
COMMENT ON COLUMN "public"."lfun_major"."major_type" IS '专业类型';
COMMENT ON COLUMN "public"."lfun_major"."major_id_lv2" IS '2级专业code,枚举major_lv2';
COMMENT ON COLUMN "public"."lfun_major"."major_id_lv3" IS '3级专业code,枚举major_lv3';
COMMENT ON COLUMN "public"."lfun_major"."created_uid" IS '创建人';
COMMENT ON COLUMN "public"."lfun_major"."updated_uid" IS '操作人';
COMMENT ON COLUMN "public"."lfun_major"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."lfun_major"."updated_at" IS '更新时间';
COMMENT ON COLUMN "public"."lfun_major"."is_deleted" IS '删除态';
COMMENT ON COLUMN "public"."lfun_major"."city" IS '城市';
COMMENT ON TABLE "public"."lfun_major" IS '专业表模型';

-- ----------------------------
-- Table structure for lfun_organization
-- ----------------------------
DROP TABLE IF EXISTS "public"."lfun_organization";
CREATE TABLE "public"."lfun_organization" (
  "id" int8 NOT NULL DEFAULT nextval('lfun_organization_id_seq'::regclass),
  "org_type" varchar(64) COLLATE "pg_catalog"."default",
  "org_name" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "parent_id" int8,
  "created_uid" int4,
  "updated_uid" int4,
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL,
  "is_deleted" bool NOT NULL,
  "school_id" int8,
  "member_cnt" int4,
  "org_code" varchar(64) COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "public"."lfun_organization"."id" IS 'ID';
COMMENT ON COLUMN "public"."lfun_organization"."org_type" IS '组织分类 行政类等';
COMMENT ON COLUMN "public"."lfun_organization"."org_name" IS '组织或者部门名称 例如行政部';
COMMENT ON COLUMN "public"."lfun_organization"."parent_id" IS '父级ID';
COMMENT ON COLUMN "public"."lfun_organization"."created_uid" IS '创建人';
COMMENT ON COLUMN "public"."lfun_organization"."updated_uid" IS '操作人';
COMMENT ON COLUMN "public"."lfun_organization"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."lfun_organization"."updated_at" IS '更新时间';
COMMENT ON COLUMN "public"."lfun_organization"."is_deleted" IS '删除态';
COMMENT ON COLUMN "public"."lfun_organization"."school_id" IS '学校ID';
COMMENT ON COLUMN "public"."lfun_organization"."member_cnt" IS '人数';
COMMENT ON COLUMN "public"."lfun_organization"."org_code" IS '组织或者部门编号 学校内唯一';
COMMENT ON TABLE "public"."lfun_organization" IS '组织架构模型';

-- ----------------------------
-- Table structure for lfun_organization_members
-- ----------------------------
DROP TABLE IF EXISTS "public"."lfun_organization_members";
CREATE TABLE "public"."lfun_organization_members" (
  "id" int8 NOT NULL DEFAULT nextval('lfun_organization_members_id_seq'::regclass),
  "org_id" int8,
  "member_name" varchar(64) COLLATE "pg_catalog"."default",
  "member_type" varchar(64) COLLATE "pg_catalog"."default",
  "birthday" varchar(64) COLLATE "pg_catalog"."default",
  "gender" varchar(64) COLLATE "pg_catalog"."default",
  "mobile" varchar(64) COLLATE "pg_catalog"."default",
  "card_type" varchar(64) COLLATE "pg_catalog"."default",
  "card_number" varchar(64) COLLATE "pg_catalog"."default",
  "identity" varchar(64) COLLATE "pg_catalog"."default",
  "created_uid" int4,
  "updated_uid" int4,
  "created_at" timestamp(6),
  "updated_at" timestamp(6),
  "is_deleted" bool,
  "teacher_id" int8
)
;
COMMENT ON COLUMN "public"."lfun_organization_members"."id" IS 'ID';
COMMENT ON COLUMN "public"."lfun_organization_members"."org_id" IS '部门ID';
COMMENT ON COLUMN "public"."lfun_organization_members"."member_name" IS '姓名';
COMMENT ON COLUMN "public"."lfun_organization_members"."member_type" IS '成员类型/岗位 例如老师 领导 职工等';
COMMENT ON COLUMN "public"."lfun_organization_members"."birthday" IS '生日';
COMMENT ON COLUMN "public"."lfun_organization_members"."gender" IS '性别';
COMMENT ON COLUMN "public"."lfun_organization_members"."mobile" IS '手机';
COMMENT ON COLUMN "public"."lfun_organization_members"."card_type" IS '证件类型';
COMMENT ON COLUMN "public"."lfun_organization_members"."card_number" IS '证件号码';
COMMENT ON COLUMN "public"."lfun_organization_members"."identity" IS '身份';
COMMENT ON COLUMN "public"."lfun_organization_members"."created_uid" IS '创建人';
COMMENT ON COLUMN "public"."lfun_organization_members"."updated_uid" IS '操作人';
COMMENT ON COLUMN "public"."lfun_organization_members"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."lfun_organization_members"."updated_at" IS '更新时间';
COMMENT ON COLUMN "public"."lfun_organization_members"."is_deleted" IS '删除态';
COMMENT ON COLUMN "public"."lfun_organization_members"."teacher_id" IS '教师ID';
COMMENT ON TABLE "public"."lfun_organization_members" IS '组织部门成员表模型';

-- ----------------------------
-- Table structure for lfun_overseas_study
-- ----------------------------
DROP TABLE IF EXISTS "public"."lfun_overseas_study";
CREATE TABLE "public"."lfun_overseas_study" (
  "overseas_study_id" int8 NOT NULL DEFAULT nextval('lfun_overseas_study_overseas_study_id_seq'::regclass),
  "teacher_id" int8 NOT NULL,
  "start_date" "sys"."date" NOT NULL,
  "end_date" "sys"."date" NOT NULL,
  "country_region" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "training_institution_name" varchar(64) COLLATE "pg_catalog"."default",
  "project_name" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "organizing_institution_name" varchar(64) COLLATE "pg_catalog"."default",
  "is_deleted" bool NOT NULL
)
;
COMMENT ON COLUMN "public"."lfun_overseas_study"."overseas_study_id" IS 'overseas_studyID';
COMMENT ON COLUMN "public"."lfun_overseas_study"."teacher_id" IS '教师ID';
COMMENT ON COLUMN "public"."lfun_overseas_study"."start_date" IS '开始日期';
COMMENT ON COLUMN "public"."lfun_overseas_study"."end_date" IS '结束日期';
COMMENT ON COLUMN "public"."lfun_overseas_study"."country_region" IS '国家地区';
COMMENT ON COLUMN "public"."lfun_overseas_study"."training_institution_name" IS '研修机构名称';
COMMENT ON COLUMN "public"."lfun_overseas_study"."project_name" IS '项目名称';
COMMENT ON COLUMN "public"."lfun_overseas_study"."organizing_institution_name" IS '项目组织单位名称';
COMMENT ON COLUMN "public"."lfun_overseas_study"."is_deleted" IS '是否删除';
COMMENT ON TABLE "public"."lfun_overseas_study" IS 'overseas_study信息表';

-- ----------------------------
-- Table structure for lfun_planning_school
-- ----------------------------
DROP TABLE IF EXISTS "public"."lfun_planning_school";
CREATE TABLE "public"."lfun_planning_school" (
  "id" int8 NOT NULL DEFAULT nextval('lfun_planning_school_id_seq'::regclass),
  "planning_school_name" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "planning_school_no" varchar(64) COLLATE "pg_catalog"."default",
  "planning_school_code" varchar(64) COLLATE "pg_catalog"."default",
  "planning_school_operation_license_number" varchar(64) COLLATE "pg_catalog"."default",
  "block" varchar(64) COLLATE "pg_catalog"."default",
  "borough" varchar(64) COLLATE "pg_catalog"."default",
  "province" varchar(64) COLLATE "pg_catalog"."default",
  "city" varchar(64) COLLATE "pg_catalog"."default",
  "planning_school_operation_type" varchar(64) COLLATE "pg_catalog"."default",
  "planning_school_org_type" varchar(64) COLLATE "pg_catalog"."default",
  "planning_school_level" varchar(64) COLLATE "pg_catalog"."default",
  "status" varchar(64) COLLATE "pg_catalog"."default",
  "kg_level" varchar(64) COLLATE "pg_catalog"."default",
  "planning_school_short_name" varchar(64) COLLATE "pg_catalog"."default",
  "planning_school_en_name" varchar(64) COLLATE "pg_catalog"."default",
  "create_planning_school_date" varchar(64) COLLATE "pg_catalog"."default",
  "social_credit_code" varchar(64) COLLATE "pg_catalog"."default",
  "founder_type" varchar(64) COLLATE "pg_catalog"."default",
  "founder_type_lv2" varchar(64) COLLATE "pg_catalog"."default",
  "founder_type_lv3" varchar(64) COLLATE "pg_catalog"."default",
  "founder_name" varchar(64) COLLATE "pg_catalog"."default",
  "founder_code" varchar(64) COLLATE "pg_catalog"."default",
  "urban_rural_nature" varchar(64) COLLATE "pg_catalog"."default",
  "planning_school_org_form" varchar(64) COLLATE "pg_catalog"."default",
  "planning_school_closure_date" varchar(64) COLLATE "pg_catalog"."default",
  "department_unit_number" varchar(64) COLLATE "pg_catalog"."default",
  "sy_zones" varchar(64) COLLATE "pg_catalog"."default",
  "historical_evolution" text COLLATE "pg_catalog"."default",
  "sy_zones_pro" varchar(64) COLLATE "pg_catalog"."default",
  "primary_planning_school_system" varchar(64) COLLATE "pg_catalog"."default",
  "primary_planning_school_entry_age" varchar(64) COLLATE "pg_catalog"."default",
  "junior_middle_planning_school_system" varchar(64) COLLATE "pg_catalog"."default",
  "junior_middle_planning_school_entry_age" varchar(64) COLLATE "pg_catalog"."default",
  "senior_middle_planning_school_system" varchar(64) COLLATE "pg_catalog"."default",
  "created_uid" int4,
  "updated_uid" int4,
  "created_at" timestamp(6),
  "updated_at" timestamp(6),
  "is_deleted" bool NOT NULL,
  "planning_school_edu_level" varchar(64) COLLATE "pg_catalog"."default",
  "planning_school_category" varchar(64) COLLATE "pg_catalog"."default",
  "process_instance_id" int8,
  "workflow_status" varchar(64) COLLATE "pg_catalog"."default",
  "location_economic_attribute" varchar(64) COLLATE "pg_catalog"."default",
  "urban_ethnic_nature" varchar(64) COLLATE "pg_catalog"."default",
  "leg_repr_certificatenumber" varchar(64) COLLATE "pg_catalog"."default",
  "admin" varchar(64) COLLATE "pg_catalog"."default",
  "admin_phone" varchar(64) COLLATE "pg_catalog"."default",
  "old_planning_school_no" varchar(64) COLLATE "pg_catalog"."default",
  "org_center_info" varchar(255) COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "public"."lfun_planning_school"."id" IS 'ID';
COMMENT ON COLUMN "public"."lfun_planning_school"."planning_school_name" IS '学校名称';
COMMENT ON COLUMN "public"."lfun_planning_school"."planning_school_no" IS '学校编号';
COMMENT ON COLUMN "public"."lfun_planning_school"."planning_school_code" IS '园所标识码';
COMMENT ON COLUMN "public"."lfun_planning_school"."planning_school_operation_license_number" IS '办学许可证号';
COMMENT ON COLUMN "public"."lfun_planning_school"."block" IS '地域管辖区,枚举country';
COMMENT ON COLUMN "public"."lfun_planning_school"."borough" IS '行政管辖区,枚举country';
COMMENT ON COLUMN "public"."lfun_planning_school"."province" IS '省份,枚举province';
COMMENT ON COLUMN "public"."lfun_planning_school"."city" IS '城市,枚举city';
COMMENT ON COLUMN "public"."lfun_planning_school"."planning_school_operation_type" IS '办学类型,枚举school_nature_lv3';
COMMENT ON COLUMN "public"."lfun_planning_school"."planning_school_org_type" IS '学校办别';
COMMENT ON COLUMN "public"."lfun_planning_school"."planning_school_level" IS '学校星级';
COMMENT ON COLUMN "public"."lfun_planning_school"."status" IS '状态,枚举planningschool_status';
COMMENT ON COLUMN "public"."lfun_planning_school"."kg_level" IS '星级,枚举kg_level';
COMMENT ON COLUMN "public"."lfun_planning_school"."planning_school_short_name" IS '园所简称';
COMMENT ON COLUMN "public"."lfun_planning_school"."planning_school_en_name" IS '园所英文名称';
COMMENT ON COLUMN "public"."lfun_planning_school"."create_planning_school_date" IS '建校年月';
COMMENT ON COLUMN "public"."lfun_planning_school"."social_credit_code" IS '统一社会信用代码';
COMMENT ON COLUMN "public"."lfun_planning_school"."founder_type" IS '枚举founder_type';
COMMENT ON COLUMN "public"."lfun_planning_school"."founder_type_lv2" IS '举办者类型二级,枚举founder_type_lv2';
COMMENT ON COLUMN "public"."lfun_planning_school"."founder_type_lv3" IS '举办者类型三级,枚举founder_type_lv3';
COMMENT ON COLUMN "public"."lfun_planning_school"."founder_name" IS '举办者名称';
COMMENT ON COLUMN "public"."lfun_planning_school"."founder_code" IS '举办者识别码';
COMMENT ON COLUMN "public"."lfun_planning_school"."urban_rural_nature" IS '城乡性质,枚举urban_rural_nature';
COMMENT ON COLUMN "public"."lfun_planning_school"."planning_school_org_form" IS '办学组织形式';
COMMENT ON COLUMN "public"."lfun_planning_school"."planning_school_closure_date" IS '学校关闭日期';
COMMENT ON COLUMN "public"."lfun_planning_school"."department_unit_number" IS '属地管理行政部门单位号';
COMMENT ON COLUMN "public"."lfun_planning_school"."sy_zones" IS '属地管理行政部门所在地地区';
COMMENT ON COLUMN "public"."lfun_planning_school"."historical_evolution" IS '历史沿革';
COMMENT ON COLUMN "public"."lfun_planning_school"."sy_zones_pro" IS '属地管理教育行政部门所在地（省级）';
COMMENT ON COLUMN "public"."lfun_planning_school"."primary_planning_school_system" IS '小学学制';
COMMENT ON COLUMN "public"."lfun_planning_school"."primary_planning_school_entry_age" IS '小学入学年龄';
COMMENT ON COLUMN "public"."lfun_planning_school"."junior_middle_planning_school_system" IS '初中学制';
COMMENT ON COLUMN "public"."lfun_planning_school"."junior_middle_planning_school_entry_age" IS '初中入学年龄';
COMMENT ON COLUMN "public"."lfun_planning_school"."senior_middle_planning_school_system" IS '高中学制';
COMMENT ON COLUMN "public"."lfun_planning_school"."created_uid" IS '创建人';
COMMENT ON COLUMN "public"."lfun_planning_school"."updated_uid" IS '操作人';
COMMENT ON COLUMN "public"."lfun_planning_school"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."lfun_planning_school"."updated_at" IS '更新时间';
COMMENT ON COLUMN "public"."lfun_planning_school"."is_deleted" IS '删除态';
COMMENT ON COLUMN "public"."lfun_planning_school"."planning_school_edu_level" IS '教育层次,枚举school_nature';
COMMENT ON COLUMN "public"."lfun_planning_school"."planning_school_category" IS '学校（机构）类别,枚举school_nature_lv2';
COMMENT ON COLUMN "public"."lfun_planning_school"."process_instance_id" IS '流程ID';
COMMENT ON COLUMN "public"."lfun_planning_school"."workflow_status" IS '工作流审核状态';
COMMENT ON COLUMN "public"."lfun_planning_school"."location_economic_attribute" IS '所属地经济属性,枚举economic_attributes';
COMMENT ON COLUMN "public"."lfun_planning_school"."urban_ethnic_nature" IS '所在地民族属性,枚举ethnic_attributes';
COMMENT ON COLUMN "public"."lfun_planning_school"."leg_repr_certificatenumber" IS '法人证书号';
COMMENT ON COLUMN "public"."lfun_planning_school"."admin" IS '管理员';
COMMENT ON COLUMN "public"."lfun_planning_school"."admin_phone" IS '管理员手机';
COMMENT ON COLUMN "public"."lfun_planning_school"."old_planning_school_no" IS '旧的学校编号(例如一期)';
COMMENT ON COLUMN "public"."lfun_planning_school"."org_center_info" IS '组织中心信息';
COMMENT ON TABLE "public"."lfun_planning_school" IS '规划校';

-- ----------------------------
-- Table structure for lfun_planning_school_communications
-- ----------------------------
DROP TABLE IF EXISTS "public"."lfun_planning_school_communications";
CREATE TABLE "public"."lfun_planning_school_communications" (
  "id" int8 NOT NULL DEFAULT nextval('lfun_planning_school_communications_id_seq'::regclass),
  "planning_school_id" int8,
  "postal_code" varchar(64) COLLATE "pg_catalog"."default",
  "fax_number" varchar(64) COLLATE "pg_catalog"."default",
  "email" varchar(64) COLLATE "pg_catalog"."default",
  "school_web_url" varchar(1000) COLLATE "pg_catalog"."default",
  "related_license_upload" varchar(64) COLLATE "pg_catalog"."default",
  "detailed_address" varchar(64) COLLATE "pg_catalog"."default",
  "contact_number" varchar(64) COLLATE "pg_catalog"."default",
  "area_code" varchar(64) COLLATE "pg_catalog"."default",
  "long" varchar(64) COLLATE "pg_catalog"."default",
  "lat" varchar(64) COLLATE "pg_catalog"."default",
  "leg_repr_name" varchar(64) COLLATE "pg_catalog"."default",
  "party_leader_name" varchar(64) COLLATE "pg_catalog"."default",
  "party_leader_position" varchar(64) COLLATE "pg_catalog"."default",
  "adm_leader_name" varchar(64) COLLATE "pg_catalog"."default",
  "adm_leader_position" varchar(64) COLLATE "pg_catalog"."default",
  "loc_area" varchar(64) COLLATE "pg_catalog"."default",
  "loc_area_pro" varchar(64) COLLATE "pg_catalog"."default",
  "created_uid" int4,
  "updated_uid" int4,
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL,
  "is_deleted" bool NOT NULL
)
;
COMMENT ON COLUMN "public"."lfun_planning_school_communications"."id" IS 'ID';
COMMENT ON COLUMN "public"."lfun_planning_school_communications"."planning_school_id" IS '规划校id';
COMMENT ON COLUMN "public"."lfun_planning_school_communications"."postal_code" IS '邮政编码';
COMMENT ON COLUMN "public"."lfun_planning_school_communications"."fax_number" IS '传真电话';
COMMENT ON COLUMN "public"."lfun_planning_school_communications"."email" IS '单位电子信箱';
COMMENT ON COLUMN "public"."lfun_planning_school_communications"."school_web_url" IS '校园网域名';
COMMENT ON COLUMN "public"."lfun_planning_school_communications"."related_license_upload" IS '相关证照上传';
COMMENT ON COLUMN "public"."lfun_planning_school_communications"."detailed_address" IS '园所详细地址';
COMMENT ON COLUMN "public"."lfun_planning_school_communications"."contact_number" IS '联系电话';
COMMENT ON COLUMN "public"."lfun_planning_school_communications"."area_code" IS '电话区号';
COMMENT ON COLUMN "public"."lfun_planning_school_communications"."long" IS '所在经度';
COMMENT ON COLUMN "public"."lfun_planning_school_communications"."lat" IS '所在纬度';
COMMENT ON COLUMN "public"."lfun_planning_school_communications"."leg_repr_name" IS '法定代表人姓名';
COMMENT ON COLUMN "public"."lfun_planning_school_communications"."party_leader_name" IS '党组织负责人姓名';
COMMENT ON COLUMN "public"."lfun_planning_school_communications"."party_leader_position" IS '党组织负责人职务';
COMMENT ON COLUMN "public"."lfun_planning_school_communications"."adm_leader_name" IS '行政负责人姓名';
COMMENT ON COLUMN "public"."lfun_planning_school_communications"."adm_leader_position" IS '行政负责人职务';
COMMENT ON COLUMN "public"."lfun_planning_school_communications"."loc_area" IS '园所所在地区';
COMMENT ON COLUMN "public"."lfun_planning_school_communications"."loc_area_pro" IS '园所所在地(省级)';
COMMENT ON COLUMN "public"."lfun_planning_school_communications"."created_uid" IS '创建人';
COMMENT ON COLUMN "public"."lfun_planning_school_communications"."updated_uid" IS '操作人';
COMMENT ON COLUMN "public"."lfun_planning_school_communications"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."lfun_planning_school_communications"."updated_at" IS '更新时间';
COMMENT ON COLUMN "public"."lfun_planning_school_communications"."is_deleted" IS '删除态';
COMMENT ON TABLE "public"."lfun_planning_school_communications" IS '规划校通信表';

-- ----------------------------
-- Table structure for lfun_planning_school_eduinfo
-- ----------------------------
DROP TABLE IF EXISTS "public"."lfun_planning_school_eduinfo";
CREATE TABLE "public"."lfun_planning_school_eduinfo" (
  "id" int8 NOT NULL DEFAULT nextval('lfun_planning_school_eduinfo_id_seq'::regclass),
  "planning_school_id" int8,
  "is_ethnic_school" bool NOT NULL,
  "is_att_class" bool NOT NULL,
  "att_class_type" varchar(64) COLLATE "pg_catalog"."default",
  "is_province_feat" bool NOT NULL,
  "is_bilingual_clas" bool NOT NULL,
  "minority_lang_code" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "is_profitable" bool NOT NULL,
  "prof_org_name" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "is_prov_demo" bool NOT NULL,
  "is_latest_year" bool NOT NULL,
  "is_town_kinderg" bool NOT NULL,
  "is_incl_kinderg" bool NOT NULL,
  "is_affil_school" bool NOT NULL,
  "affil_univ_code" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "affil_univ_name" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "is_last_yr_revok" bool NOT NULL,
  "is_school_counted" bool NOT NULL,
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL,
  "created_uid" int4,
  "updated_uid" int4,
  "is_deleted" bool NOT NULL
)
;
COMMENT ON COLUMN "public"."lfun_planning_school_eduinfo"."id" IS 'ID';
COMMENT ON COLUMN "public"."lfun_planning_school_eduinfo"."planning_school_id" IS '规划校id';
COMMENT ON COLUMN "public"."lfun_planning_school_eduinfo"."is_ethnic_school" IS '是否民族校';
COMMENT ON COLUMN "public"."lfun_planning_school_eduinfo"."is_att_class" IS '是否附设班';
COMMENT ON COLUMN "public"."lfun_planning_school_eduinfo"."att_class_type" IS '附设班类型';
COMMENT ON COLUMN "public"."lfun_planning_school_eduinfo"."is_province_feat" IS '是否省特色';
COMMENT ON COLUMN "public"."lfun_planning_school_eduinfo"."is_bilingual_clas" IS '是否具有双语教学班';
COMMENT ON COLUMN "public"."lfun_planning_school_eduinfo"."minority_lang_code" IS '少数民族语言编码';
COMMENT ON COLUMN "public"."lfun_planning_school_eduinfo"."is_profitable" IS '是否营利性';
COMMENT ON COLUMN "public"."lfun_planning_school_eduinfo"."prof_org_name" IS '营利性机构名称';
COMMENT ON COLUMN "public"."lfun_planning_school_eduinfo"."is_prov_demo" IS '是否省示范';
COMMENT ON COLUMN "public"."lfun_planning_school_eduinfo"."is_latest_year" IS '是否最新年份';
COMMENT ON COLUMN "public"."lfun_planning_school_eduinfo"."is_town_kinderg" IS '是否乡镇幼儿园';
COMMENT ON COLUMN "public"."lfun_planning_school_eduinfo"."is_incl_kinderg" IS '是否普惠性幼儿园';
COMMENT ON COLUMN "public"."lfun_planning_school_eduinfo"."is_affil_school" IS '是否附属学校';
COMMENT ON COLUMN "public"."lfun_planning_school_eduinfo"."affil_univ_code" IS '附属于高校（机构）标识码';
COMMENT ON COLUMN "public"."lfun_planning_school_eduinfo"."affil_univ_name" IS '附属于高校（机构）名称';
COMMENT ON COLUMN "public"."lfun_planning_school_eduinfo"."is_last_yr_revok" IS '是否上年撤销';
COMMENT ON COLUMN "public"."lfun_planning_school_eduinfo"."is_school_counted" IS '是否计校数';
COMMENT ON COLUMN "public"."lfun_planning_school_eduinfo"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."lfun_planning_school_eduinfo"."updated_at" IS '更新时间';
COMMENT ON COLUMN "public"."lfun_planning_school_eduinfo"."created_uid" IS '创建人';
COMMENT ON COLUMN "public"."lfun_planning_school_eduinfo"."updated_uid" IS '操作人';
COMMENT ON COLUMN "public"."lfun_planning_school_eduinfo"."is_deleted" IS '删除态';
COMMENT ON TABLE "public"."lfun_planning_school_eduinfo" IS '规划校教学信息表';

-- ----------------------------
-- Table structure for lfun_research_achievements
-- ----------------------------
DROP TABLE IF EXISTS "public"."lfun_research_achievements";
CREATE TABLE "public"."lfun_research_achievements" (
  "research_achievements_id" int8 NOT NULL DEFAULT nextval('lfun_research_achievements_research_achievements_id_seq'::regclass),
  "teacher_id" int8 NOT NULL,
  "research_achievement_type" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "type" varchar(64) COLLATE "pg_catalog"."default",
  "representative_or_project" bool,
  "name" varchar(64) COLLATE "pg_catalog"."default",
  "disciplinary_field" varchar(64) COLLATE "pg_catalog"."default",
  "role" varchar(64) COLLATE "pg_catalog"."default",
  "research_date" "sys"."date",
  "approval_number" varchar(64) COLLATE "pg_catalog"."default",
  "funding_amount" varchar(64) COLLATE "pg_catalog"."default",
  "start_year_month" "sys"."date",
  "end_date" "sys"."date",
  "ranking" varchar(64) COLLATE "pg_catalog"."default",
  "entrusting_unit" varchar(64) COLLATE "pg_catalog"."default",
  "source" varchar(64) COLLATE "pg_catalog"."default",
  "publisher_name" varchar(64) COLLATE "pg_catalog"."default",
  "publication_number" varchar(64) COLLATE "pg_catalog"."default",
  "total_words" int4,
  "self_written_words" int4,
  "journal_name" varchar(64) COLLATE "pg_catalog"."default",
  "volume_number" int4,
  "issue_number" int4,
  "indexing_status" varchar(64) COLLATE "pg_catalog"."default",
  "start_page" int4,
  "end_page" int4,
  "personal_rank" varchar(64) COLLATE "pg_catalog"."default",
  "research_level" varchar(64) COLLATE "pg_catalog"."default",
  "other_level" varchar(64) COLLATE "pg_catalog"."default",
  "authorized_country" varchar(64) COLLATE "pg_catalog"."default",
  "authorized_organization" varchar(64) COLLATE "pg_catalog"."default",
  "completion_location" varchar(64) COLLATE "pg_catalog"."default",
  "work_description" varchar(64) COLLATE "pg_catalog"."default",
  "patent_number" varchar(64) COLLATE "pg_catalog"."default",
  "entrusting_party" varchar(64) COLLATE "pg_catalog"."default",
  "certificate_number" varchar(64) COLLATE "pg_catalog"."default",
  "validity_period" varchar(64) COLLATE "pg_catalog"."default",
  "standard_number" varchar(64) COLLATE "pg_catalog"."default",
  "publishing_organization" varchar(64) COLLATE "pg_catalog"."default",
  "is_deleted" bool NOT NULL,
  "report_name" varchar(64) COLLATE "pg_catalog"."default",
  "report_date" "sys"."date",
  "publish_date" "sys"."date"
)
;
COMMENT ON COLUMN "public"."lfun_research_achievements"."research_achievements_id" IS 'research_achievementsID';
COMMENT ON COLUMN "public"."lfun_research_achievements"."teacher_id" IS '教师ID';
COMMENT ON COLUMN "public"."lfun_research_achievements"."research_achievement_type" IS '科研成果种类';
COMMENT ON COLUMN "public"."lfun_research_achievements"."type" IS '类型';
COMMENT ON COLUMN "public"."lfun_research_achievements"."representative_or_project" IS '是否代表性成果或项目';
COMMENT ON COLUMN "public"."lfun_research_achievements"."name" IS '名称';
COMMENT ON COLUMN "public"."lfun_research_achievements"."disciplinary_field" IS '学科领域';
COMMENT ON COLUMN "public"."lfun_research_achievements"."role" IS '本人角色';
COMMENT ON COLUMN "public"."lfun_research_achievements"."research_date" IS '日期';
COMMENT ON COLUMN "public"."lfun_research_achievements"."approval_number" IS '批准号';
COMMENT ON COLUMN "public"."lfun_research_achievements"."funding_amount" IS '经费额度';
COMMENT ON COLUMN "public"."lfun_research_achievements"."start_year_month" IS '开始年月';
COMMENT ON COLUMN "public"."lfun_research_achievements"."end_date" IS '结束日期';
COMMENT ON COLUMN "public"."lfun_research_achievements"."ranking" IS '本人排名';
COMMENT ON COLUMN "public"."lfun_research_achievements"."entrusting_unit" IS '委托单位';
COMMENT ON COLUMN "public"."lfun_research_achievements"."source" IS '来源';
COMMENT ON COLUMN "public"."lfun_research_achievements"."publisher_name" IS '出版社名称';
COMMENT ON COLUMN "public"."lfun_research_achievements"."publication_number" IS '出版号';
COMMENT ON COLUMN "public"."lfun_research_achievements"."total_words" IS '总字数';
COMMENT ON COLUMN "public"."lfun_research_achievements"."self_written_words" IS '本人撰写字数';
COMMENT ON COLUMN "public"."lfun_research_achievements"."journal_name" IS '发表刊物名称';
COMMENT ON COLUMN "public"."lfun_research_achievements"."volume_number" IS '卷号';
COMMENT ON COLUMN "public"."lfun_research_achievements"."issue_number" IS '期号';
COMMENT ON COLUMN "public"."lfun_research_achievements"."indexing_status" IS '论文收录情况枚举indexing_status_lv1';
COMMENT ON COLUMN "public"."lfun_research_achievements"."start_page" IS '起始页码';
COMMENT ON COLUMN "public"."lfun_research_achievements"."end_page" IS '结束页码';
COMMENT ON COLUMN "public"."lfun_research_achievements"."personal_rank" IS '本人排名枚举personal_rank_lv1';
COMMENT ON COLUMN "public"."lfun_research_achievements"."research_level" IS '等级';
COMMENT ON COLUMN "public"."lfun_research_achievements"."other_level" IS '其他等级';
COMMENT ON COLUMN "public"."lfun_research_achievements"."authorized_country" IS '授权国家';
COMMENT ON COLUMN "public"."lfun_research_achievements"."authorized_organization" IS '授权单位';
COMMENT ON COLUMN "public"."lfun_research_achievements"."completion_location" IS '完成地点';
COMMENT ON COLUMN "public"."lfun_research_achievements"."work_description" IS '本人工作描述';
COMMENT ON COLUMN "public"."lfun_research_achievements"."patent_number" IS '专利号';
COMMENT ON COLUMN "public"."lfun_research_achievements"."entrusting_party" IS '委托方';
COMMENT ON COLUMN "public"."lfun_research_achievements"."certificate_number" IS '证书号';
COMMENT ON COLUMN "public"."lfun_research_achievements"."validity_period" IS '有效期';
COMMENT ON COLUMN "public"."lfun_research_achievements"."standard_number" IS '标准号';
COMMENT ON COLUMN "public"."lfun_research_achievements"."publishing_organization" IS '发布单位';
COMMENT ON COLUMN "public"."lfun_research_achievements"."is_deleted" IS '是否删除';
COMMENT ON COLUMN "public"."lfun_research_achievements"."report_name" IS '报告名称';
COMMENT ON COLUMN "public"."lfun_research_achievements"."report_date" IS '报告日期';
COMMENT ON COLUMN "public"."lfun_research_achievements"."publish_date" IS '发布日期';
COMMENT ON TABLE "public"."lfun_research_achievements" IS 'research_achievements信息表';

-- ----------------------------
-- Table structure for lfun_school
-- ----------------------------
DROP TABLE IF EXISTS "public"."lfun_school";
CREATE TABLE "public"."lfun_school" (
  "id" int8 NOT NULL DEFAULT nextval('lfun_school_id_seq'::regclass),
  "planning_school_id" int8,
  "school_name" varchar(64) COLLATE "pg_catalog"."default",
  "school_no" varchar(64) COLLATE "pg_catalog"."default",
  "school_code" varchar(64) COLLATE "pg_catalog"."default",
  "school_operation_license_number" varchar(64) COLLATE "pg_catalog"."default",
  "block" varchar(64) COLLATE "pg_catalog"."default",
  "borough" varchar(64) COLLATE "pg_catalog"."default",
  "school_operation_type" varchar(64) COLLATE "pg_catalog"."default",
  "school_org_type" varchar(64) COLLATE "pg_catalog"."default",
  "school_level" varchar(64) COLLATE "pg_catalog"."default",
  "status" varchar(64) COLLATE "pg_catalog"."default",
  "kg_level" varchar(64) COLLATE "pg_catalog"."default",
  "school_short_name" varchar(64) COLLATE "pg_catalog"."default",
  "school_en_name" varchar(64) COLLATE "pg_catalog"."default",
  "create_school_date" varchar(64) COLLATE "pg_catalog"."default",
  "social_credit_code" varchar(64) COLLATE "pg_catalog"."default",
  "founder_type" varchar(64) COLLATE "pg_catalog"."default",
  "founder_type_lv2" varchar(64) COLLATE "pg_catalog"."default",
  "founder_type_lv3" varchar(64) COLLATE "pg_catalog"."default",
  "founder_name" varchar(64) COLLATE "pg_catalog"."default",
  "founder_code" varchar(64) COLLATE "pg_catalog"."default",
  "urban_rural_nature" varchar(64) COLLATE "pg_catalog"."default",
  "school_org_form" varchar(64) COLLATE "pg_catalog"."default",
  "school_closure_date" varchar(64) COLLATE "pg_catalog"."default",
  "department_unit_number" varchar(64) COLLATE "pg_catalog"."default",
  "sy_zones" varchar(64) COLLATE "pg_catalog"."default",
  "historical_evolution" text COLLATE "pg_catalog"."default",
  "sy_zones_pro" varchar(64) COLLATE "pg_catalog"."default",
  "primary_school_system" varchar(64) COLLATE "pg_catalog"."default",
  "primary_school_entry_age" varchar(10) COLLATE "pg_catalog"."default",
  "junior_middle_school_system" varchar(10) COLLATE "pg_catalog"."default",
  "junior_middle_school_entry_age" varchar(10) COLLATE "pg_catalog"."default",
  "senior_middle_school_system" varchar(10) COLLATE "pg_catalog"."default",
  "created_uid" int4,
  "updated_uid" int4,
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL,
  "is_deleted" bool NOT NULL,
  "school_edu_level" varchar(64) COLLATE "pg_catalog"."default",
  "school_category" varchar(64) COLLATE "pg_catalog"."default",
  "process_instance_id" int8,
  "workflow_status" varchar(64) COLLATE "pg_catalog"."default",
  "location_economic_attribute" varchar(64) COLLATE "pg_catalog"."default",
  "urban_ethnic_nature" varchar(64) COLLATE "pg_catalog"."default",
  "leg_repr_certificatenumber" varchar(64) COLLATE "pg_catalog"."default",
  "institution_category" varchar(64) COLLATE "pg_catalog"."default",
  "membership_no" varchar(64) COLLATE "pg_catalog"."default",
  "is_entity" bool,
  "admin" varchar(64) COLLATE "pg_catalog"."default",
  "admin_phone" varchar(64) COLLATE "pg_catalog"."default",
  "is_master" bool,
  "org_center_info" varchar(255) COLLATE "pg_catalog"."default",
  "old_school_no" varchar(64) COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "public"."lfun_school"."id" IS 'ID';
COMMENT ON COLUMN "public"."lfun_school"."planning_school_id" IS '规划校id';
COMMENT ON COLUMN "public"."lfun_school"."school_name" IS '学校名称';
COMMENT ON COLUMN "public"."lfun_school"."school_no" IS '学校编号';
COMMENT ON COLUMN "public"."lfun_school"."school_code" IS '学校标识码';
COMMENT ON COLUMN "public"."lfun_school"."school_operation_license_number" IS '办学许可证号';
COMMENT ON COLUMN "public"."lfun_school"."block" IS '地域管辖区';
COMMENT ON COLUMN "public"."lfun_school"."borough" IS '行政管辖区';
COMMENT ON COLUMN "public"."lfun_school"."school_operation_type" IS '办学类型';
COMMENT ON COLUMN "public"."lfun_school"."school_org_type" IS '学校办别';
COMMENT ON COLUMN "public"."lfun_school"."school_level" IS '学校星级';
COMMENT ON COLUMN "public"."lfun_school"."status" IS '状态';
COMMENT ON COLUMN "public"."lfun_school"."kg_level" IS '星级';
COMMENT ON COLUMN "public"."lfun_school"."school_short_name" IS '园所简称';
COMMENT ON COLUMN "public"."lfun_school"."school_en_name" IS '园所英文名称';
COMMENT ON COLUMN "public"."lfun_school"."create_school_date" IS '建校年月';
COMMENT ON COLUMN "public"."lfun_school"."social_credit_code" IS '统一社会信用代码';
COMMENT ON COLUMN "public"."lfun_school"."founder_type" IS '举办者类型';
COMMENT ON COLUMN "public"."lfun_school"."founder_type_lv2" IS '举办者类型二级';
COMMENT ON COLUMN "public"."lfun_school"."founder_type_lv3" IS '举办者类型三级';
COMMENT ON COLUMN "public"."lfun_school"."founder_name" IS '举办者名称';
COMMENT ON COLUMN "public"."lfun_school"."founder_code" IS '举办者识别码';
COMMENT ON COLUMN "public"."lfun_school"."urban_rural_nature" IS '城乡性质';
COMMENT ON COLUMN "public"."lfun_school"."school_org_form" IS '办学组织形式,枚举school_org_form';
COMMENT ON COLUMN "public"."lfun_school"."school_closure_date" IS '学校关闭日期';
COMMENT ON COLUMN "public"."lfun_school"."department_unit_number" IS '属地管理行政部门单位号';
COMMENT ON COLUMN "public"."lfun_school"."sy_zones" IS '属地管理行政部门所在地地区';
COMMENT ON COLUMN "public"."lfun_school"."historical_evolution" IS '历史沿革';
COMMENT ON COLUMN "public"."lfun_school"."sy_zones_pro" IS '属地管理教育行政部门所在地（省级）';
COMMENT ON COLUMN "public"."lfun_school"."primary_school_system" IS '小学学制';
COMMENT ON COLUMN "public"."lfun_school"."primary_school_entry_age" IS '小学入学年龄';
COMMENT ON COLUMN "public"."lfun_school"."junior_middle_school_system" IS '初中学制';
COMMENT ON COLUMN "public"."lfun_school"."junior_middle_school_entry_age" IS '初中入学年龄';
COMMENT ON COLUMN "public"."lfun_school"."senior_middle_school_system" IS '高中学制';
COMMENT ON COLUMN "public"."lfun_school"."created_uid" IS '创建人';
COMMENT ON COLUMN "public"."lfun_school"."updated_uid" IS '操作人';
COMMENT ON COLUMN "public"."lfun_school"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."lfun_school"."updated_at" IS '更新时间';
COMMENT ON COLUMN "public"."lfun_school"."is_deleted" IS '删除态';
COMMENT ON COLUMN "public"."lfun_school"."school_edu_level" IS '教育层次';
COMMENT ON COLUMN "public"."lfun_school"."school_category" IS '学校（机构）类别,枚举school_category';
COMMENT ON COLUMN "public"."lfun_school"."process_instance_id" IS '流程ID';
COMMENT ON COLUMN "public"."lfun_school"."workflow_status" IS '工作流审核状态';
COMMENT ON COLUMN "public"."lfun_school"."location_economic_attribute" IS '所属地经济属性';
COMMENT ON COLUMN "public"."lfun_school"."urban_ethnic_nature" IS '所在地民族属性';
COMMENT ON COLUMN "public"."lfun_school"."leg_repr_certificatenumber" IS '法人证书号';
COMMENT ON COLUMN "public"."lfun_school"."institution_category" IS ' 单位分类';
COMMENT ON COLUMN "public"."lfun_school"."membership_no" IS ' 隶属单位号';
COMMENT ON COLUMN "public"."lfun_school"."is_entity" IS ' 是否实体';
COMMENT ON COLUMN "public"."lfun_school"."admin" IS '管理员';
COMMENT ON COLUMN "public"."lfun_school"."admin_phone" IS '管理员手机';
COMMENT ON COLUMN "public"."lfun_school"."is_master" IS '是否主分校';
COMMENT ON COLUMN "public"."lfun_school"."org_center_info" IS '组织中心信息';
COMMENT ON COLUMN "public"."lfun_school"."old_school_no" IS '旧的学校编号(例如一期)';
COMMENT ON TABLE "public"."lfun_school" IS '学校';

-- ----------------------------
-- Table structure for lfun_school_communications
-- ----------------------------
DROP TABLE IF EXISTS "public"."lfun_school_communications";
CREATE TABLE "public"."lfun_school_communications" (
  "id" int8 NOT NULL DEFAULT nextval('lfun_school_communications_id_seq'::regclass),
  "school_id" int8,
  "postal_code" varchar(64) COLLATE "pg_catalog"."default",
  "fax_number" varchar(64) COLLATE "pg_catalog"."default",
  "email" varchar(64) COLLATE "pg_catalog"."default",
  "school_web_url" varchar(1000) COLLATE "pg_catalog"."default",
  "related_license_upload" varchar(64) COLLATE "pg_catalog"."default",
  "detailed_address" varchar(64) COLLATE "pg_catalog"."default",
  "contact_number" varchar(64) COLLATE "pg_catalog"."default",
  "area_code" varchar(64) COLLATE "pg_catalog"."default",
  "long" varchar(64) COLLATE "pg_catalog"."default",
  "lat" varchar(64) COLLATE "pg_catalog"."default",
  "leg_repr_name" varchar(64) COLLATE "pg_catalog"."default",
  "party_leader_name" varchar(64) COLLATE "pg_catalog"."default",
  "party_leader_position" varchar(64) COLLATE "pg_catalog"."default",
  "adm_leader_name" varchar(64) COLLATE "pg_catalog"."default",
  "adm_leader_position" varchar(64) COLLATE "pg_catalog"."default",
  "loc_area" varchar(64) COLLATE "pg_catalog"."default",
  "loc_area_pro" varchar(64) COLLATE "pg_catalog"."default",
  "created_uid" int4,
  "updated_uid" int4,
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL,
  "is_deleted" bool NOT NULL
)
;
COMMENT ON COLUMN "public"."lfun_school_communications"."id" IS 'ID';
COMMENT ON COLUMN "public"."lfun_school_communications"."school_id" IS '学校id';
COMMENT ON COLUMN "public"."lfun_school_communications"."postal_code" IS '邮政编码';
COMMENT ON COLUMN "public"."lfun_school_communications"."fax_number" IS '传真电话';
COMMENT ON COLUMN "public"."lfun_school_communications"."email" IS '单位电子信箱';
COMMENT ON COLUMN "public"."lfun_school_communications"."school_web_url" IS '校园网域名';
COMMENT ON COLUMN "public"."lfun_school_communications"."related_license_upload" IS '相关证照上传';
COMMENT ON COLUMN "public"."lfun_school_communications"."detailed_address" IS '园所详细地址';
COMMENT ON COLUMN "public"."lfun_school_communications"."contact_number" IS '联系电话';
COMMENT ON COLUMN "public"."lfun_school_communications"."area_code" IS '电话区号';
COMMENT ON COLUMN "public"."lfun_school_communications"."long" IS '所在经度';
COMMENT ON COLUMN "public"."lfun_school_communications"."lat" IS '所在纬度';
COMMENT ON COLUMN "public"."lfun_school_communications"."leg_repr_name" IS '法定代表人姓名';
COMMENT ON COLUMN "public"."lfun_school_communications"."party_leader_name" IS '党组织负责人姓名';
COMMENT ON COLUMN "public"."lfun_school_communications"."party_leader_position" IS '党组织负责人职务';
COMMENT ON COLUMN "public"."lfun_school_communications"."adm_leader_name" IS '行政负责人姓名';
COMMENT ON COLUMN "public"."lfun_school_communications"."adm_leader_position" IS '行政负责人职务';
COMMENT ON COLUMN "public"."lfun_school_communications"."loc_area" IS '园所所在地区';
COMMENT ON COLUMN "public"."lfun_school_communications"."loc_area_pro" IS '园所所在地(省级)';
COMMENT ON COLUMN "public"."lfun_school_communications"."created_uid" IS '创建人';
COMMENT ON COLUMN "public"."lfun_school_communications"."updated_uid" IS '操作人';
COMMENT ON COLUMN "public"."lfun_school_communications"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."lfun_school_communications"."updated_at" IS '更新时间';
COMMENT ON COLUMN "public"."lfun_school_communications"."is_deleted" IS '删除态';
COMMENT ON TABLE "public"."lfun_school_communications" IS '学校通信表';

-- ----------------------------
-- Table structure for lfun_school_eduinfo
-- ----------------------------
DROP TABLE IF EXISTS "public"."lfun_school_eduinfo";
CREATE TABLE "public"."lfun_school_eduinfo" (
  "id" int8 NOT NULL DEFAULT nextval('lfun_school_eduinfo_id_seq'::regclass),
  "school_id" int8,
  "is_ethnic_school" bool,
  "is_att_class" bool,
  "att_class_type" varchar(64) COLLATE "pg_catalog"."default",
  "is_province_feat" bool,
  "is_bilingual_clas" bool,
  "minority_lang_code" varchar(64) COLLATE "pg_catalog"."default",
  "is_profitable" bool,
  "prof_org_name" varchar(64) COLLATE "pg_catalog"."default",
  "is_prov_demo" bool,
  "is_latest_year" bool,
  "is_town_kinderg" bool,
  "is_incl_kinderg" bool,
  "is_affil_school" bool,
  "affil_univ_code" varchar(64) COLLATE "pg_catalog"."default",
  "affil_univ_name" varchar(64) COLLATE "pg_catalog"."default",
  "is_last_yr_revok" bool,
  "is_school_counted" bool,
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL,
  "created_uid" int4,
  "updated_uid" int4,
  "is_deleted" bool NOT NULL
)
;
COMMENT ON COLUMN "public"."lfun_school_eduinfo"."id" IS 'ID';
COMMENT ON COLUMN "public"."lfun_school_eduinfo"."school_id" IS '学校id';
COMMENT ON COLUMN "public"."lfun_school_eduinfo"."is_ethnic_school" IS '是否民族校';
COMMENT ON COLUMN "public"."lfun_school_eduinfo"."is_att_class" IS '是否附设班';
COMMENT ON COLUMN "public"."lfun_school_eduinfo"."att_class_type" IS '附设班类型';
COMMENT ON COLUMN "public"."lfun_school_eduinfo"."is_province_feat" IS '是否省特色';
COMMENT ON COLUMN "public"."lfun_school_eduinfo"."is_bilingual_clas" IS '是否具有双语教学班';
COMMENT ON COLUMN "public"."lfun_school_eduinfo"."minority_lang_code" IS '少数民族语言编码';
COMMENT ON COLUMN "public"."lfun_school_eduinfo"."is_profitable" IS '是否营利性';
COMMENT ON COLUMN "public"."lfun_school_eduinfo"."prof_org_name" IS '营利性机构名称';
COMMENT ON COLUMN "public"."lfun_school_eduinfo"."is_prov_demo" IS '是否省示范';
COMMENT ON COLUMN "public"."lfun_school_eduinfo"."is_latest_year" IS '是否最新年份';
COMMENT ON COLUMN "public"."lfun_school_eduinfo"."is_town_kinderg" IS '是否乡镇幼儿园';
COMMENT ON COLUMN "public"."lfun_school_eduinfo"."is_incl_kinderg" IS '是否普惠性幼儿园';
COMMENT ON COLUMN "public"."lfun_school_eduinfo"."is_affil_school" IS '是否附属学校';
COMMENT ON COLUMN "public"."lfun_school_eduinfo"."affil_univ_code" IS '附属于高校（机构）标识码';
COMMENT ON COLUMN "public"."lfun_school_eduinfo"."affil_univ_name" IS '附属于高校（机构）名称';
COMMENT ON COLUMN "public"."lfun_school_eduinfo"."is_last_yr_revok" IS '是否上年撤销';
COMMENT ON COLUMN "public"."lfun_school_eduinfo"."is_school_counted" IS '是否计校数';
COMMENT ON COLUMN "public"."lfun_school_eduinfo"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."lfun_school_eduinfo"."updated_at" IS '更新时间';
COMMENT ON COLUMN "public"."lfun_school_eduinfo"."created_uid" IS '创建人';
COMMENT ON COLUMN "public"."lfun_school_eduinfo"."updated_uid" IS '操作人';
COMMENT ON COLUMN "public"."lfun_school_eduinfo"."is_deleted" IS '删除态';
COMMENT ON TABLE "public"."lfun_school_eduinfo" IS '学校教学信息表';

-- ----------------------------
-- Table structure for lfun_student_family_info
-- ----------------------------
DROP TABLE IF EXISTS "public"."lfun_student_family_info";
CREATE TABLE "public"."lfun_student_family_info" (
  "student_family_info_id" int8 NOT NULL DEFAULT nextval('lfun_student_family_info_student_family_info_id_seq'::regclass),
  "student_id" int8 NOT NULL,
  "name" varchar(64) COLLATE "pg_catalog"."default",
  "gender" varchar(64) COLLATE "pg_catalog"."default",
  "relationship" varchar(64) COLLATE "pg_catalog"."default",
  "is_guardian" bool,
  "identification_type" varchar(64) COLLATE "pg_catalog"."default",
  "identification_number" varchar(64) COLLATE "pg_catalog"."default",
  "birthday" "sys"."date",
  "phone_number" varchar(64) COLLATE "pg_catalog"."default",
  "ethnicity" varchar(64) COLLATE "pg_catalog"."default",
  "health_status" varchar(64) COLLATE "pg_catalog"."default",
  "nationality" varchar(64) COLLATE "pg_catalog"."default",
  "political_status" varchar(64) COLLATE "pg_catalog"."default",
  "contact_address" varchar(64) COLLATE "pg_catalog"."default",
  "workplace" varchar(64) COLLATE "pg_catalog"."default",
  "family_member_occupation" varchar(128) COLLATE "pg_catalog"."default",
  "is_deleted" bool NOT NULL,
  "identity" varchar(64) COLLATE "pg_catalog"."default",
  "identity_type" varchar(64) COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "public"."lfun_student_family_info"."student_family_info_id" IS 'ID';
COMMENT ON COLUMN "public"."lfun_student_family_info"."student_id" IS '学生ID';
COMMENT ON COLUMN "public"."lfun_student_family_info"."name" IS '姓名';
COMMENT ON COLUMN "public"."lfun_student_family_info"."gender" IS '性别';
COMMENT ON COLUMN "public"."lfun_student_family_info"."relationship" IS '关系枚举relation';
COMMENT ON COLUMN "public"."lfun_student_family_info"."is_guardian" IS '是否监护人';
COMMENT ON COLUMN "public"."lfun_student_family_info"."identification_type" IS '证件类型';
COMMENT ON COLUMN "public"."lfun_student_family_info"."identification_number" IS '证件号码';
COMMENT ON COLUMN "public"."lfun_student_family_info"."birthday" IS '出生日期';
COMMENT ON COLUMN "public"."lfun_student_family_info"."phone_number" IS '手机号';
COMMENT ON COLUMN "public"."lfun_student_family_info"."ethnicity" IS '民族';
COMMENT ON COLUMN "public"."lfun_student_family_info"."health_status" IS '健康状态';
COMMENT ON COLUMN "public"."lfun_student_family_info"."nationality" IS '国籍';
COMMENT ON COLUMN "public"."lfun_student_family_info"."political_status" IS '政治面貌';
COMMENT ON COLUMN "public"."lfun_student_family_info"."contact_address" IS '联系地址';
COMMENT ON COLUMN "public"."lfun_student_family_info"."workplace" IS '工作单位';
COMMENT ON COLUMN "public"."lfun_student_family_info"."family_member_occupation" IS '家庭成员职业枚举family_member_occupation';
COMMENT ON COLUMN "public"."lfun_student_family_info"."is_deleted" IS '是否删除';
COMMENT ON COLUMN "public"."lfun_student_family_info"."identity" IS '身份';
COMMENT ON COLUMN "public"."lfun_student_family_info"."identity_type" IS '身份类型';
COMMENT ON TABLE "public"."lfun_student_family_info" IS '学生家庭信息模型';

-- ----------------------------
-- Table structure for lfun_student_inner_transaction
-- ----------------------------
DROP TABLE IF EXISTS "public"."lfun_student_inner_transaction";
CREATE TABLE "public"."lfun_student_inner_transaction" (
  "id" int8 NOT NULL DEFAULT nextval('lfun_student_inner_transaction_id_seq'::regclass),
  "student_id" int8,
  "school_id" int8,
  "class_id" varchar(30) COLLATE "pg_catalog"."default",
  "transaction_type" varchar(255) COLLATE "pg_catalog"."default",
  "transaction_reason" varchar(255) COLLATE "pg_catalog"."default",
  "transaction_remark" varchar(255) COLLATE "pg_catalog"."default",
  "transaction_time" timestamp(6) NOT NULL,
  "transaction_user" varchar(255) COLLATE "pg_catalog"."default",
  "transaction_user_id" int4,
  "created_uid" int4,
  "updated_uid" int4,
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL,
  "approval_status" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "is_deleted" bool NOT NULL
)
;
COMMENT ON COLUMN "public"."lfun_student_inner_transaction"."id" IS 'ID';
COMMENT ON COLUMN "public"."lfun_student_inner_transaction"."student_id" IS '学生ID';
COMMENT ON COLUMN "public"."lfun_student_inner_transaction"."school_id" IS '学校ID';
COMMENT ON COLUMN "public"."lfun_student_inner_transaction"."class_id" IS '班级id';
COMMENT ON COLUMN "public"."lfun_student_inner_transaction"."transaction_type" IS '异动类型,枚举transaction_type';
COMMENT ON COLUMN "public"."lfun_student_inner_transaction"."transaction_reason" IS '异动原因';
COMMENT ON COLUMN "public"."lfun_student_inner_transaction"."transaction_remark" IS '备注';
COMMENT ON COLUMN "public"."lfun_student_inner_transaction"."transaction_time" IS '操作时间';
COMMENT ON COLUMN "public"."lfun_student_inner_transaction"."transaction_user" IS '操作人';
COMMENT ON COLUMN "public"."lfun_student_inner_transaction"."transaction_user_id" IS '操作人ID';
COMMENT ON COLUMN "public"."lfun_student_inner_transaction"."created_uid" IS '创建人';
COMMENT ON COLUMN "public"."lfun_student_inner_transaction"."updated_uid" IS '操作人';
COMMENT ON COLUMN "public"."lfun_student_inner_transaction"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."lfun_student_inner_transaction"."updated_at" IS '更新时间';
COMMENT ON COLUMN "public"."lfun_student_inner_transaction"."approval_status" IS '审批状态';
COMMENT ON COLUMN "public"."lfun_student_inner_transaction"."is_deleted" IS '删除态';
COMMENT ON TABLE "public"."lfun_student_inner_transaction" IS '学生校内异动表';

-- ----------------------------
-- Table structure for lfun_student_session
-- ----------------------------
DROP TABLE IF EXISTS "public"."lfun_student_session";
CREATE TABLE "public"."lfun_student_session" (
  "session_id" int8 NOT NULL DEFAULT nextval('lfun_student_session_session_id_seq'::regclass),
  "session_name" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "session_alias" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "session_status" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "school_id" int8,
  "year" varchar(64) COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "public"."lfun_student_session"."session_id" IS '届别ID';
COMMENT ON COLUMN "public"."lfun_student_session"."session_name" IS '届别名称';
COMMENT ON COLUMN "public"."lfun_student_session"."session_alias" IS '届别别名';
COMMENT ON COLUMN "public"."lfun_student_session"."session_status" IS '届别状态';
COMMENT ON COLUMN "public"."lfun_student_session"."school_id" IS '学校id';
COMMENT ON COLUMN "public"."lfun_student_session"."year" IS '年度';
COMMENT ON TABLE "public"."lfun_student_session" IS '学生届别模型';

-- ----------------------------
-- Table structure for lfun_student_temporary_study
-- ----------------------------
DROP TABLE IF EXISTS "public"."lfun_student_temporary_study";
CREATE TABLE "public"."lfun_student_temporary_study" (
  "id" int8 NOT NULL,
  "student_id" int8,
  "student_name" varchar(255) COLLATE "pg_catalog"."default",
  "id_number" varchar(64) COLLATE "pg_catalog"."default",
  "student_gender" varchar(64) COLLATE "pg_catalog"."default",
  "edu_number" varchar(64) COLLATE "pg_catalog"."default",
  "student_no" varchar(255) COLLATE "pg_catalog"."default",
  "school_id" int8,
  "session_id" int8,
  "grade_id" int8,
  "class_id" int8,
  "origin_school_id" int8,
  "origin_session_id" int8,
  "origin_grade_id" int8,
  "origin_class_id" int8,
  "apply_user" varchar(255) COLLATE "pg_catalog"."default",
  "apply_time" varchar(255) COLLATE "pg_catalog"."default",
  "doc_upload" varchar(255) COLLATE "pg_catalog"."default",
  "process_instance_id" int8,
  "reason" varchar(255) COLLATE "pg_catalog"."default",
  "remark" varchar(255) COLLATE "pg_catalog"."default",
  "status" varchar(64) COLLATE "pg_catalog"."default",
  "created_uid" int4,
  "updated_uid" int4,
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL,
  "is_deleted" bool NOT NULL
)
;
COMMENT ON COLUMN "public"."lfun_student_temporary_study"."student_id" IS '学生ID';
COMMENT ON COLUMN "public"."lfun_student_temporary_study"."student_name" IS '学生姓名';
COMMENT ON COLUMN "public"."lfun_student_temporary_study"."id_number" IS '证件号码';
COMMENT ON COLUMN "public"."lfun_student_temporary_study"."student_gender" IS '学生性别';
COMMENT ON COLUMN "public"."lfun_student_temporary_study"."edu_number" IS '学籍号';
COMMENT ON COLUMN "public"."lfun_student_temporary_study"."student_no" IS '学号';
COMMENT ON COLUMN "public"."lfun_student_temporary_study"."school_id" IS '学校ID';
COMMENT ON COLUMN "public"."lfun_student_temporary_study"."session_id" IS '届别id';
COMMENT ON COLUMN "public"."lfun_student_temporary_study"."grade_id" IS '年级ID';
COMMENT ON COLUMN "public"."lfun_student_temporary_study"."class_id" IS '班级id';
COMMENT ON COLUMN "public"."lfun_student_temporary_study"."origin_school_id" IS '原学校ID';
COMMENT ON COLUMN "public"."lfun_student_temporary_study"."origin_session_id" IS '原届别id';
COMMENT ON COLUMN "public"."lfun_student_temporary_study"."origin_grade_id" IS '原年级ID';
COMMENT ON COLUMN "public"."lfun_student_temporary_study"."origin_class_id" IS '原班级id';
COMMENT ON COLUMN "public"."lfun_student_temporary_study"."apply_user" IS '申请人';
COMMENT ON COLUMN "public"."lfun_student_temporary_study"."apply_time" IS '申请时间';
COMMENT ON COLUMN "public"."lfun_student_temporary_study"."doc_upload" IS '附件';
COMMENT ON COLUMN "public"."lfun_student_temporary_study"."process_instance_id" IS '流程ID';
COMMENT ON COLUMN "public"."lfun_student_temporary_study"."reason" IS '原因';
COMMENT ON COLUMN "public"."lfun_student_temporary_study"."remark" IS '备注';
COMMENT ON COLUMN "public"."lfun_student_temporary_study"."status" IS '状态';
COMMENT ON COLUMN "public"."lfun_student_temporary_study"."created_uid" IS '创建人';
COMMENT ON COLUMN "public"."lfun_student_temporary_study"."updated_uid" IS '操作人';
COMMENT ON COLUMN "public"."lfun_student_temporary_study"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."lfun_student_temporary_study"."updated_at" IS '更新时间';
COMMENT ON COLUMN "public"."lfun_student_temporary_study"."is_deleted" IS '删除态';
COMMENT ON TABLE "public"."lfun_student_temporary_study" IS '临时就读表';

-- ----------------------------
-- Table structure for lfun_student_transaction
-- ----------------------------
DROP TABLE IF EXISTS "public"."lfun_student_transaction";
CREATE TABLE "public"."lfun_student_transaction" (
  "id" int8 NOT NULL DEFAULT nextval('lfun_student_transaction_id_seq'::regclass),
  "school_name" varchar(255) COLLATE "pg_catalog"."default",
  "grade_name" varchar(255) COLLATE "pg_catalog"."default",
  "classes" varchar(255) COLLATE "pg_catalog"."default",
  "transfer_time" varchar(255) COLLATE "pg_catalog"."default",
  "transfer_reason" varchar(255) COLLATE "pg_catalog"."default",
  "doc_upload" varchar(255) COLLATE "pg_catalog"."default",
  "student_id" int8,
  "student_no" varchar(255) COLLATE "pg_catalog"."default",
  "student_name" varchar(255) COLLATE "pg_catalog"."default",
  "current_org" varchar(255) COLLATE "pg_catalog"."default",
  "apply_user" varchar(255) COLLATE "pg_catalog"."default",
  "apply_time" varchar(255) COLLATE "pg_catalog"."default",
  "school_id" int8,
  "relation_id" int8,
  "transaction_type" varchar(30) COLLATE "pg_catalog"."default",
  "transaction_type_lv2" varchar(30) COLLATE "pg_catalog"."default",
  "country_no" varchar(255) COLLATE "pg_catalog"."default",
  "reason" varchar(255) COLLATE "pg_catalog"."default",
  "province_id" varchar(30) COLLATE "pg_catalog"."default",
  "city_id" varchar(30) COLLATE "pg_catalog"."default",
  "district_id" varchar(30) COLLATE "pg_catalog"."default",
  "area_id" varchar(30) COLLATE "pg_catalog"."default",
  "direction" varchar(30) COLLATE "pg_catalog"."default",
  "transfer_in_type" varchar(30) COLLATE "pg_catalog"."default",
  "session" varchar(30) COLLATE "pg_catalog"."default",
  "attached_class" varchar(30) COLLATE "pg_catalog"."default",
  "grade_id" varchar(30) COLLATE "pg_catalog"."default",
  "class_id" varchar(30) COLLATE "pg_catalog"."default",
  "major_id" varchar(30) COLLATE "pg_catalog"."default",
  "major_name" varchar(30) COLLATE "pg_catalog"."default",
  "remark" varchar(255) COLLATE "pg_catalog"."default",
  "status" varchar(64) COLLATE "pg_catalog"."default",
  "is_valid" bool NOT NULL,
  "created_uid" int4,
  "updated_uid" int4,
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL,
  "is_deleted" bool NOT NULL,
  "process_instance_id" int8
)
;
COMMENT ON COLUMN "public"."lfun_student_transaction"."id" IS '班级ID';
COMMENT ON COLUMN "public"."lfun_student_transaction"."school_name" IS '学校名称';
COMMENT ON COLUMN "public"."lfun_student_transaction"."grade_name" IS '年级';
COMMENT ON COLUMN "public"."lfun_student_transaction"."classes" IS '班级';
COMMENT ON COLUMN "public"."lfun_student_transaction"."transfer_time" IS '转入/出时间';
COMMENT ON COLUMN "public"."lfun_student_transaction"."transfer_reason" IS '转学原因';
COMMENT ON COLUMN "public"."lfun_student_transaction"."doc_upload" IS '附件';
COMMENT ON COLUMN "public"."lfun_student_transaction"."student_id" IS '学生ID';
COMMENT ON COLUMN "public"."lfun_student_transaction"."student_no" IS '学号';
COMMENT ON COLUMN "public"."lfun_student_transaction"."student_name" IS '学生姓名';
COMMENT ON COLUMN "public"."lfun_student_transaction"."current_org" IS '当前机构';
COMMENT ON COLUMN "public"."lfun_student_transaction"."apply_user" IS '申请人';
COMMENT ON COLUMN "public"."lfun_student_transaction"."apply_time" IS '申请时间';
COMMENT ON COLUMN "public"."lfun_student_transaction"."school_id" IS '学校ID';
COMMENT ON COLUMN "public"."lfun_student_transaction"."relation_id" IS '关联学校ID';
COMMENT ON COLUMN "public"."lfun_student_transaction"."transaction_type" IS '异动类型';
COMMENT ON COLUMN "public"."lfun_student_transaction"."transaction_type_lv2" IS '异动类型2级,枚举transaction_type_lv2';
COMMENT ON COLUMN "public"."lfun_student_transaction"."country_no" IS '国家学籍号码';
COMMENT ON COLUMN "public"."lfun_student_transaction"."reason" IS '转学原因';
COMMENT ON COLUMN "public"."lfun_student_transaction"."province_id" IS '省份';
COMMENT ON COLUMN "public"."lfun_student_transaction"."city_id" IS '市';
COMMENT ON COLUMN "public"."lfun_student_transaction"."district_id" IS '区县';
COMMENT ON COLUMN "public"."lfun_student_transaction"."area_id" IS '区';
COMMENT ON COLUMN "public"."lfun_student_transaction"."direction" IS '出入方向';
COMMENT ON COLUMN "public"."lfun_student_transaction"."transfer_in_type" IS '转入类型';
COMMENT ON COLUMN "public"."lfun_student_transaction"."session" IS '届别';
COMMENT ON COLUMN "public"."lfun_student_transaction"."attached_class" IS '附设班';
COMMENT ON COLUMN "public"."lfun_student_transaction"."grade_id" IS '年级ID';
COMMENT ON COLUMN "public"."lfun_student_transaction"."class_id" IS '班级id';
COMMENT ON COLUMN "public"."lfun_student_transaction"."major_id" IS '专业id';
COMMENT ON COLUMN "public"."lfun_student_transaction"."major_name" IS '专业';
COMMENT ON COLUMN "public"."lfun_student_transaction"."remark" IS '备注';
COMMENT ON COLUMN "public"."lfun_student_transaction"."status" IS '状态';
COMMENT ON COLUMN "public"."lfun_student_transaction"."is_valid" IS '是否有效';
COMMENT ON COLUMN "public"."lfun_student_transaction"."created_uid" IS '创建人';
COMMENT ON COLUMN "public"."lfun_student_transaction"."updated_uid" IS '操作人';
COMMENT ON COLUMN "public"."lfun_student_transaction"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."lfun_student_transaction"."updated_at" IS '更新时间';
COMMENT ON COLUMN "public"."lfun_student_transaction"."is_deleted" IS '删除态';
COMMENT ON COLUMN "public"."lfun_student_transaction"."process_instance_id" IS '流程ID';
COMMENT ON TABLE "public"."lfun_student_transaction" IS '转学休学入学毕业申请表';

-- ----------------------------
-- Table structure for lfun_student_transaction_flow
-- ----------------------------
DROP TABLE IF EXISTS "public"."lfun_student_transaction_flow";
CREATE TABLE "public"."lfun_student_transaction_flow" (
  "id" int4 NOT NULL DEFAULT nextval('lfun_student_transaction_flow_id_seq'::regclass),
  "student_id" int4,
  "apply_id" int4,
  "stage" varchar(255) COLLATE "pg_catalog"."default",
  "description" varchar(600) COLLATE "pg_catalog"."default",
  "remark" varchar(255) COLLATE "pg_catalog"."default",
  "created_uid" int4,
  "updated_uid" int4,
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL,
  "is_deleted" bool NOT NULL
)
;
COMMENT ON COLUMN "public"."lfun_student_transaction_flow"."id" IS '班级ID';
COMMENT ON COLUMN "public"."lfun_student_transaction_flow"."student_id" IS '学生ID';
COMMENT ON COLUMN "public"."lfun_student_transaction_flow"."apply_id" IS '申请ID';
COMMENT ON COLUMN "public"."lfun_student_transaction_flow"."stage" IS '阶段';
COMMENT ON COLUMN "public"."lfun_student_transaction_flow"."description" IS '流程描述';
COMMENT ON COLUMN "public"."lfun_student_transaction_flow"."remark" IS '流程备注';
COMMENT ON COLUMN "public"."lfun_student_transaction_flow"."created_uid" IS '创建人';
COMMENT ON COLUMN "public"."lfun_student_transaction_flow"."updated_uid" IS '操作人';
COMMENT ON COLUMN "public"."lfun_student_transaction_flow"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."lfun_student_transaction_flow"."updated_at" IS '更新时间';
COMMENT ON COLUMN "public"."lfun_student_transaction_flow"."is_deleted" IS '删除态';
COMMENT ON TABLE "public"."lfun_student_transaction_flow" IS '转学休学入学毕业申请流程表';

-- ----------------------------
-- Table structure for lfun_students
-- ----------------------------
DROP TABLE IF EXISTS "public"."lfun_students";
CREATE TABLE "public"."lfun_students" (
  "student_id" int8 NOT NULL DEFAULT nextval('lfun_students_student_id_seq'::regclass),
  "student_name" varchar(64) COLLATE "pg_catalog"."default",
  "student_gender" varchar(64) COLLATE "pg_catalog"."default",
  "enrollment_number" varchar(64) COLLATE "pg_catalog"."default",
  "birthday" "sys"."date",
  "id_type" varchar(64) COLLATE "pg_catalog"."default",
  "id_number" varchar(64) COLLATE "pg_catalog"."default",
  "photo" varchar(64) COLLATE "pg_catalog"."default",
  "approval_status" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "is_deleted" bool NOT NULL
)
;
COMMENT ON COLUMN "public"."lfun_students"."student_id" IS '学生ID';
COMMENT ON COLUMN "public"."lfun_students"."student_name" IS '学生姓名';
COMMENT ON COLUMN "public"."lfun_students"."student_gender" IS '学生性别';
COMMENT ON COLUMN "public"."lfun_students"."enrollment_number" IS '报名号';
COMMENT ON COLUMN "public"."lfun_students"."birthday" IS '生日';
COMMENT ON COLUMN "public"."lfun_students"."id_type" IS '证件类别,枚举id_type';
COMMENT ON COLUMN "public"."lfun_students"."id_number" IS '证件号码';
COMMENT ON COLUMN "public"."lfun_students"."photo" IS '照片';
COMMENT ON COLUMN "public"."lfun_students"."approval_status" IS '状态,枚举student_approval_status';
COMMENT ON COLUMN "public"."lfun_students"."is_deleted" IS '是否删除';
COMMENT ON TABLE "public"."lfun_students" IS '学生表关键信息模型';

-- ----------------------------
-- Table structure for lfun_students_base_info
-- ----------------------------
DROP TABLE IF EXISTS "public"."lfun_students_base_info";
CREATE TABLE "public"."lfun_students_base_info" (
  "student_base_id" int8 NOT NULL DEFAULT nextval('lfun_students_base_info_student_base_id_seq'::regclass),
  "student_id" int8 NOT NULL,
  "name_pinyin" varchar(64) COLLATE "pg_catalog"."default",
  "session" varchar(64) COLLATE "pg_catalog"."default",
  "session_id" int8,
  "edu_number" varchar(64) COLLATE "pg_catalog"."default",
  "student_number" varchar(64) COLLATE "pg_catalog"."default",
  "graduation_type" varchar(10) COLLATE "pg_catalog"."default",
  "graduation_remarks" varchar(255) COLLATE "pg_catalog"."default",
  "credential_notes" varchar(255) COLLATE "pg_catalog"."default",
  "graduation_photo" varchar(255) COLLATE "pg_catalog"."default",
  "grade" varchar(64) COLLATE "pg_catalog"."default",
  "classroom" varchar(64) COLLATE "pg_catalog"."default",
  "class_number" varchar(64) COLLATE "pg_catalog"."default",
  "class_id" int8,
  "grade_id" int8,
  "school_id" int8,
  "school" varchar(64) COLLATE "pg_catalog"."default",
  "registration_date" "sys"."date",
  "residence_address" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "residence_district" varchar(64) COLLATE "pg_catalog"."default",
  "birthplace_district" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "native_place_district" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "religious_belief" varchar(64) COLLATE "pg_catalog"."default",
  "residence_nature" varchar(64) COLLATE "pg_catalog"."default",
  "enrollment_date" "sys"."date",
  "contact_number" varchar(64) COLLATE "pg_catalog"."default",
  "health_condition" varchar(64) COLLATE "pg_catalog"."default",
  "political_status" varchar(64) COLLATE "pg_catalog"."default",
  "ethnicity" varchar(64) COLLATE "pg_catalog"."default",
  "blood_type" varchar(64) COLLATE "pg_catalog"."default",
  "home_phone_number" varchar(64) COLLATE "pg_catalog"."default",
  "email_or_other_contact" varchar(64) COLLATE "pg_catalog"."default",
  "migrant_children" bool,
  "disabled_person" bool,
  "only_child" bool,
  "left_behind_children" bool,
  "floating_population" bool,
  "overseas_chinese" varchar(64) COLLATE "pg_catalog"."default",
  "residence_address_detail" varchar(64) COLLATE "pg_catalog"."default",
  "communication_district" varchar(64) COLLATE "pg_catalog"."default",
  "postal_code" varchar(64) COLLATE "pg_catalog"."default",
  "communication_address" varchar(64) COLLATE "pg_catalog"."default",
  "photo_upload_time" varchar(64) COLLATE "pg_catalog"."default",
  "identity_card_validity_period" varchar(64) COLLATE "pg_catalog"."default",
  "specialty" varchar(64) COLLATE "pg_catalog"."default",
  "permanent_address" varchar(64) COLLATE "pg_catalog"."default",
  "remark" varchar(64) COLLATE "pg_catalog"."default",
  "county" varchar(64) COLLATE "pg_catalog"."default",
  "emporary_borrowing_status" varchar(64) COLLATE "pg_catalog"."default",
  "flow_out_time" varchar(64) COLLATE "pg_catalog"."default",
  "flow_out_reason" varchar(64) COLLATE "pg_catalog"."default",
  "is_deleted" bool NOT NULL,
  "identity" varchar(64) COLLATE "pg_catalog"."default",
  "birth_place" varchar(64) COLLATE "pg_catalog"."default",
  "admission_date" "sys"."date",
  "health_status" varchar(64) COLLATE "pg_catalog"."default",
  "nationality" varchar(64) COLLATE "pg_catalog"."default",
  "enrollment_method" varchar(64) COLLATE "pg_catalog"."default",
  "identity_type" varchar(64) COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "public"."lfun_students_base_info"."student_base_id" IS '主键';
COMMENT ON COLUMN "public"."lfun_students_base_info"."student_id" IS '学生ID';
COMMENT ON COLUMN "public"."lfun_students_base_info"."name_pinyin" IS '姓名拼音';
COMMENT ON COLUMN "public"."lfun_students_base_info"."session" IS '届别';
COMMENT ON COLUMN "public"."lfun_students_base_info"."session_id" IS '届别id';
COMMENT ON COLUMN "public"."lfun_students_base_info"."edu_number" IS '学籍号';
COMMENT ON COLUMN "public"."lfun_students_base_info"."student_number" IS '学号';
COMMENT ON COLUMN "public"."lfun_students_base_info"."graduation_type" IS '毕业类型';
COMMENT ON COLUMN "public"."lfun_students_base_info"."graduation_remarks" IS '毕业备注';
COMMENT ON COLUMN "public"."lfun_students_base_info"."credential_notes" IS '制证备注';
COMMENT ON COLUMN "public"."lfun_students_base_info"."graduation_photo" IS '毕业照';
COMMENT ON COLUMN "public"."lfun_students_base_info"."grade" IS '年级';
COMMENT ON COLUMN "public"."lfun_students_base_info"."classroom" IS '班级';
COMMENT ON COLUMN "public"."lfun_students_base_info"."class_number" IS '班号';
COMMENT ON COLUMN "public"."lfun_students_base_info"."class_id" IS '班级id';
COMMENT ON COLUMN "public"."lfun_students_base_info"."grade_id" IS '年级id';
COMMENT ON COLUMN "public"."lfun_students_base_info"."school_id" IS '学校id';
COMMENT ON COLUMN "public"."lfun_students_base_info"."school" IS '学校';
COMMENT ON COLUMN "public"."lfun_students_base_info"."registration_date" IS '登记日期';
COMMENT ON COLUMN "public"."lfun_students_base_info"."residence_address" IS '户口所在地（详细）';
COMMENT ON COLUMN "public"."lfun_students_base_info"."residence_district" IS '户口所在地new';
COMMENT ON COLUMN "public"."lfun_students_base_info"."native_place_district" IS '籍贯';
COMMENT ON COLUMN "public"."lfun_students_base_info"."religious_belief" IS '宗教信仰,枚举religious_belief';
COMMENT ON COLUMN "public"."lfun_students_base_info"."residence_nature" IS '户口性质';
COMMENT ON COLUMN "public"."lfun_students_base_info"."enrollment_date" IS '入学日期';
COMMENT ON COLUMN "public"."lfun_students_base_info"."contact_number" IS '联系电话';
COMMENT ON COLUMN "public"."lfun_students_base_info"."health_condition" IS '健康状况';
COMMENT ON COLUMN "public"."lfun_students_base_info"."political_status" IS '政治面貌';
COMMENT ON COLUMN "public"."lfun_students_base_info"."ethnicity" IS '民族';
COMMENT ON COLUMN "public"."lfun_students_base_info"."blood_type" IS '血型枚举blood_type';
COMMENT ON COLUMN "public"."lfun_students_base_info"."home_phone_number" IS '家庭电话';
COMMENT ON COLUMN "public"."lfun_students_base_info"."email_or_other_contact" IS '电子信箱/其他联系方式';
COMMENT ON COLUMN "public"."lfun_students_base_info"."migrant_children" IS '是否随迁子女';
COMMENT ON COLUMN "public"."lfun_students_base_info"."disabled_person" IS '是否残疾人';
COMMENT ON COLUMN "public"."lfun_students_base_info"."only_child" IS '是否独生子女';
COMMENT ON COLUMN "public"."lfun_students_base_info"."left_behind_children" IS '是否留守儿童';
COMMENT ON COLUMN "public"."lfun_students_base_info"."floating_population" IS '是否流动人口';
COMMENT ON COLUMN "public"."lfun_students_base_info"."overseas_chinese" IS '是否港澳台侨胞';
COMMENT ON COLUMN "public"."lfun_students_base_info"."residence_address_detail" IS '户口所在地（详细）';
COMMENT ON COLUMN "public"."lfun_students_base_info"."communication_district" IS '通信地址行政区';
COMMENT ON COLUMN "public"."lfun_students_base_info"."postal_code" IS '邮政编码';
COMMENT ON COLUMN "public"."lfun_students_base_info"."communication_address" IS '通信地址';
COMMENT ON COLUMN "public"."lfun_students_base_info"."photo_upload_time" IS '照片上传时间';
COMMENT ON COLUMN "public"."lfun_students_base_info"."identity_card_validity_period" IS '身份证件有效期';
COMMENT ON COLUMN "public"."lfun_students_base_info"."specialty" IS '特长';
COMMENT ON COLUMN "public"."lfun_students_base_info"."permanent_address" IS '常住地址';
COMMENT ON COLUMN "public"."lfun_students_base_info"."remark" IS '备注';
COMMENT ON COLUMN "public"."lfun_students_base_info"."county" IS '区县';
COMMENT ON COLUMN "public"."lfun_students_base_info"."emporary_borrowing_status" IS '临时借读状态';
COMMENT ON COLUMN "public"."lfun_students_base_info"."flow_out_time" IS '流出时间';
COMMENT ON COLUMN "public"."lfun_students_base_info"."flow_out_reason" IS '流出原因';
COMMENT ON COLUMN "public"."lfun_students_base_info"."is_deleted" IS '是否删除';
COMMENT ON COLUMN "public"."lfun_students_base_info"."identity" IS '身份';
COMMENT ON COLUMN "public"."lfun_students_base_info"."birth_place" IS '出生地';
COMMENT ON COLUMN "public"."lfun_students_base_info"."admission_date" IS '入学年月new';
COMMENT ON COLUMN "public"."lfun_students_base_info"."health_status" IS '枚举health_status';
COMMENT ON COLUMN "public"."lfun_students_base_info"."nationality" IS '国籍/地区';
COMMENT ON COLUMN "public"."lfun_students_base_info"."enrollment_method" IS '就读方式枚举enrollment_method';
COMMENT ON COLUMN "public"."lfun_students_base_info"."identity_type" IS '身份类型';
COMMENT ON TABLE "public"."lfun_students_base_info" IS '学生表基本信息模型';

-- ----------------------------
-- Table structure for lfun_subject
-- ----------------------------
DROP TABLE IF EXISTS "public"."lfun_subject";
CREATE TABLE "public"."lfun_subject" (
  "id" int8 NOT NULL DEFAULT nextval('lfun_subject_id_seq'::regclass),
  "subject_name" varchar(64) COLLATE "pg_catalog"."default",
  "subject_alias" varchar(64) COLLATE "pg_catalog"."default",
  "subject_level" varchar(64) COLLATE "pg_catalog"."default",
  "course_name" varchar(24) COLLATE "pg_catalog"."default",
  "grade_id" int8,
  "subject_description" varchar(255) COLLATE "pg_catalog"."default",
  "subject_requirement" varchar(255) COLLATE "pg_catalog"."default",
  "credit_hour" int4,
  "week_credit_hour" int4,
  "self_study_credit_hour" int4,
  "teach_method" varchar(40) COLLATE "pg_catalog"."default",
  "textbook_code" varchar(40) COLLATE "pg_catalog"."default",
  "reference_book" varchar(40) COLLATE "pg_catalog"."default",
  "created_uid" int4,
  "updated_uid" int4,
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL,
  "is_deleted" bool NOT NULL,
  "school_id" int8,
  "course_no" varchar(24) COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "public"."lfun_subject"."id" IS 'ID';
COMMENT ON COLUMN "public"."lfun_subject"."subject_name" IS '课程名称=年级+学科';
COMMENT ON COLUMN "public"."lfun_subject"."subject_alias" IS '课程别名';
COMMENT ON COLUMN "public"."lfun_subject"."subject_level" IS '课程等级 国家/地方/校本,枚举subject_level';
COMMENT ON COLUMN "public"."lfun_subject"."course_name" IS '学科名称';
COMMENT ON COLUMN "public"."lfun_subject"."grade_id" IS '年级ID';
COMMENT ON COLUMN "public"."lfun_subject"."subject_description" IS '课程简介';
COMMENT ON COLUMN "public"."lfun_subject"."subject_requirement" IS '课程要求';
COMMENT ON COLUMN "public"."lfun_subject"."credit_hour" IS '总学时';
COMMENT ON COLUMN "public"."lfun_subject"."week_credit_hour" IS '周学时';
COMMENT ON COLUMN "public"."lfun_subject"."self_study_credit_hour" IS '自学学时';
COMMENT ON COLUMN "public"."lfun_subject"."teach_method" IS '授课方式,枚举teach_method';
COMMENT ON COLUMN "public"."lfun_subject"."textbook_code" IS '教材编码';
COMMENT ON COLUMN "public"."lfun_subject"."reference_book" IS '参考书目';
COMMENT ON COLUMN "public"."lfun_subject"."created_uid" IS '创建人';
COMMENT ON COLUMN "public"."lfun_subject"."updated_uid" IS '操作人';
COMMENT ON COLUMN "public"."lfun_subject"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."lfun_subject"."updated_at" IS '更新时间';
COMMENT ON COLUMN "public"."lfun_subject"."is_deleted" IS '删除态';
COMMENT ON COLUMN "public"."lfun_subject"."school_id" IS '学校ID';
COMMENT ON COLUMN "public"."lfun_subject"."course_no" IS '学科编码';
COMMENT ON TABLE "public"."lfun_subject" IS '课程表模型';

-- ----------------------------
-- Table structure for lfun_system_config
-- ----------------------------
DROP TABLE IF EXISTS "public"."lfun_system_config";
CREATE TABLE "public"."lfun_system_config" (
  "id" int8 NOT NULL DEFAULT nextval('lfun_system_config_id_seq'::regclass),
  "config_name" varchar(255) COLLATE "pg_catalog"."default",
  "config_code" varchar(255) COLLATE "pg_catalog"."default",
  "config_value" varchar(1024) COLLATE "pg_catalog"."default",
  "config_remark" varchar(255) COLLATE "pg_catalog"."default",
  "school_id" int4,
  "created_uid" int4,
  "updated_uid" int4,
  "created_at" timestamp(6),
  "updated_at" timestamp(6),
  "is_deleted" bool NOT NULL
)
;
COMMENT ON COLUMN "public"."lfun_system_config"."id" IS 'ID';
COMMENT ON COLUMN "public"."lfun_system_config"."config_name" IS '配置项';
COMMENT ON COLUMN "public"."lfun_system_config"."config_code" IS '配置项编码';
COMMENT ON COLUMN "public"."lfun_system_config"."config_value" IS '配置项值';
COMMENT ON COLUMN "public"."lfun_system_config"."config_remark" IS '简述';
COMMENT ON COLUMN "public"."lfun_system_config"."created_uid" IS '创建人';
COMMENT ON COLUMN "public"."lfun_system_config"."updated_uid" IS '操作人';
COMMENT ON COLUMN "public"."lfun_system_config"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."lfun_system_config"."updated_at" IS '更新时间';
COMMENT ON COLUMN "public"."lfun_system_config"."is_deleted" IS '删除态';
COMMENT ON TABLE "public"."lfun_system_config" IS '系统配置表';

-- ----------------------------
-- Table structure for lfun_talent_program
-- ----------------------------
DROP TABLE IF EXISTS "public"."lfun_talent_program";
CREATE TABLE "public"."lfun_talent_program" (
  "talent_program_id" int8 NOT NULL DEFAULT nextval('lfun_talent_program_talent_program_id_seq'::regclass),
  "teacher_id" int8 NOT NULL,
  "talent_project_name" varchar(64) COLLATE "pg_catalog"."default",
  "selected_year" varchar(64) COLLATE "pg_catalog"."default",
  "is_deleted" bool NOT NULL,
  "approval_status" varchar(64) COLLATE "pg_catalog"."default" NOT NULL
)
;
COMMENT ON COLUMN "public"."lfun_talent_program"."talent_program_id" IS 'talent_programID';
COMMENT ON COLUMN "public"."lfun_talent_program"."teacher_id" IS '教师ID';
COMMENT ON COLUMN "public"."lfun_talent_program"."talent_project_name" IS '人才项目名称枚举talent_project_name_lv1';
COMMENT ON COLUMN "public"."lfun_talent_program"."selected_year" IS '入选年份';
COMMENT ON COLUMN "public"."lfun_talent_program"."is_deleted" IS '是否删除';
COMMENT ON COLUMN "public"."lfun_talent_program"."approval_status" IS '审批状态';
COMMENT ON TABLE "public"."lfun_talent_program" IS 'talent_program信息表';

-- ----------------------------
-- Table structure for lfun_teacher_borrow
-- ----------------------------
DROP TABLE IF EXISTS "public"."lfun_teacher_borrow";
CREATE TABLE "public"."lfun_teacher_borrow" (
  "teacher_borrow_id" int8 NOT NULL DEFAULT nextval('lfun_teacher_borrow_teacher_borrow_id_seq'::regclass),
  "original_unit_id" int8,
  "original_unit_name" varchar(64) COLLATE "pg_catalog"."default",
  "original_position" varchar(64) COLLATE "pg_catalog"."default",
  "original_district_province_id" int4,
  "original_district_city_id" int4,
  "original_district_area_id" int4,
  "original_region_province_id" int4,
  "original_region_city_id" int4,
  "original_region_area_id" int4,
  "borrow_in_date" "sys"."date",
  "current_unit_id" int8,
  "current_position" varchar(64) COLLATE "pg_catalog"."default",
  "current_unit_name" varchar(64) COLLATE "pg_catalog"."default",
  "current_district_province_id" int4,
  "current_district_city_id" int4,
  "current_district_area_id" int4,
  "current_region_province_id" int4,
  "current_region_city_id" int4,
  "current_region_area_id" int4,
  "borrow_out_date" "sys"."date",
  "borrow_reason" varchar(64) COLLATE "pg_catalog"."default",
  "remark" varchar(64) COLLATE "pg_catalog"."default",
  "teacher_id" int8 NOT NULL,
  "is_deleted" bool NOT NULL,
  "borrow_type" varchar(255) COLLATE "pg_catalog"."default" NOT NULL
)
;
COMMENT ON COLUMN "public"."lfun_teacher_borrow"."teacher_borrow_id" IS 'teacher_borrowID';
COMMENT ON COLUMN "public"."lfun_teacher_borrow"."original_unit_id" IS '原单位';
COMMENT ON COLUMN "public"."lfun_teacher_borrow"."original_unit_name" IS '原单位名称';
COMMENT ON COLUMN "public"."lfun_teacher_borrow"."original_position" IS '原岗位';
COMMENT ON COLUMN "public"."lfun_teacher_borrow"."original_district_province_id" IS '原行政属地省';
COMMENT ON COLUMN "public"."lfun_teacher_borrow"."original_district_city_id" IS '原行政属地市';
COMMENT ON COLUMN "public"."lfun_teacher_borrow"."original_district_area_id" IS '原行政属地区';
COMMENT ON COLUMN "public"."lfun_teacher_borrow"."original_region_province_id" IS '原管辖区域省';
COMMENT ON COLUMN "public"."lfun_teacher_borrow"."original_region_city_id" IS '原管辖区域市';
COMMENT ON COLUMN "public"."lfun_teacher_borrow"."original_region_area_id" IS '原管辖区域区';
COMMENT ON COLUMN "public"."lfun_teacher_borrow"."borrow_in_date" IS '借入日期';
COMMENT ON COLUMN "public"."lfun_teacher_borrow"."current_unit_id" IS '现单位';
COMMENT ON COLUMN "public"."lfun_teacher_borrow"."current_position" IS '现岗位';
COMMENT ON COLUMN "public"."lfun_teacher_borrow"."current_unit_name" IS '现单位名称';
COMMENT ON COLUMN "public"."lfun_teacher_borrow"."current_district_province_id" IS '现行政属地省';
COMMENT ON COLUMN "public"."lfun_teacher_borrow"."current_district_city_id" IS '现行政属地市';
COMMENT ON COLUMN "public"."lfun_teacher_borrow"."current_district_area_id" IS '现行政属地区';
COMMENT ON COLUMN "public"."lfun_teacher_borrow"."current_region_province_id" IS '现管辖区域省';
COMMENT ON COLUMN "public"."lfun_teacher_borrow"."current_region_city_id" IS '现管辖区域市';
COMMENT ON COLUMN "public"."lfun_teacher_borrow"."current_region_area_id" IS '现管辖区域区';
COMMENT ON COLUMN "public"."lfun_teacher_borrow"."borrow_out_date" IS '借出日期';
COMMENT ON COLUMN "public"."lfun_teacher_borrow"."borrow_reason" IS '借动原因';
COMMENT ON COLUMN "public"."lfun_teacher_borrow"."remark" IS '备注';
COMMENT ON COLUMN "public"."lfun_teacher_borrow"."teacher_id" IS '教师ID';
COMMENT ON COLUMN "public"."lfun_teacher_borrow"."is_deleted" IS '是否删除';
COMMENT ON COLUMN "public"."lfun_teacher_borrow"."borrow_type" IS '借动类型';
COMMENT ON TABLE "public"."lfun_teacher_borrow" IS 'teacher_borrow信息表';

-- ----------------------------
-- Table structure for lfun_teacher_ethic_records
-- ----------------------------
DROP TABLE IF EXISTS "public"."lfun_teacher_ethic_records";
CREATE TABLE "public"."lfun_teacher_ethic_records" (
  "teacher_ethic_records_id" int8 NOT NULL DEFAULT nextval('lfun_teacher_ethic_records_teacher_ethic_records_id_seq'::regclass),
  "teacher_id" int8 NOT NULL,
  "ethics_assessment_date" "sys"."date",
  "ethics_assessment_conclusion" varchar(64) COLLATE "pg_catalog"."default",
  "assessment_institution_name" varchar(64) COLLATE "pg_catalog"."default",
  "honor_level" varchar(64) COLLATE "pg_catalog"."default",
  "honor_title" varchar(64) COLLATE "pg_catalog"."default",
  "honor_date" "sys"."date",
  "awarding_institution_name" varchar(64) COLLATE "pg_catalog"."default",
  "honor_record_description" varchar(64) COLLATE "pg_catalog"."default",
  "disciplinary_category" varchar(64) COLLATE "pg_catalog"."default",
  "disciplinary_reason" varchar(64) COLLATE "pg_catalog"."default",
  "disciplinary_date" "sys"."date",
  "disciplinary_institution_name" varchar(64) COLLATE "pg_catalog"."default",
  "disciplinary_record_description" varchar(64) COLLATE "pg_catalog"."default",
  "disciplinary_occurrence_date" "sys"."date",
  "disciplinary_revocation_date" "sys"."date",
  "disciplinary_revocation_reason" varchar(64) COLLATE "pg_catalog"."default",
  "is_deleted" bool,
  "approval_status" varchar(64) COLLATE "pg_catalog"."default",
  "ethic_type" varchar(64) COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "public"."lfun_teacher_ethic_records"."teacher_ethic_records_id" IS 'teacher_ethic_recordsID';
COMMENT ON COLUMN "public"."lfun_teacher_ethic_records"."teacher_id" IS '教师ID';
COMMENT ON COLUMN "public"."lfun_teacher_ethic_records"."ethics_assessment_date" IS '师德考核时间';
COMMENT ON COLUMN "public"."lfun_teacher_ethic_records"."ethics_assessment_conclusion" IS '师德考核结论';
COMMENT ON COLUMN "public"."lfun_teacher_ethic_records"."assessment_institution_name" IS '考核单位名称';
COMMENT ON COLUMN "public"."lfun_teacher_ethic_records"."honor_level" IS '荣誉级别';
COMMENT ON COLUMN "public"."lfun_teacher_ethic_records"."honor_title" IS '荣誉称号';
COMMENT ON COLUMN "public"."lfun_teacher_ethic_records"."honor_date" IS '荣誉日期';
COMMENT ON COLUMN "public"."lfun_teacher_ethic_records"."awarding_institution_name" IS '荣誉授予单位名称';
COMMENT ON COLUMN "public"."lfun_teacher_ethic_records"."honor_record_description" IS '荣誉记录描述';
COMMENT ON COLUMN "public"."lfun_teacher_ethic_records"."disciplinary_category" IS '处分类别';
COMMENT ON COLUMN "public"."lfun_teacher_ethic_records"."disciplinary_reason" IS '处分原因';
COMMENT ON COLUMN "public"."lfun_teacher_ethic_records"."disciplinary_date" IS '处分日期';
COMMENT ON COLUMN "public"."lfun_teacher_ethic_records"."disciplinary_institution_name" IS '处分单位名称';
COMMENT ON COLUMN "public"."lfun_teacher_ethic_records"."disciplinary_record_description" IS '处分记录描述';
COMMENT ON COLUMN "public"."lfun_teacher_ethic_records"."disciplinary_occurrence_date" IS '处分发生日期';
COMMENT ON COLUMN "public"."lfun_teacher_ethic_records"."disciplinary_revocation_date" IS '处分撤销日期';
COMMENT ON COLUMN "public"."lfun_teacher_ethic_records"."disciplinary_revocation_reason" IS '处分撤销原因';
COMMENT ON COLUMN "public"."lfun_teacher_ethic_records"."is_deleted" IS '是否删除';
COMMENT ON COLUMN "public"."lfun_teacher_ethic_records"."approval_status" IS '审批状态';
COMMENT ON COLUMN "public"."lfun_teacher_ethic_records"."ethic_type" IS '师德类型';
COMMENT ON TABLE "public"."lfun_teacher_ethic_records" IS 'teacher_ethic_records信息表';

-- ----------------------------
-- Table structure for lfun_teacher_job_appointments
-- ----------------------------
DROP TABLE IF EXISTS "public"."lfun_teacher_job_appointments";
CREATE TABLE "public"."lfun_teacher_job_appointments" (
  "teacher_job_appointments_id" int8 NOT NULL DEFAULT nextval('lfun_teacher_job_appointments_teacher_job_appointments_id_seq'::regclass),
  "teacher_id" int8 NOT NULL,
  "position_category" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "position_level" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "school_level_position" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "is_concurrent_other_positions" bool NOT NULL,
  "concurrent_position" varchar(255) COLLATE "pg_catalog"."default",
  "appointment_start_date" "sys"."date" NOT NULL,
  "start_date" "sys"."date",
  "is_deleted" bool NOT NULL,
  "approval_status" varchar(64) COLLATE "pg_catalog"."default" NOT NULL
)
;
COMMENT ON COLUMN "public"."lfun_teacher_job_appointments"."teacher_job_appointments_id" IS 'teacher_job_appointmentsID';
COMMENT ON COLUMN "public"."lfun_teacher_job_appointments"."teacher_id" IS '教师ID';
COMMENT ON COLUMN "public"."lfun_teacher_job_appointments"."position_category" IS '岗位类别';
COMMENT ON COLUMN "public"."lfun_teacher_job_appointments"."position_level" IS '岗位等级';
COMMENT ON COLUMN "public"."lfun_teacher_job_appointments"."school_level_position" IS '校级职务';
COMMENT ON COLUMN "public"."lfun_teacher_job_appointments"."is_concurrent_other_positions" IS '是否兼任其他岗位';
COMMENT ON COLUMN "public"."lfun_teacher_job_appointments"."concurrent_position" IS '兼任岗位类别';
COMMENT ON COLUMN "public"."lfun_teacher_job_appointments"."appointment_start_date" IS '聘任开始时间';
COMMENT ON COLUMN "public"."lfun_teacher_job_appointments"."start_date" IS '任职开始年月时间';
COMMENT ON COLUMN "public"."lfun_teacher_job_appointments"."is_deleted" IS '是否删除';
COMMENT ON COLUMN "public"."lfun_teacher_job_appointments"."approval_status" IS '审批状态';
COMMENT ON TABLE "public"."lfun_teacher_job_appointments" IS 'teacher_job_appointments信息表';

-- ----------------------------
-- Table structure for lfun_teacher_learn_experience
-- ----------------------------
DROP TABLE IF EXISTS "public"."lfun_teacher_learn_experience";
CREATE TABLE "public"."lfun_teacher_learn_experience" (
  "teacher_learn_experience_id" int8 NOT NULL DEFAULT nextval('lfun_teacher_learn_experience_teacher_learn_experience_id_seq'::regclass),
  "teacher_id" int8,
  "education_obtained" varchar(64) COLLATE "pg_catalog"."default",
  "country_or_region_of_education" varchar(64) COLLATE "pg_catalog"."default",
  "institution_of_education_obtained" varchar(64) COLLATE "pg_catalog"."default",
  "major_learned" varchar(64) COLLATE "pg_catalog"."default",
  "is_major_normal" bool,
  "admission_date" "sys"."date",
  "graduation_date" "sys"."date",
  "degree_level" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "degree_name" varchar(64) COLLATE "pg_catalog"."default",
  "country_or_region_of_degree_obtained" varchar(64) COLLATE "pg_catalog"."default",
  "institution_of_degree_obtained" varchar(64) COLLATE "pg_catalog"."default",
  "degree_award_date" "sys"."date",
  "study_mode" varchar(64) COLLATE "pg_catalog"."default",
  "type_of_institution" varchar(64) COLLATE "pg_catalog"."default",
  "is_deleted" bool NOT NULL
)
;
COMMENT ON COLUMN "public"."lfun_teacher_learn_experience"."teacher_learn_experience_id" IS 'teacher_learn_experienceID';
COMMENT ON COLUMN "public"."lfun_teacher_learn_experience"."teacher_id" IS '教师ID';
COMMENT ON COLUMN "public"."lfun_teacher_learn_experience"."education_obtained" IS '获的学历';
COMMENT ON COLUMN "public"."lfun_teacher_learn_experience"."country_or_region_of_education" IS '获得学历国家/地区';
COMMENT ON COLUMN "public"."lfun_teacher_learn_experience"."institution_of_education_obtained" IS '获得学历的院校机构';
COMMENT ON COLUMN "public"."lfun_teacher_learn_experience"."major_learned" IS '所学妆业';
COMMENT ON COLUMN "public"."lfun_teacher_learn_experience"."is_major_normal" IS '是否师范类专业';
COMMENT ON COLUMN "public"."lfun_teacher_learn_experience"."admission_date" IS '入学时间';
COMMENT ON COLUMN "public"."lfun_teacher_learn_experience"."graduation_date" IS '毕业时间';
COMMENT ON COLUMN "public"."lfun_teacher_learn_experience"."degree_level" IS '学位层次';
COMMENT ON COLUMN "public"."lfun_teacher_learn_experience"."degree_name" IS '学位名称';
COMMENT ON COLUMN "public"."lfun_teacher_learn_experience"."country_or_region_of_degree_obtained" IS '获取学位过家地区';
COMMENT ON COLUMN "public"."lfun_teacher_learn_experience"."institution_of_degree_obtained" IS '获得学位院校机构';
COMMENT ON COLUMN "public"."lfun_teacher_learn_experience"."degree_award_date" IS '学位授予时间';
COMMENT ON COLUMN "public"."lfun_teacher_learn_experience"."study_mode" IS '学习方式';
COMMENT ON COLUMN "public"."lfun_teacher_learn_experience"."type_of_institution" IS '在学单位类别';
COMMENT ON COLUMN "public"."lfun_teacher_learn_experience"."is_deleted" IS '是否删除';
COMMENT ON TABLE "public"."lfun_teacher_learn_experience" IS 'teacher_learn_experience信息表';

-- ----------------------------
-- Table structure for lfun_teacher_professional_titles
-- ----------------------------
DROP TABLE IF EXISTS "public"."lfun_teacher_professional_titles";
CREATE TABLE "public"."lfun_teacher_professional_titles" (
  "teacher_professional_titles_id" int8 NOT NULL DEFAULT nextval('lfun_teacher_professional_tit_teacher_professional_titles_i_seq'::regclass),
  "teacher_id" int8 NOT NULL,
  "current_professional_title" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "employing_institution_name" varchar(64) COLLATE "pg_catalog"."default",
  "employment_start_date" "sys"."date" NOT NULL,
  "employment_end_date" "sys"."date",
  "is_deleted" bool NOT NULL,
  "approval_status" varchar(64) COLLATE "pg_catalog"."default" NOT NULL
)
;
COMMENT ON COLUMN "public"."lfun_teacher_professional_titles"."teacher_professional_titles_id" IS 'teacher_professional_titlesID';
COMMENT ON COLUMN "public"."lfun_teacher_professional_titles"."teacher_id" IS '教师ID';
COMMENT ON COLUMN "public"."lfun_teacher_professional_titles"."current_professional_title" IS '现专业技术职务';
COMMENT ON COLUMN "public"."lfun_teacher_professional_titles"."employing_institution_name" IS '聘任单位名称';
COMMENT ON COLUMN "public"."lfun_teacher_professional_titles"."employment_start_date" IS '聘任开始时间';
COMMENT ON COLUMN "public"."lfun_teacher_professional_titles"."employment_end_date" IS '聘任结束时间';
COMMENT ON COLUMN "public"."lfun_teacher_professional_titles"."is_deleted" IS '是否删除';
COMMENT ON COLUMN "public"."lfun_teacher_professional_titles"."approval_status" IS '审批状态';
COMMENT ON TABLE "public"."lfun_teacher_professional_titles" IS 'teacher_professional_titles信息表';

-- ----------------------------
-- Table structure for lfun_teacher_qualifications
-- ----------------------------
DROP TABLE IF EXISTS "public"."lfun_teacher_qualifications";
CREATE TABLE "public"."lfun_teacher_qualifications" (
  "teacher_qualifications_id" int8 NOT NULL DEFAULT nextval('lfun_teacher_qualifications_teacher_qualifications_id_seq'::regclass),
  "teacher_id" int8 NOT NULL,
  "teacher_qualification_type" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "qualification_number" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "teaching_subject" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "certificate_issue_date" "sys"."date" NOT NULL,
  "issuing_authority" varchar(64) COLLATE "pg_catalog"."default",
  "first_registration_date" "sys"."date",
  "regular_registration_date" "sys"."date",
  "regular_registration_conclusion" varchar(64) COLLATE "pg_catalog"."default",
  "is_deleted" bool NOT NULL
)
;
COMMENT ON COLUMN "public"."lfun_teacher_qualifications"."teacher_qualifications_id" IS 'teacher_qualificationsID';
COMMENT ON COLUMN "public"."lfun_teacher_qualifications"."teacher_id" IS '教师ID';
COMMENT ON COLUMN "public"."lfun_teacher_qualifications"."teacher_qualification_type" IS '教师资格证种类';
COMMENT ON COLUMN "public"."lfun_teacher_qualifications"."qualification_number" IS '资格证号码';
COMMENT ON COLUMN "public"."lfun_teacher_qualifications"."teaching_subject" IS '任教学科';
COMMENT ON COLUMN "public"."lfun_teacher_qualifications"."certificate_issue_date" IS '证书颁发时间';
COMMENT ON COLUMN "public"."lfun_teacher_qualifications"."issuing_authority" IS '颁发机构';
COMMENT ON COLUMN "public"."lfun_teacher_qualifications"."first_registration_date" IS '首次注册日期';
COMMENT ON COLUMN "public"."lfun_teacher_qualifications"."regular_registration_date" IS '定期注册日期';
COMMENT ON COLUMN "public"."lfun_teacher_qualifications"."regular_registration_conclusion" IS '定期注册结论';
COMMENT ON COLUMN "public"."lfun_teacher_qualifications"."is_deleted" IS '是否删除';
COMMENT ON TABLE "public"."lfun_teacher_qualifications" IS 'teacher_qualifications信息表';

-- ----------------------------
-- Table structure for lfun_teacher_retire
-- ----------------------------
DROP TABLE IF EXISTS "public"."lfun_teacher_retire";
CREATE TABLE "public"."lfun_teacher_retire" (
  "teacher_retire_id" int8 NOT NULL DEFAULT nextval('lfun_teacher_retire_teacher_retire_id_seq'::regclass),
  "teacher_id" int8 NOT NULL,
  "transaction_type" varchar(64) COLLATE "pg_catalog"."default",
  "transaction_remark" varchar(255) COLLATE "pg_catalog"."default",
  "retire_date" "sys"."date",
  "transaction_time" timestamp(6) NOT NULL,
  "is_deleted" bool NOT NULL,
  "retire_number" varchar(255) COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "public"."lfun_teacher_retire"."teacher_retire_id" IS '变动主键id';
COMMENT ON COLUMN "public"."lfun_teacher_retire"."teacher_id" IS '教师ID';
COMMENT ON COLUMN "public"."lfun_teacher_retire"."transaction_type" IS '变动类型';
COMMENT ON COLUMN "public"."lfun_teacher_retire"."transaction_remark" IS '备注';
COMMENT ON COLUMN "public"."lfun_teacher_retire"."retire_date" IS '任职日期';
COMMENT ON COLUMN "public"."lfun_teacher_retire"."transaction_time" IS '操作时间';
COMMENT ON COLUMN "public"."lfun_teacher_retire"."is_deleted" IS '删除态';
COMMENT ON COLUMN "public"."lfun_teacher_retire"."retire_number" IS '离退休号';
COMMENT ON TABLE "public"."lfun_teacher_retire" IS '教师离退休表';

-- ----------------------------
-- Table structure for lfun_teacher_skill_certificates
-- ----------------------------
DROP TABLE IF EXISTS "public"."lfun_teacher_skill_certificates";
CREATE TABLE "public"."lfun_teacher_skill_certificates" (
  "teacher_skill_certificates_id" int8 NOT NULL DEFAULT nextval('lfun_teacher_skill_certificat_teacher_skill_certificates_id_seq'::regclass),
  "teacher_id" int8 NOT NULL,
  "language" varchar(64) COLLATE "pg_catalog"."default",
  "proficiency_level" varchar(64) COLLATE "pg_catalog"."default",
  "other_skill_name" varchar(64) COLLATE "pg_catalog"."default",
  "other_skill_level" varchar(64) COLLATE "pg_catalog"."default",
  "certificate_type" varchar(64) COLLATE "pg_catalog"."default",
  "language_certificate_name" varchar(64) COLLATE "pg_catalog"."default",
  "issue_year_month" "sys"."date",
  "issuing_authority" varchar(64) COLLATE "pg_catalog"."default",
  "certificate_number" varchar(64) COLLATE "pg_catalog"."default",
  "is_deleted" bool NOT NULL
)
;
COMMENT ON COLUMN "public"."lfun_teacher_skill_certificates"."teacher_skill_certificates_id" IS 'teacher_skill_certificatesID';
COMMENT ON COLUMN "public"."lfun_teacher_skill_certificates"."teacher_id" IS '教师ID';
COMMENT ON COLUMN "public"."lfun_teacher_skill_certificates"."language" IS '语种';
COMMENT ON COLUMN "public"."lfun_teacher_skill_certificates"."proficiency_level" IS '掌握程度';
COMMENT ON COLUMN "public"."lfun_teacher_skill_certificates"."other_skill_name" IS '其他技能名称';
COMMENT ON COLUMN "public"."lfun_teacher_skill_certificates"."other_skill_level" IS '其他技能程度';
COMMENT ON COLUMN "public"."lfun_teacher_skill_certificates"."certificate_type" IS '证书类型';
COMMENT ON COLUMN "public"."lfun_teacher_skill_certificates"."language_certificate_name" IS '语言证书名称';
COMMENT ON COLUMN "public"."lfun_teacher_skill_certificates"."issue_year_month" IS '发证年月';
COMMENT ON COLUMN "public"."lfun_teacher_skill_certificates"."issuing_authority" IS '发证单位';
COMMENT ON COLUMN "public"."lfun_teacher_skill_certificates"."certificate_number" IS '证书编号';
COMMENT ON COLUMN "public"."lfun_teacher_skill_certificates"."is_deleted" IS '是否删除';
COMMENT ON TABLE "public"."lfun_teacher_skill_certificates" IS 'teacher_skill_certificates信息表';

-- ----------------------------
-- Table structure for lfun_teacher_transaction
-- ----------------------------
DROP TABLE IF EXISTS "public"."lfun_teacher_transaction";
CREATE TABLE "public"."lfun_teacher_transaction" (
  "transaction_id" int8 NOT NULL DEFAULT nextval('lfun_teacher_transaction_transaction_id_seq'::regclass),
  "teacher_id" int8 NOT NULL,
  "transaction_type" varchar(64) COLLATE "pg_catalog"."default",
  "transaction_remark" varchar(255) COLLATE "pg_catalog"."default",
  "original_position" varchar(64) COLLATE "pg_catalog"."default",
  "current_position" varchar(64) COLLATE "pg_catalog"."default",
  "position_date" "sys"."date",
  "transaction_time" timestamp(6) NOT NULL,
  "is_deleted" bool NOT NULL,
  "is_active" bool NOT NULL
)
;
COMMENT ON COLUMN "public"."lfun_teacher_transaction"."transaction_id" IS '变动主键id';
COMMENT ON COLUMN "public"."lfun_teacher_transaction"."teacher_id" IS '教师ID';
COMMENT ON COLUMN "public"."lfun_teacher_transaction"."transaction_type" IS '变动类型';
COMMENT ON COLUMN "public"."lfun_teacher_transaction"."transaction_remark" IS '备注';
COMMENT ON COLUMN "public"."lfun_teacher_transaction"."original_position" IS '原任职岗位';
COMMENT ON COLUMN "public"."lfun_teacher_transaction"."current_position" IS '现任职岗位';
COMMENT ON COLUMN "public"."lfun_teacher_transaction"."position_date" IS '任职日期';
COMMENT ON COLUMN "public"."lfun_teacher_transaction"."transaction_time" IS '操作时间';
COMMENT ON COLUMN "public"."lfun_teacher_transaction"."is_deleted" IS '删除态';
COMMENT ON COLUMN "public"."lfun_teacher_transaction"."is_active" IS '是否已经恢复在职';
COMMENT ON TABLE "public"."lfun_teacher_transaction" IS '教师变动修改表';

-- ----------------------------
-- Table structure for lfun_teacher_work_experience
-- ----------------------------
DROP TABLE IF EXISTS "public"."lfun_teacher_work_experience";
CREATE TABLE "public"."lfun_teacher_work_experience" (
  "teacher_work_experience_id" int8 NOT NULL DEFAULT nextval('lfun_teacher_work_experience_teacher_work_experience_id_seq'::regclass),
  "teacher_id" int8 NOT NULL,
  "employment_institution_name" varchar(64) COLLATE "pg_catalog"."default",
  "start_date" "sys"."date",
  "end_date" "sys"."date",
  "on_duty_position" varchar(64) COLLATE "pg_catalog"."default",
  "institution_nature_category" varchar(64) COLLATE "pg_catalog"."default",
  "is_deleted" bool NOT NULL
)
;
COMMENT ON COLUMN "public"."lfun_teacher_work_experience"."teacher_work_experience_id" IS 'teacher_work_experienceID';
COMMENT ON COLUMN "public"."lfun_teacher_work_experience"."teacher_id" IS '教师ID';
COMMENT ON COLUMN "public"."lfun_teacher_work_experience"."employment_institution_name" IS '任职单位名称';
COMMENT ON COLUMN "public"."lfun_teacher_work_experience"."start_date" IS '开始时间';
COMMENT ON COLUMN "public"."lfun_teacher_work_experience"."end_date" IS '结束时间';
COMMENT ON COLUMN "public"."lfun_teacher_work_experience"."on_duty_position" IS '在职岗位';
COMMENT ON COLUMN "public"."lfun_teacher_work_experience"."institution_nature_category" IS '单位性质类别';
COMMENT ON COLUMN "public"."lfun_teacher_work_experience"."is_deleted" IS '是否删除';
COMMENT ON TABLE "public"."lfun_teacher_work_experience" IS 'teacher_work_experience信息表';

-- ----------------------------
-- Table structure for lfun_teachers
-- ----------------------------
DROP TABLE IF EXISTS "public"."lfun_teachers";
CREATE TABLE "public"."lfun_teachers" (
  "teacher_id" int8 NOT NULL DEFAULT nextval('lfun_teachers_teacher_id_seq'::regclass),
  "teacher_gender" varchar(64) COLLATE "pg_catalog"."default",
  "teacher_name" varchar(64) COLLATE "pg_catalog"."default",
  "teacher_id_type" varchar(64) COLLATE "pg_catalog"."default",
  "teacher_id_number" varchar(64) COLLATE "pg_catalog"."default",
  "teacher_date_of_birth" "sys"."date",
  "teacher_employer" int8,
  "teacher_avatar" varchar(64) COLLATE "pg_catalog"."default",
  "is_deleted" bool NOT NULL,
  "teacher_main_status" varchar(64) COLLATE "pg_catalog"."default",
  "teacher_sub_status" varchar(64) COLLATE "pg_catalog"."default",
  "identity" varchar(64) COLLATE "pg_catalog"."default",
  "mobile" varchar(64) COLLATE "pg_catalog"."default",
  "is_approval" bool NOT NULL,
  "identity_type" varchar(64) COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "public"."lfun_teachers"."teacher_id" IS '教师ID';
COMMENT ON COLUMN "public"."lfun_teachers"."teacher_gender" IS '教师性别';
COMMENT ON COLUMN "public"."lfun_teachers"."teacher_name" IS '教师名称';
COMMENT ON COLUMN "public"."lfun_teachers"."teacher_id_type" IS '证件类型';
COMMENT ON COLUMN "public"."lfun_teachers"."teacher_id_number" IS '证件号';
COMMENT ON COLUMN "public"."lfun_teachers"."teacher_date_of_birth" IS '出生日期';
COMMENT ON COLUMN "public"."lfun_teachers"."teacher_employer" IS '任职单位';
COMMENT ON COLUMN "public"."lfun_teachers"."teacher_avatar" IS '头像';
COMMENT ON COLUMN "public"."lfun_teachers"."is_deleted" IS '是否删除';
COMMENT ON COLUMN "public"."lfun_teachers"."teacher_main_status" IS '主状态';
COMMENT ON COLUMN "public"."lfun_teachers"."teacher_sub_status" IS '子状态';
COMMENT ON COLUMN "public"."lfun_teachers"."identity" IS '身份';
COMMENT ON COLUMN "public"."lfun_teachers"."mobile" IS '手机号';
COMMENT ON COLUMN "public"."lfun_teachers"."is_approval" IS '是否在审批中';
COMMENT ON COLUMN "public"."lfun_teachers"."identity_type" IS '身份类型';
COMMENT ON TABLE "public"."lfun_teachers" IS '教师表模型';

-- ----------------------------
-- Table structure for lfun_teachers_info
-- ----------------------------
DROP TABLE IF EXISTS "public"."lfun_teachers_info";
CREATE TABLE "public"."lfun_teachers_info" (
  "teacher_base_id" int8 NOT NULL DEFAULT nextval('lfun_teachers_info_teacher_base_id_seq'::regclass),
  "teacher_id" int8 NOT NULL,
  "ethnicity" varchar(255) COLLATE "pg_catalog"."default",
  "nationality" varchar(255) COLLATE "pg_catalog"."default",
  "political_status" varchar(255) COLLATE "pg_catalog"."default",
  "native_place" varchar(255) COLLATE "pg_catalog"."default",
  "birth_place" varchar(255) COLLATE "pg_catalog"."default",
  "former_name" varchar(255) COLLATE "pg_catalog"."default",
  "marital_status" varchar(255) COLLATE "pg_catalog"."default",
  "health_condition" varchar(255) COLLATE "pg_catalog"."default",
  "highest_education" varchar(255) COLLATE "pg_catalog"."default",
  "institution_of_highest_education" varchar(255) COLLATE "pg_catalog"."default",
  "special_education_start_time" "sys"."date",
  "start_working_date" "sys"."date",
  "enter_school_time" "sys"."date",
  "source_of_staff" varchar(255) COLLATE "pg_catalog"."default",
  "staff_category" varchar(255) COLLATE "pg_catalog"."default",
  "in_post" bool,
  "employment_form" varchar(255) COLLATE "pg_catalog"."default",
  "contract_signing_status" varchar(255) COLLATE "pg_catalog"."default",
  "current_post_type" varchar(255) COLLATE "pg_catalog"."default",
  "current_post_level" varchar(255) COLLATE "pg_catalog"."default",
  "current_technical_position" varchar(255) COLLATE "pg_catalog"."default",
  "full_time_special_education_major_graduate" bool,
  "received_preschool_education_training" bool,
  "full_time_normal_major_graduate" bool,
  "received_special_education_training" bool,
  "has_special_education_certificate" bool,
  "information_technology_application_ability" varchar COLLATE "pg_catalog"."default",
  "free_normal_college_student" bool,
  "participated_in_basic_service_project" bool,
  "basic_service_start_date" "sys"."date",
  "basic_service_end_date" "sys"."date",
  "special_education_teacher" bool,
  "dual_teacher" bool,
  "has_occupational_skill_level_certificate" bool,
  "enterprise_work_experience" varchar(255) COLLATE "pg_catalog"."default",
  "county_level_backbone" bool,
  "psychological_health_education_teacher" bool,
  "recruitment_method" varchar(255) COLLATE "pg_catalog"."default",
  "teacher_number" varchar(255) COLLATE "pg_catalog"."default",
  "is_deleted" bool NOT NULL,
  "department" varchar(255) COLLATE "pg_catalog"."default",
  "org_id" int8,
  "hmotf" varchar(255) COLLATE "pg_catalog"."default",
  "hukou_type" varchar(255) COLLATE "pg_catalog"."default",
  "main_teaching_level" varchar(255) COLLATE "pg_catalog"."default",
  "teacher_qualification_cert_num" varchar(255) COLLATE "pg_catalog"."default",
  "teaching_discipline" varchar(255) COLLATE "pg_catalog"."default",
  "language" varchar(255) COLLATE "pg_catalog"."default",
  "language_proficiency_level" varchar(255) COLLATE "pg_catalog"."default",
  "language_certificate_name" varchar(255) COLLATE "pg_catalog"."default",
  "contact_address" varchar(255) COLLATE "pg_catalog"."default",
  "contact_address_details" varchar(255) COLLATE "pg_catalog"."default",
  "email" varchar(255) COLLATE "pg_catalog"."default",
  "highest_education_level" varchar(255) COLLATE "pg_catalog"."default",
  "highest_degree_name" varchar(255) COLLATE "pg_catalog"."default",
  "is_major_graduate" bool,
  "other_contact_address_details" varchar(255) COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "public"."lfun_teachers_info"."teacher_base_id" IS '教师基本信息ID';
COMMENT ON COLUMN "public"."lfun_teachers_info"."teacher_id" IS '教师ID';
COMMENT ON COLUMN "public"."lfun_teachers_info"."ethnicity" IS '民族';
COMMENT ON COLUMN "public"."lfun_teachers_info"."nationality" IS '国家地区';
COMMENT ON COLUMN "public"."lfun_teachers_info"."political_status" IS '政治面貌';
COMMENT ON COLUMN "public"."lfun_teachers_info"."native_place" IS '籍贯';
COMMENT ON COLUMN "public"."lfun_teachers_info"."birth_place" IS '出生地';
COMMENT ON COLUMN "public"."lfun_teachers_info"."former_name" IS '曾用名';
COMMENT ON COLUMN "public"."lfun_teachers_info"."marital_status" IS '婚姻状况';
COMMENT ON COLUMN "public"."lfun_teachers_info"."health_condition" IS '健康状况';
COMMENT ON COLUMN "public"."lfun_teachers_info"."highest_education" IS '最高学历';
COMMENT ON COLUMN "public"."lfun_teachers_info"."institution_of_highest_education" IS '获得最高学历的院校或者机构';
COMMENT ON COLUMN "public"."lfun_teachers_info"."special_education_start_time" IS '特教开时时间';
COMMENT ON COLUMN "public"."lfun_teachers_info"."start_working_date" IS '参加工作年月';
COMMENT ON COLUMN "public"."lfun_teachers_info"."enter_school_time" IS '进本校时间';
COMMENT ON COLUMN "public"."lfun_teachers_info"."source_of_staff" IS '教职工来源';
COMMENT ON COLUMN "public"."lfun_teachers_info"."staff_category" IS '教职工类别';
COMMENT ON COLUMN "public"."lfun_teachers_info"."in_post" IS '是否在编';
COMMENT ON COLUMN "public"."lfun_teachers_info"."employment_form" IS '用人形式';
COMMENT ON COLUMN "public"."lfun_teachers_info"."contract_signing_status" IS '合同签订情况';
COMMENT ON COLUMN "public"."lfun_teachers_info"."current_post_type" IS '现在岗位类型';
COMMENT ON COLUMN "public"."lfun_teachers_info"."current_post_level" IS '现岗位等级';
COMMENT ON COLUMN "public"."lfun_teachers_info"."current_technical_position" IS '现专业技术职务';
COMMENT ON COLUMN "public"."lfun_teachers_info"."full_time_special_education_major_graduate" IS '是否全日制特殊教育专业毕业';
COMMENT ON COLUMN "public"."lfun_teachers_info"."received_preschool_education_training" IS '是否受过学前教育培训';
COMMENT ON COLUMN "public"."lfun_teachers_info"."full_time_normal_major_graduate" IS '是否全日制师范类专业毕业';
COMMENT ON COLUMN "public"."lfun_teachers_info"."received_special_education_training" IS '是否受过特教专业培训';
COMMENT ON COLUMN "public"."lfun_teachers_info"."has_special_education_certificate" IS '是否有特教证书';
COMMENT ON COLUMN "public"."lfun_teachers_info"."information_technology_application_ability" IS '信息技术应用能力';
COMMENT ON COLUMN "public"."lfun_teachers_info"."free_normal_college_student" IS '是否免费师范生';
COMMENT ON COLUMN "public"."lfun_teachers_info"."participated_in_basic_service_project" IS '是否参加基层服务项目';
COMMENT ON COLUMN "public"."lfun_teachers_info"."basic_service_start_date" IS '基层服务起始日期';
COMMENT ON COLUMN "public"."lfun_teachers_info"."basic_service_end_date" IS '基层服务结束日期';
COMMENT ON COLUMN "public"."lfun_teachers_info"."special_education_teacher" IS '是否特教';
COMMENT ON COLUMN "public"."lfun_teachers_info"."dual_teacher" IS '是否双师型';
COMMENT ON COLUMN "public"."lfun_teachers_info"."has_occupational_skill_level_certificate" IS '是否具备职业技能等级证书';
COMMENT ON COLUMN "public"."lfun_teachers_info"."enterprise_work_experience" IS '企业工作时长';
COMMENT ON COLUMN "public"."lfun_teachers_info"."county_level_backbone" IS '是否县级以上骨干';
COMMENT ON COLUMN "public"."lfun_teachers_info"."psychological_health_education_teacher" IS '是否心理健康教育教师';
COMMENT ON COLUMN "public"."lfun_teachers_info"."recruitment_method" IS '招聘方式';
COMMENT ON COLUMN "public"."lfun_teachers_info"."teacher_number" IS '教职工号';
COMMENT ON COLUMN "public"."lfun_teachers_info"."is_deleted" IS '是否删除';
COMMENT ON COLUMN "public"."lfun_teachers_info"."department" IS '部门';
COMMENT ON COLUMN "public"."lfun_teachers_info"."org_id" IS '机构ID';
COMMENT ON COLUMN "public"."lfun_teachers_info"."hmotf" IS '港澳台侨外';
COMMENT ON COLUMN "public"."lfun_teachers_info"."hukou_type" IS '户口类别';
COMMENT ON COLUMN "public"."lfun_teachers_info"."main_teaching_level" IS '主要任课学段';
COMMENT ON COLUMN "public"."lfun_teachers_info"."teacher_qualification_cert_num" IS '教师资格证编号';
COMMENT ON COLUMN "public"."lfun_teachers_info"."teaching_discipline" IS '任教学科';
COMMENT ON COLUMN "public"."lfun_teachers_info"."language" IS '语种';
COMMENT ON COLUMN "public"."lfun_teachers_info"."language_proficiency_level" IS '语言掌握程度';
COMMENT ON COLUMN "public"."lfun_teachers_info"."language_certificate_name" IS '语言证书名称';
COMMENT ON COLUMN "public"."lfun_teachers_info"."contact_address" IS '通讯地址省市县';
COMMENT ON COLUMN "public"."lfun_teachers_info"."contact_address_details" IS '通讯地址详细信息';
COMMENT ON COLUMN "public"."lfun_teachers_info"."email" IS '电子信箱';
COMMENT ON COLUMN "public"."lfun_teachers_info"."highest_education_level" IS '最高学历层次';
COMMENT ON COLUMN "public"."lfun_teachers_info"."highest_degree_name" IS '最高学位名称';
COMMENT ON COLUMN "public"."lfun_teachers_info"."is_major_graduate" IS '是否为师范生';
COMMENT ON COLUMN "public"."lfun_teachers_info"."other_contact_address_details" IS '其他联系方式';
COMMENT ON TABLE "public"."lfun_teachers_info" IS '教师基本信息表模型';

-- ----------------------------
-- Table structure for lfun_transfer_details
-- ----------------------------
DROP TABLE IF EXISTS "public"."lfun_transfer_details";
CREATE TABLE "public"."lfun_transfer_details" (
  "transfer_details_id" int8 NOT NULL DEFAULT nextval('lfun_transfer_details_transfer_details_id_seq'::regclass),
  "original_position" varchar(64) COLLATE "pg_catalog"."default",
  "transfer_in_date" "sys"."date",
  "current_position" varchar(64) COLLATE "pg_catalog"."default",
  "transfer_out_date" "sys"."date",
  "transfer_reason" varchar(64) COLLATE "pg_catalog"."default",
  "remark" varchar(64) COLLATE "pg_catalog"."default",
  "teacher_id" int8,
  "is_deleted" bool NOT NULL,
  "transfer_type" varchar(255) COLLATE "pg_catalog"."default",
  "original_district_province_id" int4,
  "original_district_city_id" int4,
  "original_district_area_id" int4,
  "original_region_province_id" int4,
  "original_region_city_id" int4,
  "original_region_area_id" int4,
  "current_unit_id" int8,
  "current_district_province_id" int4,
  "current_district_city_id" int4,
  "current_district_area_id" int4,
  "current_region_province_id" int4,
  "current_region_city_id" int4,
  "current_region_area_id" int4,
  "original_unit_id" int8,
  "original_unit_name" varchar(64) COLLATE "pg_catalog"."default",
  "current_unit_name" varchar(64) COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "public"."lfun_transfer_details"."transfer_details_id" IS 'transfer_detailsID';
COMMENT ON COLUMN "public"."lfun_transfer_details"."original_position" IS '原岗位';
COMMENT ON COLUMN "public"."lfun_transfer_details"."transfer_in_date" IS '调入日期';
COMMENT ON COLUMN "public"."lfun_transfer_details"."current_position" IS '现岗位';
COMMENT ON COLUMN "public"."lfun_transfer_details"."transfer_out_date" IS '调出日期';
COMMENT ON COLUMN "public"."lfun_transfer_details"."transfer_reason" IS '调动原因';
COMMENT ON COLUMN "public"."lfun_transfer_details"."remark" IS '备注';
COMMENT ON COLUMN "public"."lfun_transfer_details"."teacher_id" IS '教师ID';
COMMENT ON COLUMN "public"."lfun_transfer_details"."is_deleted" IS '是否删除';
COMMENT ON COLUMN "public"."lfun_transfer_details"."transfer_type" IS '调动类型';
COMMENT ON COLUMN "public"."lfun_transfer_details"."original_district_province_id" IS '原行政属地省';
COMMENT ON COLUMN "public"."lfun_transfer_details"."original_district_city_id" IS '原行政属地市';
COMMENT ON COLUMN "public"."lfun_transfer_details"."original_district_area_id" IS '原行政属地区';
COMMENT ON COLUMN "public"."lfun_transfer_details"."original_region_province_id" IS '原管辖区域省';
COMMENT ON COLUMN "public"."lfun_transfer_details"."original_region_city_id" IS '原管辖区域市';
COMMENT ON COLUMN "public"."lfun_transfer_details"."original_region_area_id" IS '原管辖区域区';
COMMENT ON COLUMN "public"."lfun_transfer_details"."current_unit_id" IS '现单位';
COMMENT ON COLUMN "public"."lfun_transfer_details"."current_district_province_id" IS '现行政属地省';
COMMENT ON COLUMN "public"."lfun_transfer_details"."current_district_city_id" IS '现行政属地市';
COMMENT ON COLUMN "public"."lfun_transfer_details"."current_district_area_id" IS '现行政属地区';
COMMENT ON COLUMN "public"."lfun_transfer_details"."current_region_province_id" IS '现管辖区域省';
COMMENT ON COLUMN "public"."lfun_transfer_details"."current_region_city_id" IS '现管辖区域市';
COMMENT ON COLUMN "public"."lfun_transfer_details"."current_region_area_id" IS '现管辖区域区';
COMMENT ON COLUMN "public"."lfun_transfer_details"."original_unit_id" IS '原单位';
COMMENT ON COLUMN "public"."lfun_transfer_details"."original_unit_name" IS '原单位名称';
COMMENT ON COLUMN "public"."lfun_transfer_details"."current_unit_name" IS '现单位名称';
COMMENT ON TABLE "public"."lfun_transfer_details" IS 'transfer_details信息表';

-- ----------------------------
-- Table structure for lfun_user_org_relation
-- ----------------------------
DROP TABLE IF EXISTS "public"."lfun_user_org_relation";
CREATE TABLE "public"."lfun_user_org_relation" (
  "id" int8 NOT NULL,
  "user_id" int8,
  "org_id" varchar(255) COLLATE "pg_catalog"."default",
  "is_deleted" bool NOT NULL
)
;
COMMENT ON COLUMN "public"."lfun_user_org_relation"."user_id" IS '用户ID';
COMMENT ON COLUMN "public"."lfun_user_org_relation"."org_id" IS '组织ID';
COMMENT ON COLUMN "public"."lfun_user_org_relation"."is_deleted" IS '是否删除';
COMMENT ON TABLE "public"."lfun_user_org_relation" IS '组织中心用户关联表';

-- ----------------------------
-- Primary Key structure for table lfun_annual_review
-- ----------------------------
ALTER TABLE "public"."lfun_annual_review" ADD CONSTRAINT "lfun_annual_review_pkey" PRIMARY KEY ("annual_review_id");

-- ----------------------------
-- Primary Key structure for table lfun_attach_relations
-- ----------------------------
ALTER TABLE "public"."lfun_attach_relations" ADD CONSTRAINT "lfun_attach_relations_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table lfun_attachments
-- ----------------------------
ALTER TABLE "public"."lfun_attachments" ADD CONSTRAINT "lfun_attachments_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table lfun_campus
-- ----------------------------
ALTER TABLE "public"."lfun_campus" ADD CONSTRAINT "lfun_campus_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table lfun_campus_communications
-- ----------------------------
ALTER TABLE "public"."lfun_campus_communications" ADD CONSTRAINT "lfun_campus_communications_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table lfun_campus_eduinfo
-- ----------------------------
ALTER TABLE "public"."lfun_campus_eduinfo" ADD CONSTRAINT "lfun_campus_eduinfo_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table lfun_class_division_records
-- ----------------------------
ALTER TABLE "public"."lfun_class_division_records" ADD CONSTRAINT "lfun_class_division_records_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table lfun_classes
-- ----------------------------
ALTER TABLE "public"."lfun_classes" ADD CONSTRAINT "lfun_classes_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table lfun_course
-- ----------------------------
ALTER TABLE "public"."lfun_course" ADD CONSTRAINT "lfun_course_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table lfun_course_school_nature
-- ----------------------------
ALTER TABLE "public"."lfun_course_school_nature" ADD CONSTRAINT "lfun_course_school_nature_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table lfun_domestic_training
-- ----------------------------
ALTER TABLE "public"."lfun_domestic_training" ADD CONSTRAINT "lfun_domestic_training_pkey" PRIMARY KEY ("domestic_training_id");

-- ----------------------------
-- Primary Key structure for table lfun_education_year
-- ----------------------------
ALTER TABLE "public"."lfun_education_year" ADD CONSTRAINT "lfun_education_year_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table lfun_educational_teaching
-- ----------------------------
ALTER TABLE "public"."lfun_educational_teaching" ADD CONSTRAINT "lfun_educational_teaching_pkey" PRIMARY KEY ("educational_teaching_id");

-- ----------------------------
-- Primary Key structure for table lfun_enum_value
-- ----------------------------
ALTER TABLE "public"."lfun_enum_value" ADD CONSTRAINT "lfun_enum_value_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table lfun_grade
-- ----------------------------
ALTER TABLE "public"."lfun_grade" ADD CONSTRAINT "lfun_grade_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table lfun_graduation_student
-- ----------------------------
ALTER TABLE "public"."lfun_graduation_student" ADD CONSTRAINT "lfun_graduation_student_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table lfun_institutions
-- ----------------------------
ALTER TABLE "public"."lfun_institutions" ADD CONSTRAINT "lfun_institutions_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table lfun_leader_info
-- ----------------------------
ALTER TABLE "public"."lfun_leader_info" ADD CONSTRAINT "lfun_leader_info_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table lfun_major
-- ----------------------------
ALTER TABLE "public"."lfun_major" ADD CONSTRAINT "lfun_major_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table lfun_organization
-- ----------------------------
ALTER TABLE "public"."lfun_organization" ADD CONSTRAINT "lfun_organization_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table lfun_organization_members
-- ----------------------------
ALTER TABLE "public"."lfun_organization_members" ADD CONSTRAINT "lfun_organization_members_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table lfun_overseas_study
-- ----------------------------
ALTER TABLE "public"."lfun_overseas_study" ADD CONSTRAINT "lfun_overseas_study_pkey" PRIMARY KEY ("overseas_study_id");

-- ----------------------------
-- Primary Key structure for table lfun_planning_school
-- ----------------------------
ALTER TABLE "public"."lfun_planning_school" ADD CONSTRAINT "lfun_planning_school_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table lfun_planning_school_communications
-- ----------------------------
ALTER TABLE "public"."lfun_planning_school_communications" ADD CONSTRAINT "lfun_planning_school_communications_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table lfun_planning_school_eduinfo
-- ----------------------------
ALTER TABLE "public"."lfun_planning_school_eduinfo" ADD CONSTRAINT "lfun_planning_school_eduinfo_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table lfun_research_achievements
-- ----------------------------
ALTER TABLE "public"."lfun_research_achievements" ADD CONSTRAINT "lfun_research_achievements_pkey" PRIMARY KEY ("research_achievements_id");

-- ----------------------------
-- Primary Key structure for table lfun_school
-- ----------------------------
ALTER TABLE "public"."lfun_school" ADD CONSTRAINT "lfun_school_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table lfun_school_communications
-- ----------------------------
ALTER TABLE "public"."lfun_school_communications" ADD CONSTRAINT "lfun_school_communications_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table lfun_school_eduinfo
-- ----------------------------
ALTER TABLE "public"."lfun_school_eduinfo" ADD CONSTRAINT "lfun_school_eduinfo_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table lfun_student_family_info
-- ----------------------------
ALTER TABLE "public"."lfun_student_family_info" ADD CONSTRAINT "lfun_student_family_info_pkey" PRIMARY KEY ("student_family_info_id");

-- ----------------------------
-- Primary Key structure for table lfun_student_inner_transaction
-- ----------------------------
ALTER TABLE "public"."lfun_student_inner_transaction" ADD CONSTRAINT "lfun_student_inner_transaction_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table lfun_student_session
-- ----------------------------
ALTER TABLE "public"."lfun_student_session" ADD CONSTRAINT "lfun_student_session_pkey" PRIMARY KEY ("session_id");

-- ----------------------------
-- Primary Key structure for table lfun_student_temporary_study
-- ----------------------------
ALTER TABLE "public"."lfun_student_temporary_study" ADD CONSTRAINT "lfun_student_temporary_study_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table lfun_student_transaction
-- ----------------------------
ALTER TABLE "public"."lfun_student_transaction" ADD CONSTRAINT "lfun_student_transaction_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table lfun_student_transaction_flow
-- ----------------------------
ALTER TABLE "public"."lfun_student_transaction_flow" ADD CONSTRAINT "lfun_student_transaction_flow_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table lfun_students
-- ----------------------------
ALTER TABLE "public"."lfun_students" ADD CONSTRAINT "lfun_students_pkey" PRIMARY KEY ("student_id");

-- ----------------------------
-- Primary Key structure for table lfun_students_base_info
-- ----------------------------
ALTER TABLE "public"."lfun_students_base_info" ADD CONSTRAINT "lfun_students_base_info_pkey" PRIMARY KEY ("student_base_id");

-- ----------------------------
-- Primary Key structure for table lfun_subject
-- ----------------------------
ALTER TABLE "public"."lfun_subject" ADD CONSTRAINT "lfun_subject_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table lfun_system_config
-- ----------------------------
ALTER TABLE "public"."lfun_system_config" ADD CONSTRAINT "lfun_system_config_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table lfun_talent_program
-- ----------------------------
ALTER TABLE "public"."lfun_talent_program" ADD CONSTRAINT "lfun_talent_program_pkey" PRIMARY KEY ("talent_program_id");

-- ----------------------------
-- Primary Key structure for table lfun_teacher_borrow
-- ----------------------------
ALTER TABLE "public"."lfun_teacher_borrow" ADD CONSTRAINT "lfun_teacher_borrow_pkey" PRIMARY KEY ("teacher_borrow_id");

-- ----------------------------
-- Primary Key structure for table lfun_teacher_ethic_records
-- ----------------------------
ALTER TABLE "public"."lfun_teacher_ethic_records" ADD CONSTRAINT "lfun_teacher_ethic_records_pkey" PRIMARY KEY ("teacher_ethic_records_id");

-- ----------------------------
-- Primary Key structure for table lfun_teacher_job_appointments
-- ----------------------------
ALTER TABLE "public"."lfun_teacher_job_appointments" ADD CONSTRAINT "lfun_teacher_job_appointments_pkey" PRIMARY KEY ("teacher_job_appointments_id");

-- ----------------------------
-- Primary Key structure for table lfun_teacher_learn_experience
-- ----------------------------
ALTER TABLE "public"."lfun_teacher_learn_experience" ADD CONSTRAINT "lfun_teacher_learn_experience_pkey" PRIMARY KEY ("teacher_learn_experience_id");

-- ----------------------------
-- Primary Key structure for table lfun_teacher_professional_titles
-- ----------------------------
ALTER TABLE "public"."lfun_teacher_professional_titles" ADD CONSTRAINT "lfun_teacher_professional_titles_pkey" PRIMARY KEY ("teacher_professional_titles_id");

-- ----------------------------
-- Primary Key structure for table lfun_teacher_qualifications
-- ----------------------------
ALTER TABLE "public"."lfun_teacher_qualifications" ADD CONSTRAINT "lfun_teacher_qualifications_pkey" PRIMARY KEY ("teacher_qualifications_id");

-- ----------------------------
-- Primary Key structure for table lfun_teacher_retire
-- ----------------------------
ALTER TABLE "public"."lfun_teacher_retire" ADD CONSTRAINT "lfun_teacher_retire_pkey" PRIMARY KEY ("teacher_retire_id");

-- ----------------------------
-- Primary Key structure for table lfun_teacher_skill_certificates
-- ----------------------------
ALTER TABLE "public"."lfun_teacher_skill_certificates" ADD CONSTRAINT "lfun_teacher_skill_certificates_pkey" PRIMARY KEY ("teacher_skill_certificates_id");

-- ----------------------------
-- Primary Key structure for table lfun_teacher_transaction
-- ----------------------------
ALTER TABLE "public"."lfun_teacher_transaction" ADD CONSTRAINT "lfun_teacher_transaction_pkey" PRIMARY KEY ("transaction_id");

-- ----------------------------
-- Primary Key structure for table lfun_teacher_work_experience
-- ----------------------------
ALTER TABLE "public"."lfun_teacher_work_experience" ADD CONSTRAINT "lfun_teacher_work_experience_pkey" PRIMARY KEY ("teacher_work_experience_id");

-- ----------------------------
-- Primary Key structure for table lfun_teachers
-- ----------------------------
ALTER TABLE "public"."lfun_teachers" ADD CONSTRAINT "lfun_teachers_pkey" PRIMARY KEY ("teacher_id");

-- ----------------------------
-- Primary Key structure for table lfun_teachers_info
-- ----------------------------
ALTER TABLE "public"."lfun_teachers_info" ADD CONSTRAINT "lfun_teachers_info_pkey" PRIMARY KEY ("teacher_base_id");

-- ----------------------------
-- Primary Key structure for table lfun_transfer_details
-- ----------------------------
ALTER TABLE "public"."lfun_transfer_details" ADD CONSTRAINT "lfun_transfer_details_pkey" PRIMARY KEY ("transfer_details_id");

-- ----------------------------
-- Primary Key structure for table lfun_user_org_relation
-- ----------------------------
ALTER TABLE "public"."lfun_user_org_relation" ADD CONSTRAINT "lfun_user_org_relation_pkey" PRIMARY KEY ("id");
