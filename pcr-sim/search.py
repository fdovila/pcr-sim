# encoding: utf-8
# Austin G. Davis-Richardson

''' I decided to drop BLAST in favor of writing my own search algorithm.
It's faster because there's no disk IO'''

class SequenceError(Exception):
    pass

nucleotides = {
 'A': 'A',    # Adenosine
 'C': 'C',    # Cytidine
 'G': 'G',      # Guanine
 'T': 'T',      # Thymidine
 'U': 'U',      # Uridine
 'R': 'AG',     # Purine
 'Y': 'TC',     # Pyrimidine
 'K': 'GT',     # Keto
 'M': 'AC',     # Amino
 'S': 'GC',     # Strong Interaction (3H)
 'W': 'AT',     # Weak Interaction (2H)
 'B': 'CGT',    # Not Adenine
 'D': 'ATG',    # Not Cytosine
 'H': 'ACT',    # Not Guanine
 'V': 'ACG',    # Neither Thymidine nor Uridine
 'N': 'GATCU',  # Any nucleotide
}

class Search:
    ''' an object representing fuzzy, ungapped queryage. '''
    
    def __init__(self, **kwargs):
        ''' instantiate the search object, only have to do once, I guess. 
You can set attributes here (if allowed). '''
        defaults = {
            # G≡C while A=T
            'score': 1,
            'miss_pen': 1,
            'padding': 10 }
        for attr in defaults:
            if attr in kwargs:
                setattr(self, attr, kwargs[attr])
            else:
                setattr(self, attr, defaults[attr])                
        self.padding = ' '*self.padding
            
    def _compare(self, offset):
        ''' returns score reflecting string identity '''
        sub = self.subject[offset:len(self.query) + offset]
        score = 0
        for i, j in zip(sub, self.query):
            try:
                if nucleotides[i] == nucleotides[j] and 'N' not in (i, j):
                    score += self.score
                if i is not j:
                    score -= self.miss_pen
                else: continue
            except KeyError:
                raise SequenceError, 'funky nucleotide? %s or %s' % (i, j) 
        return score
        
    @property
    def alignments(self):
        ''' returns a string of all possible alignments '''
        assert self.scores
        rez = []

        for score, offset in self.scores:
            rez += '\n%-5s => %s \n%-7s  %s \n' % \
             (score, self.query, offset, self.subject[offset:offset+len(self.query)] )
        return ''.join(rez)
        
    def find(self, **kwargs):
        ''' Performs actual query - returns int representing start pos\'n. '''
        assert 'query' in kwargs
        
        # This way you can recycle the object.
        if 'subject' in kwargs:
            self.subject = kwargs['subject']
            self.query = kwargs['query']
        else:
            self.query = kwargs['query']
        
        self.scores = []
        for offset in range(len(self.subject)):
            score = self._compare(offset)
            self.scores.append((score, offset))
        self.score, self.offset = max(self.scores, key = lambda x: x[0])


        return (self.score, self.offset)