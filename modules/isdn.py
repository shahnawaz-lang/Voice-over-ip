import datetime
from textfsm import TextFSM
from typing import Union, List, Any, Optional, Annotated
from pydantic import BaseModel, Field
from pydantic.types import NaiveDatetime

ISDNTextTemplateType = Annotated[list, Field(max_length=3)]


class ISDNBaseModel(BaseModel):

    @classmethod
    def from_list(cls, arg_list: List[str]):
        return cls()

class ISDNCallInfo(BaseModel):
    """
    Represents a peer-dial peer information
    """
    call_ref: Union[str, None] = None
    calling_num: Union[str, None] = None
    called_num: Union[str, None] = None


class ISDNMessage(BaseModel):
    """
    Represents a message from the provider
    """
    date: Union[str, NaiveDatetime, datetime.datetime, None] = None
    sig: Union[str, None] = None
    int: Union[str, None] = None
    protocol: Union[str, None] = None
    trans: Union[str, None] = None
    msg: Union[str, None] = None
    pd: Union[str, None] = None
    callref: Union[str, None] = None


class ISDNDialPeer(BaseModel):
    """
    Represents a dial-peer
    """
    ccapi_id: Union[str, None] = None
    calling_num: Union[str, None] = None
    called_num: Union[str, None] = None
    in_dial: Union[str, None] = None
    out_dial: Union[str, None] = None
    disconnect: Union[str, None] = None


class ISDNParser(BaseModel):
    text_file: Union[str, bytes]
    text_fsm_templates: ISDNTextTemplateType

    _isdn_messages: Union[List[ISDNMessage], None] = None
    _isdn_dial_peers: Union[List[ISDNDialPeer], None] = None
    _isdn_call_info: Union[List[ISDNCallInfo], None] = None

    def model_post_init(self, __context: Any) -> None:
        tmp1, tmp2, tmp3 = [*self.text_fsm_templates]
        with open(self.text_file, "r") as f:
            file = f.read()
        self._isdn_call_info = [ISDNCallInfo(**t1) for t1 in tmp1.ParseText(file)]
        self._isdn_messages = [ISDNMessage(**t2) for t2 in tmp2.ParseText(file)]
        self._isdn_dial_peers = [ISDNDialPeer(**t3) for t3 in tmp3.ParseText(file)]

    def parse_calls(self) -> dict:
        call_refs: list = [c.callref for c in self._isdn_messages if c.msg == "SETUP"]
        calls: dict = {}
        call_nums: dict = {}

        for mgs in self._isdn_call_info:
            for dp in self._isdn_dial_peers:
                # match numbers regardless of their translation
                if (dp.calling_num[-len(mgs.calling_number):] == mgs.calling_number) and (
                        dp.called_num[-len(mgs.calling_number):] == mgs.called_number):
                    call_nums[mgs.callref] = dp

        for ref in range(len(call_refs)):
            calls[call_nums[call_refs[ref]] if (call_refs[ref] in call_nums) else None] = list(
                filter(lambda i: call_refs[ref][3:6] == i.callref[3:6], self._isdn_lmgs))
        return calls

class ISDNOutput(BaseModel):
    isdn_calls: dict

    def _display(self, calls):
        print('----------------------------\n')
        print(f'calling number = {calls.calling_num}, called number = {calls.called_num}, Cause={calls.disconnect}\n')
        print(f'Incoming dial-peer = {calls.in_dial}, Outgoing dial-peer = {calls.out_dial}\n')
        for call in self.calls:
            print(call.int)
            if call.trans == 'RX':
                print(f'PROVIDER ---({call.msg})--> ROUTER[{call.callref}]\n')
            if call.trans == 'TX':
                print(f'PROVIDER <--({call.msg})--- ROUTER[{call.callref}]\n')

    def print_calls(self, search: Optional[bool] = False,
                    calling_number: Optional[str] = None,
                    called_number: Optional[str] = None,
                    cause: Optional[str] = None):
        for call, _ in self.isdn_calls.items():
            if search:
                if (((call.calling_num == calling_number)
                     and (call.called_num == called_number))
                        or (call.disconnect == cause)):
                    self._display(call)
            else:
                self._output(call)
