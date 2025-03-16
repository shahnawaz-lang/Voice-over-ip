"""
  Template module:
    FSM templates for parsing ISDN and CCAPI messages
"""
import glob
import os.path
from typing import Generator
from io import TextIOWrapper
from pydantic import BaseModel, ConfigDict
from contextlib import contextmanager, ExitStack
import textfsm  # type: ignore


class TextFSMTemplates(BaseModel):
    """
    Represents the textfsm templates
    """
    calling_nums: textfsm.TextFSM
    ccapi: textfsm.TextFSM
    isdn: textfsm.TextFSM
    model_config = ConfigDict(arbitrary_types_allowed=True)


@contextmanager
def open_file(file_name: str) -> Generator[TextIOWrapper, None, None]:
    """
    Open a file and return a file object
    Args:
        file_name: str: The name of the file to open
    Returns:
        file: file object
    """
    file = open(file_name)
    try:
        yield file
    finally:
        file.close()


def load_fsm_templates() -> TextFSMTemplates:
    """
    Read the FSM templates from the template path.
    The template names are passed as a list of strings
    The templates include: `calling_nums`, `ccapi`, `isdn`
    Returns:
        data: list: A list of textfsm objects
    """
    with ExitStack() as stack:
        path = os.path.join(os.path.dirname(__file__), "templates")
        files = [stack.enter_context(open_file(file))
                 for file in glob.glob(f"{path}/*.template")]
        data = list(map(textfsm.TextFSM, files))
    return TextFSMTemplates(calling_nums=data[0], ccapi=data[1], isdn=data[2])
