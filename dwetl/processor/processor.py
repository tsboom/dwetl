import pdb
import pprint
from dwetl.exceptions import DWETLException
import dwetl
from sqlalchemy import func

class Processor:
    """
    Abstract class that encapsulates a processing step.

    Subclasses should implement the "job_name" and "process_item" methods.
    """
    def __init__(self, reader, writer, job_info, logger, error_writer=None):
        self.reader = reader
        self.writer = writer
        self.job_info = job_info
        self.logger = logger
        self.error_writer = error_writer


    def execute(self):
        for row_dict in self.reader:
            processed_row_dict = self.process_item(row_dict)

            if processed_row_dict:
                try:
                    self.writer.write_row(processed_row_dict)
                except DWETLException as e:
                    # this will catch SQL Alchemy exceptions
                    error = e.error_text
                    # save the dictionary of the problem row if it is available as .params
                    if e.error_row:
                        error_row = e.error_row

                    # Increment dw_error_id value from the table or set as 1 for the first time
                    error_table_base_class = dwetl.Base.classes['dw_db_errors']
                    max_dw_error_id = self.error_writer.session.query(func.max(error_table_base_class.dw_error_id)).scalar()
                    if max_dw_error_id ==  None:
                        dw_error_id = 1
                    else:
                        dw_error_id = max_dw_error_id + 1

                    # create error row dictionary that will be added to the error table
                    #import pdb; pdb.set_trace()
                    error_row_dict = {
                        'dw_error_id': dw_error_id,
                        'dw_error_type': e.error_type,
                        'dw_error_text': error,
                        'dw_error_row': error_row,
                        'em_create_dw_prcsng_cycle_id': processed_row_dict['em_create_dw_prcsng_cycle_id'],
                        'em_create_dw_job_name': processed_row_dict['em_create_dw_job_name'],
                        'em_create_dw_job_version_no': processed_row_dict['em_create_dw_job_version_no'],
                        'em_create_user_id': processed_row_dict['em_create_user_id'],
                        'em_create_tmstmp': processed_row_dict['em_create_tmstmp'],
                        'em_create_dw_job_exectn_id': processed_row_dict['em_create_dw_job_exectn_id'],
                        'em_update_dw_prcsng_cycle_id': processed_row_dict['em_update_dw_prcsng_cycle_id'],
                        'em_update_dw_job_name': processed_row_dict['em_update_dw_job_name'],
                        'em_update_dw_job_version_no': processed_row_dict['em_update_dw_job_version_no'],
                        'em_update_user_id': processed_row_dict['em_update_user_id'],
                        'em_update_tmstmp': processed_row_dict['em_update_tmstmp'],
                        'em_update_dw_job_exectn_id': processed_row_dict['em_update_dw_job_exectn_id']
                    }

                    # write error to the error table
                    error_record = self.error_writer.write_row(error_row_dict)

                    # log error
                    self.logger.info(f'{e.error_type} found')
                    print(f'\n{e.error_type} found: {error}')
                    print(f'Problem row:\n{error_row}')



    def job_name(self):
        raise NotImplementedError

    def process_item(self, item):
        raise NotImplementedError
