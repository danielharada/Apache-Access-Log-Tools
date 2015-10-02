#accessLogProcessing module

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
        
        file_contents.append(line_dict.copy())    

    data_frame = pd.DataFrame(file_contents)
    f.close()
    return data_frame


def top_10_user_agents(data_frame):
    #columns wanted - User Agent, Count of Requests
    return data_frame['user_agent'].value_counts().head(10)

def top_10_ip_addresses(data_frame):
    #columns - IP Address, Count of Requests
    return data_frame['ip_address'].value_counts().head(10)

def top_10_request_URIs(data_frame):
    #columns - Request URIs, Count of Requests
    return data_frame['http_request_uri'].value_counts().head(10)

def top_10_referers(data_frame):
    #columns - Referer URI, Count of Requests
    return data_frame['referer'].value_counts().head(10)

def top_10_slowest_requests(data_frame):
    #columns - Request response time, request URI, HTTP status of request, response size, response content type, timestamp, IP address   
    return data_frame[['time_to_serve_request_milliseconds', 'http_request_uri', 'http_status', 'response_size_bytes', 'content_type', 'request_received_timestamp', 'ip_address']].sort(columns='time_to_serve_request_milliseconds', ascending=False).head(10)

def top_10_largest_response_sizes(data_frame):
    #columns - Response size, request URI, HTTP status of request, request response time, response content type, timestamp, IP address 
    return data_frame[['response_size_bytes', 'http_request_uri', 'http_status', 'time_to_serve_request_milliseconds', 'content_type', 'request_received_timestamp', 'ip_address']].sort(columns='response_size_bytes', ascending=False).head(10)

def counts_by_status_code(data_frame):
    #columns - status code, total counts
    return data_frame['http_status'].value_counts()



def print_aggregates(log_file):
    data_frame = read_apache_log_to_dataFrame(log_file)

    print('Top 10 User Agents' + '\n')
    print(top_10_user_agents(data_frame))
    print()
      
    print('Top 10 IP Addresses' + '\n')
    print(top_10_ip_addresses(data_frame))
    print()
          
    print('Top 10 Request URIs' + '\n')
    print(top_10_request_URIs(data_frame))
    print()

    print('Top 10 Referers' + '\n')
    print(top_10_referers(data_frame))
    print()
    
    print('Status code counts')
    print(counts_by_status_code(data_frame))
    print()
    
    print('Top 10 Slowest Requests')
    print(top_10_slowest_requests(data_frame))
    print()
    
    print('Top 10 Largest Response Sizes')
    print(top_10_largest_response_sizes(data_frame))    
          
    return
          



if __name__ == "__main__":
    path_to_file = '/Users/daniel.harada/Test-HTTPD-Access.log'
    test_data_frame = read_apache_log_to_dataFrame(path_to_file)
    print(test_data_frame[:10])