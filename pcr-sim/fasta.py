# Two objects for handling FASTA files
# dna is a DNA object representing a FASTA record with a header and sequence
# fasta is a FASTA iterator that yields DNA objects

from string import maketrans
_complement = maketrans('GATCRYgatcry','CTAGYRctagyr')

class Dna:
    ''' Object representing a FASTA record. '''
    def __init__(self, header, sequence):
        self._head = header
        self._seq = sequence
    def __repr__(self):
        return '<DNA: %s >' % (self._head)
    def __str__(self, separator=''):
        return '>%s\n%s' % (self._head, self.seq)
    def __len__(self):
        return len(''.join(self._seq))
    @property
    def seq(self, separator=''):
        return separator.join(self._seq)
    @property
    def head(self):
        return self._head
    @property
    def revcomp(self):
        return self.seq.translate(_complement)
    
class Fasta:
    ''' A FASTA iterator/generates DNA objects. '''
    def __init__(self, handle):
        self.handle = handle
    def __repr__(self):
        return '<FASTA: for handle = %s>' % handle
    def __iter__(self):
        header, sequence = '', []
        for line in self.handle:
            if line[0] == '>':
                if sequence: yield Dna(header, sequence)
                header = line[1:-1]
                sequence = []
            else:
                sequence.append(line.strip().upper())
        yield Dna(header, sequence)
        