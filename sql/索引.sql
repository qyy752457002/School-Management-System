CREATE INDEX "block" ON "public"."lfun_planning_school" (
  "block"
);

CREATE INDEX "block" ON "public"."lfun_school" (
  "block"
);
CREATE INDEX "teacher_employer" ON "public"."lfun_teachers" (
  "teacher_employer"
);
CREATE INDEX "school_id" ON "public"."lfun_students_base_info" (
  "school_id"
);
CREATE INDEX "planning_school_no" ON "public"."lfun_planning_school" (
  "planning_school_no"
);
CREATE INDEX "process_instance_id" ON "public"."lfun_planning_school" (
  "process_instance_id"
);

CREATE INDEX "school_no" ON "public"."lfun_school" (
  "school_no"
);
CREATE INDEX "process_instance_id" ON "public"."lfun_school" (
  "process_instance_id"
);

CREATE INDEX "teacher_name" ON "public"."lfun_teachers" (
  "teacher_name"
);
CREATE INDEX "teacher_id_number" ON "public"."lfun_teachers" (
  "teacher_id_number"
);
CREATE INDEX "mobile" ON "public"."lfun_teachers" (
  "mobile"
);
CREATE INDEX "teacher_id" ON "public"."lfun_teachers_info" (
  "teacher_id"
);
CREATE INDEX "student_name" ON "public"."lfun_students" (
  "student_name"
);
CREATE INDEX "enrollment_number" ON "public"."lfun_students" (
  "enrollment_number"
);
CREATE INDEX "id_number" ON "public"."lfun_students" (
  "id_number"
);

CREATE INDEX "student_id" ON "public"."lfun_students_base_info" (
  "student_id"
);
CREATE INDEX "edu_number" ON "public"."lfun_students_base_info" (
  "edu_number"
);


CREATE INDEX "student_number" ON "public"."lfun_students_base_info" (
  "student_number"
);
CREATE INDEX "school_id" ON "public"."lfun_students_base_info" (
  "school_id"
);
CREATE INDEX "grade_id" ON "public"."lfun_students_base_info" (
  "grade_id"
);
CREATE INDEX "class_id" ON "public"."lfun_students_base_info" (
  "class_id"
);