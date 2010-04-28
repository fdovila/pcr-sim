from optparse import OptionParser
import sys
from fasta import *
from blast import *

VERSION = '0.0.1'

def main(argv):
    """Simulates a PCR, outputs \"contigs\" """
    
    parser = OptionParser(description='pcr-sim.py - Simulates PCR on a given input FASTA file using BLAST.', version=VERSION)
    parser.add_option("-v", "--verbose", dest="verbose", default=False,
                    action="store_false", help="Print Debugging Information")
    parser.add_option("-i", "--infile", dest="filename",
                    help="Specify Input FASTA file", metavar="INFILE")
    parser.add_option("-f", "--forward", dest="forward",
                    help="Specify forward primer (5' to 3')",
                    metavar="FORWARD")
    parser.add_option("-r", "--reverse", dest="reverse",
                    help="Specify reverse primer (5' to 3')",
                    metavar="REVERSE")
                    
    (options, args) = parser.parse_args()

    with open(options.filename, 'r') as handle:
        records = fasta(handle)
        for record in records:
            sequence = record.sequence()
            
           # print 'record = %s' % record.head
          
            rxn = reaction(sequence,
            options.forward,
            options.reverse)
            rxn.react()
                        
            product = dna(record.head, rxn.product)
            if rxn.product:
                print product
            
            
    
    
if __name__ == '__main__':
    try:
        main(sys.argv)
    except KeyboardInterrupt:
        print 'User Exited!'
        quit()
