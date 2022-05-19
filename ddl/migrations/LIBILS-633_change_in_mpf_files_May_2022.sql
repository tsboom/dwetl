ALTER TABLE dw_stg_2_mpf_lbry_entity
ALTER COLUMN in_lbry_entity_cd TYPE varchar(5);

ALTER TABLE dw_stg_2_mpf_collection
ALTER COLUMN in_lbry_entity_cd TYPE varchar(5);

ALTER TABLE dw_stg_2_mpf_collection
ALTER COLUMN rm_dq_check_excptn_cnt drop not null;



ALTER TABLE dw_stg_1_mpf_matrl_form
ALTER COLUMN matrl_form_name TYPE character varying(100);

-- changing the dw_stg_2_mpf_item_prcs_status table


DROP TABLE public.dw_stg_2_mpf_item_prcs_status;



CREATE TABLE public.dw_stg_2_mpf_item_prcs_status (
    db_operation_cd character varying(1) NOT NULL,
    in_usmai_mbr_lbry_cd character(2) NOT NULL,
    pp_usmai_mbr_lbry_cd character(2),
    dq_usmai_mbr_lbry_cd character(2),
    in_item_prcs_status_cd character varying(2) NOT NULL,
    pp_item_prcs_status_cd character varying(2),
    dq_item_prcs_status_cd character varying(2),
    in_item_prcs_status_desc character varying(100),
    pp_item_prcs_status_desc character varying(100),
    dq_item_prcs_status_desc character varying(100),
    db_operation_effective_date character varying(10),
    lbry_staff_lms_user_id character varying(10),
    rm_suspend_rec_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_suspend_rec_reason_cd character(3),
    rm_dq_check_excptn_cnt smallint DEFAULT 0 NOT NULL,
    em_create_dw_prcsng_cycle_id integer NOT NULL,
    em_create_dw_job_exectn_id integer NOT NULL,
    em_create_dw_job_name character varying(100) NOT NULL,
    em_create_dw_job_version_no character varying(20) NOT NULL,
    em_create_user_id character varying(20) NOT NULL,
    em_create_tmstmp timestamp without time zone NOT NULL,
    em_update_dw_prcsng_cycle_id integer,
    em_update_dw_job_exectn_id integer,
    em_update_dw_job_name character varying(100),
    em_update_dw_job_version_no character varying(20),
    em_update_user_id character varying(20),
    em_update_tmstmp timestamp without time zone
  )
WITH (autovacuum_enabled='true');

ALTER TABLE public.dw_stg_2_mpf_item_prcs_status OWNER TO usmai_dw;


ALTER TABLE public.dw_stg_2_mpf_item_prcs_status
  ADD CONSTRAINT pk_dw_stg_2_mpf_item_prcs_status PRIMARY KEY (in_usmai_mbr_lbry_cd, in_item_prcs_status_cd, em_create_dw_prcsng_cycle_id);

-- ALTER TABLE dw_stg_2_mpf_item_prcs_status
-- ALTER COLUMN in_mbr_lbry_cd drop not null;

-- alter table users alter column email drop not null;
-- ALTER COLUMN rm_dq_check_excptn_cnt smallint NULL;
-- MODIFY Age int NOT NULL;
-- ALTER rm_dq_check_excptn_cnt NULL;
