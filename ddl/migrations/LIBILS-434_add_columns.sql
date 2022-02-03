BEGIN;

ALTER TABLE dw_stg_2_bib_rec_z13u
RENAME COLUMN dq_z13u_user_defined_2 TO dq_z13u_user_defined_2;

ALTER TABLE dw_stg_2_bib_rec_z13u
ADD COLUMN t3_z13u_user_defined_3__bib_rec_type_desc character varying(500);

ALTER TABLE dw_stg_2_bib_rec_z13u
ADD COLUMN t4_z13u_user_defined_3__bib_rec_bib_lvl_cd character(1);

ALTER TABLE dw_stg_2_bib_rec_z13u
ADD COLUMN t5_z13u_user_defined_3__bib_rec_bib_lvl_desc character varying(500);

ALTER TABLE dw_stg_2_bib_rec_z13u
ADD COLUMN t6_z13u_user_defined_3__bib_rec_encoding_lvl_cdc character(1);

ALTER TABLE dw_stg_2_bib_rec_z13u
ADD COLUMN t7_z13u_user_defined_3__bib_rec_encoding_lvl_desc character varying(500);

-- how to make not null in this postgres script?
ALTER TABLE dw_stg_2_bib_rec_z00
ADD COLUMN rec_trigger_key character(9) NOT NULL;

ALTER TABLE dw_db_errors
ALTER COLUMN dw_error_row TYPE character varying(5000)
ADD COLUMN em_update_dw_prcsng_cycle_id integer,	
ADD COLUMN em_update_dw_job_exectn_id integer,	
ADD COLUMN em_update_dw_job_name character varying(100),	
ADD COLUMN em_update_dw_job_version_no character varying(20),	
ADD COLUMN em_update_reason_txt character varying(100),	
ADD COLUMN em_update_user_id character varying(20),	
ADD COLUMN em_update_tmstmp timestamp without time zone;

-- I need to add a column to the primary key to this table. will dropping a constraint mess with the data? I'm scared. 
ALTER TABLE dw_stg_2_bib_rec_z00 DROP CONSTRAINT pk_dw_stg_2_bib_rec_z00;
ALTER TABLE dw_stg_2_bib_rec_z00 ADD CONSTRAINT ADD CONSTRAINT pk_dw_stg_2_bib_rec_z00 PRIMARY KEY (db_operation_cd, dw_stg_2_aleph_lbry_name, rec_trigger_key, in_z00_doc_number, em_create_dw_prcsng_cycle_id);

COMMIT;




