#!/usr/bin/env python
from optparse import OptionParser
import sys
from fasta import *
from search import *

VERSION = '0.0.1'

def main(argv):
    """Simulates a PCR, outputs \"contigs\" """
    
    parser = OptionParser(description='pcrsim.py - Simulates PCR on a given input FASTA file using BLAST.', 
    usage = 'pcrsim.py -i infile -f forward_primer -r reverse_primer',
    version=VERSION)
    parser.add_option("-v", "--verbose", dest="verbose", default=False,
                    action="store_false", help="Print Debugging Information")
    parser.add_option("-i", "--infile", dest="filename",
                    help="Specify Input FASTA file", type="string")
    parser.add_option("-f", "--forward", dest="forward",
                    help="Specify forward primer (5' to 3')",
                    type="string")
    parser.add_option("-r", "--reverse", dest="reverse",
                    help="Specify reverse primer (5' to 3')",
                    type="string")
    parser.add_option("-n", "--notprimed", dest="notprimed",
                    help="Save not primed sequences to not_primed (optional)",
                    type="string")
                    
    (options, args) = parser.parse_args()
    
    if not (options.filename or options.forward or options.reverse):
        print >> sys.stderr, 'Usage:', parser.usage
        quit()
        
    if options.notprimed:
        hnotprimed = open(options.notprimed, 'w')

    with open(options.filename, 'r') as handle:
        records = Fasta(handle)
        for record in records:
            template = record.sequence()

            forward = Search.match(template, options.forward)
            reverse = Search.match(template, options.reverse)
        
            print forward.start, reverse.stop
                                
#            if rxn.product:
 #               print product
  #          else:
   #             if options.notprimed: print >> hnotprimed, record           
    
if __name__ == '__main__':
    try:
        main(sys.argv)
    except KeyboardInterrupt:
        print >> sys.stderr, 'User Exited!'
        quit()
