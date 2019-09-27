ALTER TABLE dw_stg_1_mpf_mbr_lbry
DROP COLUMN em_create_tmstmp;

ALTER TABLE dw_stg_1_mpf_mbr_lbry
ADD COLUMN em_create_tmstmp timestamp without time zone;

ALTER TABLE dw_stg_1_mpf_mbr_lbry
ALTER COLUMN em_create_tmstmp SET NOT NULL;
