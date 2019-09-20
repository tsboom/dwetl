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
-- Name: dw_stg_2_lbry_item_fact_z103_bib_full; Type: TABLE; Schema: public; Owner: usmai_dw
--

CREATE TABLE public.dw_stg_2_lbry_item_fact_z103_bib_full (
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

ALTER TABLE public.dw_stg_2_lbry_item_fact_z103_bib_full OWNER TO usmai_dw;


--
-- Name: dw_stg_1_mai39_z13u pk_dw_stg_1_mai60_z13u; Type: CONSTRAINT; Schema: public; Owner: usmai_dw
--

ALTER TABLE ONLY public.dw_stg_1_mai39_z13u
    ADD CONSTRAINT pk_dw_stg_1_mai39_z13u PRIMARY KEY (db_operation_cd, rec_trigger_key, em_create_dw_prcsng_cycle_id);

ALTER TABLE ONLY public.dw_stg_1_mai50_z30_full
    ADD CONSTRAINT pk_dw_stg_1_mai50_z30_full PRIMARY KEY (db_operation_cd, rec_trigger_key, em_create_dw_prcsng_cycle_id);



ALTER TABLE ONLY public.dw_stg_1_mai50_z103_bib_full
    ADD CONSTRAINT pk_dw_stg_1_mai50_z103_bib_full PRIMARY KEY (db_operation_cd, rec_trigger_key, em_create_dw_prcsng_cycle_id);


ALTER TABLE ONLY public.dw_stg_2_lbry_item_fact_z103_bib_full
    ADD CONSTRAINT pk_dw_stg_2_lbry_item_fact_z103_bib_full PRIMARY KEY (db_operation_cd, rec_trigger_key, em_create_dw_prcsng_cycle_id);
