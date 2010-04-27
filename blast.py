# Austin Davis-Richardson
# harekrishna@gmail.com

# blast.py
# This is used by pcr-sim to perform and parse BLAST alignments
# Requires NCBI Blast+ (specifically bl2seq)

# User editable variables:
bl2seq = '/usr/bin/bl2seq'      # Location of bl2seq
delete = 'rm'                   # Location of delete command
                                # (If I ever care to make this MS-Friendly)
import subprocess
from random import randint
import string

_complement = string.maketrans('GATCRYgatcry','CTAGYRctagyr')

class reaction:
    ''' Simulates a PCR reaction using BLAST.
    Try running using multiprocessing module! '''
    def __init__(self, template, forward, reverse):
        self.id = hex(randint(0,65535))[2:]
        self.template = template
        self.forward = forward
        self.reverse = reverse.translate(_complement)[::-1]
        self.start = { 'posn': 0, 'score': 0.0 }
        self.stop = { 'posn': 0, 'score': 0.0 }
        
    def __repr__(self):
        return '<RXN: %s..., %s... vs %s...>' % \
        (self.forward[0:5], self.reverse[0:5], self.template[0:20])

    def _makefile(self, filename, data):
        ''' Creates a file for BLAST to use '''
        with open(filename, 'w') as output:
            output.write(data)
    
    def _remfiles(self):
        ''' Removes necessary files. '''
        subprocess.Popen([delete,
        'blst.out.%s' % self.id,
        'blst.tem.%s' % self.id,
        'blst.que.%s' % self.id,
        ])
        
    def _blasty(self):
        ''' Performs a blast! '''
        
        # Runs the bl2seq command
        blast_process = subprocess.Popen([bl2seq,
        '-p', 'blastn',
        '-D', '1',
        '-i', 'blst.tem.%s' % self.id,
        '-j', 'blst.que.%s' % self.id,
        '-o', 'blst.out.%s' % self.id,
        ])
        blast_process.wait()
        
        output = open('blst.out.%s' % self.id, 'r').readlines()
        output = output[3].split()
        results = {
            'start': int(output[5]),
            'stop': int(output[6]),
            'score': float(output[9])
        }
        return results

    def react(self):
        ''' Performs the actual BLAST, returns region between hits. 
        I wish there was a way to do this without opening files. '''
        
        # Create template
        self._makefile('blst.tem.%s' % self.id, self.template)
        
        # Create & BLAST forward primer
        self._makefile('blst.que.%s' % self.id, self.forward)
        results = self._blasty()
        self.start['posn'] = results['start']
        self.start['score'] = results['score']    
        
        # Create & BLAST reverse primer
        self._makefile('blst.que.%s' % self.id, self.reverse)
        results = self._blasty()
        self.stop['posn'] = results['stop']
        self.stop['score'] = results['score']  
                 
        # Remove files
        self._remfiles()
        
        # Create PCR product
        self.product = self.template[self.start['posn']-1:self.stop['posn']-3]
        
        self.product

def test():
    print 'Testing!'
    go = reaction('agagtttgatcatggctcagattgaacgctggcggcaggcctaacacatgcaagtcgagcggatgacgggagcttgctccttgattcagcggcggacgggtgagtaatgcctaggaatctgcctggtagtgggggacaacgtttcgaaaggaacgctaataccgcatacgtcctacgggagaaagcaggggaccttcgggccttgcgctatcagatgagcctaggtcggattagctagttggtggggtaatggctcaccaaggcgacgatccgtaactggtctgagaggatgatcagtcacactggaactgagacacggtccagac','gatcatggctcagattgaacgctggcgg','gtgactgatcatcctctcagaccagt')
    go.react()
    
    if go.product == 'gatcatggctcagattgaacgctggcggcaggcctaacacatgcaagtcgagcggatgacgggagcttgctccttgattcagcggcggacgggtgagtaatgcctaggaatctgcctggtagtgggggacaacgtttcgaaaggaacgctaataccgcatacgtcctacgggagaaagcaggggaccttcgggccttgcgctatcagatgagcctaggtcggattagctagttggtggggtaatggctcaccaaggcgacgatccgtaactggtctgagaggatgatcagt':
        print 'Everything went better than expected!'
    else:
        print 'Some kind of error!'
        
    
if __name__ == '__main__':
    test()
    
    
