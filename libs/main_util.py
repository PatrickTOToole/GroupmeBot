import requests
import datetime


def get_msg_info(message, access_token, num_from_current, field):
    return read_msgs(message, access_token)[num_from_current][field]


def read_msgs(get_request_url, groupme_access_token):
    return requests.get(get_request_url, params={'token': groupme_access_token})


def send_msg(param):
    requests.post('https://api.groupme.com/v3/bots/post', params=param)


def parse_time():
    current_date_data = datetime.datetime.now()
    parsed_time = current_date_data.strftime("%Y-%m-%d %H:%M:%S")
    return parsed_time


def update_log(output_text, log_file):
    print(output_text)
    log_file.write("[" + parse_time() + "] " + output_text + "\n")
