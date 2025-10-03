# Standard library imports
import json

# Third-party imports
from tabulate import tabulate

# Local imports
from fwk.shared.variables_util import varc
from fwk.fwk_logger.fwk_logging import get_logger

logger = get_logger(__name__, varc.framework_logs_path)

class ReportingMethods():
    '''This class consist of all report file builder methods'''
    
    @staticmethod
    def report_creator():
        '''This function is used to create report files of different formats'''
        
        # Change report.txt name based on build or customized name in CI/CD
        with open(f"{varc.test_suite_path}/report.txt", "w", encoding='utf-8') as file:
            json.dump(varc.header_dict, file, indent=4)  # Write the dictionary as JSON to the file
            file.write('\n\n') # Add two newlines after the JSON content
                
        # Create report.json
        with open(f"{varc.test_suite_path}/report.json", "w", encoding='utf-8') as json_file:
            json.dump(varc.header_dict, json_file, indent=4)
        
    @staticmethod
    def report_updater(test_dict):
        '''This function is used to update report files
        Args:
            test_dict (dict): Test dictionary containing test information
        '''
        
        test_name = test_dict['updated_name']

        # Set verdict based on conditions
        current_verdict = test_dict['verdicts']['final-verdict']
        process_errors = test_dict['verdicts'].get('process-specific-errors', 'NA')
        
        # Normalize verdicts so reports show PASS/FAIL instead of engine enums
        # Map COMPLETED -> PASS, FAILED/RETRY -> FAIL. Preserve PASS/FAIL/SKIPPED as-is.
        normalized_verdict = current_verdict
        if current_verdict is None:
            # Determine based on errors if not already set
            if process_errors and process_errors != 'NA' and 'failed' in str(process_errors).lower():
                normalized_verdict = 'FAIL'
            else:
                normalized_verdict = 'PASS'
        elif current_verdict == 'COMPLETED':
            normalized_verdict = 'PASS'
        elif current_verdict in ('FAILED', 'RETRY'):
            normalized_verdict = 'FAIL'

        # Write back normalized verdict
        test_dict['verdicts']['final-verdict'] = normalized_verdict
        # If verdict is already set to FAIL, keep it as FAIL
        # (don't override FAIL with PASS)
            
        # Create formatted report dictionary with only required keys
        report_data = {
            "logs_errors": test_dict['verdicts'].get('logs_errors', 'NA'),
            # Use correct key from verdicts dict (hyphenated)
            "process_specific_errors": test_dict['verdicts'].get('process-specific-errors', 'NA'),
            "detailed_analysis_logs": test_dict.get('detailed_analysis', {}).get('logs'),
            "detailed_analysis_pytest_logs": test_dict.get('detailed_analysis', {}).get('pytest_logs'),
            "sharepoint_test_artifacts_id": test_dict.get('upload_storage', {}).get('share_point', {}).get('test_artifacts_id'),
        
            "launch_time": test_dict['verdicts'].get('launch-time'),
            "execution_time": test_dict['verdicts'].get('execution-time'),
            "final_verdict": test_dict['verdicts'].get('final-verdict'),
            "subtest_dict": test_dict.get('subtest_dict', {}),
            "name": test_dict['name'],
            "new_count": test_dict.get('new_count', 0),
            "commands_executed": test_dict.get('commands_executed', []),
            "execution_metrics": test_dict.get('execution_metrics', {}),
            "result_logs_analysis": test_dict.get('result_logs_analysis', {}),
        }

        #updation of report.json
        with open(f"{varc.test_suite_path}/report.json", "r", encoding='utf-8') as json_file:
            data = json.load(json_file)
            if "test" not in data:
                data['test']={}
            test_key = test_name
            data['test'][test_key]=report_data
        with open(f"{varc.test_suite_path}/report.json", "w", encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4)
        
        # Convert the dictionary to a list of lists
        value_table = []
        headers_list = list(test_dict['verdicts'].keys())
        table_headers = ["Test"] + headers_list
        values_list = [str(val) if val is not None else 'NA' for val in test_dict['verdicts'].values()]
        value_table.append([test_name] + values_list)
        
        # Generate the table in tabular format with lines after each row
        process_table = tabulate(
            value_table, 
            headers=table_headers, 
            tablefmt="rounded_grid", 
            maxcolwidths=[None,30,70,None,None]
        )
        # Print the table on the terminal
        print('\n',process_table)
        logger.debug(process_table)
        
        #Can add results of all analysis test done in below table
        if(test_dict['subtest_dict']):
            analysis_table=None
            table_headers = ['Subtest','Result']
            table_obj = []
            for key, value in test_dict['subtest_dict'].items():
                row = [key,value]
                table_obj.append(row)
            analysis_table = tabulate(table_obj, headers=table_headers,tablefmt="presto")
            print('\n',analysis_table)
            logger.debug(analysis_table)
        
        # Write all results to report.txt
        with open(f"{varc.test_suite_path}/report.txt", "a", encoding='utf-8') as file:
            # Write main test results
            file.write(f"{process_table}\n\n")

            # Write detailed analysis logs
            detailed_logs = test_dict.get('detailed_analysis', {})
            if detailed_logs.get('logs'):
                file.write("Lines in which logs issues occurred:\n\n")
                file.write("\n".join(detailed_logs['logs']) + "\n\n")

            # Write pytest logs for UI tests
            if detailed_logs.get('pytest_logs'):
                file.write("Lines in which pytest logs issues occurred:\n\n")
                file.write("\n".join(detailed_logs['pytest_logs']) + "\n\n")

            # Write ATF warnings
            if test_dict.get('dmf_warnings'):
                file.write("Warnings encountered while running DMF:\n\n")
                file.write("\n".join(test_dict['dmf_warnings']) + "\n\n")
                            
            # Write subtest results
            if(test_dict['subtest_dict']):
                file.write(f"{analysis_table}\n\n")
        
        # Very important to clear report_data as it may cause conflicts with next test execution
        report_data.clear()
         
    def txt_report_printer():
        '''This function is used to print report.txt file at end of testsuite run'''

        # Print sharepoint verdict
        with open(f"{varc.test_suite_path}/report.txt", "a", encoding='utf-8') as file:
            if varc.share_point_verdict:
                file.write("Sharepoint upload verdict:\n\n")
                file.write("\n".join(varc.share_point_verdict) + "\n\n")

        with open(f"{varc.test_suite_path}/report.txt", "r", encoding='utf-8') as file:
            file_content = file.read()
        logger.info(file_content)
        
    def slack_txt_report_printer():
        '''This function is used to append results to slack report.txt file at end of testsuite run'''
        
        output_lines=[]
        with open(f"{varc.test_suite_path}/report.json", "r", encoding='utf-8') as json_file:
            data = json.load(json_file)
        for test_key, test_data in data['test'].items():
            start_time = test_data["launch_time"]
            end_time = test_data["execution_time"]
            name = test_key
            verdict = test_data["final_verdict"]
            
            # Add the formatted lines
            output_lines.append(f"status_started|{name}|{start_time}")
            if verdict == "PASS":
                output_lines.append(f"status_passed|{name}|{end_time}")
            else:
                output_lines.append(f"status_failed|{name}|{end_time}")
            
        logger.info(f"slack_data={output_lines}")
        
        # append to txt file
        with open(varc.slack_report_path, "a", encoding='utf-8') as file:
            file.write("\n".join(output_lines))

        logger.info("[ATF_RUNNER] : Test results written to slack report.txt file")