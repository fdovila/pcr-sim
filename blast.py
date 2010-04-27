# Austin Davis-Richardson
# harekrishna@gmail.com

# blast.py
# This is used by pcr-sim to perform and parse blasts
# Requires NCBI Blast+ (specifically bl2seq)


import subprocess
from random import randint
import string
bl2seq = '/usr/bin/bl2seq'
delete = 'rm'
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

    def _makefiles(self):
        ''' Creates necessary files '''
        with open('blst.tem.%s' % self.id, 'w') as htemplate:
            htemplate.write(self.template)
        
        with open('blst.for.%s' % self.id, 'w') as hforward:
            hforward.write(self.forward)
        
        with open('blst.rev.%s' % self.id, 'w') as hreverse:
            hreverse.write(self.reverse)
    
    def _remfiles(self):
        ''' Removes necessary files. '''
        subprocess.Popen([delete,
        'blst.out.%s' % self.id,
        'blst.tem.%s' % self.id,
        'blst.rev.%s' % self.id,
        'blst.for.%s' % self.id
        ])
        
    def react(self):
        ''' Performs the actual BLAST, returns region between hits. 
        I wish there was a way to do this without opening files. '''
        
        self._makefiles()
        
        pblast = subprocess.Popen([bl2seq,
        '-p', 'blastn',
        '-D', '1',
        '-i', 'blst.tem.%s' % self.id,
        '-j', 'blst.for.%s' % self.id,
        '-o', 'blst.out.%s' % self.id,
        ])
        pblast.wait()

        output = open('blst.out.%s' % self.id, 'r').readlines()
        output = output[3].split()
        
        self.start['posn'] = int(output[5])
        self.start['score'] = float(output[9])
                
        pblast = subprocess.Popen([bl2seq,
        '-p', 'blastn',
        '-D', '1',
        '-i', 'blst.tem.%s' % self.id,
        '-j', 'blst.rev.%s' % self.id,
        '-o', 'blst.out.%s' % self.id,
        ])
        
        pblast.wait()

        output = open('blst.out.%s' % self.id, 'r').readlines()
        output = output[3].split()
        
        self.stop['posn'] = int(output[6])
        self.stop['score'] = float(output[9])
                
        self._remfiles()
        
        self.product = self.template[self.start['posn']-1:self.stop['posn']-3]
        

        
def test():
    print 'Testing!'
    go = reaction('agagtttgatcatggctcagattgaacgctggcggcaggcctaacacatgcaagtcgagcggatgacgggagcttgctccttgattcagcggcggacgggtgagtaatgcctaggaatctgcctggtagtgggggacaacgtttcgaaaggaacgctaataccgcatacgtcctacgggagaaagcaggggaccttcgggccttgcgctatcagatgagcctaggtcggattagctagttggtggggtaatggctcaccaaggcgacgatccgtaactggtctgagaggatgatcagtcacactggaactgagacacggtccagac','gatcatggctcagattgaacgctggcgg','gtgactgatcatcctctcagaccagt')
    go.react()
    
    if go.product == 'gatcatggctcagattgaacgctggcggcaggcctaacacatgcaagtcgagcggatgacgggagcttgctccttgattcagcggcggacgggtgagtaatgcctaggaatctgcctggtagtgggggacaacgtttcgaaaggaacgctaataccgcatacgtcctacgggagaaagcaggggaccttcgggccttgcgctatcagatgagcctaggtcggattagctagttggtggggtaatggctcaccaaggcgacgatccgtaactggtctgagaggatgatcagt':
        print 'Everything went better than expected!'
    
if __name__ == '__main__':
    test()
    
    
