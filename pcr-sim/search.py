# encoding: utf-8

# Austin G. Davis-Richardson

''' I decided to drop BLAST in favor of writing my own search algorithm.
It's faster because there's no disk IO'''



class Search:
    ''' an object representing fuzzy, ungapped queryage. '''
    
    def __init__(self):
        ''' instantiate the search object, only have to do once, I guess. '''
        pass
    
    def _compare(self, offset):
        ''' returns score reflecting string identity '''
        sub = self.subject[offset:len(self.query) + offset]
        score = 0

        for i, j in zip(sub, self.query):
            if i == j:
                score += 1
            else:
                score -= 1
        
        print 'S: %s\nQ: %s\n#: %s\nO: %s\n' % \
            (sub, self.query, score, offset)
        
        return score
        
    def find(self, *vargs):
        ''' Performs actual query - returns int representing start pos\'n. '''
        
        # This way you can recycle the object.
        if len(vargs) is 1:
            self.query = vargs[0]
        else:
            self.subject = vargs[0]
            self.query = vargs[1]
            
        assert self.subject

        self.scores = []
        
        for offset in range(len(self.subject)):
            score = self._compare(offset)
            self.scores.append((score, offset))
            
        self.score, self.offset = max(self.scores, key = lambda x: x[0])