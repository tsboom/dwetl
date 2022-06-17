--
-- PostgreSQL database dump
--

-- Dumped from database version 11.15
-- Dumped by pg_dump version 11.15

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;


DROP DATABASE IF EXISTS usmai_dw_etl_test;

--
-- Name: usmai_dw_etl_test; Type: DATABASE; Schema: -; Owner: usmai_dw
--

CREATE DATABASE usmai_dw_etl_test WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'en_US.UTF-8' LC_CTYPE = 'en_US.UTF-8' TABLESPACE = usmai_dw;


ALTER DATABASE usmai_dw_etl_test OWNER TO usmai_dw;

\connect usmai_dw_etl_test

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: dim_bib_rec; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.dim_bib_rec (
    bib_rec_dim_key bigint NOT NULL,
    bib_rec_source_system_id character(9) NOT NULL,
    bib_rec_aleph_lbry_cd character varying(5) NOT NULL,
    bib_rec_marc_rec_field_cnt smallint NOT NULL,
    bib_rec_marc_rec_data_cntnt_len_cnt smallint NOT NULL,
    bib_rec_marc_rec_data_cntnt_txt character varying(45000) NOT NULL,
    bib_rec_publication_yr_no smallint,
    bib_rec_title character varying(100) NOT NULL,
    bib_rec_author_name character varying(100),
    bib_rec_imprint_txt character varying(100),
    bib_rec_isbn_issn_source_cd character varying(5),
    bib_rec_isbn_txt character varying(100),
    bib_rec_all_associated_issns_txt character varying(100),
    bib_rec_oclc_no character varying(500),
    bib_rec_marc_rec_leader_field_txt character varying(500) NOT NULL,
    bib_rec_type_cd character(1) NOT NULL,
    bib_rec_bib_lvl_cd character(1) NOT NULL,
    bib_rec_encoding_lvl_cd character(1) NOT NULL,
    bib_rec_marc_rec_008_field_txt character varying(500) NOT NULL,
    bib_rec_language_cd character(3),
    bib_rec_issn character varying(500),
    bib_rec_display_suppressed_flag character(1),
    bib_rec_acquisition_created_flag character(1),
    bib_rec_circulation_created_flag character(1),
    bib_rec_provisional_status_flag character(1),
    bib_rec_create_dt date NOT NULL,
    bib_rec_update_dt date,
    rm_rec_type_cd character(1) NOT NULL,
    rm_rec_type_desc character varying(30) NOT NULL,
    rm_rec_version_no smallint NOT NULL,
    rm_rec_effective_from_dt date NOT NULL,
    rm_rec_effective_to_dt date NOT NULL,
    rm_current_rec_flag character(1) NOT NULL,
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
    em_update_reason_txt character varying(100),
    em_update_user_id character varying(20),
    em_update_tmstmp timestamp without time zone
)
WITH (autovacuum_enabled='true');


ALTER TABLE public.dim_bib_rec OWNER TO usmai_dw;

--
-- Name: dim_bib_rec_seq; Type: SEQUENCE; Schema: public; Owner: usmai_dw
--

CREATE SEQUENCE public.dim_bib_rec_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.dim_bib_rec_seq OWNER TO usmai_dw;

--
-- Name: dim_date; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.dim_date (
    clndr_dt_dim_key integer NOT NULL,
    clndr_dt date NOT NULL,
    clndr_dt_desc character varying(20) NOT NULL,
    usmai_fiscal_yr_no smallint NOT NULL,
    clndr_yr_no smallint NOT NULL,
    clndr_qtr_no smallint NOT NULL,
    clndr_mth_no smallint NOT NULL,
    clndr_mth_name character varying(9) NOT NULL,
    clndr_mth_abrvtn character(3) NOT NULL,
    clndr_day_no smallint NOT NULL,
    clndr_day_name character varying(9) NOT NULL,
    clndr_day_abrvtn character(3) NOT NULL,
    clndr_day_in_wk_no smallint NOT NULL,
    clndr_day_in_yr_no integer NOT NULL,
    clndr_wk_in_mth_no smallint NOT NULL,
    clndr_wk_in_yr_no smallint NOT NULL,
    clndr_yr_qtr_no smallint NOT NULL,
    clndr_yr_mth_no integer NOT NULL,
    clndr_yr_day_no integer NOT NULL,
    weekday_flag character(1) NOT NULL,
    rm_rec_type_cd character(1) NOT NULL,
    rm_rec_type_desc character varying(30) NOT NULL,
    rm_rec_version_no smallint NOT NULL,
    rm_rec_effective_from_dt date NOT NULL,
    rm_rec_effective_to_dt date NOT NULL,
    rm_current_rec_flag character(1) NOT NULL,
    em_create_dw_prcsng_cycle_id integer NOT NULL,
    em_create_dw_job_name character varying(100) NOT NULL,
    em_create_dw_job_version_no character varying(20) NOT NULL,
    em_create_dw_job_exectn_id integer NOT NULL,
    em_create_user_id character varying(20) NOT NULL,
    em_create_tmstmp timestamp without time zone NOT NULL,
    em_update_dw_prcsng_cycle_id integer,
    em_update_dw_job_name character varying(100),
    em_update_dw_job_version_no character varying(20),
    em_update_dw_job_exectn_id integer,
    em_update_reason_txt character varying(100),
    em_update_user_id character varying(20),
    em_update_tmstmp timestamp without time zone
)
WITH (autovacuum_enabled='true');


ALTER TABLE public.dim_date OWNER TO usmai_dw;

--
-- Name: dim_lbry_holding; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.dim_lbry_holding (
    lbry_holding_dim_key bigint NOT NULL,
    lbry_holding_source_system_id character(9) NOT NULL,
    lbry_holding_aleph_lbry_cd character(5) NOT NULL,
    lbry_holding_marc_rec_field_cnt smallint NOT NULL,
    lbry_holding_marc_rec_data_cntnt_len_cnt smallint NOT NULL,
    lbry_holding_marc_rec_data_cntnt_txt character varying(45000) NOT NULL,
    lbry_holding_action_note character varying(500),
    lbry_holding_disply_suppressed_flag character(1) NOT NULL,
    lbry_holding_summary_holdings_txt character varying(500),
    lbry_holding_supp_summary_holdings_txt character varying(500),
    lbry_holding_index_summary_holdings_txt character varying(500),
    lbry_holding_loc_call_no_scheme_cd character(1),
    lbry_holding_loc_call_no character varying(100),
    lbry_holding_loc_public_note character varying(500),
    lbry_holding_loc_non_public_note character varying(500),
    lbry_holding_create_dt date NOT NULL,
    lbry_holding_update_dt date,
    lbry_holding_maint_usmai_mbr_lbry_cd character(2) NOT NULL,
    lbry_holding_maint_usmai_mbr_lbry_cd_actual_source_txt character varying(500) NOT NULL,
    lbry_holding_super_holding_flag character(1) NOT NULL,
    rm_rec_type_cd character(1) NOT NULL,
    rm_rec_type_desc character varying(30) NOT NULL,
    rm_rec_version_no smallint NOT NULL,
    rm_rec_effective_from_dt date NOT NULL,
    rm_rec_effective_to_dt date NOT NULL,
    rm_current_rec_flag character(1) NOT NULL,
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
    em_update_reason_txt character varying(100),
    em_update_user_id character varying(20),
    em_update_tmstmp timestamp without time zone
)
WITH (autovacuum_enabled='true');


ALTER TABLE public.dim_lbry_holding OWNER TO usmai_dw;

--
-- Name: dim_lbry_item; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.dim_lbry_item (
    lbry_item_dim_key bigint NOT NULL,
    lbry_item_source_system_id character(15) NOT NULL,
    lbry_item_adm_no character(9) NOT NULL,
    lbry_item_seq_no character(6) NOT NULL,
    lbry_item_aleph_lbry_name character(5) NOT NULL,
    lbry_item_update_lms_staff_acct_id character varying(10),
    lbry_item_create_dt date NOT NULL,
    lbry_item_update_dt date NOT NULL,
    lbry_item_volume_issue_no character varying(200),
    lbry_item_accession_dt date,
    lbry_item_page_range_txt character varying(30),
    lbry_item_copy_no character(5),
    lbry_item_pulication_dt date NOT NULL,
    lbry_item_supplemental_matrl_title character varying(30),
    lbry_item_expected_arrival_dt date NOT NULL,
    lbry_item_actual_arrival_dt date NOT NULL,
    lbry_item_acquisition_price_txt character varying(10),
    lbry_item_barcode_no character varying(30),
    lbry_item_loc_call_no_scheme_cd character(1),
    lbry_item_loc_call_no_scheme_desc character varying(50),
    lbry_item_loc_call_no character varying(80),
    lbry_item_loc_sort_nrmlzd_call_no character varying(80),
    lbry_item_loc_temp_designation_flag character(1),
    lbry_item_loc_alt_call_no_scheme_cd character(1),
    lbry_item_loc_alt_call_no_scheme_desc character varying(50),
    lbry_item_loc_alt_call_no character varying(80),
    lbry_item_loc_alt_sort_nrmlzd_call_no character varying(80),
    lbry_item_enumeration_lvl_1_txt character varying(20),
    lbry_item_enumeration_lvl_2_txt character varying(20),
    lbry_item_enumeration_lvl_3_txt character varying(20),
    lbry_item_enumeration_lvl_4_txt character varying(20),
    lbry_item_enumeration_lvl_5_txt character varying(20),
    lbry_item_enumeration_lvl_6_txt character varying(20),
    lbry_item_alt_enumeration_lvl_1_txt character varying(20),
    lbry_item_alt_enumeration_lvl_2_txt character varying(20),
    lbry_item_chronology_lvl_1_txt character varying(20),
    lbry_item_chronology_lvl_2_txt character varying(20),
    lbry_item_chronology_lvl_3_txt character varying(20),
    lbry_item_chronology_lvl_4_txt character varying(20),
    lbry_item_alt_chronology_txt character varying(20),
    lbry_item_circulation_display_note character varying(200),
    lbry_item_opac_dislpay_txt character varying(200),
    lbry_item_staff_only_display_note character varying(200),
    lbry_item_most_recent_loan_event_dt date,
    lbry_item_most_recent_loan_event_time smallint,
    lbry_item_most_recent_loan_event_type_cd character(2),
    lbry_item_most_recent_loan_event_ip_addr character varying(20),
    lbry_item_most_recent_return_event_dt date,
    lbry_item_most_recent_return_event_time smallint,
    lbry_item_most_recent_return_event_type_cd character(2),
    lbry_item_most_recent_return_event_ip_addr character varying(20),
    lbry_item_most_recent_renew_event_dt date,
    lbry_item_most_recent_renew_event_time smallint,
    lbry_item_most_recent_renew_event_type_cd character(2),
    lbry_item_most_recent_renew_event_ip_addr character varying(20),
    rm_rec_type_cd character(1) NOT NULL,
    rm_rec_type_desc character varying(30) NOT NULL,
    rm_rec_version_no smallint NOT NULL,
    rm_rec_effective_from_dt date NOT NULL,
    rm_rec_effective_to_dt date NOT NULL,
    rm_current_rec_flag character(1) NOT NULL,
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
    em_update_reason_txt character varying(100),
    em_update_user_id character varying(20),
    em_update_tmstmp timestamp without time zone
)
WITH (autovacuum_enabled='true');


ALTER TABLE public.dim_lbry_item OWNER TO usmai_dw;

--
-- Name: dim_lbry_item_loc; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.dim_lbry_item_loc (
    lbry_item_loc_dim_key integer NOT NULL,
    lbry_item_loc_usmai_mbr_lbry_cd character(2) NOT NULL,
    lbry_item_loc_usmai_mbr_lbry_name character varying(70) NOT NULL,
    lbry_item_loc_usmai_mbr_lbry_mbrshp_type_cd character varying(10) NOT NULL,
    lbry_item_loc_lbry_entity_cd character(5) NOT NULL,
    lbry_item_loc_lbry_entity_name character varying(30) NOT NULL,
    lbry_item_loc_collection_cd character varying(5) NOT NULL,
    lbry_item_loc_collection_name character varying(80) NOT NULL,
    rm_rec_type_cd character(1) NOT NULL,
    rm_rec_type_desc character varying(30) NOT NULL,
    rm_rec_version_no smallint NOT NULL,
    rm_rec_effective_from_dt date NOT NULL,
    rm_rec_effective_to_dt date NOT NULL,
    rm_current_rec_flag character(1) NOT NULL,
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
    em_update_reason_txt character varying(100),
    em_update_user_id character varying(20),
    em_update_tmstmp timestamp without time zone
)
WITH (autovacuum_enabled='true');


ALTER TABLE public.dim_lbry_item_loc OWNER TO usmai_dw;

--
-- Name: dim_lbry_item_matrl_form; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.dim_lbry_item_matrl_form (
    lbry_item_matrl_form_dim_key smallint NOT NULL,
    lbry_item_matrl_form_cd character varying(5) NOT NULL,
    lbry_item_matrl_form_name character varying(50) NOT NULL,
    rm_rec_type_cd character(1) NOT NULL,
    rm_rec_type_desc character varying(30) NOT NULL,
    rm_rec_version_no smallint NOT NULL,
    rm_rec_effective_from_dt date NOT NULL,
    rm_rec_effective_to_dt date NOT NULL,
    rm_current_rec_flag character(1) NOT NULL,
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
    em_update_reason_txt character varying(100),
    em_update_user_id character varying(20),
    em_update_tmstmp timestamp without time zone
)
WITH (autovacuum_enabled='true');


ALTER TABLE public.dim_lbry_item_matrl_form OWNER TO usmai_dw;

--
-- Name: dim_lbry_item_prcs_status; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.dim_lbry_item_prcs_status (
    lbry_item_prcs_status_dim_key smallint NOT NULL,
    lbry_item_usmai_mbr_lbry_cd character(2) NOT NULL,
    lbry_item_prcs_status_cd character(2) NOT NULL,
    lbry_item_prcs_status_public_desc character varying(50) NOT NULL,
    lbry_item_prcs_status_internal_desc character varying(50) NOT NULL,
    rm_rec_type_cd character(1) NOT NULL,
    rm_rec_type_desc character varying(30) NOT NULL,
    rm_rec_version_no smallint NOT NULL,
    rm_rec_effective_from_dt date NOT NULL,
    rm_rec_effective_to_dt date NOT NULL,
    rm_current_rec_flag character(1) NOT NULL,
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
    em_update_reason_txt character varying(100),
    em_update_user_id character varying(20),
    em_update_tmstmp timestamp without time zone
)
WITH (autovacuum_enabled='true');


ALTER TABLE public.dim_lbry_item_prcs_status OWNER TO usmai_dw;

--
-- Name: dim_lbry_item_status; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.dim_lbry_item_status (
    lbry_item_status_dim_key smallint NOT NULL,
    lbry_item_usmai_mbr_lbry_cd character(2) NOT NULL,
    lbry_item_status_cd character(2) NOT NULL,
    lbry_item_status_desc character varying(50) NOT NULL,
    rm_rec_type_cd character(1) NOT NULL,
    rm_rec_type_desc character varying(30) NOT NULL,
    rm_rec_version_no smallint NOT NULL,
    rm_rec_effective_from_dt date NOT NULL,
    rm_rec_effective_to_dt date NOT NULL,
    rm_current_rec_flag character(1) NOT NULL,
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
    em_update_reason_txt character varying(100),
    em_update_user_id character varying(20),
    em_update_tmstmp timestamp without time zone
)
WITH (autovacuum_enabled='true');


ALTER TABLE public.dim_lbry_item_status OWNER TO usmai_dw;

--
-- Name: dw_db_errors; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.dw_db_errors (
    dw_error_id integer NOT NULL,
    dw_error_type character varying(150) NOT NULL,
    dw_error_text character varying(2000) NOT NULL,
    dw_error_row character varying(5000) NOT NULL,
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
    em_update_reason_txt character varying(100),
    em_update_user_id character varying(20),
    em_update_tmstmp timestamp without time zone
)
WITH (autovacuum_enabled='true');


ALTER TABLE public.dw_db_errors OWNER TO usmai_dw;

--
-- Name: dw_prcsing_cycle_job_exectn_id; Type: SEQUENCE; Schema: public; Owner: usmai_dw
--

CREATE SEQUENCE public.dw_prcsing_cycle_job_exectn_id
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.dw_prcsing_cycle_job_exectn_id OWNER TO usmai_dw;

--
-- Name: dw_prcsng_cycle; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.dw_prcsng_cycle (
    dw_prcsng_cycle_id integer NOT NULL,
    dw_prcsng_cycle_planned_dt date NOT NULL,
    dw_prcsng_cycle_stat_type_cd character(1) NOT NULL,
    dw_prcsng_cycle_freq_type_cd character(2) NOT NULL,
    dw_prcsng_cycle_exectn_start_tmstmp timestamp without time zone,
    dw_prcsng_cycle_exectn_end_tmstmp timestamp without time zone,
    em_create_tmstmp timestamp without time zone NOT NULL,
    em_create_user_id character varying(20) NOT NULL,
    em_update_tmstmp timestamp without time zone,
    em_update_user_id character varying(20),
    em_update_reason_txt character varying(100)
)
WITH (autovacuum_enabled='true');


ALTER TABLE public.dw_prcsng_cycle OWNER TO usmai_dw;

--
-- Name: dw_prcsng_cycle_job; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.dw_prcsng_cycle_job (
    dw_prcsng_cycle_job_name character varying(100) NOT NULL,
    dw_prcsng_cycle_job_version_no character varying(20) NOT NULL,
    dw_prcsng_cycle_job_purpose_desc character varying(300) NOT NULL,
    dw_prcsng_cycle_job_code_object_name character varying(100) NOT NULL,
    dw_prcsng_cycle_job_code_object_version_no smallint NOT NULL,
    dw_prcsng_cycle_job_code_object_loc_path_txt character varying(200) NOT NULL,
    em_create_tmstmp timestamp without time zone NOT NULL,
    em_create_user_id character varying(20) NOT NULL,
    em_update_tmstmp timestamp without time zone,
    em_update_user_id character varying(20)
)
WITH (autovacuum_enabled='true');


ALTER TABLE public.dw_prcsng_cycle_job OWNER TO usmai_dw;

--
-- Name: dw_prcsng_cycle_job_exectn; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.dw_prcsng_cycle_job_exectn (
    dw_prcsng_cycle_job_exectn_id integer NOT NULL,
    dw_prcsng_cycle_job_name character varying(100) NOT NULL,
    dw_prcsng_cycle_job_version_no character varying(20) NOT NULL,
    dw_prcsng_cycle_id integer NOT NULL,
    dw_prcsng_cycle_job_exectn_processed_rec_cnt integer,
    dw_prcsng_cycle_job_exectn_success_rec_cnt integer,
    dw_prcsng_cycle_job_exectn_suspend_rec_cnt integer,
    dw_prcsng_cycle_job_exectn_elapsed_time smallint,
    dw_prcsng_cycle_job_exectn_invoking_user_id character varying(20) NOT NULL,
    dw_prcsng_cycle_job_exectn_start_tmstmp timestamp without time zone NOT NULL,
    dw_prcsng_cycle_job_exectn_end_tmstmp timestamp without time zone,
    em_create_tmstmp timestamp without time zone NOT NULL,
    em_create_user_id character varying(20) NOT NULL,
    em_update_tmstmp timestamp without time zone,
    em_update_user_id character varying(20)
)
WITH (autovacuum_enabled='true');


ALTER TABLE public.dw_prcsng_cycle_job_exectn OWNER TO usmai_dw;

--
-- Name: dw_stg_1_ezp_sessns_snap; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.dw_stg_1_ezp_sessns_snap (
    mbr_lbry_cd character varying(2) NOT NULL,
    ezp_sessns_snap_tmstmp character varying(13) NOT NULL,
    ezp_sessns_snap_actv_sessns_cnt integer NOT NULL,
    ezp_sessns_virtual_hosts_cnt integer NOT NULL,
    em_create_dw_prcsng_cycle_id integer NOT NULL,
    em_create_dw_job_exectn_id integer NOT NULL,
    em_create_dw_job_name character varying(100) NOT NULL,
    em_create_dw_job_version_no character varying(20) NOT NULL,
    em_create_user_id character varying(20) NOT NULL,
    em_create_tmstmp timestamp without time zone NOT NULL
)
WITH (autovacuum_enabled='true');


ALTER TABLE public.dw_stg_1_ezp_sessns_snap OWNER TO usmai_dw;

--
-- Name: dw_stg_1_mai01_z00; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.dw_stg_1_mai01_z00 (
    rec_type_cd character(1) NOT NULL,
    db_operation_cd character(1) NOT NULL,
    rec_trigger_key character(9) NOT NULL,
    z00_doc_number character(9),
    z00_no_lines character varying(4),
    z00_data_len character varying(6),
    z00_data character varying(45000),
    em_create_dw_prcsng_cycle_id integer NOT NULL,
    em_create_dw_job_exectn_id integer NOT NULL,
    em_create_dw_job_name character varying(100) NOT NULL,
    em_create_dw_job_version_no character varying(20) NOT NULL,
    em_create_user_id character varying(20) NOT NULL,
    em_create_tmstmp timestamp without time zone NOT NULL
)
WITH (autovacuum_enabled='true');


ALTER TABLE public.dw_stg_1_mai01_z00 OWNER TO usmai_dw;

--
-- Name: dw_stg_1_mai01_z00_field; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.dw_stg_1_mai01_z00_field (
    rec_type_cd character(1) NOT NULL,
    db_operation_cd character(1) NOT NULL,
    rec_trigger_key character(9) NOT NULL,
    z00_doc_number character(9),
    dw_stg_1_marc_rec_field_seq_no smallint NOT NULL,
    z00_marc_rec_field_cd character varying(5),
    z00_marc_rec_field_txt character varying(2000),
    em_create_dw_prcsng_cycle_id integer NOT NULL,
    em_create_dw_job_exectn_id integer NOT NULL,
    em_create_dw_job_name character varying(100) NOT NULL,
    em_create_dw_job_version_no character varying(20) NOT NULL,
    em_create_user_id character varying(20) NOT NULL,
    em_create_tmstmp timestamp without time zone NOT NULL
)
WITH (autovacuum_enabled='true');


ALTER TABLE public.dw_stg_1_mai01_z00_field OWNER TO usmai_dw;

--
-- Name: dw_stg_1_mai01_z13; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.dw_stg_1_mai01_z13 (
    rec_type_cd character(1) NOT NULL,
    db_operation_cd character(1) NOT NULL,
    rec_trigger_key character(9) NOT NULL,
    z13_rec_key character(9),
    z13_year character varying(4),
    z13_open_date character varying(8),
    z13_update_date character(8),
    z13_call_no_key character varying(80),
    z13_call_no_code character(5),
    z13_call_no character varying(100),
    z13_author_code character(5),
    z13_author character varying(100),
    z13_title_code character(5),
    z13_title character varying(100),
    z13_imprint_code character(5),
    z13_imprint character varying(100),
    z13_isbn_issn_code character(5),
    z13_isbn_issn character varying(100),
    z13_upd_time_stamp character(15),
    em_create_dw_prcsng_cycle_id integer NOT NULL,
    em_create_dw_job_exectn_id integer NOT NULL,
    em_create_dw_job_name character varying(100) NOT NULL,
    em_create_dw_job_version_no character varying(20) NOT NULL,
    em_create_user_id character varying(20) NOT NULL,
    em_create_tmstmp timestamp without time zone NOT NULL
)
WITH (autovacuum_enabled='true');


ALTER TABLE public.dw_stg_1_mai01_z13 OWNER TO usmai_dw;

--
-- Name: dw_stg_1_mai01_z13u; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.dw_stg_1_mai01_z13u (
    rec_type_cd character(1) NOT NULL,
    db_operation_cd character(1) NOT NULL,
    rec_trigger_key character(9) NOT NULL,
    z13u_rec_key character(9),
    z13u_user_defined_1_code character(5),
    z13u_user_defined_1 character varying(500),
    z13u_user_defined_2_code character(5),
    z13u_user_defined_2 character varying(500),
    z13u_user_defined_3_code character(5),
    z13u_user_defined_3 character varying(500),
    z13u_user_defined_4_code character(5),
    z13u_user_defined_4 character varying(500),
    z13u_user_defined_5_code character(5),
    z13u_user_defined_5 character varying(500),
    z13u_user_defined_6_code character(5),
    z13u_user_defined_6 character varying(500),
    z13u_user_defined_7_code character(5),
    z13u_user_defined_7 character varying(500),
    z13u_user_defined_8_code character(5),
    z13u_user_defined_8 character varying(500),
    z13u_user_defined_9_code character(5),
    z13u_user_defined_9 character varying(500),
    z13u_user_defined_10_code character(5),
    z13u_user_defined_10 character varying(500),
    z13u_user_defined_11_code character(5),
    z13u_user_defined_11 character varying(500),
    z13u_user_defined_12_code character(5),
    z13u_user_defined_12 character varying(500),
    z13u_user_defined_13_code character(5),
    z13u_user_defined_13 character varying(500),
    z13u_user_defined_14_code character(5),
    z13u_user_defined_14 character varying(500),
    z13u_user_defined_15_code character(5),
    z13u_user_defined_15 character varying(500),
    em_create_dw_prcsng_cycle_id integer NOT NULL,
    em_create_dw_job_exectn_id integer NOT NULL,
    em_create_dw_job_name character varying(100) NOT NULL,
    em_create_dw_job_version_no character varying(20) NOT NULL,
    em_create_user_id character varying(20) NOT NULL,
    em_create_tmstmp timestamp without time zone NOT NULL
)
WITH (autovacuum_enabled='true');


ALTER TABLE public.dw_stg_1_mai01_z13u OWNER TO usmai_dw;

--
-- Name: dw_stg_1_mai39_z00; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.dw_stg_1_mai39_z00 (
    rec_type_cd character(1) NOT NULL,
    db_operation_cd character(1) NOT NULL,
    rec_trigger_key character(9) NOT NULL,
    z00_doc_number character(9),
    z00_no_lines character varying(4),
    z00_data_len character varying(6),
    z00_data character varying(45000),
    em_create_dw_prcsng_cycle_id integer NOT NULL,
    em_create_dw_job_exectn_id integer NOT NULL,
    em_create_dw_job_name character varying(100) NOT NULL,
    em_create_dw_job_version_no character varying(20) NOT NULL,
    em_create_user_id character varying(20) NOT NULL,
    em_create_tmstmp timestamp without time zone NOT NULL
)
WITH (autovacuum_enabled='true');


ALTER TABLE public.dw_stg_1_mai39_z00 OWNER TO usmai_dw;

--
-- Name: dw_stg_1_mai39_z00_field; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.dw_stg_1_mai39_z00_field (
    rec_type_cd character(1) NOT NULL,
    db_operation_cd character(1) NOT NULL,
    rec_trigger_key character(9) NOT NULL,
    z00_doc_number character(9),
    dw_stg_1_marc_rec_field_seq_no smallint NOT NULL,
    z00_marc_rec_field_cd character varying(5),
    z00_marc_rec_field_txt character varying(2000),
    em_create_dw_prcsng_cycle_id integer NOT NULL,
    em_create_dw_job_exectn_id integer NOT NULL,
    em_create_dw_job_name character varying(100) NOT NULL,
    em_create_dw_job_version_no character varying(20) NOT NULL,
    em_create_user_id character varying(20) NOT NULL,
    em_create_tmstmp timestamp without time zone NOT NULL
)
WITH (autovacuum_enabled='true');


ALTER TABLE public.dw_stg_1_mai39_z00_field OWNER TO usmai_dw;

--
-- Name: dw_stg_1_mai39_z13; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.dw_stg_1_mai39_z13 (
    rec_type_cd character(1) NOT NULL,
    db_operation_cd character(1) NOT NULL,
    rec_trigger_key character(9) NOT NULL,
    z13_rec_key character(9),
    z13_year character varying(4),
    z13_open_date character varying(8),
    z13_update_date character(8),
    z13_call_no_key character varying(80),
    z13_call_no_code character(5),
    z13_call_no character varying(100),
    z13_author_code character(5),
    z13_author character varying(100),
    z13_title_code character(5),
    z13_title character varying(100),
    z13_imprint_code character(5),
    z13_imprint character varying(100),
    z13_isbn_issn_code character(5),
    z13_isbn_issn character varying(100),
    z13_upd_time_stamp character(15),
    em_create_dw_prcsng_cycle_id integer NOT NULL,
    em_create_dw_job_exectn_id integer NOT NULL,
    em_create_dw_job_name character varying(100) NOT NULL,
    em_create_dw_job_version_no character varying(20) NOT NULL,
    em_create_user_id character varying(20) NOT NULL,
    em_create_tmstmp timestamp without time zone NOT NULL
)
WITH (autovacuum_enabled='true');


ALTER TABLE public.dw_stg_1_mai39_z13 OWNER TO usmai_dw;

--
-- Name: dw_stg_1_mai39_z13u; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.dw_stg_1_mai39_z13u (
    rec_type_cd character(1) NOT NULL,
    db_operation_cd character(1) NOT NULL,
    rec_trigger_key character(9) NOT NULL,
    z13u_rec_key character(9),
    z13u_user_defined_1_code character(5),
    z13u_user_defined_1 character varying(500),
    z13u_user_defined_2_code character(5),
    z13u_user_defined_2 character varying(500),
    z13u_user_defined_3_code character(5),
    z13u_user_defined_3 character varying(500),
    z13u_user_defined_4_code character(5),
    z13u_user_defined_4 character varying(500),
    z13u_user_defined_5_code character(5),
    z13u_user_defined_5 character varying(500),
    z13u_user_defined_6_code character(5),
    z13u_user_defined_6 character varying(500),
    z13u_user_defined_7_code character(5),
    z13u_user_defined_7 character varying(500),
    z13u_user_defined_8_code character(5),
    z13u_user_defined_8 character varying(500),
    z13u_user_defined_9_code character(5),
    z13u_user_defined_9 character varying(500),
    z13u_user_defined_10_code character(5),
    z13u_user_defined_10 character varying(500),
    z13u_user_defined_11_code character(5),
    z13u_user_defined_11 character varying(500),
    z13u_user_defined_12_code character(5),
    z13u_user_defined_12 character varying(500),
    z13u_user_defined_13_code character(5),
    z13u_user_defined_13 character varying(500),
    z13u_user_defined_14_code character(5),
    z13u_user_defined_14 character varying(500),
    z13u_user_defined_15_code character(5),
    z13u_user_defined_15 character varying(500),
    em_create_dw_prcsng_cycle_id integer NOT NULL,
    em_create_dw_job_exectn_id integer NOT NULL,
    em_create_dw_job_name character varying(100) NOT NULL,
    em_create_dw_job_version_no character varying(20) NOT NULL,
    em_create_user_id character varying(20) NOT NULL,
    em_create_tmstmp timestamp without time zone NOT NULL
)
WITH (autovacuum_enabled='true');


ALTER TABLE public.dw_stg_1_mai39_z13u OWNER TO usmai_dw;


--
-- Name: dw_stg_1_mai50_z103_bib_full; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.dw_stg_1_mai50_z103_bib_full (
    rec_type_cd character(1) NOT NULL,
    db_operation_cd character(1) NOT NULL,
    rec_trigger_key character(9) NOT NULL,
    source character(9),
    dest character(9),
    dest_lib character(5),
    dest_docnum character(9),
    em_create_dw_prcsng_cycle_id integer NOT NULL,
    em_create_dw_job_exectn_id integer NOT NULL,
    em_create_dw_job_name character varying(100) NOT NULL,
    em_create_dw_job_version_no character varying(20) NOT NULL,
    em_create_user_id character varying(20) NOT NULL,
    em_create_tmstmp timestamp without time zone NOT NULL
)
WITH (autovacuum_enabled='true');


ALTER TABLE public.dw_stg_1_mai50_z103_bib_full OWNER TO usmai_dw;

--
-- Name: dw_stg_1_mai50_z30; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.dw_stg_1_mai50_z30 (
    rec_type_cd character(1) NOT NULL,
    db_operation_cd character(1) NOT NULL,
    rec_trigger_key character(15) NOT NULL,
    z30_rec_key character(15),
    z30_barcode character(30),
    z30_sub_library character(5),
    z30_material character(5),
    z30_item_status character(2),
    z30_open_date character varying(8),
    z30_update_date character varying(8),
    z30_cataloger character(10),
    z30_date_last_return character varying(8),
    z30_hour_last_return character varying(4),
    z30_ip_last_return character varying(20),
    z30_no_loans character varying(3),
    z30_alpha character(1),
    z30_collection character(5),
    z30_call_no_type character(1),
    z30_call_no character varying(80),
    z30_call_no_key character(80),
    z30_call_no_2_type character(1),
    z30_call_no_2 character varying(80),
    z30_call_no_2_key character(80),
    z30_description character varying(200),
    z30_note_opac character varying(200),
    z30_note_circulation character varying(200),
    z30_note_internal character varying(200),
    z30_order_number character varying(30),
    z30_inventory_number character varying(20),
    z30_inventory_number_date character varying(8),
    z30_last_shelf_report_date character varying(8),
    z30_price character(10),
    z30_shelf_report_number character(20),
    z30_on_shelf_date character varying(8),
    z30_on_shelf_seq character varying(6),
    z30_rec_key_2 character(19),
    z30_rec_key_3 character(40),
    z30_pages character varying(30),
    z30_issue_date character varying(8),
    z30_expected_arrival_date character varying(8),
    z30_arrival_date character(8),
    z30_item_statistic character(10),
    z30_item_process_status character(2),
    z30_copy_id character(5),
    z30_hol_doc_number_x character(9),
    z30_temp_location character(1),
    z30_enumeration_a character varying(20),
    z30_enumeration_b character varying(20),
    z30_enumeration_c character varying(20),
    z30_enumeration_d character varying(20),
    z30_enumeration_e character varying(20),
    z30_enumeration_f character varying(20),
    z30_enumeration_g character varying(20),
    z30_enumeration_h character varying(20),
    z30_chronological_i character varying(20),
    z30_chronological_j character varying(20),
    z30_chronological_k character varying(20),
    z30_chronological_l character varying(20),
    z30_chronological_m character varying(20),
    z30_supp_index_o character varying(30),
    z30_85x_type character(1),
    z30_depository_id character(5),
    z30_linking_number character varying(9),
    z30_gap_indicator character(1),
    z30_maintenance_count character varying(3),
    z30_process_status_date character varying(8),
    z30_upd_time_stamp character(15),
    z30_ip_last_return_v6 character varying(50),
    em_create_dw_prcsng_cycle_id integer NOT NULL,
    em_create_dw_job_exectn_id integer NOT NULL,
    em_create_dw_job_name character varying(100) NOT NULL,
    em_create_dw_job_version_no character varying(20) NOT NULL,
    em_create_user_id character varying(20) NOT NULL,
    em_create_tmstmp timestamp without time zone NOT NULL
)
WITH (autovacuum_enabled='true');


ALTER TABLE public.dw_stg_1_mai50_z30 OWNER TO usmai_dw;

--
-- Name: dw_stg_1_mai50_z30_full; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.dw_stg_1_mai50_z30_full (
    rec_type_cd character(1) NOT NULL,
    db_operation_cd character(1) NOT NULL,
    rec_trigger_key character(15) NOT NULL,
    z30_rec_key character(15),
    z30_barcode character(30),
    z30_sub_library character(5),
    z30_material character(5),
    z30_item_status character(2),
    z30_open_date character varying(8),
    z30_hol_doc_number_x character(9),
    z30_order_number character varying(30),
    em_create_dw_prcsng_cycle_id integer NOT NULL,
    em_create_dw_job_exectn_id integer NOT NULL,
    em_create_dw_job_name character varying(100) NOT NULL,
    em_create_dw_job_version_no character varying(20) NOT NULL,
    em_create_user_id character varying(20) NOT NULL,
    em_create_tmstmp timestamp without time zone NOT NULL
)
WITH (autovacuum_enabled='true');


ALTER TABLE public.dw_stg_1_mai50_z30_full OWNER TO usmai_dw;

--
-- Name: dw_stg_1_mai50_z35; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.dw_stg_1_mai50_z35 (
    rec_type_cd character(1) NOT NULL,
    db_operation_cd character(1) NOT NULL,
    rec_trigger_key character(22) NOT NULL,
    z35_rec_key character(9),
    z35_item_sequence character varying(6),
    z35_event_type character(2),
    z35_time_stamp character(22),
    z35_id character(12),
    z35_material character(5),
    z35_sub_library character(5),
    z35_status character(2),
    z35_event_date numeric(8,0),
    z35_event_hour numeric(4,0),
    z35_item_status character(2),
    z35_bor_status character(2),
    z35_bor_type character(2),
    z35_cataloger_name character(10),
    z35_type character(1),
    z35_ip_address character varying(20),
    z35_query character varying(500),
    z35_note character varying(100),
    z35_upd_time_stamp character(15),
    z35_ip_address_v6 character varying(50),
    em_create_dw_prcsng_cycle_id integer NOT NULL,
    em_create_dw_job_exectn_id integer NOT NULL,
    em_create_dw_job_name character varying(100) NOT NULL,
    em_create_dw_job_version_no character varying(20) NOT NULL,
    em_create_user_id character varying(20) NOT NULL,
    em_create_tmstmp timestamp without time zone NOT NULL
)
WITH (autovacuum_enabled='true');


ALTER TABLE public.dw_stg_1_mai50_z35 OWNER TO usmai_dw;

--
-- Name: dw_stg_1_mai60_z00; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.dw_stg_1_mai60_z00 (
    rec_type_cd character(1) NOT NULL,
    db_operation_cd character(1) NOT NULL,
    rec_trigger_key character(9) NOT NULL,
    z00_doc_number character(9),
    z00_no_lines character varying(4),
    z00_data_len character varying(6),
    z00_data character varying(45000),
    em_create_dw_prcsng_cycle_id integer NOT NULL,
    em_create_dw_job_exectn_id integer NOT NULL,
    em_create_dw_job_name character varying(100) NOT NULL,
    em_create_dw_job_version_no character varying(20) NOT NULL,
    em_create_user_id character varying(20) NOT NULL,
    em_create_tmstmp timestamp without time zone NOT NULL
)
WITH (autovacuum_enabled='true');


ALTER TABLE public.dw_stg_1_mai60_z00 OWNER TO usmai_dw;

--
-- Name: dw_stg_1_mai60_z00_field; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.dw_stg_1_mai60_z00_field (
    rec_type_cd character(1) NOT NULL,
    db_operation_cd character(1) NOT NULL,
    rec_trigger_key character(9) NOT NULL,
    z00_doc_number character(9),
    dw_stg_1_marc_rec_field_seq_no smallint NOT NULL,
    z00_marc_rec_field_cd character varying(5),
    z00_marc_rec_field_txt character varying(2000),
    em_create_dw_prcsng_cycle_id integer NOT NULL,
    em_create_dw_job_exectn_id integer NOT NULL,
    em_create_dw_job_name character varying(100) NOT NULL,
    em_create_dw_job_version_no character varying(20) NOT NULL,
    em_create_user_id character varying(20) NOT NULL,
    em_create_tmstmp timestamp without time zone NOT NULL
)
WITH (autovacuum_enabled='true');


ALTER TABLE public.dw_stg_1_mai60_z00_field OWNER TO usmai_dw;

--
-- Name: dw_stg_1_mai60_z103_bib; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.dw_stg_1_mai60_z103_bib (
    rec_type_cd character(1) NOT NULL,
    db_operation_cd character(1) NOT NULL,
    rec_trigger_key character(9) NOT NULL,
    source character(9),
    dest character(9),
    dest_lib character(5),
    dest_docnum character(9),
    em_create_dw_prcsng_cycle_id integer NOT NULL,
    em_create_dw_job_exectn_id integer NOT NULL,
    em_create_dw_job_name character varying(100) NOT NULL,
    em_create_dw_job_version_no character varying(20) NOT NULL,
    em_create_user_id character varying(20) NOT NULL,
    em_create_tmstmp timestamp without time zone NOT NULL
)
WITH (autovacuum_enabled='true');


ALTER TABLE public.dw_stg_1_mai60_z103_bib OWNER TO usmai_dw;

--
-- Name: dw_stg_1_mai60_z13; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.dw_stg_1_mai60_z13 (
    rec_type_cd character(1) NOT NULL,
    db_operation_cd character(1) NOT NULL,
    rec_trigger_key character(9) NOT NULL,
    z13_rec_key character(9),
    z13_year character varying(4),
    z13_open_date character varying(8),
    z13_update_date character(8),
    z13_call_no_key character varying(80),
    z13_call_no_code character(5),
    z13_call_no character varying(100),
    z13_author_code character(5),
    z13_author character varying(100),
    z13_title_code character(5),
    z13_title character varying(100),
    z13_imprint_code character(5),
    z13_imprint character varying(100),
    z13_isbn_issn_code character(5),
    z13_isbn_issn character varying(100),
    z13_upd_time_stamp character(15),
    em_create_dw_prcsng_cycle_id integer NOT NULL,
    em_create_dw_job_exectn_id integer NOT NULL,
    em_create_dw_job_name character varying(100) NOT NULL,
    em_create_dw_job_version_no character varying(20) NOT NULL,
    em_create_user_id character varying(20) NOT NULL,
    em_create_tmstmp timestamp without time zone NOT NULL
)
WITH (autovacuum_enabled='true');


ALTER TABLE public.dw_stg_1_mai60_z13 OWNER TO usmai_dw;

--
-- Name: dw_stg_1_mai60_z13u; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.dw_stg_1_mai60_z13u (
    rec_type_cd character(1) NOT NULL,
    db_operation_cd character(1) NOT NULL,
    rec_trigger_key character(9) NOT NULL,
    z13u_rec_key character(9),
    z13u_user_defined_1_code character(5),
    z13u_user_defined_1 character varying(500),
    z13u_user_defined_2_code character(5),
    z13u_user_defined_2 character varying(500),
    z13u_user_defined_3_code character(5),
    z13u_user_defined_3 character varying(500),
    z13u_user_defined_4_code character(5),
    z13u_user_defined_4 character varying(500),
    z13u_user_defined_5_code character(5),
    z13u_user_defined_5 character varying(500),
    z13u_user_defined_6_code character(5),
    z13u_user_defined_6 character varying(500),
    z13u_user_defined_7_code character(5),
    z13u_user_defined_7 character varying(500),
    z13u_user_defined_8_code character(5),
    z13u_user_defined_8 character varying(500),
    z13u_user_defined_9_code character(5),
    z13u_user_defined_9 character varying(500),
    z13u_user_defined_10_code character(5),
    z13u_user_defined_10 character varying(500),
    z13u_user_defined_11_code character(5),
    z13u_user_defined_11 character varying(500),
    z13u_user_defined_12_code character(5),
    z13u_user_defined_12 character varying(500),
    z13u_user_defined_13_code character(5),
    z13u_user_defined_13 character varying(500),
    z13u_user_defined_14_code character(5),
    z13u_user_defined_14 character varying(500),
    z13u_user_defined_15_code character(5),
    z13u_user_defined_15 character varying(500),
    em_create_dw_prcsng_cycle_id integer NOT NULL,
    em_create_dw_job_exectn_id integer NOT NULL,
    em_create_dw_job_name character varying(100) NOT NULL,
    em_create_dw_job_version_no character varying(20) NOT NULL,
    em_create_user_id character varying(20) NOT NULL,
    em_create_tmstmp timestamp without time zone NOT NULL
)
WITH (autovacuum_enabled='true');


ALTER TABLE public.dw_stg_1_mai60_z13u OWNER TO usmai_dw;

--
-- Name: dw_stg_1_mpf_collection; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.dw_stg_1_mpf_collection (
    db_operation_cd character varying(1) NOT NULL,
    collection_cd character varying(5) NOT NULL,
    collection_name character varying(80),
    usmai_mbr_lbry_cd character varying(2) NOT NULL,
    lbry_entity_cd character varying(5) NOT NULL,
    db_operation_effective_date character(10),
    lbry_staff_lms_user_id character varying(10),
    em_create_dw_prcsng_cycle_id integer NOT NULL,
    em_create_dw_job_exectn_id integer NOT NULL,
    em_create_dw_job_name character varying(100) NOT NULL,
    em_create_dw_job_version_no character varying(20) NOT NULL,
    em_create_user_id character varying(20) NOT NULL,
    em_create_tmstmp timestamp without time zone NOT NULL
)
WITH (autovacuum_enabled='true');


ALTER TABLE public.dw_stg_1_mpf_collection OWNER TO usmai_dw;

--
-- Name: dw_stg_1_mpf_item_prcs_status; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.dw_stg_1_mpf_item_prcs_status (
    db_operation_cd character varying(1) NOT NULL,
    usmai_mbr_lbry_cd character(2) NOT NULL,
    item_prcs_status_cd character varying(2) NOT NULL,
    item_prcs_status_public_desc character varying(30),
    item_prcs_status_internal_desc character varying(50),
    db_operation_effective_date character(10),
    lbry_staff_lms_user_id character varying(10),
    em_create_dw_prcsng_cycle_id integer NOT NULL,
    em_create_dw_job_exectn_id integer NOT NULL,
    em_create_dw_job_name character varying(100) NOT NULL,
    em_create_dw_job_version_no character varying(20) NOT NULL,
    em_create_user_id character varying(20) NOT NULL,
    em_create_tmstmp timestamp without time zone NOT NULL
)
WITH (autovacuum_enabled='true');


ALTER TABLE public.dw_stg_1_mpf_item_prcs_status OWNER TO usmai_dw;

--
-- Name: dw_stg_1_mpf_item_status; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.dw_stg_1_mpf_item_status (
    db_operation_cd character varying(1) NOT NULL,
    usmai_mbr_lbry_cd character(2) NOT NULL,
    item_status_cd character varying(2) NOT NULL,
    item_status_desc character varying(30),
    db_operation_effective_date character(10),
    lbry_staff_lms_user_id character varying(10),
    em_create_dw_prcsng_cycle_id integer NOT NULL,
    em_create_dw_job_exectn_id integer NOT NULL,
    em_create_dw_job_name character varying(100) NOT NULL,
    em_create_dw_job_version_no character varying(20) NOT NULL,
    em_create_user_id character varying(20) NOT NULL,
    em_create_tmstmp timestamp without time zone NOT NULL
)
WITH (autovacuum_enabled='true');


ALTER TABLE public.dw_stg_1_mpf_item_status OWNER TO usmai_dw;

--
-- Name: dw_stg_1_mpf_lbry_entity; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.dw_stg_1_mpf_lbry_entity (
    db_operation_cd character varying(1) NOT NULL,
    usmai_mbr_lbry_cd character varying(2) NOT NULL,
    lbry_entity_cd character varying(5) NOT NULL,
    lbry_entity_name character varying(30),
    db_operation_effective_date character(10),
    lbry_staff_lms_user_id character varying(10),
    em_create_dw_prcsng_cycle_id integer NOT NULL,
    em_create_dw_job_exectn_id integer NOT NULL,
    em_create_dw_job_name character varying(100) NOT NULL,
    em_create_dw_job_version_no character varying(20) NOT NULL,
    em_create_user_id character varying(20) NOT NULL,
    em_create_tmstmp timestamp without time zone NOT NULL
)
WITH (autovacuum_enabled='true');


ALTER TABLE public.dw_stg_1_mpf_lbry_entity OWNER TO usmai_dw;

--
-- Name: dw_stg_1_mpf_matrl_form; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.dw_stg_1_mpf_matrl_form (
    db_operation_cd character varying(1) NOT NULL,
    matrl_form_cd character varying(5) NOT NULL,
    matrl_form_name character varying(30),
    db_operation_effective_date character(10),
    lbry_staff_lms_user_id character varying(10),
    em_create_dw_prcsng_cycle_id integer NOT NULL,
    em_create_dw_job_exectn_id integer NOT NULL,
    em_create_dw_job_name character varying(100) NOT NULL,
    em_create_dw_job_version_no character varying(20) NOT NULL,
    em_create_user_id character varying(20) NOT NULL,
    em_create_tmstmp timestamp without time zone NOT NULL
)
WITH (autovacuum_enabled='true');


ALTER TABLE public.dw_stg_1_mpf_matrl_form OWNER TO usmai_dw;

--
-- Name: dw_stg_1_mpf_mbr_lbry; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.dw_stg_1_mpf_mbr_lbry (
    db_operation_cd character varying(1) NOT NULL,
    usmai_mbr_lbry_cd character varying(2) NOT NULL,
    usmai_mbr_lbry_name character varying(70),
    db_operation_effective_date character(10),
    lbry_staff_lms_user_id character varying(10),
    em_create_dw_prcsng_cycle_id integer NOT NULL,
    em_create_dw_job_exectn_id integer NOT NULL,
    em_create_dw_job_name character varying(100) NOT NULL,
    em_create_dw_job_version_no character varying(20) NOT NULL,
    em_create_user_id character varying(20) NOT NULL,
    usmai_mbr_lbry_mbrshp_type_cd character varying(10),
    em_create_tmstmp timestamp without time zone NOT NULL
)
WITH (autovacuum_enabled='true');


ALTER TABLE public.dw_stg_1_mpf_mbr_lbry OWNER TO usmai_dw;

--
-- Name: dw_stg_2_bib_rec_z00; Type: TABLE; Schema: public; Owner: usmai_dw
--

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
-- Name: dw_stg_2_bib_rec_z00_field; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.dw_stg_2_bib_rec_z00_field (
    db_operation_cd character(2) NOT NULL,
    dw_stg_2_aleph_lbry_name character(5) NOT NULL,
    in_z00_doc_number character(9) NOT NULL,
    pp_z00_doc_number character(9),
    dq_z00_doc_number character(9),
    t1_z00_doc_number__bib_rec_source_system_id character(9),
    in_dw_stg_1_marc_rec_field_seq_no smallint NOT NULL,
    in_z00_marc_rec_field_cd character(5),
    pp_z00_marc_rec_field_cd character(5),
    dq_z00_marc_rec_field_cd character(5),
    t1_z00_marc_rec_field_cd__bib_rec_marc_rec_field_cd character(3),
    in_z00_marc_rec_field_txt character varying(2000),
    pp_z00_marc_rec_field_txt character varying(2000),
    dq_z00_marc_rec_field_txt character varying(2000),
    t1_z00_marc_rec_field_txt__bib_rec_marc_rec_field_txt character varying(2000),
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


ALTER TABLE public.dw_stg_2_bib_rec_z00_field OWNER TO usmai_dw;

--
-- Name: dw_stg_2_bib_rec_z13; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.dw_stg_2_bib_rec_z13 (
    db_operation_cd character(1) NOT NULL,
    dw_stg_2_aleph_lbry_name character(5) NOT NULL,
    in_z13_rec_key character(9) NOT NULL,
    in_z13_year character varying(4),
    pp_z13_year character varying(4),
    dq_z13_year character varying(4),
    t1_z13_year__bib_rec_publication_yr_no smallint,
    in_z13_open_date character varying(8),
    pp_z13_open_date character varying(8),
    dq_z13_open_date character varying(8),
    t1_z13_open_date__bib_rec_create_dt date,
    in_z13_update_date character varying(8),
    pp_z13_update_date character varying(8),
    dq_z13_update_date character varying(8),
    t1_z13_update_date__bib_rec_update_dt date,
    in_z13_author character varying(100),
    pp_z13_author character varying(100),
    dq_z13_author character varying(100),
    t1_z13_author__bib_rec_author_name character varying(100),
    in_z13_title character varying(100),
    pp_z13_title character varying(100),
    dq_z13_title character varying(100),
    t1_z13_title__bib_rec_title character varying(100),
    in_z13_imprint character varying(100),
    pp_z13_imprint character varying(100),
    dq_z13_imprint character varying(100),
    t1_z13_imprint__bib_rec_imprint_txt character varying(100),
    in_z13_isbn_issn_code character(5),
    pp_z13_isbn_issn_code character varying(5),
    dq_z13_isbn_issn_code character varying(5),
    t1_z13_isbn_issn_code__bib_rec_isbn_issn_source_cd character varying(5),
    in_z13_isbn_issn character varying(100),
    pp_z13_isbn_issn character varying(100),
    dq_z13_isbn_issn character varying(100),
    t1_z13_isbn_issn__bib_rec_isbn_txt character varying(100),
    t2_z13_isbn_issn__bib_rec_all_associated_issns_txt character varying(100),
    in_z13_upd_time_stamp character(15) DEFAULT '200001011200000'::bpchar,
    in_z13_call_no_key character varying(80),
    in_z13_call_no_code character(5),
    in_z13_call_no character varying(100),
    in_z13_author_code character(5),
    in_z13_title_code character(5),
    in_z13_imprint_code character(5),
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


ALTER TABLE public.dw_stg_2_bib_rec_z13 OWNER TO usmai_dw;

--
-- Name: dw_stg_2_bib_rec_z13u; Type: TABLE; Schema: public; Owner: usmai_dw
--

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

--
-- Name: dw_stg_2_ezp_sessns_snap; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.dw_stg_2_ezp_sessns_snap (
    in_mbr_lbry_cd character varying(2) NOT NULL,
    t1_mbr_lbry_cd__ezp_sessns_snap_mbr_lbry_dim_key character varying(2),
    in_ezp_sessns_snap_tmstmp character varying(13) NOT NULL,
    t1_ezp_sessns_snap_tmstmp__ezp_sessns_snap_clndr_dt_dim_key bigint,
    t2_ezp_sessns_snap_tmstmp__ezp_sessns_snap_tmstmp timestamp without time zone,
    t3_ezp_sessns_snap_tmstmp__ezp_sessns_snap_time_of_day_dim_key integer,
    in_ezp_sessns_snap_actv_sessns_cnt integer NOT NULL,
    t1_ezp_sessns_snap_actv_sessns_cnt integer,
    in_ezp_sessns_virtual_hosts_cnt integer NOT NULL,
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


ALTER TABLE public.dw_stg_2_ezp_sessns_snap OWNER TO usmai_dw;

--
-- Name: dw_stg_2_lbry_holding_z00; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.dw_stg_2_lbry_holding_z00 (
    db_operation_cd character(1) NOT NULL,
    dw_stg_2_aleph_lbry_name character(5) NOT NULL,
    in_z00_doc_number character(9) NOT NULL,
    pp_z00_doc_number character(9),
    dq_z00_doc_number character(9),
    t1_z00_doc_number__lbry_holding_source_system_id character(9),
    in_z00_no_lines character varying(4),
    pp_z00_no_lines character varying(4),
    dq_z00_no_lines character varying(4),
    t1_z00_no_lines__lbry_holding_marc_rec_field_cnt smallint,
    in_z00_data_len character varying(6),
    pp_z00_data_len character varying(6),
    dq_z00_data_len character varying(6),
    t1_z00_data_len__lbry_holding_marc_rec_data_cntnt_len_cnt smallint,
    in_z00_data character varying(45000),
    pp_z00_data character varying(45000),
    dq_z00_data character varying(45000),
    t1_z00_data__lbry_holding_marc_rec_data_cntnt_txt character varying(45000),
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


ALTER TABLE public.dw_stg_2_lbry_holding_z00 OWNER TO usmai_dw;

--
-- Name: dw_stg_2_lbry_holding_z00_field; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.dw_stg_2_lbry_holding_z00_field (
    db_operation_cd character(1) NOT NULL,
    dw_stg_2_aleph_lbry_name character(5) NOT NULL,
    in_z00_doc_number character(9) NOT NULL,
    pp_z00_doc_number character(9),
    dq_z00_doc_number character(9),
    t1_z00_doc_number__lbry_holding_source_system_id character(9),
    in_dw_stg_1_marc_rec_field_seq_no smallint NOT NULL,
    in_z00_marc_rec_field_cd character(5),
    pp_z00_marc_rec_field_cd character(5),
    dq_z00_marc_rec_field_cd character(5),
    t1_z00_marc_rec_field_cd__lbry_holding_marc_rec_field_cd character(5),
    in_z00_marc_rec_field_txt character varying(2000),
    pp_z00_marc_rec_field_txt character varying(2000),
    dq_z00_marc_rec_field_txt character varying(2000),
    t1_z00_marc_rec_field_txt__lbry_holding_marc_rec_field_txt character varying(2000),
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


ALTER TABLE public.dw_stg_2_lbry_holding_z00_field OWNER TO usmai_dw;

--
-- Name: dw_stg_2_lbry_holding_z13; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.dw_stg_2_lbry_holding_z13 (
    db_operation_cd character(1) NOT NULL,
    dw_stg_2_aleph_lbry_name character(5) NOT NULL,
    in_z13_rec_key character(9) NOT NULL,
    in_z13_open_date character varying(8),
    pp_z13_open_date character varying(8),
    dq_z13_open_date character varying(8),
    t1_z13_open_date__lbry_holding_create_dt date,
    in_z13_update_date character varying(8),
    pp_z13_update_date character varying(8),
    dq_z13_update_date character varying(8),
    t1_z13_update_date__lbry_holding_update_dt date,
    in_z13_call_no character varying(100),
    pp_z13_call_no character varying(100),
    dq_z13_call_no character varying(100),
    t1_z13_call_no__lbry_holding_loc_call_no character varying(100),
    in_z13_year character varying(4),
    in_z13_author_code character(5),
    in_z13_author character varying(100),
    in_z13_title_code character(5),
    in_z13_title character varying(100),
    in_z13_call_no_key character varying(80),
    in_z13_call_no_code character(5),
    in_z13_imprint_code character(5),
    in_z13_imprint character varying(100),
    in_z13_isbn_issn_code character(5),
    in_z13_isbn_issn character varying(100),
    in_z13_upd_time_stamp character(15) DEFAULT '200001011200000'::bpchar,
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


ALTER TABLE public.dw_stg_2_lbry_holding_z13 OWNER TO usmai_dw;

--
-- Name: dw_stg_2_lbry_holding_z13u; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.dw_stg_2_lbry_holding_z13u (
    db_operation_cd character(1) NOT NULL,
    dw_stg_2_aleph_lbry_name character(5) NOT NULL,
    in_z13u_rec_key character(9) NOT NULL,
    in_z13u_user_defined_3 character varying(500),
    pp_z13u_user_defined_3 character varying(500),
    dq_z13u_user_defined_3 character varying(500),
    t1_z13u_user_defined_3__lbry_holding_disply_suppressed_flag character(1),
    in_z13u_user_defined_4 character varying(500),
    pp_z13u_user_defined_4 character varying(500),
    dq_in_z13u_user_defined_4 character varying(500),
    t1_in_z13u_user_defined_4__lbry_holding_loc_non_public_note character varying(500),
    in_z13u_user_defined_5 character varying(500),
    pp_z13u_user_defined_5 character varying(500),
    dq_z13u_user_defined_5 character varying(500),
    t1_z13u_user_defined_5__lbry_holding_loc_public_note character varying(500),
    in_z13u_user_defined_6 character varying(500),
    pp_z13u_user_defined_6 character varying(500),
    dq_z13u_user_defined_6 character varying(500),
    t1_z13u_user_defined_6__lbry_holding_action_note character varying(500),
    in_z13u_user_defined_7 character varying(500),
    pp_z13u_user_defined_7 character varying(500),
    dq_z13u_user_defined_7 character varying(500),
    t1_z13u_user_defined_7__lbry_holding_summary_holdings_txt character varying(500),
    in_z13u_user_defined_8 character varying(500),
    pp_z13u_user_defined_8 character varying(500),
    dq_z13u_user_defined_8 character varying(500),
    t1_z13u_user_defined_8__lbry_holding_supp_summary_holdings_txt character varying(500),
    in_z13u_user_defined_9 character varying(500),
    pp_z13u_user_defined_9 character varying(500),
    dq_z13u_user_defined_9 character varying(500),
    t1_z13u_user_defined_9__lbry_holding_index_summary_holdings_txt character varying(500),
    in_z13u_user_defined_10 character varying(500),
    pp_z13u_user_defined_10 character varying(500),
    dq_z13u_user_defined_10 character varying(500),
    t1_z13u_user_defined_10__lbry_hld_mnt_mbr_lbry_cd_actl_srce_txt character varying(500),
    t2_z13u_user_defined_10__lbry_holding_maint_mbr_lbry_cd character(2),
    t3_z13u_user_defined_10__lbry_holding_super_holding_flag character(1),
    in_z13u_user_defined_1_code character(5),
    in_z13u_user_defined_1 character varying(500),
    in_z13u_user_defined_2_code character(5),
    in_z13u_user_defined_2 character varying(500),
    in_z13u_user_defined_3_code character(5),
    in_z13u_user_defined_4_code character(5),
    in_z13u_user_defined_5_code character(5),
    in_z13u_user_defined_6_code character(5),
    in_z13u_user_defined_7_code character(5),
    in_z13u_user_defined_8_code character(5),
    in_z13u_user_defined_9_code character(5),
    in_z13u_user_defined_10_code character(5),
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


ALTER TABLE public.dw_stg_2_lbry_holding_z13u OWNER TO usmai_dw;

--
-- Name: dw_stg_2_lbry_item_event_z35; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.dw_stg_2_lbry_item_event_z35 (
    db_operation_cd character(1) NOT NULL,
    dw_stg_2_aleph_lbry_name character(5) NOT NULL,
    in_z35_rec_key character(9) NOT NULL,
    in_z35_item_sequence character varying(6),
    in_z35_event_type character(2),
    in_z35_time_stamp character(22) NOT NULL,
    in_z35_id character(12),
    in_z35_material character(5),
    in_z35_sub_library character(5),
    in_z35_status character(2),
    in_z35_event_date numeric(8,0),
    in_z35_event_hour numeric(4,0),
    in_z35_item_status character(2),
    in_z35_bor_status character(2),
    in_z35_bor_type character(2),
    in_z35_cataloger_name character(10),
    in_z35_type character(1),
    in_z35_ip_address character varying(20),
    in_z35_query character varying(500),
    in_z35_note character varying(100),
    in_z35_upd_time_stamp character(15),
    in_z35_ip_address_v6 character varying(50),
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


ALTER TABLE public.dw_stg_2_lbry_item_event_z35 OWNER TO usmai_dw;

--
-- Name: dw_stg_2_lbry_item_fact_z103_bib_full; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.dw_stg_2_lbry_item_fact_z103_bib_full (
    rec_type_cd character(1) NOT NULL,
    db_operation_cd character(1) NOT NULL,
    rec_trigger_key character(15) NOT NULL,
    in_source character(9),
    in_dest character(9),
    in_dest_lib character(5),
    in_dest_docnum character(9),
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


ALTER TABLE public.dw_stg_2_lbry_item_fact_z103_bib_full OWNER TO usmai_dw;

--
-- Name: dw_stg_2_lbry_item_fact_z30_full; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.dw_stg_2_lbry_item_fact_z30_full (
    rec_type_cd character(1) NOT NULL,
    db_operation_cd character(1) NOT NULL,
    rec_trigger_key character(15) NOT NULL,
    z30_sub_library character(5),
    z30_collection character(5),
    z30_material character(5),
    z30_item_status character(2),
    z30_item_process_status character(2),
    z30_open_date character varying(8),
    z30_order_number character varying(30),
    z30_no_loans character varying(3),
    em_create_dw_prcsng_cycle_id integer NOT NULL,
    em_create_dw_job_exectn_id integer NOT NULL,
    em_create_dw_job_name character varying(100) NOT NULL,
    em_create_dw_job_version_no character varying(20) NOT NULL,
    em_create_user_id character varying(20) NOT NULL,
    em_create_tmstmp timestamp without time zone NOT NULL
)
WITH (autovacuum_enabled='true');


ALTER TABLE public.dw_stg_2_lbry_item_fact_z30_full OWNER TO usmai_dw;

--
-- Name: dw_stg_2_lbry_item_z30; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.dw_stg_2_lbry_item_z30 (
    db_operation_cd character(1) NOT NULL,
    dw_stg_2_aleph_lbry_name character(5) NOT NULL,
    in_z30_rec_key character(15) NOT NULL,
    pp_z30_rec_key character(15),
    dq_z30_rec_key character(15),
    t1_z30_rec_key__lbry_item_source_system_id character(15),
    t2_z30_rec_key__lbry_item_adm_no character(9),
    t3_z30_rec_key__lbry_item_seq_no character(6),
    in_z30_barcode character(30),
    pp_z30_barcode character varying(30),
    dq_z30_barcode character varying(30),
    t1_z30_barcode__lbry_item_barcode_no character varying(30),
    in_z30_sub_library character(5),
    pp_z30_sub_library character(5),
    dq_z30_sub_library character(5),
    t1_z30_sub_library__lbry_entity character(5),
    in_z30_material character(5),
    pp_z30_material character varying(5),
    dq_z30_material character varying(5),
    t1_z30_material__lbry_item_matrl_form_cd character varying(5),
    in_z30_item_status character(2),
    pp_z30_item_status character(2),
    dq_z30_item_status character(2),
    t1_z30_item_status__lbry_item_status_cd character(2),
    in_z30_open_date character varying(8),
    pp_z30_open_date character varying(8),
    dq_z30_open_date character varying(8),
    t1_z30_open_date__lbry_item_create_dt date,
    in_z30_update_date character varying(8),
    pp_z30_update_date character varying(8),
    dq_z30_update_date character varying(8),
    t1_z30_update_date__lbry_item_update_dt date,
    in_z30_cataloger character(10),
    pp_z30_cataloger character varying(10),
    dq_z30_cataloger character varying(10),
    t1_z30_cataloger__lbry_item_update_lms_staff_acct_id character varying(10),
    in_z30_no_loans character varying(3),
    pp_z30_no_loans character varying(3),
    dq_z30_no_loans character varying(3),
    t1_z30_no_loans__lbry_item_total_to_date_loan_cnt smallint,
    in_z30_collection character(5),
    pp_z30_collection character varying(5),
    dq_z30_collection character varying(5),
    t1_z30_collection__lbry_item_loc_collection_cd character varying(5),
    in_z30_call_no_type character(1),
    pp_z30_call_no_type character(1),
    dq_z30_call_no_type character(1),
    t1_z30_call_no_type__lbry_item_loc_call_no_scheme_cd character(1),
    t2_z30_call_no_type__lbry_item_loc_call_no_scheme_desc character varying(50),
    in_z30_call_no character varying(80),
    pp_z30_call_no character varying(80),
    dq_z30_call_no character varying(80),
    t1_z30_call_no__lbry_item_loc_call_no character varying(80),
    in_z30_call_no_key character(80),
    pp_z30_call_no_key character varying(80),
    dq_z30_call_no_key character varying(80),
    t1_z30_call_no_key__lbry_item_loc_sort_nrmlzd_call_no character varying(80),
    in_z30_call_no_2_type character(1),
    pp_z30_call_no_2_type character(1),
    dq_z30_call_no_2_type character(1),
    t1_z30_call_no_2_type__lbry_item_loc_alt_call_no_scheme_cd character(1),
    t2_z30_call_no_2_type__lbry_item_loc_alt_call_no_scheme_desc character varying(50),
    in_z30_call_no_2 character varying(80),
    pp_z30_call_no_2 character varying(80),
    dq_z30_call_no_2 character varying(80),
    t1_z30_call_no_2__lbry_item_loc_alt_call_no character varying(80),
    in_z30_call_no_2_key character(80),
    pp_z30_call_no_2_key character varying(80),
    dq_z30_call_no_2_key character varying(80),
    t1_z30_call_no_2_key__lbry_item_loc_alt_sort_nrmlzd_call_no character varying(80),
    in_z30_description character varying(200),
    pp_z30_description character varying(200),
    dq_z30_description character varying(200),
    t1_z30_description__lbry_item_volume_issue_no character varying(200),
    in_z30_note_opac character varying(200),
    pp_z30_note_opac character varying(200),
    dq_z30_note_opac character varying(200),
    t1_z30_note_opac__lbry_item_opac_dislpay_txt character varying(200),
    in_z30_note_circulation character varying(200),
    pp_z30_note_circulation character varying(200),
    dq_z30_note_circulation character varying(200),
    t1_z30_note_circulation__lbry_item_circulation_display_note character varying(200),
    in_z30_note_internal character varying(200),
    pp_z30_note_internal character varying(200),
    dq_z30_note_internal character varying(200),
    t1_z30_note_internal__lbry_item_staff_only_display_note character varying(200),
    in_z30_order_number character varying(30),
    pp_z30_order_number character varying(30),
    dq_z30_order_number character varying(30),
    t1_z30_order_number__lbry_item_po_no character varying(30),
    in_z30_inventory_number character varying(20),
    in_z30_inventory_number_date character varying(8),
    pp_z30_inventory_number_date character varying(8),
    dq_z30_inventory_number_date character varying(8),
    t1_z30_inventory_number_date__lbry_item_accession_dt date,
    in_z30_price character(10),
    pp_z30_price character varying(10),
    dq_z30_price character varying(10),
    t1_z30_price__lbry_item_acquisition_price_txt character varying(10),
    in_z30_pages character varying(30),
    pp_z30_pages character varying(30),
    dq_z30_pages character varying(30),
    t1_z30_pages__lbry_item_page_range_txt character varying(30),
    in_z30_issue_date character varying(8),
    pp_z30_issue_date character varying(8),
    dq_z30_issue_date character varying(8),
    t1_z30_issue_date__lbry_item_pulication_dt date,
    in_z30_expected_arrival_date character varying(8),
    pp_z30_expected_arrival_date character varying(8),
    dq_z30_expected_arrival_date character varying(8),
    t1_z30_expected_arrival_date__lbry_item_expected_arrival_dt date,
    in_z30_arrival_date character(8),
    pp_z30_arrival_date character(8),
    dq_z30_arrival_date character(8),
    t1_z30_arrival_date__lbry_item_actual_arrival_dt date,
    in_z30_item_process_status character(2),
    pp_z30_item_process_status character(2),
    dq_z30_item_process_status character(2),
    t1_z30_item_process_status__lbry_item_prcs_status_cd character(2),
    in_z30_copy_id character(5),
    pp_z30_copy_id character(5),
    dq_z30_copy_id character(5),
    t1_z30_copy_id__lbry_item_copy_no character(5),
    in_z30_hol_doc_number_x character(9),
    pp_z30_hol_doc_number_x character(9),
    dq_z30_hol_doc_number_x character(9),
    t1_z30_hol_doc_number_x__lbry_holding_source_system_id character(9),
    in_z30_temp_location character(1),
    pp_z30_temp_location character(1),
    dq_z30_temp_location character(1),
    t1_z30_temp_location__lbry_item_loc_temp_designation_flag character(1),
    in_z30_enumeration_a character varying(20),
    pp_z30_enumeration_a character varying(20),
    dq_z30_enumeration_a character varying(20),
    t1_z30_enumeration_a__lbry_item_enumeration_lvl_1_txt character varying(20),
    in_z30_enumeration_b character varying(20),
    pp_z30_enumeration_b character varying(20),
    dq_z30_enumeration_b character varying(20),
    t1_z30_enumeration_b__lbry_item_enumeration_lvl_2_txt character varying(20),
    in_z30_enumeration_c character varying(20),
    pp_z30_enumeration_c character varying(20),
    dq_z30_enumeration_c character varying(20),
    t1_z30_enumeration_c__lbry_item_enumeration_lvl_3_txt character varying(20),
    in_z30_enumeration_d character varying(20),
    pp_z30_enumeration_d character varying(20),
    dq_z30_enumeration_d character varying(20),
    t1_z30_enumeration_d__lbry_item_enumeration_lvl_4_txt character varying(20),
    in_z30_enumeration_e character varying(20),
    pp_z30_enumeration_e character varying(20),
    dq_z30_enumeration_e character varying(20),
    t1_z30_enumeration_e__lbry_item_enumeration_lvl_5_txt character varying(20),
    in_z30_enumeration_f character varying(20),
    pp_z30_enumeration_f character varying(20),
    dq_z30_enumeration_f character varying(20),
    t1_z30_enumeration_f__lbry_item_enumeration_lvl_6_txt character varying(20),
    in_z30_enumeration_g character varying(20),
    pp_z30_enumeration_g character varying(20),
    dq_z30_enumeration_g character varying(20),
    t1_z30_enumeration_g__lbry_item_alt_enumeration_lvl_1_txt character varying(20),
    in_z30_enumeration_h character varying(20),
    pp_z30_enumeration_h character varying(20),
    dq_z30_enumeration_h character varying(20),
    t1_z30_enumeration_h__lbry_item_alt_enumeration_lvl_2_txt character varying(20),
    in_z30_chronological_i character varying(20),
    pp_z30_chronological_i character varying(20),
    dq_z30_chronological_i character varying(20),
    t1_z30_chronological_i__lbry_item_chronology_lvl_1_txt character varying(20),
    in_z30_chronological_j character varying(20),
    pp_z30_chronological_j character varying(20),
    dq_z30_chronological_j character varying(20),
    t1_z30_chronological_j__lbry_item_chronology_lvl_2_txt character varying(20),
    in_z30_chronological_k character varying(20),
    pp_z30_chronological_k character varying(20),
    dq_z30_chronological_k character varying(20),
    t1_z30_chronological_k__lbry_item_chronology_lvl_3_txt character varying(20),
    in_z30_chronological_l character varying(20),
    pp_z30_chronological_l character varying(20),
    dq_z30_chronological_l character varying(20),
    t1_z30_chronological_l__lbry_item_chronology_lvl_4_txt character varying(20),
    in_z30_chronological_m character varying(20),
    pp_z30_chronological_m character varying(20),
    dq_z30_chronological_m character varying(20),
    t1_z30_chronological_m__lbry_item_alt_chronology_txt character varying(20),
    in_z30_supp_index_o character varying(30),
    pp_z30_supp_index_o character varying(30),
    dq_z30_supp_index_o character varying(30),
    t1_z30_supp_index_o__lbry_item_supplemental_matrl_title character varying(30),
    in_z30_alpha character(1),
    in_z30_last_shelf_report_date character varying(8),
    in_z30_shelf_report_number character(20),
    in_z30_on_shelf_date character varying(8),
    in_z30_on_shelf_seq character varying(6),
    in_z30_rec_key_2 character(19),
    in_z30_rec_key_3 character(40),
    in_z30_date_last_return character varying(8),
    in_z30_hour_last_return character varying(4),
    in_z30_ip_last_return character varying(20),
    in_z30_item_statistic character(10),
    in_z30_85x_type character(1),
    in_z30_depository_id character(5),
    in_z30_linking_number character varying(9),
    in_z30_gap_indicator character(1),
    in_z30_maintenance_count character varying(3),
    in_z30_process_status_date character varying(8),
    in_z30_upd_time_stamp character(15),
    in_z30_ip_last_return_v6 character varying(50),
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


ALTER TABLE public.dw_stg_2_lbry_item_z30 OWNER TO usmai_dw;

--
-- Name: dw_stg_2_mpf_collection; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.dw_stg_2_mpf_collection (
    db_operation_cd character varying(1) NOT NULL,
    in_collection_cd character varying(5) NOT NULL,
    pp_collection_cd character varying(5),
    dq_collection_cd character varying(5),
    t1_collection_cd__lbry_item_loc_collection_cd character varying(5),
    in_collection_name character varying(100),
    pp_collection_name character varying(100),
    dq_collection_name character varying(100),
    t1_collection_name__lbry_item_loc_collection_name character varying(100),
    in_usmai_mbr_lbry_cd character varying(2) NOT NULL,
    pp_usmai_mbr_lbry_cd character varying(2),
    dq_usmai_mbr_lbry_cd character varying(2),
    t1_usmai_mbr_lbry_cd__lbry_item_loc_usmai_mbr_lbry_cd character(2),
    t2_usmai_mbr_lbry_cd__lbry_item_loc_usmai_mbr_lbry_name character varying(70),
    in_lbry_entity_cd character varying(3) NOT NULL,
    pp_lbry_entity_cd character varying(3),
    dq_lbry_entity_cd character varying(3),
    t1_lbry_entity_cd__lbry_item_loc_lbry_entity_cd character varying(3),
    t2_lbry_entity_cd__lbry_item_loc_lbry_entity_name character varying(30),
    db_operation_effective_date character varying(10),
    lbry_staff_lms_user_id character varying(10),
    rm_suspend_rec_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_suspend_rec_reason_cd character(3),
    rm_dq_check_excptn_cnt smallint NOT NULL,
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


ALTER TABLE public.dw_stg_2_mpf_collection OWNER TO usmai_dw;

--
-- Name: dw_stg_2_mpf_item_prcs_status; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.dw_stg_2_mpf_item_prcs_status (
    db_operation_cd character varying(1) NOT NULL,
    in_mbr_lbry_cd character(2) NOT NULL,
    in_item_prcs_status_cd character varying(2) NOT NULL,
    in_item_prcs_status_desc character varying(100),
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

--
-- Name: dw_stg_2_mpf_item_status; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.dw_stg_2_mpf_item_status (
    db_operation_cd character varying(1) NOT NULL,
    in_usmai_mbr_lbry_cd character(2) NOT NULL,
    pp_usmai_mbr_lbry_cd character(2),
    dq_usmai_mbr_lbry_cd character(2),
    t1_usmai_mbr_lbry_cd__lbry_item_usmai_mbr_lbry_cd character(2),
    in_item_status_cd character varying(2) NOT NULL,
    pp_item_status_cd character varying(2),
    dq_item_status_cd character(2),
    t1_item_status_cd__lbry_item_status_cd character(2),
    in_item_status_desc character varying(100),
    pp_item_status_desc character varying(100),
    dq_item_status_desc character varying(100),
    t1_item_status_desc__lbry_item_status_desc character varying(100),
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


ALTER TABLE public.dw_stg_2_mpf_item_status OWNER TO usmai_dw;

--
-- Name: dw_stg_2_mpf_lbry_entity; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.dw_stg_2_mpf_lbry_entity (
    db_operation_cd character varying(1) NOT NULL,
    in_usmai_mbr_lbry_cd character varying(2) NOT NULL,
    pp_usmai_mbr_lbry_cd character varying(2),
    dq_usmai_mbr_lbry_cd character varying(2),
    t1_usmai_mbr_lbry_cd__usmai_mbr_lbry_cd character(2),
    t2_usmai_mbr_lbry_cd__usmai_mbr_lbry_name character varying(70),
    in_lbry_entity_cd character varying(3) NOT NULL,
    pp_lbry_entity_cd character varying(3),
    dq_lbry_entity_cd character varying(3),
    t1_lbry_entity_cd__lbry_entity_cd character varying(3),
    in_lbry_entity_name character varying(70),
    pp_lbry_entity_name character varying(70),
    dq_lbry_entity_name character varying(70),
    t1_lbry_entity_name__lbry_entity_name character varying(70),
    db_operation_effective_date character varying(10),
    lbry_staff_lms_user_id character varying(10),
    rm_suspend_rec_cd character(1) DEFAULT 'N'::bpchar NOT NULL,
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


ALTER TABLE public.dw_stg_2_mpf_lbry_entity OWNER TO usmai_dw;

--
-- Name: dw_stg_2_mpf_matrl_form; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.dw_stg_2_mpf_matrl_form (
    db_operation_cd character varying(1) NOT NULL,
    matrl_form_cd character varying(2) NOT NULL,
    matrl_form_name character varying(30),
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


ALTER TABLE public.dw_stg_2_mpf_matrl_form OWNER TO usmai_dw;

--
-- Name: dw_stg_2_mpf_mbr_lbry; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.dw_stg_2_mpf_mbr_lbry (
    db_operation_cd character varying(1) NOT NULL,
    in_usmai_mbr_lbry_cd character varying(2) NOT NULL,
    pp_usmai_mbr_lbry_cd character varying(2),
    dq_usmai_mbr_lbry_cd character varying(2),
    t1_usmai_mbr_lbry_cd__usmai_mbr_lbry_cd character(2),
    in_usmai_mbr_lbry_name character varying(70),
    pp_in_usmai_mbr_lbry_name character varying(70),
    dq_in_usmai_mbr_lbry_name character varying(70),
    t1_usmai_mbr_lbry_name__usmai_mbr_lbry_name character varying(70),
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


ALTER TABLE public.dw_stg_2_mpf_mbr_lbry OWNER TO usmai_dw;

--
-- Name: dw_stg_3_dim_bib_rec; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.dw_stg_3_dim_bib_rec (
    db_operation_cd character(1) NOT NULL,
    bib_rec_dim_key bigint,
    bib_rec_source_system_id character(9) NOT NULL,
    bib_rec_aleph_lbry_cd character varying(5) NOT NULL,
    bib_rec_marc_rec_field_cnt smallint,
    bib_rec_marc_rec_data_cntnt_len_cnt smallint,
    bib_rec_marc_rec_data_cntnt_txt character varying(45000),
    bib_rec_publication_yr_no smallint,
    bib_rec_title character varying(100),
    bib_rec_author_name character varying(100),
    bib_rec_imprint_txt character varying(100),
    bib_rec_isbn_issn_source_cd character varying(5),
    bib_rec_isbn_txt character varying(100),
    bib_rec_all_associated_issns_txt character varying(100),
    bib_rec_oclc_no character varying(500),
    bib_rec_marc_rec_leader_field_txt character varying(500),
    bib_rec_type_cd character(1),
    bib_rec_bib_lvl_cd character(1),
    bib_rec_encoding_lvl_cd character(1),
    bib_rec_marc_rec_008_field_txt character varying(500),
    bib_rec_language_cd character(3),
    bib_rec_issn character varying(500),
    bib_rec_display_suppressed_flag character(1),
    bib_rec_acquisition_created_flag character(1),
    bib_rec_circulation_created_flag character(1),
    bib_rec_provisional_status_flag character(1),
    bib_rec_create_dt date,
    bib_rec_update_dt date,
    rm_bib_rec_marc_rec_field_cnt_chg_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_bib_rec_marc_rec_field_cnt_chg_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_bib_rec_marc_rec_data_cntnt_len_cnt_chg_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_bib_rec_marc_rec_data_cntnt_len_cnt_chg_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_bib_rec_marc_rec_data_cntnt_txt_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_bib_rec_marc_rec_data_cntnt_txt_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_bib_rec_publication_yr_no_chg_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_bib_rec_publication_yr_no_chg_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_bib_rec_title_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_bib_rec_title_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_bib_rec_author_name_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_bib_rec_author_name_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_bib_rec_imprint_txt_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_bib_rec_imprint_txt_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_bib_rec_isbn_issn_source_cd_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_bib_rec_isbn_issn_source_cd_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_bib_rec_isbn_txt_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_bib_rec_isbn_txt_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_bib_rec_all_associated_issns_txt_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_bib_rec_all_associated_issns_txt_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_bib_rec_oclc_no_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_bib_rec_oclc_no_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_bib_rec_marc_rec_leader_field_txt_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_bib_rec_marc_rec_leader_field_txt_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_bib_rec_type_cd_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_bib_rec_type_cd_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_bib_rec_bib_lvl_cd_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_bib_rec_bib_lvl_cd_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_bib_rec_encoding_lvl_cd_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_bib_rec_encoding_lvl_cd_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_bib_rec_marc_rec_008_field_txt_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_bib_rec_marc_rec_008_field_txt_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_bib_rec_language_cd_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_bib_rec_language_cd_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_bib_rec_issn_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_bib_rec_issn_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_bib_rec_display_suppressed_flag_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_bib_rec_display_suppressed_flag_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_bib_rec_acquisition_created_flag_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_bib_rec_acquisition_created_flag_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_bib_rec_circulation_created_flag_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_bib_rec_circulation_created_flag_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_bib_rec_provisional_status_flag_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_bib_rec_provisional_status_flag_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_bib_rec_create_dt_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_bib_rec_create_dt_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_bib_rec_update_dt_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_bib_rec_update_dt_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_type_1_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_type_2_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_suspend_rec_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_suspend_rec_reason_cd character(3),
    rm_rec_type_cd character(1),
    rm_rec_type_desc character varying(30),
    rm_rec_version_no smallint,
    rm_rec_effective_from_dt date,
    rm_rec_effective_to_dt date,
    rm_current_rec_flag character(1),
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


ALTER TABLE public.dw_stg_3_dim_bib_rec OWNER TO usmai_dw;

--
-- Name: dw_stg_3_dim_lbry_entity; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.dw_stg_3_dim_lbry_entity (
    db_operation_cd character(20) NOT NULL,
    lbry_entity_dim_key smallint,
    usmai_mbr_lbry_cd character(2) NOT NULL,
    usmai_mbr_lbry_name character varying(70),
    usmai_mbr_lbry_mbrshp_type_cd character varying(10),
    lbry_entity_cd character varying(5) NOT NULL,
    lbry_entity_name character varying(70),
    lbry_entity_name_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_entity_name_chng_dtcd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_type_1_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_type_2_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_suspend_rec_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_suspend_rec_reason_cd character(3),
    rm_rec_type_cd character(1),
    rm_rec_type_desc character varying(30),
    rm_rec_version_no smallint,
    rm_rec_effective_from_dt date,
    rm_rec_effective_to_dt date,
    rm_current_rec_flag character(1),
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
    em_update_reason_txt character varying(100),
    em_update_user_id character varying(20),
    em_update_tmstmp timestamp without time zone
)
WITH (autovacuum_enabled='true');


ALTER TABLE public.dw_stg_3_dim_lbry_entity OWNER TO usmai_dw;

--
-- Name: dw_stg_3_dim_lbry_holding; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.dw_stg_3_dim_lbry_holding (
    db_operation_cd character(1) NOT NULL,
    lbry_holding_dim_key bigint,
    lbry_holding_source_system_id character(9) NOT NULL,
    lbry_holding_aleph_lbry_cd character(5) NOT NULL,
    lbry_holding_marc_rec_field_cnt smallint,
    lbry_holding_marc_rec_data_cntnt_len_cnt smallint,
    lbry_holding_marc_rec_data_cntnt_txt character varying(45000),
    lbry_holding_action_note character varying(500),
    lbry_holding_disply_suppressed_flag character(1),
    lbry_holding_summary_holdings_txt character varying(500),
    lbry_holding_supp_summary_holdings_txt character varying(500),
    lbry_holding_index_summary_holdings_txt character varying(500),
    lbry_holding_loc_call_no_scheme_cd character(1),
    lbry_holding_loc_call_no character varying(100),
    lbry_holding_loc_public_note character varying(500),
    lbry_holding_loc_non_public_note character varying(500),
    lbry_holding_create_dt date,
    lbry_holding_update_dt date,
    lbry_holding_maint_usmai_mbr_lbry_cd character(2),
    lbry_holding_maint_usmai_mbr_lbry_cd_actual_source_txt character varying(500),
    lbry_holding_super_holding_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_holding_marc_rec_field_cnt_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_holding_marc_rec_field_cnt_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_holding_marc_rec_data_cntnt_len_cnt_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_holding_marc_rec_data_cntnt_len_cnt_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_holding_marc_rec_data_cntnt_txt_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_holding_marc_rec_data_cntnt_txt_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_holding_action_note_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_holding_action_note_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_holding_disply_suppressed_flag_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_holding_disply_suppressed_flag_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_holding_summary_holdings_txt_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_holding_summary_holdings_txt_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_holding_supp_summary_holdings_txt_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_holding_supp_summary_holdings_txt_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_holding_index_summary_holdings_txt_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_holding_index_summary_holdings_txt_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_holding_loc_call_no_scheme_cd_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_holding_loc_call_no_scheme_cd_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_holding_loc_call_no_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_holding_loc_call_no_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_holding_loc_public_note_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_holding_loc_public_note_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_holding_create_dt_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_holding_create_dt_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_holding_update_dt_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_holding_update_dt_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_holding_maint_usmai_mbr_lbry_cd_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_holding_maint_usmai_mbr_lbry_cd_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_hold_maint_usmai_mbr_lbry_cd_actl_srce_txt_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_hold_maint_usmai_mbr_lbry_cd_actl_srce_txt_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_holding_super_holding_flag_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_holding_super_holding_flag_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_type_1_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_type_2_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_suspend_rec_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_suspend_rec_reason_cd character(3),
    rm_rec_type_cd character(1),
    rm_rec_type_desc character varying(30),
    rm_rec_version_no smallint,
    rm_rec_effective_from_dt date,
    rm_rec_effective_to_dt date,
    rm_current_rec_flag character(1),
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
    em_update_reason_txt character varying(100),
    em_update_user_id character varying(20),
    em_update_tmstmp timestamp without time zone
)
WITH (autovacuum_enabled='true');


ALTER TABLE public.dw_stg_3_dim_lbry_holding OWNER TO usmai_dw;

--
-- Name: dw_stg_3_dim_lbry_item; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.dw_stg_3_dim_lbry_item (
    db_operation_cd character(1) NOT NULL,
    lbry_item_dim_key bigint,
    lbry_item_source_system_id character(15) NOT NULL,
    lbry_item_adm_no character(9) NOT NULL,
    lbry_item_seq_no character(6) NOT NULL,
    lbry_item_aleph_lbry_name character(5) NOT NULL,
    lbry_item_update_lms_staff_acct_id character varying(10),
    lbry_item_create_dt date,
    lbry_item_update_dt date,
    lbry_item_volume_issue_no character varying(200),
    lbry_item_accession_dt date,
    lbry_item_page_range_txt character varying(30),
    lbry_item_copy_no character(5),
    lbry_item_pulication_dt date,
    lbry_item_supplemental_matrl_title character varying(30),
    lbry_item_expected_arrival_dt date,
    lbry_item_actual_arrival_dt date,
    lbry_item_acquisition_price_txt character varying(10),
    lbry_item_barcode_no character varying(30),
    lbry_item_loc_call_no_scheme_cd character(1),
    lbry_item_loc_call_no_scheme_desc character varying(50),
    lbry_item_loc_call_no character varying(80),
    lbry_item_loc_sort_nrmlzd_call_no character varying(80),
    lbry_item_loc_temp_designation_flag character(1),
    lbry_item_loc_alt_call_no_scheme_cd character(1),
    lbry_item_loc_alt_call_no_scheme_desc character varying(50),
    lbry_item_loc_alt_call_no character varying(80),
    lbry_item_loc_alt_sort_nrmlzd_call_no character varying(80),
    lbry_item_enumeration_lvl_1_txt character varying(20),
    lbry_item_enumeration_lvl_2_txt character varying(20),
    lbry_item_enumeration_lvl_3_txt character varying(20),
    lbry_item_enumeration_lvl_4_txt character varying(20),
    lbry_item_enumeration_lvl_5_txt character varying(20),
    lbry_item_enumeration_lvl_6_txt character varying(20),
    lbry_item_alt_enumeration_lvl_1_txt character varying(20),
    lbry_item_alt_enumeration_lvl_2_txt character varying(20),
    lbry_item_chronology_lvl_1_txt character varying(20),
    lbry_item_chronology_lvl_2_txt character varying(20),
    lbry_item_chronology_lvl_3_txt character varying(20),
    lbry_item_chronology_lvl_4_txt character varying(20),
    lbry_item_alt_chronology_txt character varying(20),
    lbry_item_circulation_display_note character varying(200),
    lbry_item_opac_dislpay_txt character varying(200),
    lbry_item_staff_only_display_note character varying(200),
    lbry_item_most_recent_loan_event_dt date,
    lbry_item_most_recent_loan_event_time smallint,
    lbry_item_most_recent_loan_event_type_cd character(2),
    lbry_item_most_recent_loan_event_ip_addr character varying(20),
    lbry_item_most_recent_return_event_dt date,
    lbry_item_most_recent_return_event_time smallint,
    lbry_item_most_recent_return_event_type_cd character(2),
    lbry_item_most_recent_return_event_ip_addr character varying(20),
    lbry_item_most_recent_renew_event_dt date,
    lbry_item_most_recent_renew_event_time smallint,
    lbry_item_most_recent_renew_event_type_cd character(2),
    lbry_item_most_recent_renew_event_ip_addr character varying(20),
    lbry_item_update_lms_staff_acct_id_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_update_lms_staff_acct_id_chng_dtcd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_create_dt_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_create_dt_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_update_dt_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_update_dt_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_volume_issue_no_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_volume_issue_no_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_accession_dt_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_accession_dt_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_page_range_txt_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_page_range_txt_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_copy_no_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_copy_no_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_pulication_dt_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_pulication_dt_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_supplemental_matrl_title_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_supplemental_matrl_title_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_expected_arrival_dt_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_expected_arrival_dt_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_actual_arrival_dt_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_actual_arrival_dt_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_acquisition_price_txt_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_acquisition_price_txt_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_barcode_no_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_barcode_no_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_loc_call_no_scheme_cd_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_loc_call_no_scheme_cd_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_loc_call_no_scheme_desc_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_loc_call_no_scheme_desc_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_loc_call_no_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_loc_call_no_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_loc_sort_nrmlzd_call_no_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_loc_sort_nrmlzd_call_no_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_loc_temp_designation_flag_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_loc_temp_designation_flag_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_loc_alt_call_no_scheme_cd_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_loc_alt_call_no_scheme_cd_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_loc_alt_call_no_scheme_desc_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_loc_alt_call_no_scheme_desc_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_loc_alt_call_no_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_loc_alt_call_no_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_loc_alt_sort_nrmlzd_call_no_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_loc_alt_sort_nrmlzd_call_no_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_enumeration_lvl_1_txt_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_enumeration_lvl_1_txt_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_enumeration_lvl_2_txt_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_enumeration_lvl_2_txt_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_enumeration_lvl_3_txt_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_enumeration_lvl_3_txt_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_enumeration_lvl_4_txt_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_enumeration_lvl_4_txt_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_enumeration_lvl_5_txt_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_enumeration_lvl_5_txt_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_enumeration_lvl_6_txt_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_enumeration_lvl_6_txt_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_alt_enumeration_lvl_1_txt_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_alt_enumeration_lvl_1_txt_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_alt_enumeration_lvl_2_txt_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_alt_enumeration_lvl_2_txt_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_chronology_lvl_1_txt_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_chronology_lvl_1_txt_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_chronology_lvl_2_txt_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_chronology_lvl_2_txt_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_chronology_lvl_3_txt_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_chronology_lvl_3_txt_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_chronology_lvl_4_txt_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_chronology_lvl_4_txt_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_alt_chronology_txt_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_alt_chronology_txt_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_circulation_display_note_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_circulation_display_note_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_opac_dislpay_txt_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_opac_dislpay_txt_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_staff_only_display_note_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_staff_only_display_note_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_most_recent_loan_event_dt_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_most_recent_loan_event_dt_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_most_recent_loan_event_time_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_most_recent_loan_event_time_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_most_recent_loan_event_type_cd_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_most_recent_loan_event_type_cd_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_most_recent_loan_event_ip_addr_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_most_recent_loan_event_ip_addr_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_most_recent_return_event_dt_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_most_recent_return_event_dt_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_most_recent_return_event_time_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_most_recent_return_event_time_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_most_recent_return_event_type_cd_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_most_recent_return_event_type_cd_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_most_recent_return_event_ip_addr_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_most_recent_return_event_ip_addr_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_most_recent_renew_event_dt_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_most_recent_renew_event_dt_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_most_recent_renew_event_time_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_most_recent_renew_event_time_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_most_recent_renew_event_type_cd_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_most_recent_renew_event_type_cd_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_most_recent_renew_event_ip_addr_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_most_recent_renew_event_ip_addr_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_type_1_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_type_2_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_suspend_rec_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_suspend_rec_reason_cd character(3),
    rm_rec_type_cd character(1),
    rm_rec_type_desc character varying(30),
    rm_rec_version_no smallint,
    rm_rec_effective_from_dt date,
    rm_rec_effective_to_dt date,
    rm_current_rec_flag character(1),
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
    em_update_reason_txt character varying(100),
    em_update_user_id character varying(20),
    em_update_tmstmp timestamp without time zone
)
WITH (autovacuum_enabled='true');


ALTER TABLE public.dw_stg_3_dim_lbry_item OWNER TO usmai_dw;

--
-- Name: dw_stg_3_dim_lbry_item_loc; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.dw_stg_3_dim_lbry_item_loc (
    db_operation_cd character(1) NOT NULL,
    lbry_item_loc_dim_key integer,
    lbry_item_loc_usmai_mbr_lbry_cd character(2) NOT NULL,
    lbry_item_loc_usmai_mbr_lbry_name character varying(70) NOT NULL,
    lbry_item_loc_usmai_mbr_lbry_mbrshp_type_cd character varying(10) NOT NULL,
    lbry_item_loc_lbry_entity_cd character(5) NOT NULL,
    lbry_item_loc_lbry_entity_name character varying(30) NOT NULL,
    lbry_item_loc_collection_cd character varying(5) NOT NULL,
    lbry_item_loc_collection_name character varying(80) NOT NULL,
    lbry_item_loc_collection_name_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_loc_collection_name_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_type_1_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_type_2_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_suspend_rec_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_suspend_rec_reason_cd character(3),
    rm_rec_type_cd character(1),
    rm_rec_type_desc character varying(30),
    rm_rec_version_no smallint,
    rm_rec_effective_from_dt date,
    rm_rec_effective_to_dt date,
    rm_current_rec_flag character(1),
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
    em_update_reason_txt character varying(100),
    em_update_user_id character varying(20),
    em_update_tmstmp timestamp without time zone
)
WITH (autovacuum_enabled='true');


ALTER TABLE public.dw_stg_3_dim_lbry_item_loc OWNER TO usmai_dw;

--
-- Name: dw_stg_3_dim_lbry_item_matrl_form; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.dw_stg_3_dim_lbry_item_matrl_form (
    db_operation_cd character(1) NOT NULL,
    lbry_item_matrl_form_dim_key smallint,
    lbry_item_matrl_form_cd character varying(5) NOT NULL,
    lbry_item_matrl_form_name character varying(50),
    lbry_item_matrl_form_name_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_matrl_form_name_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_type_1_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_type_2_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_suspend_rec_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_suspend_rec_reason_cd character(3),
    rm_rec_type_cd character(1),
    rm_rec_type_desc character varying(30),
    rm_rec_version_no smallint,
    rm_rec_effective_from_dt date,
    rm_rec_effective_to_dt date,
    rm_current_rec_flag character(1),
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
    em_update_reason_txt character varying(100),
    em_update_user_id character varying(20),
    em_update_tmstmp timestamp without time zone
)
WITH (autovacuum_enabled='true');


ALTER TABLE public.dw_stg_3_dim_lbry_item_matrl_form OWNER TO usmai_dw;

--
-- Name: dw_stg_3_dim_lbry_item_prcs_status; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.dw_stg_3_dim_lbry_item_prcs_status (
    db_operation_cd character(1) NOT NULL,
    lbry_item_prcs_status_dim_key smallint,
    lbry_item_usmai_mbr_lbry_cd character(2) NOT NULL,
    lbry_item_prcs_status_cd character(2) NOT NULL,
    lbry_item_prcs_status_public_desc character varying(50),
    lbry_item_prcs_status_public_desc_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_prcs_status_public_desc_chng_dtctd_flag character varying(1) DEFAULT 'N'::character varying NOT NULL,
    lbry_item_prcs_status_internal_desc character varying(50),
    lbry_item_prcs_status_internal_desc_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_prcs_status_internal_desc_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_type_1_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_type_2_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_suspend_rec_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_suspend_rec_reason_cd character(3),
    rm_rec_type_cd character(1),
    rm_rec_type_desc character varying(30),
    rm_rec_version_no smallint,
    rm_rec_effective_from_dt date,
    rm_rec_effective_to_dt date,
    rm_current_rec_flag character(1),
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
    em_update_reason_txt character varying(100),
    em_update_user_id character varying(20),
    em_update_tmstmp timestamp without time zone
)
WITH (autovacuum_enabled='true');


ALTER TABLE public.dw_stg_3_dim_lbry_item_prcs_status OWNER TO usmai_dw;

--
-- Name: dw_stg_3_dim_lbry_item_status; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.dw_stg_3_dim_lbry_item_status (
    db_operation_cd character(1) NOT NULL,
    lbry_item_status_dim_key smallint,
    lbry_item_usmai_mbr_lbry_cd character(2) NOT NULL,
    lbry_item_status_cd character(2) NOT NULL,
    lbry_item_status_desc character varying(50),
    lbry_item_status_desc_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    lbry_item_status_desc_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_type_1_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_type_2_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_suspend_rec_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_suspend_rec_reason_cd character(3),
    rm_rec_type_cd character(1),
    rm_rec_type_desc character varying(30),
    rm_rec_version_no smallint,
    rm_rec_effective_from_dt date,
    rm_rec_effective_to_dt date,
    rm_current_rec_flag character(1),
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
    em_update_reason_txt character varying(100),
    em_update_user_id character varying(20),
    em_update_tmstmp timestamp without time zone
)
WITH (autovacuum_enabled='true');


ALTER TABLE public.dw_stg_3_dim_lbry_item_status OWNER TO usmai_dw;

--
-- Name: dw_stg_3_dim_usmai_mbr_lbry; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.dw_stg_3_dim_usmai_mbr_lbry (
    db_operation_cd character(1) NOT NULL,
    usmai_mbr_lbry_dim_key smallint,
    usmai_mbr_lbry_cd character(2) NOT NULL,
    usmai_mbr_lbry_name character varying(70),
    usmai_mbr_lbry_name_chng_chk_flag character(1),
    usmai_mbr_lbry_name_chng_dtctd_flag character(1),
    usmai_mbr_lbry_mbrshp_type_cd character varying(10),
    usmai_mbr_lbry_mbrshp_type_cd_chng_chk_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    usmai_mbr_lbry_mbrshp_type_cd_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_type_1_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_type_2_chng_dtctd_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_suspend_rec_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    rm_suspend_rec_reason_cd character(3),
    rm_rec_type_cd character(1),
    rm_rec_type_desc character varying(30),
    rm_rec_version_no smallint,
    rm_rec_effective_from_dt date,
    rm_rec_effective_to_dt date,
    rm_current_rec_flag character(1),
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
    em_update_reason_txt character varying(100),
    em_update_user_id character varying(20),
    em_update_tmstmp timestamp without time zone
)
WITH (autovacuum_enabled='true');


ALTER TABLE public.dw_stg_3_dim_usmai_mbr_lbry OWNER TO usmai_dw;

--
-- Name: dw_stg_3_fact_lbry_item; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.dw_stg_3_fact_lbry_item (
    lbry_item_fact_key bigint NOT NULL,
    bib_rec_dim_key bigint,
    bib_rec_source_system_id character(9),
    lbry_holding_dim_key bigint,
    lbry_holding_source_system_id character(9),
    lbry_item_dim_key bigint,
    lbry_item_source_system_id character(15),
    lbry_item_loc_dim_key integer,
    lbry_item_loc_lbry_entity_cd character(5),
    lbry_item_loc_collection_cd character(5),
    lbry_item_holding_loc_dim_key integer,
    lbry_item_holding_loc_lbry_entity_cd character(5),
    lbry_item_holding_loc_collection_cd character(5),
    lbry_item_matrl_form_dim_key smallint,
    lbry_item_matrl_form_cd character varying(5),
    lbry_item_status_dim_key smallint,
    lbry_item_status_mbr_lbry_cd character(2),
    lbry_item_status_cd character(2),
    lbry_item_prcs_status_dim_key smallint,
    lbry_item_prcs_status_mbr_lbry_cd bigint,
    lbry_item_prcs_status_cd character(2),
    lbry_item_as_of_clndr_dt_dim_key integer,
    lbry_item_as_of_clndr_dt date,
    lbry_item_create_clndr_dt_dim_key integer,
    lbry_item_create_clndr_dt date,
    lbry_item_po_no character varying(30),
    lbry_item_total_to_date_loan_cnt smallint,
    em_create_dw_prcsng_cycle_id integer,
    em_create_dw_job_exectn_id integer,
    em_create_dw_job_name character varying(100),
    em_create_dw_job_version_no character varying(20),
    em_create_user_id character varying(20),
    em_create_tmstmp timestamp without time zone,
    em_update_dw_prcsng_cycle_id integer,
    em_update_dw_job_exectn_id integer,
    em_update_dw_job_name character varying(100),
    em_update_dw_job_version_no character varying(20),
    em_update_user_id character varying(20),
    em_update_tmstmp timestamp without time zone,
    em_update_reason_txt character varying(100)
)
WITH (autovacuum_enabled='true');


ALTER TABLE public.dw_stg_3_fact_lbry_item OWNER TO usmai_dw;

--
-- Name: fact_ezp_sessns_snap; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.fact_ezp_sessns_snap (
    ezp_sessns_snap_clndr_dt_dim_key bigint NOT NULL,
    ezp_sessns_snap_mbr_lbry_dim_key bigint NOT NULL,
    ezp_sessns_snap_time_of_day_dim_key bigint NOT NULL,
    ezp_sessns_snap_tmstmp timestamp without time zone NOT NULL,
    ezp_sessns_snap_actv_sessns_cnt integer NOT NULL,
    ezp_sessns_snap_fact_key bigint NOT NULL,
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
    em_update_reason_txt character varying(100),
    em_update_user_id character varying(20),
    em_update_tmstmp timestamp without time zone
)
WITH (autovacuum_enabled='true');


ALTER TABLE public.fact_ezp_sessns_snap OWNER TO usmai_dw;

--
-- Name: fact_lbry_item; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.fact_lbry_item (
    lbry_item_fact_key bigint NOT NULL,
    bib_rec_dim_key bigint NOT NULL,
    lbry_holding_dim_key bigint NOT NULL,
    lbry_item_dim_key bigint NOT NULL,
    lbry_item_loc_dim_key integer NOT NULL,
    lbry_item_holding_loc_dim_key integer NOT NULL,
    lbry_item_matrl_form_dim_key smallint NOT NULL,
    lbry_item_status_dim_key smallint NOT NULL,
    lbry_item_prcs_status_dim_key smallint NOT NULL,
    lbry_item_as_of_clndr_dt_dim_key integer NOT NULL,
    lbry_item_create_clndr_dt_dim_key integer NOT NULL,
    lbry_item_po_no character varying(30),
    lbry_item_exists_flag smallint NOT NULL,
    lbry_item_total_to_date_loan_cnt smallint NOT NULL,
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
    em_update_reason_txt character varying(100),
    em_update_user_id character varying(20),
    em_update_tmstmp timestamp without time zone
)
WITH (autovacuum_enabled='true');


ALTER TABLE public.fact_lbry_item OWNER TO usmai_dw;

--
-- Name: out_bib_rec_marc_rec_field; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.out_bib_rec_marc_rec_field (
    bib_rec_dim_key bigint NOT NULL,
    bib_rec_marc_rec_field_out_seq_no smallint NOT NULL,
    bib_rec_source_system_id character(9) NOT NULL,
    bib_rec_marc_rec_field_cd character varying(5) NOT NULL,
    bib_rec_marc_rec_field_txt character varying(2000) NOT NULL,
    rm_rec_type_cd character(1) NOT NULL,
    rm_rec_type_desc character varying(30) NOT NULL,
    rm_rec_version_no smallint NOT NULL,
    rm_rec_effective_from_dt date NOT NULL,
    rm_rec_effective_to_dt date NOT NULL,
    rm_current_rec_flag character(1) NOT NULL,
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
    em_update_reason_txt character varying(100),
    em_update_user_id character varying(20),
    em_update_tmstmp timestamp without time zone
)
WITH (autovacuum_enabled='true');


ALTER TABLE public.out_bib_rec_marc_rec_field OWNER TO usmai_dw;

--
-- Name: out_lbry_holding_marc_rec_field; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.out_lbry_holding_marc_rec_field (
    lbry_holding_dim_key bigint NOT NULL,
    lbry_holding_marc_rec_field_out_seq_no smallint NOT NULL,
    lbry_holding_source_system_id character(9) NOT NULL,
    lbry_holding_marc_rec_field_cd character varying(5) NOT NULL,
    lbry_holding_marc_rec_field_txt character varying(2000) NOT NULL,
    rm_rec_type_cd character(1) NOT NULL,
    rm_rec_type_desc character varying(30) NOT NULL,
    rm_rec_version_no smallint NOT NULL,
    rm_rec_effective_from_dt date NOT NULL,
    rm_rec_effective_to_dt date NOT NULL,
    rm_current_rec_flag character(1) NOT NULL,
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
    em_update_reason_txt character varying(100),
    em_update_user_id character varying(20),
    em_update_tmstmp timestamp without time zone
)
WITH (autovacuum_enabled='true');


ALTER TABLE public.out_lbry_holding_marc_rec_field OWNER TO usmai_dw;

--
-- Name: dw_prcsng_cycle_job_exectn dw_prcsng_cycle_episode_job_exectn_key; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.dw_prcsng_cycle_job_exectn
    ADD CONSTRAINT dw_prcsng_cycle_episode_job_exectn_key PRIMARY KEY (dw_prcsng_cycle_job_exectn_id);


--
-- Name: dw_prcsng_cycle dw_prcsng_cycle_episode_key; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.dw_prcsng_cycle
    ADD CONSTRAINT dw_prcsng_cycle_episode_key PRIMARY KEY (dw_prcsng_cycle_id);


--
-- Name: dw_prcsng_cycle_job dw_prcsng_cycle_job_key; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.dw_prcsng_cycle_job
    ADD CONSTRAINT dw_prcsng_cycle_job_key PRIMARY KEY (dw_prcsng_cycle_job_name, dw_prcsng_cycle_job_version_no);


--
-- Name: dw_stg_1_mai39_z00_field dw_stg_1_mai39_z00_field_pkey; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.dw_stg_1_mai39_z00_field
    ADD CONSTRAINT dw_stg_1_mai39_z00_field_pkey PRIMARY KEY (db_operation_cd, rec_trigger_key, dw_stg_1_marc_rec_field_seq_no, em_create_dw_prcsng_cycle_id);


--
-- Name: dw_stg_1_mai60_z00_field dw_stg_1_mai60_z00_field_pkey; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.dw_stg_1_mai60_z00_field
    ADD CONSTRAINT dw_stg_1_mai60_z00_field_pkey PRIMARY KEY (db_operation_cd, rec_trigger_key, dw_stg_1_marc_rec_field_seq_no, em_create_dw_prcsng_cycle_id);


--
-- Name: dim_bib_rec indx_dim_bib_rec_pk; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.dim_bib_rec
    ADD CONSTRAINT indx_dim_bib_rec_pk PRIMARY KEY (bib_rec_dim_key);


--
-- Name: dim_date indx_dim_date_pk; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.dim_date
    ADD CONSTRAINT indx_dim_date_pk PRIMARY KEY (clndr_dt_dim_key);


--
-- Name: dim_lbry_holding indx_dim_lbry_holding_pk; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.dim_lbry_holding
    ADD CONSTRAINT indx_dim_lbry_holding_pk PRIMARY KEY (lbry_holding_dim_key);


--
-- Name: dim_lbry_item_loc indx_dim_lbry_item_loc_pk; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.dim_lbry_item_loc
    ADD CONSTRAINT indx_dim_lbry_item_loc_pk PRIMARY KEY (lbry_item_loc_dim_key);


--
-- Name: dim_lbry_item_matrl_form indx_dim_lbry_item_matrl_form_pk; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.dim_lbry_item_matrl_form
    ADD CONSTRAINT indx_dim_lbry_item_matrl_form_pk PRIMARY KEY (lbry_item_matrl_form_dim_key);


--
-- Name: dim_lbry_item indx_dim_lbry_item_pk; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.dim_lbry_item
    ADD CONSTRAINT indx_dim_lbry_item_pk PRIMARY KEY (lbry_item_dim_key);


--
-- Name: dim_lbry_item_prcs_status indx_dim_lbry_item_prcs_status_pk; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.dim_lbry_item_prcs_status
    ADD CONSTRAINT indx_dim_lbry_item_prcs_status_pk PRIMARY KEY (lbry_item_prcs_status_dim_key);


--
-- Name: dim_lbry_item_status indx_dim_lbry_item_status_pk; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.dim_lbry_item_status
    ADD CONSTRAINT indx_dim_lbry_item_status_pk PRIMARY KEY (lbry_item_status_dim_key);


--
-- Name: dw_stg_3_dim_bib_rec indx_dw_stg_3_dim_bib_rec_pk; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.dw_stg_3_dim_bib_rec
    ADD CONSTRAINT indx_dw_stg_3_dim_bib_rec_pk PRIMARY KEY (db_operation_cd, bib_rec_source_system_id, bib_rec_aleph_lbry_cd, em_create_dw_prcsng_cycle_id);


--
-- Name: dw_stg_3_dim_lbry_entity indx_dw_stg_3_dim_lbry_entity_pk; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.dw_stg_3_dim_lbry_entity
    ADD CONSTRAINT indx_dw_stg_3_dim_lbry_entity_pk PRIMARY KEY (db_operation_cd, lbry_entity_cd, em_create_dw_prcsng_cycle_id);


--
-- Name: dw_stg_3_dim_lbry_holding indx_dw_stg_3_dim_lbry_holding_pk; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.dw_stg_3_dim_lbry_holding
    ADD CONSTRAINT indx_dw_stg_3_dim_lbry_holding_pk PRIMARY KEY (db_operation_cd, lbry_holding_source_system_id, lbry_holding_aleph_lbry_cd, em_create_dw_prcsng_cycle_id);


--
-- Name: dw_stg_3_dim_lbry_item_loc indx_dw_stg_3_dim_lbry_item_loc_pk; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.dw_stg_3_dim_lbry_item_loc
    ADD CONSTRAINT indx_dw_stg_3_dim_lbry_item_loc_pk PRIMARY KEY (db_operation_cd, lbry_item_loc_usmai_mbr_lbry_cd, em_create_dw_prcsng_cycle_id);


--
-- Name: dw_stg_3_dim_lbry_item_matrl_form indx_dw_stg_3_dim_lbry_item_matrl_form_pk; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.dw_stg_3_dim_lbry_item_matrl_form
    ADD CONSTRAINT indx_dw_stg_3_dim_lbry_item_matrl_form_pk PRIMARY KEY (db_operation_cd, lbry_item_matrl_form_cd, em_create_dw_prcsng_cycle_id);


--
-- Name: dw_stg_3_dim_lbry_item indx_dw_stg_3_dim_lbry_item_pk; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.dw_stg_3_dim_lbry_item
    ADD CONSTRAINT indx_dw_stg_3_dim_lbry_item_pk PRIMARY KEY (db_operation_cd, lbry_item_source_system_id, em_create_dw_prcsng_cycle_id);


--
-- Name: dw_stg_3_dim_lbry_item_prcs_status indx_dw_stg_3_dim_lbry_item_prcs_status_pk; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.dw_stg_3_dim_lbry_item_prcs_status
    ADD CONSTRAINT indx_dw_stg_3_dim_lbry_item_prcs_status_pk PRIMARY KEY (db_operation_cd, lbry_item_usmai_mbr_lbry_cd, lbry_item_prcs_status_cd, em_create_dw_prcsng_cycle_id);


--
-- Name: dw_stg_3_dim_lbry_item_status indx_dw_stg_3_dim_lbry_item_status_pk; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.dw_stg_3_dim_lbry_item_status
    ADD CONSTRAINT indx_dw_stg_3_dim_lbry_item_status_pk PRIMARY KEY (db_operation_cd, lbry_item_usmai_mbr_lbry_cd, lbry_item_status_cd, em_create_dw_prcsng_cycle_id);


--
-- Name: dw_stg_3_dim_usmai_mbr_lbry indx_dw_stg_3_dim_usmai_mbr_lbry_pk; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.dw_stg_3_dim_usmai_mbr_lbry
    ADD CONSTRAINT indx_dw_stg_3_dim_usmai_mbr_lbry_pk PRIMARY KEY (db_operation_cd, usmai_mbr_lbry_cd, em_create_dw_prcsng_cycle_id);


--
-- Name: fact_ezp_sessns_snap indx_fact_ezp_sessns_snap_pk; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.fact_ezp_sessns_snap
    ADD CONSTRAINT indx_fact_ezp_sessns_snap_pk PRIMARY KEY (ezp_sessns_snap_fact_key);


--
-- Name: fact_lbry_item indx_fact_lbry_item_pk; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.fact_lbry_item
    ADD CONSTRAINT indx_fact_lbry_item_pk PRIMARY KEY (lbry_item_fact_key);


--
-- Name: out_bib_rec_marc_rec_field out_bib_rec_marc_rec_field_pk; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.out_bib_rec_marc_rec_field
    ADD CONSTRAINT out_bib_rec_marc_rec_field_pk PRIMARY KEY (bib_rec_dim_key, bib_rec_marc_rec_field_out_seq_no);


--
-- Name: out_lbry_holding_marc_rec_field out_lbry_holding_marc_rec_field_pk; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.out_lbry_holding_marc_rec_field
    ADD CONSTRAINT out_lbry_holding_marc_rec_field_pk PRIMARY KEY (lbry_holding_dim_key, lbry_holding_marc_rec_field_out_seq_no);


--
-- Name: dw_db_errors pk_dw_db_errors; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.dw_db_errors
    ADD CONSTRAINT pk_dw_db_errors PRIMARY KEY (dw_error_id, em_create_dw_prcsng_cycle_id);


--
-- Name: dw_stg_1_mai01_z00 pk_dw_stg_1_mai01_z00; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.dw_stg_1_mai01_z00
    ADD CONSTRAINT pk_dw_stg_1_mai01_z00 PRIMARY KEY (db_operation_cd, rec_trigger_key, em_create_dw_prcsng_cycle_id);


--
-- Name: dw_stg_1_mai01_z00_field pk_dw_stg_1_mai01_z00_field; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.dw_stg_1_mai01_z00_field
    ADD CONSTRAINT pk_dw_stg_1_mai01_z00_field PRIMARY KEY (db_operation_cd, rec_trigger_key, dw_stg_1_marc_rec_field_seq_no, em_create_dw_prcsng_cycle_id);


--
-- Name: dw_stg_1_mai01_z13 pk_dw_stg_1_mai01_z13; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.dw_stg_1_mai01_z13
    ADD CONSTRAINT pk_dw_stg_1_mai01_z13 PRIMARY KEY (db_operation_cd, rec_trigger_key, em_create_dw_prcsng_cycle_id);


--
-- Name: dw_stg_1_mai01_z13u pk_dw_stg_1_mai01_z13u; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.dw_stg_1_mai01_z13u
    ADD CONSTRAINT pk_dw_stg_1_mai01_z13u PRIMARY KEY (db_operation_cd, rec_trigger_key, em_create_dw_prcsng_cycle_id);


--
-- Name: dw_stg_1_mai39_z00 pk_dw_stg_1_mai39_z00; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.dw_stg_1_mai39_z00
    ADD CONSTRAINT pk_dw_stg_1_mai39_z00 PRIMARY KEY (db_operation_cd, rec_trigger_key, em_create_dw_prcsng_cycle_id);


--
-- Name: dw_stg_1_mai39_z13 pk_dw_stg_1_mai39_z13; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.dw_stg_1_mai39_z13
    ADD CONSTRAINT pk_dw_stg_1_mai39_z13 PRIMARY KEY (db_operation_cd, rec_trigger_key, em_create_dw_prcsng_cycle_id);


--
-- Name: dw_stg_1_mai39_z13u pk_dw_stg_1_mai39_z13u; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.dw_stg_1_mai39_z13u
    ADD CONSTRAINT pk_dw_stg_1_mai39_z13u PRIMARY KEY (db_operation_cd, rec_trigger_key, em_create_dw_prcsng_cycle_id);


--
-- Name: dw_stg_1_mai50_z103_bib_full pk_dw_stg_1_mai50_z103_bib_full; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.dw_stg_1_mai50_z103_bib_full
    ADD CONSTRAINT pk_dw_stg_1_mai50_z103_bib_full PRIMARY KEY (db_operation_cd, rec_trigger_key, em_create_dw_prcsng_cycle_id);


--
-- Name: dw_stg_1_mai50_z30 pk_dw_stg_1_mai50_z30; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.dw_stg_1_mai50_z30
    ADD CONSTRAINT pk_dw_stg_1_mai50_z30 PRIMARY KEY (db_operation_cd, rec_trigger_key, em_create_dw_prcsng_cycle_id);


--
-- Name: dw_stg_1_mai50_z30_full pk_dw_stg_1_mai50_z30_full; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.dw_stg_1_mai50_z30_full
    ADD CONSTRAINT pk_dw_stg_1_mai50_z30_full PRIMARY KEY (db_operation_cd, rec_trigger_key, em_create_dw_prcsng_cycle_id);


--
-- Name: dw_stg_1_mai50_z35 pk_dw_stg_1_mai50_z35; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.dw_stg_1_mai50_z35
    ADD CONSTRAINT pk_dw_stg_1_mai50_z35 PRIMARY KEY (db_operation_cd, rec_trigger_key, em_create_dw_prcsng_cycle_id);


--
-- Name: dw_stg_1_mai60_z00 pk_dw_stg_1_mai60_z00; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.dw_stg_1_mai60_z00
    ADD CONSTRAINT pk_dw_stg_1_mai60_z00 PRIMARY KEY (rec_trigger_key, db_operation_cd, em_create_dw_prcsng_cycle_id);


--
-- Name: dw_stg_1_mai60_z103_bib pk_dw_stg_1_mai60_z103_bib; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.dw_stg_1_mai60_z103_bib
    ADD CONSTRAINT pk_dw_stg_1_mai60_z103_bib PRIMARY KEY (db_operation_cd, rec_trigger_key, em_create_dw_prcsng_cycle_id);


--
-- Name: dw_stg_1_mai60_z13 pk_dw_stg_1_mai60_z13; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.dw_stg_1_mai60_z13
    ADD CONSTRAINT pk_dw_stg_1_mai60_z13 PRIMARY KEY (db_operation_cd, rec_trigger_key, em_create_dw_prcsng_cycle_id);


--
-- Name: dw_stg_1_mai60_z13u pk_dw_stg_1_mai60_z13u; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.dw_stg_1_mai60_z13u
    ADD CONSTRAINT pk_dw_stg_1_mai60_z13u PRIMARY KEY (db_operation_cd, rec_trigger_key, em_create_dw_prcsng_cycle_id);


--
-- Name: dw_stg_1_mpf_collection pk_dw_stg_1_mpf_collection; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.dw_stg_1_mpf_collection
    ADD CONSTRAINT pk_dw_stg_1_mpf_collection PRIMARY KEY (db_operation_cd, lbry_entity_cd, collection_cd, em_create_dw_prcsng_cycle_id);


--
-- Name: dw_stg_1_mpf_item_prcs_status pk_dw_stg_1_mpf_item_prcs_status; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.dw_stg_1_mpf_item_prcs_status
    ADD CONSTRAINT pk_dw_stg_1_mpf_item_prcs_status PRIMARY KEY (db_operation_cd, usmai_mbr_lbry_cd, item_prcs_status_cd, em_create_dw_prcsng_cycle_id);


--
-- Name: dw_stg_1_mpf_item_status pk_dw_stg_1_mpf_item_status; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.dw_stg_1_mpf_item_status
    ADD CONSTRAINT pk_dw_stg_1_mpf_item_status PRIMARY KEY (db_operation_cd, usmai_mbr_lbry_cd, item_status_cd, em_create_dw_prcsng_cycle_id);


--
-- Name: dw_stg_1_mpf_lbry_entity pk_dw_stg_1_mpf_lbry_entity; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.dw_stg_1_mpf_lbry_entity
    ADD CONSTRAINT pk_dw_stg_1_mpf_lbry_entity PRIMARY KEY (db_operation_cd, lbry_entity_cd, em_create_dw_prcsng_cycle_id);


--
-- Name: dw_stg_1_mpf_matrl_form pk_dw_stg_1_mpf_matrl_form; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.dw_stg_1_mpf_matrl_form
    ADD CONSTRAINT pk_dw_stg_1_mpf_matrl_form PRIMARY KEY (db_operation_cd, matrl_form_cd, em_create_dw_prcsng_cycle_id);


--
-- Name: dw_stg_1_mpf_mbr_lbry pk_dw_stg_1_mpf_mbr_lbry; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.dw_stg_1_mpf_mbr_lbry
    ADD CONSTRAINT pk_dw_stg_1_mpf_mbr_lbry PRIMARY KEY (db_operation_cd, usmai_mbr_lbry_cd, em_create_dw_prcsng_cycle_id);


--
-- Name: dw_stg_2_bib_rec_z00 pk_dw_stg_2_bib_rec_z00; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.dw_stg_2_bib_rec_z00
    ADD CONSTRAINT pk_dw_stg_2_bib_rec_z00 PRIMARY KEY (db_operation_cd, dw_stg_2_aleph_lbry_name, rec_trigger_key, in_z00_doc_number, em_create_dw_prcsng_cycle_id);


--
-- Name: dw_stg_2_bib_rec_z00_field pk_dw_stg_2_bib_rec_z00_field; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.dw_stg_2_bib_rec_z00_field
    ADD CONSTRAINT pk_dw_stg_2_bib_rec_z00_field PRIMARY KEY (in_z00_doc_number, db_operation_cd, dw_stg_2_aleph_lbry_name, in_dw_stg_1_marc_rec_field_seq_no, em_create_dw_prcsng_cycle_id);


--
-- Name: dw_stg_2_bib_rec_z13 pk_dw_stg_2_bib_rec_z13; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.dw_stg_2_bib_rec_z13
    ADD CONSTRAINT pk_dw_stg_2_bib_rec_z13 PRIMARY KEY (db_operation_cd, dw_stg_2_aleph_lbry_name, in_z13_rec_key, em_create_dw_prcsng_cycle_id);


--
-- Name: dw_stg_2_bib_rec_z13u pk_dw_stg_2_bib_rec_z13u; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.dw_stg_2_bib_rec_z13u
    ADD CONSTRAINT pk_dw_stg_2_bib_rec_z13u PRIMARY KEY (db_operation_cd, dw_stg_2_aleph_lbry_name, in_z13u_rec_key, em_create_dw_prcsng_cycle_id);


--
-- Name: dw_stg_2_lbry_holding_z00 pk_dw_stg_2_lbry_holding_z00; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.dw_stg_2_lbry_holding_z00
    ADD CONSTRAINT pk_dw_stg_2_lbry_holding_z00 PRIMARY KEY (db_operation_cd, dw_stg_2_aleph_lbry_name, in_z00_doc_number, em_create_dw_prcsng_cycle_id);


--
-- Name: dw_stg_2_lbry_holding_z00_field pk_dw_stg_2_lbry_holding_z00_field; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.dw_stg_2_lbry_holding_z00_field
    ADD CONSTRAINT pk_dw_stg_2_lbry_holding_z00_field PRIMARY KEY (db_operation_cd, dw_stg_2_aleph_lbry_name, in_z00_doc_number, in_dw_stg_1_marc_rec_field_seq_no, em_create_dw_prcsng_cycle_id);


--
-- Name: dw_stg_2_lbry_holding_z13 pk_dw_stg_2_lbry_holding_z13; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.dw_stg_2_lbry_holding_z13
    ADD CONSTRAINT pk_dw_stg_2_lbry_holding_z13 PRIMARY KEY (db_operation_cd, dw_stg_2_aleph_lbry_name, in_z13_rec_key, em_create_dw_prcsng_cycle_id);


--
-- Name: dw_stg_2_lbry_holding_z13u pk_dw_stg_2_lbry_holding_z13u; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.dw_stg_2_lbry_holding_z13u
    ADD CONSTRAINT pk_dw_stg_2_lbry_holding_z13u PRIMARY KEY (db_operation_cd, dw_stg_2_aleph_lbry_name, in_z13u_rec_key, em_create_dw_prcsng_cycle_id);


--
-- Name: dw_stg_2_lbry_item_event_z35 pk_dw_stg_2_lbry_item_event_z35; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.dw_stg_2_lbry_item_event_z35
    ADD CONSTRAINT pk_dw_stg_2_lbry_item_event_z35 PRIMARY KEY (db_operation_cd, dw_stg_2_aleph_lbry_name, in_z35_rec_key, em_create_dw_prcsng_cycle_id, in_z35_time_stamp);


--
-- Name: dw_stg_2_lbry_item_fact_z103_bib_full pk_dw_stg_2_lbry_item_fact_z103_bib_full; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.dw_stg_2_lbry_item_fact_z103_bib_full
    ADD CONSTRAINT pk_dw_stg_2_lbry_item_fact_z103_bib_full PRIMARY KEY (db_operation_cd, rec_trigger_key, em_create_dw_prcsng_cycle_id);


--
-- Name: dw_stg_2_lbry_item_fact_z30_full pk_dw_stg_2_lbry_item_fact_z30_full; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.dw_stg_2_lbry_item_fact_z30_full
    ADD CONSTRAINT pk_dw_stg_2_lbry_item_fact_z30_full PRIMARY KEY (db_operation_cd, rec_trigger_key, em_create_dw_prcsng_cycle_id);


--
-- Name: dw_stg_2_lbry_item_z30 pk_dw_stg_2_lbry_item_z30; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.dw_stg_2_lbry_item_z30
    ADD CONSTRAINT pk_dw_stg_2_lbry_item_z30 PRIMARY KEY (db_operation_cd, dw_stg_2_aleph_lbry_name, in_z30_rec_key, em_create_dw_prcsng_cycle_id);


--
-- Name: dw_stg_2_mpf_collection pk_dw_stg_2_mpf_collection; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.dw_stg_2_mpf_collection
    ADD CONSTRAINT pk_dw_stg_2_mpf_collection PRIMARY KEY (db_operation_cd, in_lbry_entity_cd, in_usmai_mbr_lbry_cd, in_collection_cd, em_create_dw_prcsng_cycle_id);


--
-- Name: dw_stg_2_mpf_item_prcs_status pk_dw_stg_2_mpf_item_prcs_status; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.dw_stg_2_mpf_item_prcs_status
    ADD CONSTRAINT pk_dw_stg_2_mpf_item_prcs_status PRIMARY KEY (in_mbr_lbry_cd, in_item_prcs_status_cd, em_create_dw_prcsng_cycle_id);


--
-- Name: dw_stg_2_mpf_item_status pk_dw_stg_2_mpf_item_status; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.dw_stg_2_mpf_item_status
    ADD CONSTRAINT pk_dw_stg_2_mpf_item_status PRIMARY KEY (db_operation_cd, in_usmai_mbr_lbry_cd, in_item_status_cd, em_create_dw_prcsng_cycle_id);


--
-- Name: dw_stg_2_mpf_lbry_entity pk_dw_stg_2_mpf_lbry_entity; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.dw_stg_2_mpf_lbry_entity
    ADD CONSTRAINT pk_dw_stg_2_mpf_lbry_entity PRIMARY KEY (db_operation_cd, in_usmai_mbr_lbry_cd, in_lbry_entity_cd, em_create_dw_prcsng_cycle_id);


--
-- Name: dw_stg_2_mpf_matrl_form pk_dw_stg_2_mpf_matrl_form; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.dw_stg_2_mpf_matrl_form
    ADD CONSTRAINT pk_dw_stg_2_mpf_matrl_form PRIMARY KEY (matrl_form_cd, em_create_dw_prcsng_cycle_id);


--
-- Name: dw_stg_2_mpf_mbr_lbry pk_dw_stg_2_mpf_mbr_lbry; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.dw_stg_2_mpf_mbr_lbry
    ADD CONSTRAINT pk_dw_stg_2_mpf_mbr_lbry PRIMARY KEY (db_operation_cd, in_usmai_mbr_lbry_cd, em_create_dw_prcsng_cycle_id);


--
-- Name: dw_stg_3_fact_lbry_item pk_dw_stg_3_fact_lbry_item; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.dw_stg_3_fact_lbry_item
    ADD CONSTRAINT pk_dw_stg_3_fact_lbry_item PRIMARY KEY (lbry_item_fact_key);


--
-- Name: dw_stg_1_ezp_sessns_snap pk_stg_1_ezp_sessns_snap; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.dw_stg_1_ezp_sessns_snap
    ADD CONSTRAINT pk_stg_1_ezp_sessns_snap PRIMARY KEY (mbr_lbry_cd, ezp_sessns_snap_tmstmp, em_create_dw_prcsng_cycle_id);


--
-- Name: dw_stg_2_ezp_sessns_snap pk_stg_2_ezp_sessns_snap; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.dw_stg_2_ezp_sessns_snap
    ADD CONSTRAINT pk_stg_2_ezp_sessns_snap PRIMARY KEY (in_mbr_lbry_cd, in_ezp_sessns_snap_tmstmp, em_create_dw_prcsng_cycle_id);


--
-- Name: IX_Relationship2; Type: INDEX; Schema: public; Owner: usmai_dw
--

CREATE INDEX "IX_Relationship2" ON public.dw_prcsng_cycle_job_exectn USING btree (dw_prcsng_cycle_id);


--
-- Name: indx_dim_bib_rec_nk; Type: INDEX; Schema: public; Owner: usmai_dw
--

CREATE UNIQUE INDEX indx_dim_bib_rec_nk ON public.dim_bib_rec USING btree (bib_rec_source_system_id, rm_rec_effective_from_dt, rm_rec_effective_to_dt);


--
-- Name: indx_dim_date_nk; Type: INDEX; Schema: public; Owner: usmai_dw
--

CREATE UNIQUE INDEX indx_dim_date_nk ON public.dim_date USING btree (clndr_dt, rm_rec_effective_from_dt, rm_rec_effective_to_dt);


--
-- Name: indx_dim_lbry_holding_nk; Type: INDEX; Schema: public; Owner: usmai_dw
--

CREATE UNIQUE INDEX indx_dim_lbry_holding_nk ON public.dim_lbry_holding USING btree (lbry_holding_source_system_id, rm_rec_effective_from_dt, rm_rec_effective_to_dt);


--
-- Name: indx_dim_lbry_item_loc_nk; Type: INDEX; Schema: public; Owner: usmai_dw
--

CREATE UNIQUE INDEX indx_dim_lbry_item_loc_nk ON public.dim_lbry_item_loc USING btree (lbry_item_loc_lbry_entity_cd, lbry_item_loc_collection_cd, rm_rec_effective_from_dt, rm_rec_effective_to_dt);


--
-- Name: indx_dim_lbry_item_matrl_form_nk; Type: INDEX; Schema: public; Owner: usmai_dw
--

CREATE UNIQUE INDEX indx_dim_lbry_item_matrl_form_nk ON public.dim_lbry_item_matrl_form USING btree (lbry_item_matrl_form_cd, rm_rec_effective_from_dt, rm_rec_effective_to_dt);


--
-- Name: indx_dim_lbry_item_nk; Type: INDEX; Schema: public; Owner: usmai_dw
--

CREATE UNIQUE INDEX indx_dim_lbry_item_nk ON public.dim_lbry_item USING btree (lbry_item_source_system_id, rm_rec_effective_from_dt, rm_rec_effective_to_dt);


--
-- Name: indx_dim_lbry_item_prcs_status_nk; Type: INDEX; Schema: public; Owner: usmai_dw
--

CREATE UNIQUE INDEX indx_dim_lbry_item_prcs_status_nk ON public.dim_lbry_item_prcs_status USING btree (lbry_item_usmai_mbr_lbry_cd, lbry_item_prcs_status_cd, rm_rec_effective_from_dt, rm_rec_effective_to_dt);


--
-- Name: indx_dim_lbry_item_status_nk; Type: INDEX; Schema: public; Owner: usmai_dw
--

CREATE UNIQUE INDEX indx_dim_lbry_item_status_nk ON public.dim_lbry_item_status USING btree (lbry_item_usmai_mbr_lbry_cd, lbry_item_status_cd, rm_rec_effective_from_dt, rm_rec_effective_to_dt);


--
-- Name: indx_fact_lbry_item_as_of_clnfr_dt; Type: INDEX; Schema: public; Owner: usmai_dw
--

CREATE INDEX indx_fact_lbry_item_as_of_clnfr_dt ON public.fact_lbry_item USING btree (lbry_item_as_of_clndr_dt_dim_key);


--
-- Name: indx_fact_lbry_item_bib_rec_dim; Type: INDEX; Schema: public; Owner: usmai_dw
--

CREATE INDEX indx_fact_lbry_item_bib_rec_dim ON public.fact_lbry_item USING btree (bib_rec_dim_key);


--
-- Name: indx_fact_lbry_item_create_clndr_dt; Type: INDEX; Schema: public; Owner: usmai_dw
--

CREATE INDEX indx_fact_lbry_item_create_clndr_dt ON public.fact_lbry_item USING btree (lbry_item_create_clndr_dt_dim_key);


--
-- Name: indx_fact_lbry_item_lbry_holding; Type: INDEX; Schema: public; Owner: usmai_dw
--

CREATE INDEX indx_fact_lbry_item_lbry_holding ON public.fact_lbry_item USING btree (lbry_holding_dim_key);


--
-- Name: indx_fact_lbry_item_lbry_holding_loc; Type: INDEX; Schema: public; Owner: usmai_dw
--

CREATE INDEX indx_fact_lbry_item_lbry_holding_loc ON public.fact_lbry_item USING btree (lbry_item_holding_loc_dim_key);


--
-- Name: indx_fact_lbry_item_lbry_item_loc; Type: INDEX; Schema: public; Owner: usmai_dw
--

CREATE INDEX indx_fact_lbry_item_lbry_item_loc ON public.fact_lbry_item USING btree (lbry_item_loc_dim_key);


--
-- Name: indx_fact_lbry_item_matrl_form; Type: INDEX; Schema: public; Owner: usmai_dw
--

CREATE INDEX indx_fact_lbry_item_matrl_form ON public.fact_lbry_item USING btree (lbry_item_matrl_form_dim_key);


--
-- Name: indx_fact_lbry_item_prcs_status; Type: INDEX; Schema: public; Owner: usmai_dw
--

CREATE INDEX indx_fact_lbry_item_prcs_status ON public.fact_lbry_item USING btree (lbry_item_prcs_status_dim_key);


--
-- Name: indx_fact_lbry_item_status; Type: INDEX; Schema: public; Owner: usmai_dw
--

CREATE INDEX indx_fact_lbry_item_status ON public.fact_lbry_item USING btree (lbry_item_status_dim_key);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: usmai_dw
--

REVOKE ALL ON SCHEMA public FROM postgres;
REVOKE ALL ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO usmai_dw;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--
