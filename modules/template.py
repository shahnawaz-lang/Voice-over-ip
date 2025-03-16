"""
  Template module:
    FSM templates for parsing ISDN and CCAPI messages
"""
from typing import List
from contextlib import contextmanager, ExitStack
import textfsm


@contextmanager
def open_file(file_name: str):
    file = open(file_name)
    try:
        yield file
    finally:
        file.close()


def read_fsm_templates(template_names: List[str], template_path: str) -> list:
    with ExitStack() as stack:
        files = [stack.enter_context(open_file(f"{template_path}/{file}.template")) for file in template_names]
        data = list(map(textfsm.TextFSM, files))
    return data
