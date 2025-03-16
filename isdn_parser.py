from modules.isdn import ISDNParser, ISDNOutput
from modules.template import read_fsm_templates
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='This module is used to parse isdn messages')
    parser.add_argument('-f', '--file', help='import a text file', type=str)
    parser.add_argument('-s', '--search', action='store_const', const='True', help='Enable the search flag')
    parser.add_argument('-cgn', '--calling', help='Calling Number', type=str)
    parser.add_argument('-cdn', '--called', help='Called Number', type=str)
    parser.add_argument('-ca', '--cause', help='Cause Code', type=str)
    args = parser.parse_args()

    text_fsm_templates = read_fsm_templates(template_names=["calling_nums", "ccapi", "isdn"],
                                            template_path="modules/templates")
    isdn_parser = ISDNParser(text_file=args.file,
                             text_fsm_templates=text_fsm_templates)
    calls = ISDNOutput(isdn_calls=isdn_parser.parse_calls())
    calls.print_calls(search=args.search,
                      calling_number=args.calling,
                      called_number=args.called,
                      cause=args.cause)
