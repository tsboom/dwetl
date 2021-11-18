import unittest
from dwetl import specific_transform_functions



'''
specific_transform_functions.py tests
'''

class TestSpecificTransformFunctions(unittest.TestCase):

    def test_isbn_code_020(self):
        #test isbn_issn check function
        self.assertEqual(specific_transform_functions.isbn_code_020('020177091921X'),'020177091921X')
        self.assertEqual(specific_transform_functions.isbn_code_020('0021177091921X'),'')

    def test_isbn_code_022(self):
        #test isbn_issn check function
        self.assertEqual(specific_transform_functions.issn_code_022('022177091921X'),'022177091921X')
        self.assertEqual(specific_transform_functions.issn_code_022('0021177^^091921X'),'')

    def test_remove_ocm_ocn_on(self):
        self.assertEqual(specific_transform_functions.remove_ocm_ocn_on('ocn748578120'),'748578120')
        self.assertEqual(specific_transform_functions.remove_ocm_ocn_on('ocm00003739'),'00003739')
        self.assertEqual(specific_transform_functions.remove_ocm_ocn_on('on1038022607'),'1038022607')
        self.assertEqual(specific_transform_functions.remove_ocm_ocn_on('ocm^^nam^^2200241d1^45^0'),'^^nam^^2200241d1^45^0')
        self.assertEqual(specific_transform_functions.remove_ocm_ocn_on('ocn^^nam^^2200241d1^45^0'),'^^nam^^2200241d1^45^0')
        self.assertEqual(specific_transform_functions.remove_ocm_ocn_on('on^^nam^^2200241d1^45^0'),'^^nam^^2200241d1^45^0')



    def test_lookup_record_type(self):
        self.assertEqual(specific_transform_functions.lookup_record_type('^^^^^nam^^2200241d1^45^0'),'Language material')
        self.assertEqual(specific_transform_functions.lookup_record_type('^^^^^ncm^^2200241d1^45^0'),'Notated music')
        self.assertEqual(specific_transform_functions.lookup_record_type('^^^^^ndm^^2200241d1^45^0'),'Manuscript notated music')
        self.assertEqual(specific_transform_functions.lookup_record_type('^^^^^nem^^2200241d1^45^0'),'Cartographic material')
        self.assertEqual(specific_transform_functions.lookup_record_type('^^^^^nfm^^2200241d1^45^0'),'Manuscript cartographic material')
        self.assertEqual(specific_transform_functions.lookup_record_type('^^^^^ngm^^2200241d1^45^0'),'Projected medium')
        self.assertEqual(specific_transform_functions.lookup_record_type('^^^^^nim^^2200241d1^45^0'),'Nonmusical sound recording')
        self.assertEqual(specific_transform_functions.lookup_record_type('^^^^^njm^^2200241d1^45^0'),'Musical sound recording')
        self.assertEqual(specific_transform_functions.lookup_record_type('^^^^^nkm^^2200241d1^45^0'),'Two-dimensional nonprojectable graphic')
        self.assertEqual(specific_transform_functions.lookup_record_type('^^^^^nmm^^2200241d1^45^0'),'Computer file')
        self.assertEqual(specific_transform_functions.lookup_record_type('^^^^^nom^^2200241d1^45^0'),'Kit')
        self.assertEqual(specific_transform_functions.lookup_record_type('^^^^^npm^^2200241d1^45^0'),'Mixed materials')
        self.assertEqual(specific_transform_functions.lookup_record_type('^^^^^nrm^^2200241d1^45^0'),'Three-dimensional artifact or naturally occurring object')
        self.assertEqual(specific_transform_functions.lookup_record_type('^^^^^ntm^^2200241d1^45^0'),'Manuscript language material')
    #testing lookup_tables/bibliographic_level.csv for bib rec z13u
    def test_lookup_bibliographic_level(self):
        self.assertEqual(specific_transform_functions.lookup_bibliographic_level('^^^^^nam^^2200241d1^45^0'),'Monograph/Item')
        self.assertEqual(specific_transform_functions.lookup_bibliographic_level('^^^^^naa^^2200241d1^45^0'),'Monographic component part')
        self.assertEqual(specific_transform_functions.lookup_bibliographic_level('^^^^^nab^^2200241d1^45^0'),'Serial component part')
        self.assertEqual(specific_transform_functions.lookup_bibliographic_level('^^^^^nac^^2200241d1^45^0'),'Collection')
        self.assertEqual(specific_transform_functions.lookup_bibliographic_level('^^^^^nad^^2200241d1^45^0'),'Subunit')
        self.assertEqual(specific_transform_functions.lookup_bibliographic_level('^^^^^nai^^2200241d1^45^0'),'Integrating resource')
        self.assertEqual(specific_transform_functions.lookup_bibliographic_level('^^^^^nas^^2200241d1^45^0'),'Serial')
    #testing lookup_tables/encoding_level.csv for bib rec z13u
    def test_lookup_encoding_level(self):
        self.assertEqual(specific_transform_functions.lookup_encoding_level('^^^^^nam^^2200241^1^45^0'),'Full-level by authorized national bibliographic agencies and libraries participating in PCC (BIBCO and CONSER).')
        self.assertEqual(specific_transform_functions.lookup_encoding_level('^^^^^nam^^220024111^45^0'),'Full-level material not examined.')
        self.assertEqual(specific_transform_functions.lookup_encoding_level('^^^^^nam^^220024121^45^0'),'Less-than-full level material not examined.')
        self.assertEqual(specific_transform_functions.lookup_encoding_level('^^^^^nam^^220024131^45^0'),'Abbreviated level.')
        self.assertEqual(specific_transform_functions.lookup_encoding_level('^^^^^nam^^220024141^45^0'),'Core-level.')
        self.assertEqual(specific_transform_functions.lookup_encoding_level('^^^^^nam^^220024151^45^0'),'Partial (preliminary) level.')
        self.assertEqual(specific_transform_functions.lookup_encoding_level('^^^^^nam^^220024171^45^0'),'Minimal-level.')
        self.assertEqual(specific_transform_functions.lookup_encoding_level('^^^^^nam^^220024181^45^0'),'Prepublication level.')
        self.assertEqual(specific_transform_functions.lookup_encoding_level('^^^^^nam^^2200241I1^45^0'),'Full-level input by OCLC participants.' )
        self.assertEqual(specific_transform_functions.lookup_encoding_level('^^^^^nam^^2200241K1^45^0'),'Minimal-level input by OCLC participants.')
        self.assertEqual(specific_transform_functions.lookup_encoding_level('^^^^^nam^^2200241L1^45^0'),'Added from a batch process.')
        self.assertEqual(specific_transform_functions.lookup_encoding_level('^^^^^nam^^2200241M1^45^0'),'Added from a batch process.')
        self.assertEqual(specific_transform_functions.lookup_encoding_level('^^^^^nam^^2200241J1^45^0'),'Deleted record.')
        self.assertEqual(specific_transform_functions.lookup_encoding_level('^^^^^nam^^2200241u1^45^0'),'Unknown')
        self.assertEqual(specific_transform_functions.lookup_encoding_level('^^^^^nam^^2200241z1^45^0'),'Not applicable')

    def test_is_suppressed(self):
        #test to confirm is_suppressed works with upper, lower, mixed, and fail
        self.assertEqual(specific_transform_functions.is_suppressed("SUPPRESSED"),'Y')
        self.assertEqual(specific_transform_functions.is_suppressed("ezSUPPRESSED1"), 'Y')
        self.assertEqual(specific_transform_functions.is_suppressed("nimaSUPP"),'N')

    def test_is_acq_created(self):
        #test to confirm is_acq_created works with upper, lower, mixed, and fail
        self.assertEqual(specific_transform_functions.is_acq_created("ACQ-CREATED" ),'Y')
        self.assertEqual(specific_transform_functions.is_acq_created("ACQ-CReATED"),'Y')
        self.assertEqual(specific_transform_functions.is_acq_created("1ACQ-CREATEDt56ACQ-CREATED"),'Y')
        self.assertEqual(specific_transform_functions.is_acq_created("ACQ-CREATE"),'N')

    def test_is_circ_created(self):
        #test to confirm is_circ_created works with upper, lower, mixed, and fail
        self.assertEqual(specific_transform_functions.is_circ_created("CIRC-CREATED"),'Y')
        self.assertEqual(specific_transform_functions.is_circ_created("r5CIRC-CREATEDu8tb"),'Y')
        self.assertEqual(specific_transform_functions.is_circ_created("CIRC-CREAED"),'N')

    def test_is_provisional(self):
        #test to confirm is_provisional works with upper, lower, mixed, and fail
        self.assertEqual(specific_transform_functions.is_provisional("PROVISIONAL"), 'Y')
        self.assertEqual(specific_transform_functions.is_provisional(" PROVISIONAL  i"), 'Y')
        self.assertEqual(specific_transform_functions.is_provisional("546PROVISIONAgh"), 'N')



if __name__ == '__main__':
    unittest.main()
