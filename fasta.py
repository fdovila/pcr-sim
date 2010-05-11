# Two objects for handling FASTA files
# dna is a DNA object representing a FASTA record with a header and sequence
# fasta is a FASTA iterator that yields DNA objects

class Dna:
    ''' Object representing a FASTA record. '''
    def __init__(self, header, sequence):
        self.head = header
        self.seq = sequence
    def __repr__(self):
        return '<DNA: %s >' % (self.head)
    def __str__(self, separator=''):
        return '>%s\n%s' % (self.head, separator.join(self.seq))
    def __len__(self):
        return len(''.join(self.seq))
    def sequence(self, separator=''):
        return separator.join(self.seq)
        
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
                sequence.append(line.strip())
        yield Dna(header, sequence)
