#!/usr/bin/python

from annoreg import *
import argparse as arg

# I originally planned to offer other export options, but it turned out
# unnecessary and too much work in the end. I'll leave the code for it though in
# case I change my mind.
export_types = ['txt', 'text']

parser = arg.ArgumentParser(prog=__name__,
                            description = '''Create index from pdf
                                 annotations''')
parser.add_argument('doc')
parser.add_argument('-s', '--substract', action='store', default=0, type=int,
                    help='number of pages at the beginning of the document that'
                    ' are not included in the page numbering')
parser.add_argument('-S', '--sort', action='store_true', help='sort the index'
                    ' entries')
#parser.add_argument('-f', '--format', action='store', nargs='*',
#                    default='txt', choices=export_types)
parser.add_argument('-o', '--output', action='store', required=True, type=str,
                    help='name/location of the output file')
parser.add_argument('--version', action='version', version='0.1')

args = parser.parse_args()

form='txt'
if(form=='txt' or form=='text'):
    export_tsv(process_annotations(get_annotations(args.doc, args.substract),
                                   args.sort), args.output)
elif(form=='something else'):
    pass
