-- Remove current PRIMARY KEY attribute
ALTER TABLE dw_stg_1_mai39_z00_field DROP CONSTRAINT pk_dw_stg_1_mai39_z00_field;
-- Set new PRIMARY KEY
ALTER TABLE dw_stg_1_mai39_z00_field ADD PRIMARY KEY (db_operation_cd, rec_trigger_key, dw_stg_1_marc_rec_field_seq_no, em_create_dw_prcsng_cycle_id);
-- Remove current PRIMARY KEY attribute
ALTER TABLE dw_stg_1_mai60_z00_field DROP CONSTRAINT pk_dw_stg_1_mai60_z00_field;
-- Set new PRIMARY KEY
ALTER TABLE dw_stg_1_mai60_z00_field ADD PRIMARY KEY (db_operation_cd, rec_trigger_key, dw_stg_1_marc_rec_field_seq_no, em_create_dw_prcsng_cycle_id);
