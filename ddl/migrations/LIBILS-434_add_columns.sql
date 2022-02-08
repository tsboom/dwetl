BEGIN;

-- need to drop this table and recreate it because when we add columns onto it the order of the columns is inconvenient. 

DROP TABLE dw_stg_2_bib_rec_z13u;

CREATE TABLE public.dw_stg_2_bib_rec_z13u (
    db_operation_cd character(1) NOT NULL,
    dw_stg_2_aleph_lbry_name character(5) NOT NULL,
    in_z13u_rec_key character(9) NOT NULL,
    in_z13u_user_defined_2 character varying(500),
    pp_z13u_user_defined_2 character varying(500),
    dq_z13u_user_defined_2 character varying(500),
    t1_z13u_user_defined_2__bib_rec_oclc_no character varying(500),
    in_z13u_user_defined_3 character varying(500),
    pp_z13u_user_defined_3 character varying(500),
    dq_z13u_user_defined_3 character varying(500),
    t1_z13u_user_defined_3__bib_rec_marc_rec_leader_field_txt character varying(500),
    t2_z13u_user_defined_3__bib_rec_type_cd character(1),
    t3_z13u_user_defined_3__bib_rec_type_desc character varying(500),
    t4_z13u_user_defined_3__bib_rec_bib_lvl_cd character(1),
    t5_z13u_user_defined_3__bib_rec_bib_lvl_desc character varying(500),
    t6_z13u_user_defined_3__bib_rec_encoding_lvl_cd character(1),
    t7_z13u_user_defined_3__bib_rec_encoding_lvl_desc character varying(500),
    in_z13u_user_defined_4 character varying(500),
    pp_z13u_user_defined_4 character varying(500),
    dq_z13u_user_defined_4 character varying(500),
    t1_z13u_user_defined_4__bib_rec_marc_rec_008_field_txt character varying(500),
    t2_z13u_user_defined_4__bib_rec_language_cd character(3),
    in_z13u_user_defined_5 character varying(500),
    pp_z13u_user_defined_5 character varying(500),
    dq_z13u_user_defined_5 character varying(500),
    t1_z13u_user_defined_5__bib_rec_issn character varying(500),
    in_z13u_user_defined_6 character varying(500),
    pp_z13u_user_defined_6 character varying(500),
    dq_z13u_user_defined_6 character varying(500),
    t1_z13u_user_defined_6__bib_rec_display_suppressed_flag character(1),
    t2_z13u_user_defined_6__bib_rec_acquisition_created_flag character(1),
    t3_z13u_user_defined_6__bib_rec_circulation_created_flag character(1),
    t4_z13u_user_defined_6__bib_rec_provisional_status_flag character(1),
    in_z13u_user_defined_1_code character(5),
    in_z13u_user_defined_1 character varying(500),
    in_z13u_user_defined_2_code character(5),
    in_z13u_user_defined_3_code character(5),
    in_z13u_user_defined_4_code character(5),
    in_z13u_user_defined_5_code character(5),
    in_z13u_user_defined_6_code character(5),
    in_z13u_user_defined_7_code character(5),
    in_z13u_user_defined_7 character varying(500),
    in_z13u_user_defined_8_code character(5),
    in_z13u_user_defined_8 character varying(500),
    in_z13u_user_defined_9_code character(5),
    in_z13u_user_defined_9 character varying(500),
    in_z13u_user_defined_10_code character(5),
    in_z13u_user_defined_10 character varying(500),
    in_z13u_user_defined_11_code character(5),
    in_z13u_user_defined_11 character varying(500),
    in_z13u_user_defined_12_code character(5),
    in_z13u_user_defined_12 character varying(500),
    in_z13u_user_defined_13_code character(5),
    in_z13u_user_defined_13 character varying(500),
    in_z13u_user_defined_14_code character(5),
    in_z13u_user_defined_14 character varying(500),
    in_z13u_user_defined_15_code character(5),
    in_z13u_user_defined_15 character varying(500),
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


ALTER TABLE public.dw_stg_2_bib_rec_z13u OWNER TO usmai_dw;

ALTER TABLE ONLY public.dw_stg_2_bib_rec_z13u
    ADD CONSTRAINT pk_dw_stg_2_bib_rec_z13u PRIMARY KEY (db_operation_cd, dw_stg_2_aleph_lbry_name, in_z13u_rec_key, em_create_dw_prcsng_cycle_id);


ALTER TABLE dw_db_errors
-- need to write test for this in end to end 
ALTER COLUMN dw_error_row TYPE character varying(5000),
ADD COLUMN em_update_dw_prcsng_cycle_id integer,	
ADD COLUMN em_update_dw_job_exectn_id integer,	
ADD COLUMN em_update_dw_job_name character varying(100),	
ADD COLUMN em_update_dw_job_version_no character varying(20),	
ADD COLUMN em_update_reason_txt character varying(100),	
ADD COLUMN em_update_user_id character varying(20),	
ADD COLUMN em_update_tmstmp timestamp without time zone;






-- dropping this empty table because it needs a new NOT NULL column and its PK modified. 
DROP TABLE dw_stg_2_bib_rec_z00;

CREATE TABLE public.dw_stg_2_bib_rec_z00 (
    db_operation_cd character(1) NOT NULL,
    dw_stg_2_aleph_lbry_name character(5) NOT NULL,
    rec_trigger_key character(9) NOT NULL,
    in_z00_doc_number character(9) NOT NULL,
    pp_z00_doc_number character(9),
    dq_z00_doc_number character(9),
    t1_z00_doc_number__bib_rec_source_system_id character(9),
    in_z00_no_lines character varying(4),
    pp_z00_no_lines character varying(4),
    dq_z00_no_lines smallint,
    t1_z00_no_lines__bib_rec_marc_rec_field_cnt smallint,
    in_z00_data_len character varying(6),
    pp_z00_data_len character varying(6),
    dq_z00_data_len integer,
    t1_z00_data_len__bib_rec_marc_rec_data_cntnt_len_cnt integer,
    in_z00_data character varying(45000),
    pp_z00_data character varying(45000),
    dq_z00_data character varying(45000),
    t1_z00_data__bib_rec_marc_rec_data_cntnt_txt character varying(45000),
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


ALTER TABLE public.dw_stg_2_bib_rec_z00 OWNER TO usmai_dw;


--
-- Name: dw_stg_2_bib_rec_z00 pk_dw_stg_2_bib_rec_z00; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.dw_stg_2_bib_rec_z00
    ADD CONSTRAINT pk_dw_stg_2_bib_rec_z00 PRIMARY KEY (db_operation_cd, dw_stg_2_aleph_lbry_name, rec_trigger_key, in_z00_doc_number, em_create_dw_prcsng_cycle_id);


COMMIT;




