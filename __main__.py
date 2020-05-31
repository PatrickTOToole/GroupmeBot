# -*- coding: UTF-8 -*-
"""
Created: April 2, 2019
Python 3.7
@author: Patrick O'Toole
@Version: 1.2
"""
import json
import time
import sys
import os
import threading
from libs import main_inits
from libs import main_util
from pathlib import Path

print("ChatBot  -  Python 3.7")

main_dir = Path(os.path.dirname(os.path.abspath(__file__)))
debug_log_dir = main_dir / "debug_logs"
console_log_dir = main_dir / "logs"
config_dir = main_dir / "resources" / "config.json"


main_inits.make_log_dir(debug_log_dir)
main_inits.make_log_dir(console_log_dir)

config = json.load(open(config_dir))

debug = int(config['debug'])
botID = config['bot id']
groupID = config['group id']
sleep_seconds = int(config["update"])
gm_access = config["groupme access code"]

if debug == 1:
    curr_log_dir = debug_log_dir
else:
    curr_log_dir = console_log_dir

curr_log_file = curr_log_dir / main_inits.make_log()
curr_log_file = open(curr_log_file, "a+")


# String Literals
post_link = "https://api.groupme.com/v3/bots/post"
message_link = 'https://api.groupme.com/v3/groups/' + groupID + '/messages'
start_msg = config["start message"]
start_time = time.time()
base_cmd_dir = main_dir / "base_commands"
custom_cmd_dir = main_dir / "custom_commands"

reg_list = main_inits.build_registry(base_cmd_dir, custom_cmd_dir)

full_commands = []
for num in range(len(reg_list)):
    name = reg_list[num]
    name = name.strip()
    if num < 1:
        full_commands.append(main_inits.command_start(main_dir, "base_commands", name))
    else:
        full_commands.append(main_inits.command_start(main_dir, "custom_commands", name))

# Startup Message
main_inits.start_msg(botID, start_msg, curr_log_file)
cmd_arr = []
for elt in full_commands:
    cmd_arr.append(elt[0])
prompts = "\n" + main_inits.prompts_start(cmd_arr)


# Main Thread Commands
def read_chat():
    global end_program
    global command_in
    global called_by_console
    while True:
        # Checks to see if any commands have been sent in the group by a group member and executes them
        curr_msg = main_util.get_msg_info(message_link, gm_access, 0, 'text')
        for cmd in cmd_arr:
            cmd_id = -1
            if curr_msg == cmd['prompt'] or command_in == cmd['prompt']:
                curr_resp = ""
                if command_in == cmd['prompt']:
                    with lock:
                        command_in = ""
                for x in range(len(cmd_arr)):
                    if cmd['name'] == cmd_arr[x]['name']:
                        cmd_id = x

                    if cmd_id == 0:
                        curr_resp = full_commands[0][1].run(prompts)
                    else:
                        curr_resp = full_commands[cmd_id][1].run()

                main_util.send_msg({'bot_id': botID, 'text': curr_resp})
                main_util.update_log("Command \"" + str(cmd['name']) + "\" was called", curr_log_file)
                main_util.update_log("\"" + curr_resp + "\" was returned\n", curr_log_file)

        # Puts thread to sleep
        time.sleep(sleep_seconds - ((time.time() - start_time) % sleep_seconds))


# Command Thread Code
def take_inputs():
    while True:
        global command_in
        command_in = input()


command_in = ""
end_program = 0
lock = threading.Lock()
called_by_console = "False"


# Creates thread
read_thread = threading.Thread(target=read_chat)
read_thread.daemon = True
read_thread.start()
console_thread = threading.Thread(target=take_inputs)
console_thread.daemon = True
console_thread.start()

# Loop after threads established
while True:
    if command_in == '!Quit':
        main_util.send_msg({'bot_id': botID, 'text': full_commands[1][1].run()})
        sys.exit(0)
    elif end_program == 1:
        sys.exit(0)
