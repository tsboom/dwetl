from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import *
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine


# def create_db_engine():
#     # connect to database
#     engine = create_engine(DB_CONNECTION_STRING, echo=True)
#     return engine
#
# DB_CONNECTION_STRING = 'postgresql+psycopg2://usmai_dw:B1gUmD4t9@pgcommondev.lib.umd.edu/usmai_dw_etl'
#
# # use automap to reflect existing db into model
# Base = automap_base()
#
# engine = create_db_engine()
#
# # reflect existing table from db
# Base.prepare(engine, reflect=True)
#
# # assign reflected table to class name
# Z30 = Base.classes.dw_stg_1_mai50_z30


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
