from Isdn.modules.isdn import isdn_parse
import modules.isdn as isdn
import argparse

parser = argparse.ArgumentParser(description='This module is used to parse isdn messages')
parser.add_argument('-f', '--file', help='import a text file', type=str)
parser.add_argument('-s', '--search', action='store_const', const='True', help='Enable the search flag')
parser.add_argument('-cgn', '--calling', help='Calling Number', type=str)
parser.add_argument('-cdn', '--called', help='Called Number', type=str)
parser.add_argument('-ca', '--cause', help='Cause Code', type=str)
args = parser.parse_args()

calls = isdn.isdn_parse(args.file)
calls.print_calls(search=args.search, calllingNum=args.calling, calledNum=args.called, cause=args.cause)





