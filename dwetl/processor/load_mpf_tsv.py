from dwetl.processor.processor import Processor
import datetime


class LoadMpfTsv(Processor):
    """
    Processor for creating the file equivalent tables from
    MPF TSV files.

    This processing step simply appends the job_info to the given
    item, and returns the resulting dictionary.
    """
    def __init__(self, reader, writer, job_info, logger, error_writer):
        super().__init__(reader, writer, job_info, logger, error_writer)

    def job_name(self):
        return 'LoadMpfTsv'

    @classmethod
    def usmai_mbr_lbry_cd(cls, lbry_entity_cd):
        """
        Given lbry_entity_cd returns usmai_mbr_lbry_cd.
        Raises ValueError if lbry_entity_cd is empty.
        Raises TypeError if lbry_entity_cd is None.
        """
        usmai_mbr_lbry_cd = lbry_entity_cd[0:2]
        if usmai_mbr_lbry_cd == '':
            raise ValueError
        return usmai_mbr_lbry_cd

    def process_item(self, item):
        # TODO: Not sure if we are using this usmai_mbr_lbry_cd or why we need it
        if 'lbry_entity_cd' in item:
            lbry_entity_cd = item['lbry_entity_cd']
            usmai_mbr_lbry_cd = LoadMpfTsv.usmai_mbr_lbry_cd(lbry_entity_cd)
            item['usmai_mbr_lbry_cd'] = usmai_mbr_lbry_cd
        item.update(self.job_info.as_dict('create'))
        item['em_create_dw_job_name'] = self.job_name()
        item['em_create_tmstmp'] = datetime.datetime.now()
        return item
