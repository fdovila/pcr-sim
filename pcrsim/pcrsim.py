#!/usr/bin/env python
from optparse import OptionParser
import sys
from fasta import *
from search import *

VERSION = '0.1'

def main():
    """Simulates a PCR, outputs \"contigs\" """
    parser = OptionParser(
     description = 'pcrsim.py - Simulates PCR on a given input FASTA.', 
     usage = 'pcrsim.py -i infile -f forward_primer -r reverse_primer -o output',
     version = VERSION)
    parser.add_option("-i", "--infile", dest="filename",
     help="Specify Input FASTA file", type="string")
    parser.add_option("-f", "--forward", dest="forward",
     help="Specify forward primer (5' to 3')", type="string")
    parser.add_option("-r", "--reverse", dest="reverse",
     help="Specify reverse primer (5' to 3')", type="string")
    parser.add_option("-o", "--output", dest="output", 
     help="Output contigs file", type="string")
                    
    (options, args) = parser.parse_args()
    
    if not (options.filename or options.forward or options.reverse):
        print >> sys.stderr, 'Usage:', parser.usage
        quit()

    # We can just recycle this object over and over again to save time!
    S = Search(match=1, miss_pen=1)

    forward = options.forward.upper()
    reverse = options.reverse.upper()

    if options.output:
        outfile = open(options.output, 'w')
    else:
        outfile = None
        
    with open(options.filename, 'r') as handle:
        records = Fasta(handle)
        for rec in records:
            so_f = S.find(subject=rec.seq, query=forward)
            so_r = S.find(query=reverse)
            # Do the numbers make sense?
            if so_f[1] < so_r[1]:
                print >> outfile, '>%s (%s, %s)\n%s' % \
                 (rec.head, so_f[1], so_r[1], rec.seq[so_f[1]:so_r[1]])
                print '%5s -> %-5s = %5s\t%s' % \
                 (so_f[1], so_r[1], len(rec.seq[so_f[1]:so_r[1]]), rec.head)
            
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print >> sys.stderr, 'User Exited!'
        quit()
