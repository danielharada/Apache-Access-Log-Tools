#accessLogProcessing module

import argparse
import pandas as pd
import re

def get_command_line_arguments():
    parser = argparse.ArgumentParser(description='Parse Jive\'s Apache Access logs, and print out aggregated data from them.')
    parser.add_argument('input_log_files', metavar='files', nargs='+', action = 'store', default = [],
                   help='List of Apache access log files to parse')
    return parser.parse_args()

def read_apache_log_to_dataframe(opened_file_to_read):
    #If file is there, returns a dataframe composed of the lines that successfully match the access_log_regex.  If file
    #    does not exist, returns 'FileNotFound'
    
    #Apache Log Format: "%{JiveClientIP}i %l %u %t \"%r\" %>s %b %T %k \"%{Referer}i\" \"%{User-Agent}i\" \"%{Content-Type}o\" 
    #                    %{JSESSIONID}C" common
    #This regex parses a log line into the above items, with %r being separated into the request method, request URI, and HTTP 
    #    version.  The Time to serve request claims to be in milliseconds, but I think for some versions of Jive this is
    #    not true.  Sometimes it will be in whole seconds.
    access_log_regex = r'(\S+) (\S+) (\S+) \[(\S+ \S+)\] "(\S+) (\S+) (\S+)" (\S+) (\S+) (\S+) (\S+) (".*?") (".*?") (".*?") (\S+)'
    compiled_regex = re.compile(access_log_regex)
    file_contents = []
    line_dict = {}
    
    for line in f:
        regex_match = compiled_regex.search(line)

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

        #AttributeError thrown when trying to assign matched groups if a match was not found on that line (i.e. match = None)
        except AttributeError:
            print('Attribute Error for:')
            print(line)
            pass

    data_frame = pd.DataFrame(file_contents)
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



def print_aggregates(data_frame):

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
    args = get_command_line_arguments()
    
    for file in args.input_log_files:
        try:
            with open(file) as f:
                print('File:  ' + file +'\n\n')
                data_frame = read_apache_log_to_dataframe(f)
                print_aggregates(data_frame)
        except FileNotFoundError:
            print('File not found:  ' + file +'\n')


