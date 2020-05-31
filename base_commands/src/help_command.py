from libs import command_util
meta = {
    "name": "Help",
    "prompt":"!Help"
    }
def run(prompts):
    return "Current available commands" + prompts
def get_meta():
    return meta

