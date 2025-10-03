import json
from generic_utils.googledrive_upload_util import GoogleDriveUploadMethods
from fwk.shared.variables_util import varc

class UploadMethods:
    '''This class consist of methods that help prepare for cloud drive upload activities'''
                
    @staticmethod
    def google_drive_upload_caller():
        '''This function is used to call google drive upload class method'''
        
        #hardcoded secrets file
        service_account_key_path=f"{varc.cwd}/dependencies/secrets/google_drive_client_secrets.json"                
        source_path=varc.test_suite_path
        #hardcored folder ID 
        folder_id="1opQIN8Rh2OB3FV76NfBfMkw1rIS3xMJd"
        GoogleDriveUploadMethods.google_drive_uploader(source_path,folder_id,service_account_key_path)
            
    @staticmethod
    def one_drive_upload_caller():
        '''This function is used to call one drive upload class method'''
        
        #need to return these for kibana support
        headers=None
        GRAPH_API_ENDPONT=None
        testsuite_id=None
                    
        return headers,GRAPH_API_ENDPONT,testsuite_id
    
    @staticmethod
    def sharepoint_upload_caller():
        '''This function is used to call sharepoint upload class method'''
        
        GRAPH_API_ENDPONT=None
        testsuite_id=None
                    
        return GRAPH_API_ENDPONT,testsuite_id
        
    @staticmethod
    def kibana_support_caller(GRAPH_API_ENDPONT,testsuite_id):
        '''This function is used to call class that helps update data of kibana'''
        
        pass
                
                
                