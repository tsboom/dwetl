ALTER TABLE dw_stg_2_mpf_lbry_entity
ALTER COLUMN in_lbry_entity_cd TYPE varchar(5);

ALTER TABLE dw_stg_2_mpf_collection
ALTER COLUMN in_lbry_entity_cd TYPE varchar(5);

ALTER TABLE dw_stg_2_mpf_collection
ALTER COLUMN rm_dq_check_excptn_cnt drop not null;

ALTER TABLE dw_stg_2_mpf_item_prcs_status
ALTER COLUMN in_mbr_lbry_cd drop not null;
-- alter table users alter column email drop not null;
-- ALTER COLUMN rm_dq_check_excptn_cnt smallint NULL;
-- MODIFY Age int NOT NULL;
-- ALTER rm_dq_check_excptn_cnt NULL;
