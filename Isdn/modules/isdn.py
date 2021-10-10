from collections import namedtuple
from contextlib import ExitStack
from modules.util.helper import open_file
import textfsm 
        
class isdn:

    def __init__(self):  
        self._isdn_templates = ['calling_nums.template', 'isdn.template', 'ccapi.template']
        self._isdn_tinitial = namedtuple('isdn_tinitial', 'callref calling_number called_number')
        self._isdn_tmgs = namedtuple('isdn_tmgs', 'date sig int prot trans msg pd callref')
        self._isdn_tdial_peers = namedtuple('isdn_tdial_peers', 'ccapi_id calling_num called_num in_dial out_dial disconnect')

    def output(self, call, isdn_lst):
        print(f'----------------------------\n')
        print(f'calling number = {call.calling_num}, called number = {call.called_num}, Cause={call.disconnect}\n')
        print(f'Incoming dial-peer = {call.in_dial}, Outgoing dial-peer = {call.out_dial}\n')

        for c in isdn_lst:
            print(f'{c.int}')              
            if c.trans == 'RX':
                print(f'PROIVDER ---({c.msg})--> ROUTER[{c.callref}]\n')
            elif c.trans == 'TX':
                print(f'PROIVDER <--({c.msg})--- ROUTER[{c.callref}]\n')
        
class isdn_parse(isdn):
    
    def __init__(self, text_file=None):
        super().__init__()
        self._isdn_linitial = []
        self._isdn_lmgs = []
        self._isdn_ldial_peers = []
        self._call_nums = {}
        
           
        with open(text_file) as file: 
            string = file.read()
        
        with ExitStack() as stack:
            temps = [stack.enter_context(open_file(f'modules/templates/{file}')) for file in self._isdn_templates]
            
            tmp1, tmp2, tmp3 = [*map(textfsm.TextFSM, temps)]
            
            self._isdn_linitial = [self._isdn_tinitial(*t1) for t1 in tmp1.ParseText(string)]
            self._isdn_lmgs = [self._isdn_tmgs(*t2) for t2 in tmp2.ParseText(string)]
            self._isdn_ldial_peers = [self._isdn_tdial_peers(*t3) for t3 in tmp3.ParseText(string)]

            for mgs in self._isdn_linitial:
                for dp in self._isdn_ldial_peers:
                    if (dp.calling_num == mgs.calling_number) and (dp.called_num == mgs.called_number):
                        self._call_nums[f'{mgs.callref}'] = dp
                
    def get_calls(self):
        callrefs = [c.callref for c in self._isdn_lmgs if c.msg == "SETUP"]
        calls = {}
        for ref in range(len(callrefs)):
            calls[self._call_nums[callrefs[ref]] if (callrefs[ref] in self._call_nums) else None] = list(filter(lambda i: callrefs[ref][3:6] == i.callref[3:6], self._isdn_lmgs))
        return calls   

    def ladder(self, search=False, calllingNum=None, calledNum=None, cause=None):
        for call, isdn_lst in self.get_calls().items():
            if search: 
                if ((call.calling_num == calllingNum) & (call.called_num == calledNum)) or (call.disconnect == cause): 
                    self.output(call, isdn_lst)
            else:
                self.output(call, isdn_lst)