import datetime
import logging
from typing import Union, List, Any, Optional
from pydantic import BaseModel, Field
from pydantic.types import NaiveDatetime
from .template import load_fsm_templates
from isdn_parser.config import config

logger = logging.getLogger(config.get("logging", "LoggerName"))


class ISDNCallInfo(BaseModel):
    """
    Represents a peer-dial peer information
    """
    call_ref: str = Field(default=None)
    calling_num: str = Field(default=None)
    called_num: str = Field(default=None)


class ISDNMessage(BaseModel):
    """
    Represents a message from the provider
    """
    date: Union[str, NaiveDatetime, datetime.datetime]
    sig: str
    int: str
    protocol: str
    trans: str
    msg: str
    pd: str
    call_ref: str


class ISDNDialPeer(BaseModel):
    """
    Represents a dial-peer
    """
    ccapi_id: str
    calling_num: str
    called_num: str
    in_dial: str
    out_dial: str
    disconnect: str


class ISDNParser(BaseModel):
    text_file: Union[str, bytes] = Field(default=None)
    isdn_messages: List[ISDNMessage] = Field(default=None)
    isdn_dial_peers: List[ISDNDialPeer] = Field(default=None)
    isdn_call_info: List[ISDNCallInfo] = Field(default=None)

    def model_post_init(self, __context: Any) -> None:
        logger.debug("Loading ISDN messages, dial peers and call info")
        text_fsm_templates = load_fsm_templates()
        with open(self.text_file, "r") as f:
            file = f.read()
        self.isdn_call_info = [ISDNCallInfo(**t1) for t1 in text_fsm_templates.isdn.ParseText(file)]
        self.isdn_messages = [ISDNMessage(**t2) for t2 in text_fsm_templates.calling_nums.ParseText(file)]
        self.isdn_dial_peers = [ISDNDialPeer(**t3) for t3 in text_fsm_templates.ccapi.ParseText(file)]
        logger.debug("ISDN messages, dial peers and call info loaded")

    def parse_calls(self) -> dict:
        logger.debug("Parsing ISDN calls")
        call_refs: list = [c.callref for c in self.isdn_messages if c.msg == "SETUP"]
        calls: dict = {}
        call_nums: dict = {}

        for message in self.isdn_call_info:
            for dial_peer in self.isdn_dial_peers:
                # match numbers regardless of their translation
                if (dial_peer.calling_num[-len(message.calling_num):] == message.calling_num) and (
                        dial_peer.called_num[-len(message.calling_num):] == message.called_num):
                    call_nums[message.call_ref] = dial_peer

        for ref in range(len(call_refs)):
            calls[call_nums[call_refs[ref]] if (call_refs[ref] in call_nums) else None] = list(
                filter(lambda msg: call_refs[ref][3:6] == msg.call_ref[3:6], self.isdn_messages))
        return calls


class ISDNOutput(BaseModel):
    isdn_calls: dict

    @staticmethod
    def display(calls) -> None:
        logger.info("----------------------------\n")
        logger.info("calling number = %s, called number = %s, Cause=%s\n",
                    calls.calling_num, calls.called_num, calls.disconnect)
        logger.info("Incoming dial-peer = %s, Outgoing dial-peer = %s\n",
                    calls.in_dial, calls.out_dial)
        for call in calls:
            logger.info("Date = %s, Sig = %s, Int = %s\n", call.date, call.sig, call.int)
            if call.trans == 'RX':
                logger.info("PROVIDER ---(%s)--> ROUTER[%s]\n", call.msg, call.callref)
            if call.trans == 'TX':
                logger.info("ROUTER[%s] ---(%s)--> PROVIDER\n", call.callref, call.msg)

    def print_calls(self, search: Optional[bool] = False,
                    calling_number: Optional[str] = None,
                    called_number: Optional[str] = None,
                    cause: Optional[str] = None):
        for call, _ in self.isdn_calls.items():
            if search:
                logger.debug("Searching for calls with calling number = %s, called number = %s, Cause=%s\n", )
                if (((call.calling_num == calling_number)
                     and (call.called_num == called_number))
                        or (call.disconnect == cause)):
                    ISDNOutput.display(call)
            else:
                ISDNOutput.display(call)
