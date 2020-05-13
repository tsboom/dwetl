from dwetl.processor.processor import Processor
from dwetl.reader.sql_alchemy_reader import SqlAlchemyReader
from datetime import datetime
import pdb
import pprint

class EzproxyProcessor(Processor):
    """
    Processor for processing ez proxy data
    """

    def __init__(self, reader, writer, job_info, logger):
        super().__init__(reader, writer, job_info, logger)

    def job_name(self):
        return 'EzproxyProcessor'

    @classmethod
    def library_dim_lookup(cls, item):
        """
        using the mbr_lbry_cd, find the mbr_lbry_dim_key and put into 
        t1_mbr_lbry_cd__ezp_sessns_snap_mbr_lbry_dim_key
        """
        library_code = item['mbr_lbry_cd']
        
        with dwetl.reporting_database_session() as session:
            member_library_table = dwetl.Base.classes['dim_mbr_lbry']
            # look up the mbr_lbry_dim_key 
            matching_row = session.query(member_library_table).filter_by(name=library_code).first()
           
            mbr_lbry_dim_key = matching_row.mbr_lbry_dim_key

        return mbr_lbry_dim_key

    @classmethod
    def clndr_dt_dim_lookup(cls, item):
        """
        using the ezp_sessns_snap_tmstmp, get the calendar date, and look up clndr_dt_dim_key in dim_date
        """
        
        
        
    @classmethod
    def convert_tmstmp(cls, item):
        """
        convert 20200509-0000 into a timestamp readable by SqlAlchemy (datetime)
        """
        timestamp = item['in_ezp_sessns_snap_tmstmp']
        datetime_object = datetime.strptime(timestamp, '%Y%m%d-%H%M')
        
        return datetime_object

        
    def process_item(self, item):
        processed_item = Preprocess.preprocess(item, self.json_config, self.stg2_pk_list)
        processed_item.update(self.job_info.as_dict('update'))
        processed_item['em_update_dw_job_name'] = self.job_name()
        processed_item['em_update_tmstmp'] = datetime.datetime.now()
        return processed_item
