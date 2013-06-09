import re, itertools, os
from nltk.classify import NaiveBayesClassifier
from nltk.metrics import BigramAssocMeasures
from nltk.probability import FreqDist, ConditionalFreqDist
import placeranking.sentiement.negOpinions
import placeranking.sentiement.posOpinions



class SentimentAnalyzer(object):

    def evaluate_classifier(self, featx):
        negFeats = []
        posFeats = []
        posSentences = placeranking.sentiement.posOpinions.posSentenses
        negSentences = placeranking.sentiement.negOpinions.negSentences

        for i in posSentences:
            posWords = re.findall(r"[\w']+|[.,!?;]", i.rstrip())
            posWords = [featx(posWords), 'pos']
            negFeats.append(posWords)

        for i in negSentences:
            negWords = re.findall(r"[\w']+|[.,!?;]", i.rstrip())
            negWords = [featx(negWords), 'neg']
            posFeats.append(negWords)

        self.classifier = NaiveBayesClassifier.train(negFeats + posFeats)


    def create_word_scores(self):
        #creates lists of all positive and negative words
        posWords = []
        negWords = []
        posSentences = placeranking.sentiement.posOpinions.posSentenses
        negSentences = placeranking.sentiement.negOpinions.negSentences
        for i in posSentences:
            posWord = re.findall(r"[\w']+|[.,!?;]", i.rstrip())
            posWords.append(posWord)
        for i in negSentences:
            negWord = re.findall(r"[\w']+|[.,!?;]", i.rstrip())
            negWords.append(negWord)
        posWords = list(itertools.chain(*posWords))
        negWords = list(itertools.chain(*negWords))

        #build frequency distibution of all words and then frequency distributions of words within positive and negative labels
        word_fd = FreqDist()
        cond_word_fd = ConditionalFreqDist()
        for word in posWords:
            word_fd.inc(word.lower())
            cond_word_fd['pos'].inc(word.lower())
        for word in negWords:
            word_fd.inc(word.lower())
            cond_word_fd['neg'].inc(word.lower())

        #finds the number of positive and negative words, as well as the total number of words
        pos_word_count = cond_word_fd['pos'].N()
        neg_word_count = cond_word_fd['neg'].N()
        total_word_count = pos_word_count + neg_word_count

        #builds dictionary of word scores based on chi-squared test
        word_scores = {}
        for word, freq in word_fd.iteritems():
            pos_score = BigramAssocMeasures.chi_sq(cond_word_fd['pos'][word], (freq, pos_word_count), total_word_count)
            neg_score = BigramAssocMeasures.chi_sq(cond_word_fd['neg'][word], (freq, neg_word_count), total_word_count)
            word_scores[word] = pos_score + neg_score

        return word_scores

    def word_feats(self, words):
        return dict([(word, True) for word in words])

    #finds the best 'number' words based on word scores
    def find_best_words(self, word_scores, number):
        best_vals = sorted(word_scores.iteritems(), key=lambda (w, s): s, reverse=True)[:number]
        best_words = set([w for w, s in best_vals])
        return best_words

    #creates feature selection mechanism that only uses best words
    def best_word_features(self, words):
        return dict([(word, True) for word in words if word in self.best_words])

    def train(self):
        word_scores = self.create_word_scores()
        self.best_words = self.find_best_words(word_scores, 15000)
        self.evaluate_classifier(self.best_word_features)

    def analyze(self, text):
        return self.classifier.prob_classify(self.word_feats(re.findall(r"[\w']+|[.,!?;]", text.rstrip())))






