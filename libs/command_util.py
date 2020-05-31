from libs import main_util
import os
import json
from pathlib import Path


CONFIG_DIRECTORY = Path(os.path.normpath(os.getcwd() + os.sep + os.pardir))
CONFIG_DIRECTORY = CONFIG_DIRECTORY / "groupme_chatbot" / "resources" / "config.json"
config = json.load(open(CONFIG_DIRECTORY))
groupID = config['group id']
groupme_user_access_token = config["groupme access code"]
MESSAGE_LINK = 'https://api.groupme.com/v3/groups/' + groupID + '/messages'


def get_message_info(num_from_current, field):
    return main_util.read_msgs(MESSAGE_LINK, groupme_user_access_token)[num_from_current][field]
def get_all_message_info():
    return main_util.read_msgs(MESSAGE_LINK, groupme_user_access_token)
