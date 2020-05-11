 import datetime
 import os
 import sys
 import pdb
 from dwetl.job_info import JobInfoFactory, JobInfo
 from dwetl.reader.ezproxy_reader import EzproxyReader
 from dwetl.writer.sql_alchemy_writer import SqlAlchemyWriter
 
 with dwetl.database_session() as session:
     reader = TsvFileReader(file_path)
     # writer = PrintWriter()
     writer = SqlAlchemyWriter(session, dwetl.Base.classes[table])
     processor = LoadAlephTsv(reader, writer, job_info, logger)
     processor.execute()



'''
main function for running script from the command line
'''
if __name__=='__main__':
    arguments = sys.argv

    # if len(arguments) < 2 or len(arguments) > 3:
    #     print('Usage: ')
    #     print('\tload_stage_1.py [prcsng_cycle_id] [data_directory] ')
    #     sys.exit(1)
    # 
    # prcsng_cycle_id = arguments[1]
    # input_directory = os.path.dirname(os.path.realpath(__file__))
    # today = datetime.datetime.now().strftime('%Y%m%d')
    # # if 2nd argument isn't provided use today as data directory
    # data_directory = os.path.join(input_directory,'data', today)
    # 
    # # data directory can be specified as 2nd argument
    # if len(arguments) == 3:
    #     data_directory = arguments[2]
    # 
    # job_info = JobInfoFactory.create_from_prcsng_cycle_id(prcsng_cycle_id)
    # load_stage_1(job_info, data_directory)
