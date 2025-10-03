from fwk.shared.variables_util import varc

class TestCleanMethods:
    '''This class consist of methods that help clean-up environment before next test starts'''
    
    @staticmethod
    def test_clean_up_util(test_dict,updated_toml_name):
        '''This function is also used to delete previous run data."
        '''
        
        # remove old results from dict so that next test starts fresh
        test_dict['detailed_analysis']["logs"] = None
        test_dict['verdicts']["process-specific-errors"] = "NA"
        test_dict['verdicts']["logs-errors"] = "NA"
        test_dict['subtest'] = {}
        varc.analysis_event = None
        test_dict['dmf_warnings'] = []
        test_dict['detailed_analysis']["pytest_logs"] = None
        