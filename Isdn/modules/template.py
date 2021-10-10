from modules.util.helper import open_file
from contextlib import ExitStack
import textfsm

templates = ['calling_nums.template', 'isdn.template', 'ccapi.template']

with ExitStack() as stack:
    temps = [stack.enter_context(open_file(file)) for file in templates]
    temp_data = list(map(text.TextFSM, temps))

 

