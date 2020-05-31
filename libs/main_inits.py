import os
import json
import sys
from importlib import import_module
from libs.main_util import parse_time
from libs.main_util import send_msg
from libs.main_util import update_log


def command_start(main_dir, directory, name):
    name_json = name + ".json"
    meta = main_dir / directory / "meta" / name_json
    meta = json.load(open(meta))
    full_module_name = directory + ".src"
    module = import_module(full_module_name)
    output = [meta, module]
    return output


def build_registry(base_dir, custom_dir):
    registry = []
    for file in os.listdir(base_dir / "meta"):
        registry.append(file)
    for file in os.listdir(custom_dir / "meta"):
        registry.append(file)
    temp_reg = []
    for elt in registry:
        if not elt.__contains__("__"):
            if elt.__contains__(".json"):
                temp_reg.append(elt[:elt.index(".json")])
    registry = temp_reg
    return registry


def prompts_start(commands_arr):
    prompts = ""
    for command in commands_arr:
        prompts += "\n" + command['prompt']
    prompts = prompts[prompts.index('\n')+1:]
    return prompts


def make_log_dir(input_dir):
    if not os.path.exists(input_dir):
        os.makedirs(input_dir)


def start_msg(botid, init, current_log_file):
    send_msg({'bot_id': botid, 'text': init})
    update_log("\"" + init + "\" was sent", current_log_file)


def rewrite_log_files(folder, log_name):
    for file in os.listdir(folder):
        rename = folder + file
        pre, ext = os.path.splitext(rename)
        renamed = False
        if not (ext == ".log" or file == log_name):
            os.rename(rename, pre + ".log")
            renamed = True
        if not renamed:
            if os.stat(rename).st_size == 0:
                os.remove(rename)


def finalize_logs(log_dir, debug_dir, log_name):
    rewrite_log_files(log_dir / log_name)
    rewrite_log_files(debug_dir / log_name)


def make_log():
    output_log_name = str(parse_time())
    temp = (list(output_log_name))
    temp[10] = '_'
    temp[13] = '-'
    temp[16] = '-'
    output_log_name = ''.join(temp)
    output_log_name += ".txt"
    return output_log_name
