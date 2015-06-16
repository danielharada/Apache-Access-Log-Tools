#dataframeProcessing module

import pandas as pd
import re


def read_apache_log_to_dataFrame(log_file_to_read):
    file_contents = []
    access_log_regex = r'(?P<ip_address>\S+) (?P<remote_username>\S+) (?P<remote_user>\S+) \[(?P<request_received_timestamp>\S+ \S+)\] "(?P<http_request_method>\S+) (?P<http_request_uri>\S+) (?P<http_request_version>\S+)" (?P<http_status>\S+) (?P<response_size_bytes>\S+) (?P<time_to_serve_request_milliseconds>\S+) (?P<keep_alive_requests>\S+) (?P<referer>".*?") (?P<user_agent>".*?") (?P<content_type>".*?") (?P<jsession_id>\S+)'  #need to add nice line breaks
    
    compiled_regex = re.compile(access_log_regex)
    
    f = open(log_file_to_read)
    for line in f:
 
        try:
            regex_match = compiled_regex.search(line)
            line_dict = regex_match.groupdict()
            file_contents.append(line_dict.copy())
        except AttributeError:
            #AttributeError raised when nothing matches the regex and try to assign in dict.
            #I have cases currently where I expect that to happen
            #and I just want them skipped.
            #Insert error handling here if needed
            pass
            

    data_frame = pd.DataFrame(file_contents)
    f.close()
    return data_frame


def get_top_n_from_field(data_frame, field, n):
    try:        
        return data_frame[field].value_counts()[:n]
    except AttributeError:
        print('The field "{}" did not exist in the dataframe'.format(field))
        return None    #Need to figure out something better to do here.  Pass? return an empty Series?

def drop_dataframe_lines(data_frame, search_item, field_to_search, matching_location='anywhere', drop_if='matched'):
    
    #  Make sure this method does not modify data_frame in place.  Create copy and modify that! 
    
    
    location_options={'anywhere':r'{}', 'start_of_field':r'^{}', 'end_of_field':r'{}$'}
    try:
        regex = location_options[matching_location].format(search_item)
    except KeyError:
        #Print something useful so you know what happened
        pass  #remove this when exception behavior defined
    #more stuff here!
    pass


if __name__ == "__main__":
    path_to_file = '/Users/daniel.harada/Test-HTTPD-Access.log'
    test_data_frame = read_apache_log_to_dataFrame(path_to_file)
    print(test_data_frame[:10])
    print(get_top_n_from_field(test_data_frame, 'ip_address', 10)) 