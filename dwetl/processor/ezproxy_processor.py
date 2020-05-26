import dwetl
from dwetl.processor.processor import Processor
from dwetl.reader.sql_alchemy_reader import SqlAlchemyReader
from sqlalchemy import and_, func
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

    @staticmethod
    def clndr_dt_dim_lookup(item):
        """
        using the ezp_sessns_snap_tmstmp, get the calendar date, and look up clndr_dt_dim_key in dim_date
        """
        timestamp = item['in_ezp_sessns_snap_tmstmp']

        date = datetime.strptime(timestamp, '%Y%m%d-%H%M')

        # need a string YYYY-MM-DD
        datestring = date.strftime('%Y-%m-%d')

        with dwetl.reporting_database_session() as session2:
            dim_date = dwetl.ReportingBase.classes.dim_date
            # look up the calendar date
            matching_row = session2.query(dim_date).\
                filter(dim_date.clndr_dt==datestring).\
                filter(date >= func.date(dim_date.rm_rec_effective_from_dt)).\
                filter(date < func.date(dim_date.rm_rec_effective_to_dt)).first()

            clndr_dt_dim_key = matching_row.clndr_dt_dim_key
        return clndr_dt_dim_key


    @staticmethod
    def time_of_day_dim_key_lookup(item):
        """
        using ezp_sessns_snap_tmstmp
        get ezp_sessns_snap_time_of_day_dim_key
        """

        timestamp = item['in_ezp_sessns_snap_tmstmp']

        date = datetime.strptime(timestamp, '%Y%m%d-%H%M')

        # need a string HH:MM:SS
        timestring = date.strftime('%H:%M:%S')

        with dwetl.reporting_database_session() as session2:
            dim_time_of_day = dwetl.ReportingBase.classes.dim_time_of_day

            #look up the time of day
            matching_row = session2.query(dim_time_of_day).\
                filter(dim_time_of_day.time_of_day==timestring).\
                filter(date >= func.date(dim_time_of_day.rm_rec_effective_from_dt)).\
                filter(date < func.date(dim_time_of_day.rm_rec_effective_to_dt)).first()

            time_dim_key = matching_row.time_of_day_dim_key
        return time_dim_key

    @staticmethod
    def library_dim_lookup(item):
        """
        using the mbr_lbry_cd, find the mbr_lbry_dim_key and put into
        t1_mbr_lbry_cd__ezp_sessns_snap_mbr_lbry_dim_key
        """
        library_code = item['in_mbr_lbry_cd'].upper()

        timestamp = item['in_ezp_sessns_snap_tmstmp']

        date = datetime.strptime(timestamp, '%Y%m%d-%H%M')


        with dwetl.reporting_database_session() as session2:
            MemberLibrary = dwetl.ReportingBase.classes.dim_mbr_lbry

            # look up the mbr_lbry_dim_key
            matching_row = session2.query(MemberLibrary).\
                filter(MemberLibrary.mbr_lbry_cd==library_code).\
                filter(date >= func.date(MemberLibrary.rm_rec_effective_from_dt)).\
                filter(date < func.date(MemberLibrary.rm_rec_effective_to_dt)).first()

            mbr_lbry_dim_key = matching_row.mbr_lbry_dim_key

        return mbr_lbry_dim_key

    @staticmethod
    def convert_timestamp(item):

        """
        convert 20200509-0000 into a timestamp readable by SqlAlchemy (datetime)
        """
        timestamp = item['in_ezp_sessns_snap_tmstmp']
        datetime_object = datetime.strptime(timestamp, '%Y%m%d-%H%M')

        return datetime_object


    @classmethod
    def transform(cls, item, logger):
        """
        do the transformations for ez proxy data
        """
        # dictionary to hold processed item
        out_dict = {}

        # process item
        for key, value in item.items():
            if key == 'em_create_dw_prcsng_cycle_id':
                out_dict[key] = value
            if key.startswith('in_'):
                if key == '_sa_instance_state':
                    continue
                elif key == "in_ezp_sessns_snap_tmstmp":
                    # save value in pk
                    out_dict[key] = value

                    timestamp = EzproxyProcessor.convert_timestamp(item)

                    out_dict['t2_ezp_sessns_snap_tmstmp__ezp_sessns_snap_tmstmp'] = timestamp

                    # look up calendar_date_dim_key
                    calendar_date_dim_key = EzproxyProcessor.clndr_dt_dim_lookup(item)
                    out_dict['t1_ezp_sessns_snap_tmstmp__ezp_sessns_snap_clndr_dt_dim_key'] = calendar_date_dim_key

                    # look up time of day dim key
                    time_of_day_dim_key = EzproxyProcessor.time_of_day_dim_key_lookup(item)
                    out_dict['t3_ezp_sessns_snap_tmstmp__ezp_sessns_snap_time_of_day_dim_key'] = time_of_day_dim_key

                elif key == "in_mbr_lbry_cd":
                    out_dict[key] = value
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
