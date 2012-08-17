#!/usr/bin/env python3

import sys
import time
import math
import random

class VocabBuilder:
    """ Creates a vocabulary of all the words of length = wordlen,
        that can be made using characters in charset array.
        
        If unique_vocab is set to 1, then it creates all words with
        unique characters.
        
        If handle_zero is set to 1, then it ensures that a word does
        not start with 0. 
    """
    
    def __init__(self, wordlen, charset, unique_vocab = 0, handle_zero = 0):
        # input params
        self.wordlen = wordlen
        self.charset = charset
        self.unique_vocab = unique_vocab
        self.handle_zero = handle_zero
        
        # vocabulary array
        self.vocab = []
        
        # init memory for holding a word in the vocab
        word = ['' for i in xrange(0, wordlen)]
        
        # generate vocab using recursion
        if unique_vocab == 0:
            self.generate_vocab(0, word)
        else:
            self.generate_unique_vocab(0, word)
            
        # vocab created    
        print "Created vocab with", len(self.vocab), "words"
        sys.stdout.flush()
        
    def generate_vocab(self, idx, word):
        """ generate all possible words using charset """
        if idx >= self.wordlen:
            # no further scope of permutation, add word to vocab
            self.vocab.append(''.join(word))
        else:
            # put all chars in charset as idx, one by one
            for c in self.charset:
                # ensure that 0 doesnt start the word (if handle_zero is set to 1)
                if idx == 0 and self.handle_zero and c == '0': continue
                
                # put character at idx in word and recurse
                word[idx] = c
                self.generate_vocab(idx + 1, word)
                
    def generate_unique_vocab(self, idx, word):
        """ generate all possible words using charset such that one alphabet used only once in word """
        if idx >= self.wordlen:
            # no further scope of permutation, add word to vocab
            self.vocab.append(''.join(word))
        else:
            # put all chars in charset as idx, one by one
            for c in self.charset:
                # ensure that 0 doesnt start the word (if handle zero is set to 1)
                if idx == 0 and self.handle_zero and c == '0': continue
                
                # ensure that c is not used in word previously
                is_first = True
                for i in range(0, idx):
                    if c == word[i]:
                        is_first = False
                        break
                if is_first == False: continue
                
                # put character at idx in word and recurse
                word[idx] = c
                self.generate_unique_vocab(idx + 1, word)

def compute_match(word1, word2, wordlen):
    """ computes bulls and cows matches between two words, e.g., between
        ABC and ACA we have 1 bull (first A) and one cow (C)
    """
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
    return bulls, cows

class BullsCows:
    def __init__(self, wordlen, charset, initVocab):
        # input params
        self.wordlen = wordlen
        self.charset = charset
        self.initVocab = initVocab
        
        # entropy guess
        self.entropyGuess = EntropyGuess(wordlen, initVocab)
        
        # create init guess
        if len(charset) >= wordlen:
            self.initGuess = ''.join(charset[0:wordlen])
        else:
            self.initGuess = ''.join(charset) + charset[0] * (wordlen - len(charset)) 
        print 'Using initial guess:', self.initGuess
        sys.stdout.flush()
        
    def prune_vocab(self, vocab, word, bulls, cows):
        """ removes those words from vocab that do not have the same
            bulls and cows with word as provided in input
        """
        vocab1 = []
        for w in vocab:
            # gets bulls and cows for match between word and w
            b, c = compute_match(word, w, wordlen)
            
            # check if they match, then put in pruned_vocab
            if b == bulls and c == cows:
                vocab1.append(w)
        return vocab1
     
    def random_guess(self, vocab):
        """ returns a random guess from the vocab """
        i = random.randint(0, len(vocab) - 1)
        return vocab[i]
     
    def play(self, find_word, rand_guesses = 3, verbose = 1):
        """ start playing guessing game, returns the number of attempts and solution """
        # result set
        attempts = 0
        guess = self.initGuess
        
        # starting vocab, it will be pruned for subsequent guesses
        vocab = self.initVocab
        
        bulls = 0
        while bulls != self.wordlen:
            # compute bulls and cows
            bulls, cows = compute_match(find_word, guess, self.wordlen)
            
            # prune vocab
            vocab = self.prune_vocab(vocab, guess, bulls, cows)
            
            # increment num attempts
            attempts += 1
            
            # print vars
            if verbose:
                print attempts, ".", guess, 'matches', bulls, cows, '(bulls, cows) with', find_word
                if len(vocab) < 50: print vocab
                print
                sys.stdout.flush()
                
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
    
    def play_interactive(self):
        """ start playing bulls and cows interactively """
        vocab = self.initVocab
        guess = self.initGuess
        bulls = 0
        print "Think of a number. I'll try to guess"
        while bulls != self.wordlen:
            print "Guessing:", guess
            
            # input bulls and cows
            bulls = int(raw_input("Enter number of bulls:"))
            cows = int(raw_input("Enter number of cows:"))
            print bulls + cows
            
            # prune vocab
            vocab = self.prune_vocab(vocab, guess, bulls, cows)
            print vocab
            print
                
            # only one word in vocab, that must be find_word, problem solved
            if len(vocab) <= 1:
                if len(vocab) == 0:
                    print "You made a mistake in inputting bulls and cows"
                    return
                guess = vocab[0]
                break
            
            # generate a fuzzy guess (random + information gain)
            if len(vocab) < 300:
                guess = self.entropyGuess.compute_guess(vocab)
            else:
                guess = self.random_guess(vocab)
                
        print "Secret is", guess
        
    def compute_algo_stats(self):
        """ computes statistics of the algorithms, like average attempt length,
            worst attempt length and overall time taken to run the algorithm
        """
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
            attempt, guess = self.play(w, rand_guesses = 3, verbose = 0)
            
            # update result set
            num_attempts += attempt
            if attempt > worst_attempt:
                worst_attempt = attempt
                worst_attempt_word = w
        
        # print statistics
        time_diff = time.time() - start_time
        print 
        print "On average, algorithm made", num_attempts / float(len(self.initVocab)), "attempts ",
        print "and used", time_diff / float(len(self.initVocab)), "seconds per attempt"
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
            b, c = compute_match(w, word, self.wordlen)
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
            
            # update max
            if e == 0:
                return w
            elif e <= min_e:
                min_e = e
                min_w = w
                
        return min_w

charset = [str(i) for i in range(9,-1,-1)]
print "Chatset:", charset
wordlen = 4

v = VocabBuilder(wordlen, charset, unique_vocab = 0, handle_zero = 0)

b = BullsCows(wordlen, charset, v.vocab)
#print b.play('0020')
#b.play_interactive()
b.compute_algo_stats()
