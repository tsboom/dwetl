import dwetl
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
        library_code = item['in_mbr_lbry_cd'].upper()
        
        
        with dwetl.reporting_database_session() as session:
            
            MemberLibrary = dwetl.Base.classes.dim_mbr_lbry
            # look up the mbr_lbry_dim_key 
            matching_row = session.query(MemberLibrary).filter_by(mbr_lbry_cd=library_code).first()
            mbr_lbry_dim_key = matching_row.mbr_lbry_dim_key

        return mbr_lbry_dim_key

    @classmethod
    def clndr_dt_dim_lookup(cls, item):
        """
        using the ezp_sessns_snap_tmstmp, get the calendar date, and look up clndr_dt_dim_key in dim_date
        """
        timestamp = item['in_ezp_sessns_snap_tmstmp']
        
        date = datetime.strptime(timestamp, '%Y%m%d-%H%M')
        
        # need a string YYYY-MM-DD
        datestring = date.strftime('%Y-%m-%d')
        
        with dwetl.reporting_database_session() as session:
            
            dim_date = dwetl.Base.classes.dim_date
            # look up the mbr_lbry_dim_key 
            matching_row = session.query(dim_date).filter_by(clndr_dt=datestring).first()
            
            clndr_dt_dim_key = matching_row.clndr_dt_dim_key
            
        return clndr_dt_dim_key
        
        
    @classmethod
    def convert_timestamp(cls, item):

        """
        convert 20200509-0000 into a timestamp readable by SqlAlchemy (datetime)
        """
        timestamp = item['in_ezp_sessns_snap_tmstmp']
        datetime_object = datetime.strptime(timestamp, '%Y%m%d-%H%M')
        
        return datetime_object

    @classmethod
    def transform(cls, item):
        """
        do the transformations for ez proxy data 
        """
        # dictionary to hold processed item
        out_dict = {}
    
        # process item
        for key, value in item.items():
            if key == "in_ezp_sessns_snap_tmstmp":
                timestamp = EzproxyProcessor.convert_timestamp(item)
                out_dict['t2_ezp_sessns_snap_tmstmp__ezp_sessns_snap_tmstmp'] = timestamp
                
                calendar_date_dim_key = EzproxyProcessor.clndr_dt_dim_lookup(item)
                out_dict['t1_ezp_sessns_snap_clndr_dt_dim_key'] = calendar_date_dim_key
                
            elif key == "in_mbr_lbry_cd":
                library_dim_key = EzproxyProcessor.library_dim_lookup(item)
                out_dict['t1_mbr_lbry_cd__ezp_sessns_snap_mbr_lbry_dim_key'] = library_dim_key
            
            else:
                target_col_name = key.replace('in_', 't1_')
                out_dict[target_col_name] = value
                
        return out_dict
                
                    
    def process_item(self, item):
        processed_item = EzproxyProcessor.transform(item, self.logger)
        processed_item.update(self.job_info.as_dict('update'))
        processed_item['em_update_dw_job_name'] = self.job_name()
        processed_item['em_update_tmstmp'] = datetime.now()
        return processed_item
