from modules.util.helper import open_file
from contextlib import ExitStack
import textfsm

templates = ['calling_nums.template', 'isdn.template', 'ccapi.template']

def get_templates():
  with ExitStack() as stack:
    temps = map(textfsm.TextFSM, [stack.enter_context(open_file(file)) for file in templates])
  return temps

