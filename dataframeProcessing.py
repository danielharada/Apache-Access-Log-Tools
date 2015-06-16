#dataframeProcessing module

import pandas as pd
import re


def read_apache_log_to_dataFrame(log_file_to_read):
    
    f = open(log_file_to_read)
    file_contents = []
    line_dict = {}
    column_names = ['ip_address', 'remote_username', 'remote_user', 'request_received_timestamp', 'http_request_method',
                'http_request_uri', 'http_request_version', 'http_status', 'response_size_bytes',
                'time_to_serve_request_milliseconds', 'keep_alive_requests', 'referer', 'user_agent', 'content_type',
                'jsession_id']
    access_log_regex = r'(\S+) (\S+) (\S+) \[(\S+ \S+)\] "(\S+) (\S+) (\S+)" (\S+) (\S+) (\S+) (\S+) (".*?")\
     (".*?") (".*?") (\S+)'

    for line in f:

        regex_match = re.search(access_log_regex, line)

        try:
            line_dict['ip_address'] = regex_match.group(1)
            line_dict['remote_username'] = regex_match.group(2)
            line_dict['remote_user'] = regex_match.group(3)
            line_dict['request_received_timestamp'] = regex_match.group(4)
            line_dict['http_request_method'] = regex_match.group(5)
            line_dict['http_request_uri'] = regex_match.group(6)
            line_dict['http_request_version'] = regex_match.group(7)
            line_dict['http_status'] = regex_match.group(8)
            line_dict['response_size_bytes'] = regex_match.group(9)
            line_dict['time_to_serve_request_milliseconds'] = regex_match.group(10)
            line_dict['keep_alive_requests'] = regex_match.group(11)
            line_dict['referer'] = regex_match.group(12)
            line_dict['user_agent'] = regex_match.group(13)
            line_dict['content_type'] = regex_match.group(14)
            line_dict['jsession_id'] = regex_match.group(15)
            
            file_contents.append(line_dict.copy())
        except AttributeError:
            #AttributeError raised when nothing matches the regex.
            #I have cases currently where I expect that to happen
            #and I just want them skipped.
            #Insert error handling here if needed
            pass

    data_frame = pd.DataFrame(file_contents)
    f.close()
    return data_frame


def drop_dataframe_lines(data_frame, search_item, field_to_search, matching_location='anywhere', drop_if='matched'):
    
    #  Make sure this method does not modify data_frame in place.  Create copy and modify that! 
    
    
    location_options={'anywhere':r'{}', 'start_of_field':r'^{}', 'end_of_field':r'{}$'}
    try:
        regex = location_options[matching_location].format(search_item)
    except KeyError:
        #Print something useful so you know what happened
        
    #more stuff here!

