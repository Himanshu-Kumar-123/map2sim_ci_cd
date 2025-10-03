import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from fwk.shared.variables_util import varc

class GoogleDriveUploadMethods:
    '''This class consist of methods that help in uploading data to Google drive'''
    
    @staticmethod
    def google_drive_uploader(source_path, parent_id, service_account_key_path):
        '''This function is used to upload selective data to Google drive'''
        
        try:
            # Load credentials from the provided service account key file
            credentials = service_account.Credentials.from_service_account_file(service_account_key_path, scopes=['https://www.googleapis.com/auth/drive'])

            # Create a Drive service instance
            service = build('drive', 'v3', credentials=credentials)

            def upload_file(parent_id, file_path):
                file_name = os.path.basename(file_path)
                file_metadata = {
                    'name': file_name,
                    'parents': [parent_id]
                }
                media = MediaFileUpload(file_path, resumable=True)
                file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
                print(f"File '{file_name}' uploaded successfully. File ID: {file['id']}")

            def upload_recursive(parent_id, local_path):
                for item in os.listdir(local_path):
                    item_path = os.path.join(local_path, item)
                    if os.path.isfile(item_path):
                        upload_file(parent_id, item_path)
                    elif os.path.isdir(item_path):
                        folder_name = item.lower()  # Convert folder name to lowercase for case-insensitive comparison
                        if folder_name in ['videos', 'raw_data_videos', 'pp_data_videos', 'raw_data', 'pp_data']:
                            print(f"Skipping upload for folder '{item}'")
                            continue  # Skip uploading this folder
                        folder_metadata = {
                            'name': item,
                            'parents': [parent_id],
                            'mimeType': 'application/vnd.google-apps.folder'
                        }
                        folder = service.files().create(body=folder_metadata, fields='id').execute()
                        print(f"Folder '{item}' created successfully. Folder ID: {folder['id']}")
                        if item in varc.google_ids:
                            varc.google_ids[item]["test_artifacts_id"]=folder['id']
                        elif item == 'freeze_issue_logs':
                            varc.google_ids["freeze_issue_logs"]=folder['id']
                        elif item == 'p0_iter_logs':
                            varc.google_ids["p0_iter_logs"]=folder['id']
                        upload_recursive(folder['id'], item_path)

            # Check if the provided path is a directory or a file
            if os.path.isdir(source_path):
                #folder_name = os.path.basename(source_path)
                folder_metadata = {
                    'name': varc.test_suite_name,
                    'parents': [parent_id],
                    'mimeType': 'application/vnd.google-apps.folder'
                }
                folder = service.files().create(body=folder_metadata, fields='id').execute()
                print(f"Folder '{varc.test_suite_name}' created successfully. Folder ID: {folder['id']}")
                upload_recursive(folder['id'], source_path)
            elif os.path.isfile(source_path):
                upload_file(parent_id, source_path)
            
        except Exception as e:
            print('\n')
            print(f"[DMF] : Something broke while uploading files to google drive")
            print('\n')
            print(f"An error occurred: {e}")
            status=f"{source_path} upload to google drive failed, exception I captured is {e}"
            varc.google_drive_verdict.append(status)

