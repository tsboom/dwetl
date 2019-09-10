-- Table DW PROCESSING CYCLE JOB

CREATE TABLE "dw_prcsng_cycle_job"(
 "dw_prcsng_cycle_job_name" Character varying(100) NOT NULL,
 "dw_prcsng_cycle_job_version_no" Character varying(20) NOT NULL,
 "dw_prcsng_cycle_job_purpose_desc" Character varying(300) NOT NULL,
 "dw_prcsng_cycle_job_code_object_name" Character varying(100) NOT NULL,
 "dw_prcsng_cycle_job_code_object_version_no" Smallint NOT NULL,
 "dw_prcsng_cycle_job_code_object_loc_path_txt" Character varying(200) NOT NULL,
 "em_create_tmstmp" Timestamp NOT NULL,
 "em_create_user_id" Character varying(20) NOT NULL,
 "em_update_tmstmp" Timestamp,
 "em_update_user_id" Character varying(20)
)
WITH (
 autovacuum_enabled=true)
;

-- Add keys for table DW PROCESSING CYCLE JOB

ALTER TABLE "dw_prcsng_cycle_job" ADD CONSTRAINT "dw_prcsng_cycle_job_key" PRIMARY KEY ("dw_prcsng_cycle_job_name","dw_prcsng_cycle_job_version_no")
;

-- Table DW_PRCSNG_CYCLE_JOB_EXECTN

CREATE TABLE "dw_prcsng_cycle_job_exectn"(
 "dw_prcsng_cycle_job_exectn_id" Integer NOT NULL,
 "dw_prcsng_cycle_job_name" Character varying(100) NOT NULL,
 "dw_prcsng_cycle_job_version_no" Character varying(20) NOT NULL,
 "dw_prcsng_cycle_id" Integer NOT NULL,
 "dw_prcsng_cycle_job_exectn_processed_rec_cnt" Integer,
 "dw_prcsng_cycle_job_exectn_success_rec_cnt" Integer,
 "dw_prcsng_cycle_job_exectn_suspend_rec_cnt" Integer,
 "dw_prcsng_cycle_job_exectn_elapsed_time" Smallint,
 "dw_prcsng_cycle_job_exectn_invoking_user_id" Character varying(20) NOT NULL,
 "dw_prcsng_cycle_job_exectn_start_tmstmp" Timestamp NOT NULL,
 "dw_prcsng_cycle_job_exectn_end_tmstmp" Timestamp,
 "em_create_tmstmp" Timestamp NOT NULL,
 "em_create_user_id" Character varying(20) NOT NULL,
 "em_update_tmstmp" Timestamp,
 "em_update_user_id" Character varying(20)
)
WITH (
 autovacuum_enabled=true)
;

-- Create indexes for table DW_PRCSNG_CYCLE_JOB_EXECTN

CREATE INDEX "IX_Relationship2" ON "dw_prcsng_cycle_job_exectn" ("dw_prcsng_cycle_id")
;

-- Add keys for table DW_PRCSNG_CYCLE_JOB_EXECTN

ALTER TABLE "dw_prcsng_cycle_job_exectn" ADD CONSTRAINT "dw_prcsng_cycle_episode_job_exectn_key" PRIMARY KEY ("dw_prcsng_cycle_job_exectn_id")
;

-- Table DW_PRCSNG_CYCLE

CREATE TABLE "dw_prcsng_cycle"(
 "dw_prcsng_cycle_id" Integer NOT NULL,
 "dw_prcsng_cycle_planned_dt" Date NOT NULL,
 "dw_prcsng_cycle_stat_type_cd" Character(1) NOT NULL,
 "dw_prcsng_cycle_freq_type_cd" Character(2) NOT NULL,
 "dw_prcsng_cycle_exectn_start_tmstmp" Timestamp,
 "dw_prcsng_cycle_exectn_end_tmstmp" Timestamp,
 "em_create_tmstmp" Timestamp NOT NULL,
 "em_create_user_id" Character varying(20) NOT NULL,
 "em_update_tmstmp" Timestamp,
 "em_update_user_id" Character varying(20),
 "em_update_reason_txt" Character varying(100)
)
WITH (
 autovacuum_enabled=true)
;

-- Add keys for table DW_PRCSNG_CYCLE

ALTER TABLE "dw_prcsng_cycle" ADD CONSTRAINT "dw_prcsng_cycle_episode_key" PRIMARY KEY ("dw_prcsng_cycle_id")
;
