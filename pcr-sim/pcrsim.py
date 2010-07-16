#!/usr/bin/env python
from optparse import OptionParser
import sys
from fasta import *
from search import *

VERSION = '0.0.1'

def main(argv):
    """Simulates a PCR, outputs \"contigs\" """
    
    parser = OptionParser(
        description='pcrsim.py - Simulates PCR on a given input FASTA.', 
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

    # We can just recycle this object over and over again to save time!
    S = Search(gc_score=2, at_score=1, miss_penn=1)

    forward = options.forward.upper()
    reverse = Dna('r', options.reverse.upper()).revcomp

    with open(options.filename, 'r') as handle:
        records = Fasta(handle)
        for i, rec in enumerate(records):
            so_f = S.find(subject=rec.seq, query=forward)
            S.scores.sort(key=lambda x: x[0])
            
            # Let's try printing all configurations!
            print S.alignments          
            
            so_r = S.find(query=reverse)
            print S.alignments
            print '%5s-> <-%-5s/%5s\n%s' % \
                (so_f[1], so_r[1], len(rec.seq), '-'*25)

            
if __name__ == '__main__':
    try:
        main(sys.argv)
    except KeyboardInterrupt:
        print >> sys.stderr, 'User Exited!'
        quit()
