# Austin Davis-Richardson
# harekrishna@gmail.com

# blast.py
# This is used by pcr-sim to perform and parse BLAST alignments
# Requires NCBI Blast+ (specifically bl2seq)

# Does not really work in conjunction with fasta.py
# I guess I should make it take DNA objects rather than sequence strings.

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
    Create a reaction object:
    a = reaction('template','forward','reverse')
    '''
    def __init__(self, template, forward, reverse):
        '''Must provide template, forward primer and reverse primer as
        strings'''
        self.id = hex(randint(0,65535))[2:]
        self.template = template
        self.forward = forward
        self.reverse = reverse.translate(_complement)[::-1]
        self.start = { 'posn': 0, 'score': -1 }
        self.stop = { 'posn': 0, 'score': -1 }
        self.product = 'Nothing!'
        self.raw_output = ''
        
    def __repr__(self):
        '''Representation of objectw'''
        return '<RXN ID = %s>' % \
        (self.id)

    def _makefile(self, filename, data):
        ''' Creates a file for BLAST to use '''
        with open(filename, 'w') as output:
            output.write(data)
    
    def _remfiles(self):
        ''' Removes necessary files. '''
        rem = subprocess.Popen([delete,
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
    
        # For testing right now...  Fix this.  Make an exception object?
        
        try:
            output = open('blst.out.%s' % self.id, 'r').readlines()
            self.raw_output = output 
            print '(%s)' % self.raw_output[3].split()  
            output = output[3].split()
        except:
            return False # Bad BLAST!
        else:
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
        if results:
            self.start['posn'] = results['start']
            self.start['score'] = results['score']    
        
        # Create & BLAST reverse primer
        self._makefile('blst.que.%s' % self.id, self.reverse)
        results = self._blasty()
        if results:
            self.stop['posn'] = results['stop']
            self.stop['score'] = results['score']  
                 
        # Remove files
        self._remfiles()
        
        # Create PCR product
        self.product = self.template[self.start['posn']-1:self.stop['posn']]
        
        return self.product

def test():
    ''' A simple test
    returns 0 if everything went better than expected and 1 otherwise.'''
    
    forward = 'gatcatggctcagattgaacgctggcgg'
    reverse = 'gtgactgatcatcctctcagaccagtaa'
    
    go = reaction(forward + reverse, forward, reverse)
    go.react()
    
    if go.product == forward+reverse:
        return 0
    else:
        return 1


if __name__ == '__main__':
    test()
    
    
