from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData, Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import *
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.engine import reflection
from sqlalchemy import MetaData
import logging
import database_credentials
import pdb

from datetime import datetime

from sqlalchemy import (MetaData, Table, Column, Integer, Numeric, String,
                        DateTime, ForeignKey)



metadata = MetaData()

bibliographic_record_dimension = Table('dw_stg_3_bib_rec_dim', metadata,
    Column('bib_rec_dim_key', Integer(), primary_key=True),
    Column('bib_record_rec_type_desc', String(50)),
    Column('bib_rec_id', String(9)),
    Column('bib_rec_aleph_lbry_name', String(5)),
    Column('bib_rec_marc_rec_field_cnt', Integer()),
    Column('bib_rec_marc_rec_data_content_len_cnt',	Integer()),
    Column('bib_rec_marc_rec_data_content_txt', String(45000)),
    Column('bib_rec_publication_year_no', Integer()),
    Column('bib_rec_title',	String(100)),
    Column('bib_rec_author_name', String(100)),
    Column('bib_rec_imprint_txt', String(100)),
    Column('bib_rec_isbn_issn_source_cd', String(5)),
    Column('bib_rec_isbn_txt', String(100)),
    Column('bib_rec_all_associated_issns_txt', String(100)),
    Column('bib_rec_oclc_no', String(500)),
    Column('bib_rec_marc_rec_leader_field_txt',	String(500)),
    Column('bib_rec_type_cd', String(1)),
    Column('bib_rec_type_desc',	String(50)),
    Column('bib_rec_bib_lvl_cd', String(1)),
    Column('bib_rec_bib_lvl_desc', String()),
    Column('bib_rec_encoding_lvl_cd', String(1)),
    Column('bib_rec_encoding_lvl_desc', String()),
    Column('bib_rec_marc_rec_008_field_txt', String(500)),
    Column('bib_rec_language_cd', String(3)),
    Column('bib_rec_issn', String(500)),
    Column('bib_rec_display_suppressed_flag', String(1)),
    Column('bib_rec_acquisition_created_flag', String(1)),
    Column('bib_rec_circulation_created_flag', String(1)),
    Column('bib_rec_provisional_status_flag', String(1)),
    Column('bib_rec_create_dt',	DateTime()),
    Column('bib_rec_updt_dt', DateTime()),
    Column('bib_rec_marc_rec_fields_key', Integer())
)

library_item_dimension = Table('dw_stg_3_lbry_item_dim', metadata,
    Column('lbry_item_dim_key', String(), primary_key=True),
    Column('lbry_item_rec_type_desc', String(50)),
    Column('lbry_item_source_system_id', String(15)),
    Column('lbry_item_adm_no', String(9)),
    Column('lbry_item_seq_no', 'String(6)),
    Column('lbry_item_aleph_lbry_name', String(5)),
    Column('lbry_lms_staff_acct_id', String(10)),
    Column('lbry_item_create_dt', DateTime()),
    Column('lbry_item_update_dt', DateTime()),
    Column('lbry_item_total_loan_event_cnt', Integer()),
    Column('lbry_item_volume_issue_no', String(20)),
    Column('lbry_item_accession_dt', DateTime()),
    Column('lbry_item_page_range_txt', String(30)),
    Column('lbry_item_copy_no', String(5)),
    Column('lbry_item_publication_dt', DateTime()),
    Column('lbry_item_supplemental_material_title', String(30)),
    Column('lbry_item_expected_arrival_dt', DateTime()),
    Column('lbry_item_actual_arrival_dt', DateTime()),
    Column('lbry_item_acquisition_price_amt', String(10)),
    Column('lbry_item_barcode_no', String(30)),
    Column('lbry_item_loc_call_no_scheme_cd', String(1)),
    Column('lbry_item_loc_call_no_scheme_desc', String(50)),
    Column('lbry_item_loc_call_no', String(80)),
    Column('lbry_item_loc_sort_nrmlzd_call_no', String(80)),
    Column('lbry_item_loc_temp_designation_flag', String(1)),
    Column('lbry_item_alt_loc_call_no_scheme_cd', String(1)),
    Column('lbry_item_alt_loc_call_no_scheme_desc', String(50)),
    Column('lbry_item_alt_loc_call_no', String(80)),
    Column('lbry_item_alt_loc_sort_nrmlzd_call_no', String(80)),
    Column('lbry_item_enumeration_lvl_1_txt', String(20)),
    Column('lbry_item_enumeration_lvl_2_txt', String(20)),
    Column('lbry_item_enumeration_lvl_3_txt', String(20)),
    Column('lbry_item_enumeration_lvl_4_txt', String(20)),
    Column('lbry_item_enumeration_lvl_5_txt', String(20)),
    Column('lbry_item_enumeration_lvl_6_txt', String(20)),
    Column('lbry_item_alt_enumeration_lvl_1_txt', String(20)),
    Column('lbry_item_alt_enumeration_lvl_2_txt', String(20)),
    Column('lbry_item_chronology_lvl_1_txt', String(20)),
    Column('lbry_item_chronology_lvl_2_txt', String(20)),
    Column('lbry_item_chronology_lvl_3_txt', String(20)),
    Column('lbry_item_chronology_lvl_4_txt', String(20)),
    Column('lbry_item_alt_chronology_txt', String(20)),
    Column('lbry_item_crcltn_display_note',	String(200)),
    Column('lbry_item_opac_display_txt', String(200)),
    Column('lbry_item_staff_only_display_note', String(200))
)


















'''
I'm not manually defining File_equivalent tables for now
'''
# Base = declarative_base()
#
#
# class Z30(Base):
#     __tablename__ = 'test_z30'
#
#     H = Column(String(1))
#     db_operation_cd = Column(String(1))
#     trigger_rec_key = Column(String(15))
#     z30_rec_key = Column(String, primary_key=True)
#     z30_barcode = Column(String(30))
#     z30_sub_library = Column(String(5))
#     z30_material = Column(String(5))
#     z30_item_status = Column(String(2))
#     z30_open_date = Column(String(8))
#     z30_update_date = Column(String(8))
#     z30_cataloger = Column(String(10))
#     z30_date_last_return = Column(String(8))
#     z30_hour_last_return = Column(String(4))
#     z30_ip_last_return = Column(String(20))
#     z30_no_loans = Column(String(3))
#     z30_alpha = Column(String(1))
#     z30_collection = Column(String(5))
#     z30_call_no_type = Column(String(1))
#     z30_call_no = Column(String(80))
#     z30_call_no_key = Column(String(80))
#     z30_call_no_2_type = Column(String(1))
#     z30_call_no_2 = Column(String(80))
#     z30_call_no_2_key = Column(String(80))
#     z30_description = Column(String(200))
#     z30_note_opac = Column(String(200))
#     z30_note_circulation = Column(String(200))
#     z30_note_internal = Column(String(200))
#     z30_order_number = Column(String(30))
#     z30_inventory_number = Column(String(20))
#     z30_inventory_number_date = Column(String(8))
#     z30_last_shelf_report_date = Column(String(8))
#     z30_price = Column(String(10))
#     z30_shelf_report_number = Column(String(20))
#     z30_on_shelf_date = Column(String(8))
#     z30_on_shelf_seq = Column(String(6))
#     z30_rec_key_2 = Column(String(19))
#     z30_rec_key_3 = Column(String(40))
#     z30_pages = Column(String(30))
#     z30_issue_date = Column(String(8))
#     z30_expected_arrival_date = Column(String(8))
#     z30_arrival_date = Column(String(10))
#     z30_item_statistic = Column(String(10))
#     z30_item_process_status = Column(String(2))
#     z30_copy_id = Column(String(5))
#     z30_hol_doc_number_x = Column(String(9))
#     z30_temp_location = Column(String(1))
#     z30_enumeration_a = Column(String(20))
#     z30_enumeration_b = Column(String(20))
#     z30_enumeration_c = Column(String(20))
#     z30_enumeration_d = Column(String(20))
#     z30_enumeration_e = Column(String(20))
#     z30_enumeration_f = Column(String(20))
#     z30_enumeration_g = Column(String(20))
#     z30_enumeration_h = Column(String(20))
#     z30_chronological_i = Column(String(20))
#     z30_chronological_j = Column(String(20))
#     z30_chronological_k = Column(String(20))
#     z30_chronological_l = Column(String(20))
#     z30_chronological_m = Column(String(20))
#     z30_supp_index_o = Column(String(30))
#     z30_85x_type = Column(String(1))
#     z30_depository_id = Column(String(5))
#     z30_linking_number = Column(String(9))
#     z30_gap_indicator = Column(String(1))
#     z30_maintenance_count = Column(String(8))
#     z30_process_status_date = Column(String(20))
#     z30_upd_time_stamp = Column(String(15))
#     z30_ip_last_return_v6 = Column(String(50))
#     em_create_dw_prcssng_cycle_id = Column(Integer, nullable=False)
#     em_create_dw_job_exectn_no = Column(Integer, nullable=False)
#     em_create_dw_job_name = Column(String(100), nullable=False)
#     em_create_dw_job_version_no = Column(String(20), nullable=False)
#     em_create_user_id = Column(String(20), nullable=False)
#     em_create_tmstmp = Column(DateTime, default=datetime.datetime.now, nullable=False)
#
#     def __repr__(self):
# ...        return "<Z30(name='%s', fullname='%s', password='%s')>" % (
# ...                             self.name, self.fullname, self.password)
