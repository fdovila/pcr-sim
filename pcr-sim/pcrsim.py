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
    parser.add_option("-i", "--infile", dest="filename",
        help="Specify Input FASTA file", type="string")
    parser.add_option("-f", "--forward", dest="forward",
        help="Specify forward primer (5' to 3')",
        type="string")
    parser.add_option("-r", "--reverse", dest="reverse",
        help="Specify reverse primer (5' to 3')",
        type="string")
                    
    (options, args) = parser.parse_args()
    
    if not (options.filename or options.forward or options.reverse):
        print >> sys.stderr, 'Usage:', parser.usage
        quit()

    # We can just recycle this object over and over again to save time!
    S = Search(match=1, miss_pen=1)

    forward = options.forward.upper()
    reverse = options.reverse.upper()

    with open(options.filename, 'r') as handle:
        records = Fasta(handle)
        for rec in records:
            so_f = S.find(subject=rec.seq, query=forward)
            S.scores.sort(key=lambda x: x[0])
            
            # Let's try printing all configurations!
            print S.alignments
            
            so_r = S.find(query=reverse)
            #print S.alignments
            print '%5s -> %-5s = %5s' % \
                (so_f[1], so_r[1], len(rec.seq[so_f[1]:so_r[1]]))
            
if __name__ == '__main__':
    try:
        main(sys.argv)
    except KeyboardInterrupt:
        print >> sys.stderr, 'User Exited!'
        quit()
