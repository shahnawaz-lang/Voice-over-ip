import modules.isdn as isdn
import argparse

parser = argparse.ArgumentParser(description='This module is used to parse isdn messages')
parser.add_argument('-f', '--file', help='import a text file', type=str)

args = parser.parse_args()
isdn.isdn_parse(args.file).ladder()





