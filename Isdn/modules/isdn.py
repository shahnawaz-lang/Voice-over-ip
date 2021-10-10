from modules.util.helper import open_file
from collections import namedtuple
from modules.template import temp_data 

tmp1, tmp2, tmp3 = [*temp_data]

isdn_tinitial = namedtuple('isdn_tinitial', 'callref calling_number called_number')
isdn_tmgs = namedtuple('isdn_tmgs', 'date sig int prot trans msg pd callref')
isdn_tdial_peers = namedtuple('isdn_tdial_peers', 'ccapi_id calling_num called_num in_dial out_dial disconnect')

class isdn_ouput: 

    @staticmethod
    def output(call, isdn_mgs):
        print(f'----------------------------\n')
        print(f'calling number = {call.calling_num}, called number = {call.called_num}, Cause={call.disconnect}\n')
        print(f'Incoming dial-peer = {call.in_dial}, Outgoing dial-peer = {call.out_dial}\n')

        for c in isdn_mgs:
            print(f'{c.int}')              
            if c.trans == 'RX':
                print(f'PROIVDER ---({c.msg})--> ROUTER[{c.callref}]\n')
            elif c.trans == 'TX':
                print(f'PROIVDER <--({c.msg})--- ROUTER[{c.callref}]\n')
    
        
class isdn_parse():

    def __init__(self, text_file=None):
        
        with open(text_file) as file:
            self.text_file = file.read() 
            
        self._isdn_linitial = [isdn_tinitial(*t1) for t1 in tmp1.ParseText(self.text_file)]
        self._isdn_lmgs = [isdn_tmgs(*t2) for t2 in tmp2.ParseText(self.text_file)]
        self._isdn_ldial_peers = [isdn_tdial_peers(*t3) for t3 in tmp3.ParseText(self.text_file)]
               
    def parse_calls(self):
        callrefs = [c.callref for c in self._isdn_lmgs if c.msg == "SETUP"]
        calls, call_nums = [dict(), dict()]

        for mgs in self._isdn_linitial:
            for dp in self._isdn_ldial_peers:
                if (dp.calling_num == mgs.calling_number) and (dp.called_num == mgs.called_number):
                    self._call_nums[f'{mgs.callref}'] = dp

        for ref in range(len(callrefs)):
            calls[call_nums[callrefs[ref]] if (callrefs[ref] in call_nums) else None] = list(filter(lambda i: callrefs[ref][3:6] == i.callref[3:6], self._isdn_lmgs))
        return calls   

    def print_calls(self, search=False, calllingNum=None, calledNum=None, cause=None):
        for call, isdn_lst in self.parse_calls().items():
            if search: 
                if ((call.calling_num == calllingNum) & (call.called_num == calledNum)) or (call.disconnect == cause): 
                    isdn_ouput.output(call, isdn_lst)
            else:
                isdn_ouput.output(call, isdn_lst)
