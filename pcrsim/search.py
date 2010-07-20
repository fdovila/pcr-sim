# encoding: utf-8
# Austin G. Davis-Richardson

''' I decided to drop BLAST in favor of writing my own search algorithm.
It's faster because there's no disk IO'''

# Nucleotide match/mismatch scores
nucleotides = {
 'A': ('A', 2),          # Adenosine
 'C': ('C', 3),          # Cytidine
 'G': ('G', 3),          # Guanine
 'T': ('T', 2),          # Thymidine
 'U': ('U', 2),          # Uridine
 'R': ('AG', 2.5),       # Purine
 'Y': ('TC', 2.5),       # Pyrimidine
 'K': ('GT', 2.5),       # Keto
 'M': ('AC', 2.5),       # Amino
 'S': ('GC', 3),         # Strong Interaction (3H)
 'W': ('AT', 2),         # Weak Interaction (2H)
 'B': ('CGTU', 8/3),     # Not Adenine
 'D': ('ATGU', 7/3),     # Not Cytosine
 'H': ('ACTU', 7/3),     # Not Guanine
 'V': ('ACG', 8/3),      # Neither Thymidine nor Uridine
 'N': ('GATCU', 0),      # Any nucleotide
}

unweighted_nucleotides = {
 'A': ('A', 1),          # Adenosine
 'C': ('C', 1),          # Cytidine
 'G': ('G', 1),          # Guanine
 'T': ('T', 1),          # Thymidine
 'U': ('U', 1),          # Uridine
 'R': ('AG', 1),       # Purine
 'Y': ('TC', 1),       # Pyrimidine
 'K': ('GT', 1),       # Keto
 'M': ('AC', 1),       # Amino
 'S': ('GC', 1),         # Strong Interaction (3H)
 'W': ('AT', 1),         # Weak Interaction (2H)
 'B': ('CGTU', 1),     # Not Adenine
 'D': ('ATGU', 1),     # Not Cytosine
 'H': ('ACTU', 1),     # Not Guanine
 'V': ('ACG', 1),      # Neither Thymidine nor Uridine
 'N': ('GATCU', 1),      # Any nucleotide
}


class SequenceError(Exception):
    ''' Bad nucleotide '''
    pass
    

class Search:
    ''' an object representing fuzzy, ungapped queryage.
Instantiate search object prior to querying.  This allows for recycling
and efficiency.

    S = Search(**kwargs)
         match = Match score Multiplier (int)
         mismatch = Mismatch score multiplier (int)
         pad = ' ' (padding char, no effect if you change it)
    '''
    def __init__(self, **kwargs):

        defaults = {
              # Score multipliers
              'match': 1,
              'mismatch': 1,
              'pad': ' ',
            }
            
        for attr in defaults:
            if attr in kwargs:
                setattr(self, attr, kwargs[attr])
            else:
                setattr(self, attr, defaults[attr])
    
    def _compare(self, offset):
        ''' returns score reflecting string identity '''
        sub = self.subject[offset:len(self.query) + offset]
        score = 0
        for s, q in zip(sub, self.query):
            if self.pad in (s, q): continue
            try:
                h = nucleotides[q]
                if (s in h[0]) or (s == q):
                    score += self.match*h[1]
                elif s is not q:
                    score -= self.mismatch*h[1]
                else: continue # what's this for?
            except KeyError:
                raise SequenceError, '\n\nERROR: Funky Nucleotide: \'%s\'' % q
        return score
        
    @property
    def alignments(self):
        ''' Returns a string of all possible alignments '''
        assert self.scores
        rez = []
        for score, offset in sorted(self.scores, key=lambda x: -x[0]):
            rez += '\n%-5s => %s \n%-7s  %s \n' % \
                (score, self.query, offset, 
                self.subject[offset:offset+len(self.query)] )
        return ''.join(rez)
    
    def find(self, **kwargs):
        ''' Performs actual query - returns (score, offset) '''
        assert 'query' in kwargs
        self.scores = []
        # This way you can recycle the object.
        if 'subject' in kwargs:
            self.query = kwargs['query']
            self.subject = kwargs['subject']
            self.subject = self.pad*len(self.query) + self.subject
        else:
            self.query = kwargs['query']
        for offset in range(len(self.subject)):
            score = self._compare(offset)
            self.scores.append((score, offset))
        self.score, self.offset = max(self.scores, key = lambda x: x[0])
        return (self.score, self.offset)