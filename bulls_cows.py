#!/usr/bin/env python3

import sys
import time
import math
import random

class VocabBuilder:
    """ Creates a vocabulary of all the words of length = wordlen, that can be made using characters in charset array """
    def __init__(self, wordlen, charset):
        self.wordlen = wordlen
        self.charset = charset
        self.vocab = []
        
        # init memory for holding a word
        word = ['' for i in xrange(0, wordlen)]
        
        # generate vocab (using recursion)
        self.__generate_vocab__(0, word)
        #self.__generate_unique_vocab__(0, word)
        print "Created vocab with", len(self.vocab), "words"
        
    def __generate_vocab__(self, idx, word):
        """ generate all possible words using charset """
        if idx >= self.wordlen:
            # no further scope of permutation, add word to vocab
            self.vocab.append(''.join(word))
        else:
            # put all chars in charset as idx, one by one
            for c in self.charset:
                word[idx] = c
                self.__generate_vocab__(idx + 1, word)
                
    def __generate_unique_vocab__(self, idx, word):
        """ generate all possible words using charset """
        if idx >= self.wordlen:
            # no further scope of permutation, add word to vocab
            self.vocab.append(''.join(word))
        else:
            # put all chars in charset as idx, one by one
            for c in self.charset:
                is_first = True
                for i in range(0, idx):
                    if c == word[i]:
                        is_first = False
                        break
                    
                if is_first == False: continue
                
                word[idx] = c
                self.__generate_unique_vocab__(idx + 1, word)

def compute_match(word1, word2, wordlen):
    """ computes bulls and cows matches between two words, e.g., between ABC and ACA we have 1 bull (first A) and one cow (C) """
    bulls = 0
    cows = 0
    
    # maintains char count
    m = {}
    for i in range(0, wordlen):
        c1 = word1[i]
        c2 = word2[i]
        
        if c1 == c2:
            # both characters match, found a bull
            bulls += 1
        else:
            # 1. check if c1 has a match with a char in word2 with index < idx
            # 2. check if c2 has a match with a char in word1 with index < idx
            
            # add c1 to the char count map, using +1 as its indicator
            if m.has_key(c1):
                # check if count of c1 is < 0, we found a cow
                if m[c1] < 0:
                    cows += 1
                
                # increase char count of c1
                m[c1] += 1
            else:
                m[c1] = 1
                
            # add c2 to the char count map, using -1 as its indicator
            if m.has_key(c2):
                # check if count of c2 is > 0, we found a cow
                if m[c2] > 0:
                    cows += 1
                
                # decrement char count of c2 (as it cancels a char in word1)
                m[c2] -= 1
            else:
                m[c2] = -1
                
    # return matches
    return [bulls, cows]

class BullsCows:
    def __init__(self, wordlen, charset):
        self.wordlen = wordlen
        self.charset = charset
        
        # create initial vocab
        v = VocabBuilder(wordlen, charset)
        self.initVocab = v.vocab
        
        # entropy guess
        self.entropyGuess = EntropyGuess(self.wordlen, self.initVocab)
        
        # create init guess
        if len(charset) >= wordlen:
            self.initGuess = ''.join(charset[0:wordlen])
        else:
            self.initGuess = ''.join(charset) + charset[0] * (wordlen - len(charset)) 
        print 'Initial guess:', self.initGuess
        
    def prune_vocab(self, vocab, word, bulls, cows):
        """ removes those words from vocab that do not have the same bulls and cows with word as provided in input """
        vocab1 = []
        for w in vocab:
            # gets bulls and cows for match between word and w
            [b, c] = compute_match(word, w, wordlen)
            
            # check if they match, then put in pruned_vocab
            if b == bulls and c == cows:
                vocab1.append(w)
                
        return vocab1
     
    def random_guess(self, vocab):
        """ returns a random guess from the vocab """
        i = random.randint(0, len(vocab) - 1)
        return vocab[i]
     
    def play(self, find_word, rand_guesses = 4, verbose = 1):
        """ start playing guessing game, returns the number of attempts and solution """
        # result set
        attempts = 0
        guess = self.initGuess
        
        # starting vocab, it will be pruned for subsequent guesses
        vocab = self.initVocab
        
        bulls = 0
        while bulls != self.wordlen:
            # compute bulls and cows
            [bulls, cows] = compute_match(find_word, guess, self.wordlen)
            
            # prune vocab
            vocab = self.prune_vocab(vocab, guess, bulls, cows)
            
            # increment num attempts
            attempts += 1
            
            # print vars
            if verbose:
                print attempts, ".", guess, 'matches', bulls, cows, '(bulls, cows) with', find_word
                print vocab
                print
                
            # only one word in vocab, that must be find_word, problem solved
            if len(vocab) <= 1:
                guess = vocab[0]
                attempts += 1
                break
            
            # candidate guesses
            # guess = vocab[0] # pick first as guess
            # guess = self.random_guess(vocab) # pick random as a guess
            
            # generate a fuzzy guess (random + information gain)
            if attempts <= rand_guesses:
                guess = self.random_guess(vocab)
            else:
                guess = self.entropyGuess.compute_guess(vocab)
             
        return attempts, guess
    
    def compute_algo_stats(self):
        """ computes statistics of the algorithms, like average attempt length, worst attempt length and overall time taken to run the algorithm """
        # result set
        num_attempts = 0
        worst_attempt = -1
        worst_attempt_word = None
        start_time = time.time()
        
        # play string guessing for all words in vocab
        iteration = 0
        
        print "Measuring algorithm statistics"
        for w in self.initVocab:
            
            # print num iterations
            iteration += 1
            if iteration % 200 == 0:
                print "     iteration:", iteration
                sys.stdout.flush()
                
            # num attempts for w
            attempt, guess = self.play(w, 3, 0)
            
            # update result set
            num_attempts += attempt
            if attempt > worst_attempt:
                worst_attempt = attempt
                worst_attempt_word = w
        
        # print statistics
        time_diff = time.time() - start_time
        print 
        print "On average, algorithm made", num_attempts / float(len(self.initVocab)), "attempts and used", time_diff / float(len(self.initVocab)), "seconds per attempt"
        print "Worst attempt is", worst_attempt, "on word", worst_attempt_word
        print "Total time taken:", time.time() - start_time

class EntropyGuess:
    def __init__(self, wordlen, initVocab):
        self.wordlen = wordlen
        self.initVocab = initVocab
        
        # theoretically max entropy
        self.maxEntropy = len(initVocab) * math.log10(len(initVocab))
        
    def compute_information_gain(self, word, vocab):
        """ computes information gain of a word over the set of words in vocab """
        
        # compute the num of elements per partition (as created by w)
        bucket_freq = [0 for i in xrange(0,41)]
        for w in vocab:
            [b, c] = compute_match(w, word, self.wordlen)
            bucket_freq[10*b+c] += 1
            
        # compute information gain
        e = 0
        for f in bucket_freq:
            if f > 1:
                e+= f * math.log10(f)
                
        return e
     
    def compute_guess(self, vocab):
        """ calculates guess that minimizes entropy """
        min_e = self.maxEntropy
        min_w = None
        for w in self.initVocab:
            
            # compute information gain
            e = self.compute_information_gain(w, vocab)
            
            if e == 0:
                return w
            elif e <= min_e:
                min_e = e
                min_w = w
                
        return min_w

charset = [str(i) for i in range(0,10)]
wordlen = 4

b = BullsCows(wordlen, charset)
#print b.play('0002')
b.compute_algo_stats()