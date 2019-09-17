import os

class JobInfo():
    """
    This class finds out the processing metadata for a job.

    It builds a job_info object.
    """
    def __init__(self, prcsng_cycle_id, job_exectn_id, job_version_no, user_id):
        self.prcsng_cycle_id = prcsng_cycle_id
        self.job_exectn_id = job_exectn_id
        self.job_version_no = job_version_no
        self.user_id = user_id

    def set_prcsng_cycle_id(self, session):
        '''
        Look into the db to see if processing cycle id exists, and increment the number.
        If there is nothing, use 1.
        '''
        # query to see what current process ID is
        max_prcsng_id = self.session.query(func.max(table_base_class.em_create_dw_prcsng_cycle_id))
