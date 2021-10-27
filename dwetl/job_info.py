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

    def as_dict(self, type):
        result = {}
        for key, val in self.__dict__.items():
            prefix = f'em_{type}_dw_'
            if key == 'user_id':
                prefix = f'em_{type}_'
            result[prefix + key] = val
        return result


class JobInfoFactory():
    '''
    builds job info objects
    '''
    # create job_info using max processing cycle id + 1 of any table
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
    
        logger.info(f'Unique processing cycle ID used for this job: {cls.prcsng_cycle_id}')    
        print(f'Unique processing cycle ID used for this job: {cls.prcsng_cycle_id}')

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
    
    # TODO: Need to look closer at where this method is being used. Now that the processing cycle ID
    # is based off of the reporting db instead of the ETL db, we are not calculating the max here, but
    # we pass in the reporting processing cycle id from ezproxy_etl.py, and make sure its unique in the
    # etl db. If it isn't increment the largest processing cycle id by 1. 
    @classmethod
    def create_job_info_from_reporting_db(cls, session, table_base_class, reporting_max_prcsng_id, logger):
        cls.session = session
        cls.table_base_class = table_base_class
        cls.user_id = getpass.getuser()
        cls.job_exectn_id = 1
        cls.job_version_no = dwetl.version
   
        # determine the processing cycle id by checking if reporting db processing cycle id already exists in the etl db
        processing_cycle_query = cls.session.query(table_base_class.dw_prcsng_cycle_id==reporting_max_prcsng_id)
        does_exist = cls.session.query(processing_cycle_query.exists()).scalar()
        logger.info(f'Checking the reporting max processing ID of {reporting_max_prcsng_id}...')

        if does_exist:
            # compare the reporting_max_prcsng_id with the max value in etl db and use a number 1 higher than the largest max
            max_prcsng_id = cls.session.query(func.max(table_base_class.dw_prcsng_cycle_id)).scalar() 
            if max_prcsng_id >= reporting_max_prcsng_id:
                cls.prcsng_cycle_id = max_prcsng_id + 1
            else:
                logger.warning(f"Processing cycle ID was not unique due to a previous failed run in the ETL db.")
                print(f"Processing cycle ID was not unique due to a previous failed run in the ETL db.")
                cls.prcsng_cycle_id = reporting_max_prcsng_id + 1
        else:
            # if the reporting processing cycle id doesn't exist in the etl db, use the reporting max + 1 so it's unique
            cls.prcsng_cycle_id = reporting_max_prcsng_id + 1
        logger.info(f'Unique processing cycle ID used for this job: {cls.prcsng_cycle_id}')    
        print(f'Unique processing cycle ID used for this job: {cls.prcsng_cycle_id}')

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

    @classmethod
    def create_from_prcsng_cycle_id(cls, prcsng_cycle_id):
        user_id =  getpass.getuser()
        job_exectn_id = 1
        job_version_no = dwetl.version
        job_info = JobInfo(prcsng_cycle_id, user_id, job_version_no, job_exectn_id)
        return job_info
