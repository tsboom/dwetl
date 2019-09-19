import os
import pdb
import datetime
import getpass
from sqlalchemy import func
import dwetl


class JobInfo():
    """
    This class holds the processing metadata for a job.
    """
    def __init__(self, prcsng_cycle_id, user_id, job_version_no, job_exectn_id):
        self.prcsng_cycle_id = prcsng_cycle_id
        self.user_id = user_id
        self.job_exectn_id = job_exectn_id
        self.job_version_no = job_version_no


class JobInfoFactory():
    '''
    builds job info objects
    '''

    @classmethod
    def create_job_info_from_db(cls, session, table_base_class):
        cls.session = session
        cls.table_base_class = table_base_class
        max_prcsng_id = cls.session.query(func.max(table_base_class.dw_prcsng_cycle_id)).scalar()
        if max_prcsng_id == None:
            cls.prcsng_cycle_id = 1
        else:
            cls.prcsng_cycle_id = max_prcsng_id + 1
        cls.user_id = getpass.getuser()
        cls.job_exectn_id = 1
        cls.job_version_no = dwetl.version


        row = {
            'dw_prcsng_cycle_id': cls.prcsng_cycle_id,
            'dw_prcsng_cycle_planned_dt': datetime.datetime.now(),
            'dw_prcsng_cycle_stat_type_cd': '',
            'dw_prcsng_cycle_freq_type_cd': '',
            'dw_prcsng_cycle_exectn_start_tmstmp': datetime.datetime.now(),
            'em_create_tmstmp': datetime.datetime.now(),
            'em_create_user_id': cls.user_id
        }

        record = cls.table_base_class(**row)
        cls.session.add(record)
        return JobInfo(cls.prcsng_cycle_id, cls.user_id, cls.job_version_no, cls.job_exectn_id)
