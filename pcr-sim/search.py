# encoding: utf-8
# Austin G. Davis-Richardson

''' I decided to drop BLAST in favor of writing my own search algorithm.
It's faster because there's no disk IO'''

class Search:
    ''' an object representing fuzzy, ungapped queryage. '''
    
    def __init__(self, **kwargs):
        ''' instantiate the search object, only have to do once, I guess. 
You can set attributes here (if allowed). '''
        defaults = {
            # G≡C while A=T
            'gc_score': 3,
            'at_score': 2,
            # Could make this the opposite of match
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
            if (i or j) in 'Nn ': continue
            if i == j and i in 'GgCc': score += self.gc_score
            if i == j and i in 'AaTt': score += self.at_score
            if i is not j: score -= self.miss_pen  
        return score
        
    def find(self, *vargs):
        ''' Performs actual query - returns int representing start pos\'n. '''
        assert len(vargs) > 0 
        # This way you can recycle the object.
        if len(vargs) is 1:
            self.query = vargs[0]
        else:
            self.subject = self.padding + vargs[0] + self.padding
            self.query = vargs[1]
        self.scores = []
        for offset in range(len(self.subject)):
            score = self._compare(offset)
            self.scores.append((score, offset))
        self.score, self.offset = max(self.scores, key = lambda x: x[0])
        
        print 'Q: %s\nS: %s\n' % \
         (self.query, self.subject[self.offset:self.offset+len(self.query)])

        return (self.score, self.offset)