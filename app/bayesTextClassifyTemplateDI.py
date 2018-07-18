import os
import codecs
import math

""" Source: A Programmer's Guide to Data Mining
Chapter 7 Naïve Bayes and unstructured text
URL: http://guidetodatamining.com/chapter7/
CC By-NC RON ZACHARSKI   2015 
"""
class BayesText:
    def __init__(self, trainingdir, stopwordlist):
        """This class implements a naive Bayes approach to text
        classification
        trainingdir is the training data. Each subdirectory of
        trainingdir is titled with the name of the classification
        category -- those subdirectories in turn contain the text
        files for that category.
        The stopwordlist is a list of words (one per line) will be
        removed before any counting takes place.
        """
        self.vocabulary = {}
        self.prob = {}
        self.totals = {}
        self.stopwords = {}
        f = open(stopwordlist)
        for line in f:
            self.stopwords[line.strip()] = 1
        f.close()
        categories = os.listdir(trainingdir)
        # filter out files that are not directories
        self.categories = [filename for filename in categories
                           if os.path.isdir(trainingdir + filename)]
        print("Counting ...")
        for category in self.categories:
            # print('    ' + category)
            (self.prob[category],
             self.totals[category]) = self.train(trainingdir, category)
        # I am going to eliminate any word in the vocabulary
        # that doesn't occur at least 3 times

        # DI -- I commented this to test
        todelete = []
        for word in self.vocabulary:
            if self.vocabulary[word] < 3:
                # mark word for deletion
                # can't delete now because you can't delete
                # from a list you are currently iterating over
                todelete.append(word)
        # now delete
        for word in todelete:
            del self.vocabulary[word]

        # now compute probabilities
        vocablength = len(self.vocabulary)
        print("Computing probabilities:")
        for category in self.categories:
            # print('    ' + category)
            denominator = self.totals[category] + vocablength
            for word in self.vocabulary:
                if word in self.prob[category]:
                    count = self.prob[category][word]
                else:
                    count = 1
                self.prob[category][word] = (count + 1) / denominator
        print("DONE TRAINING\n\n")

    def train(self, trainingdir, category):
        """counts word occurrences for a particular category"""
        currentdir = trainingdir + category
        files = os.listdir(currentdir)
        counts = {}
        total = 0
        for file in files:
            # print(currentdir + '/' + file)
            f = codecs.open(currentdir + '/' + file, 'r', 'iso8859-1')
            for line in f:
                tokens = line.split()
                for token in tokens:
                    # get rid of punctuation and lowercase token
                    token = token.strip('\'".,?:-')
                    token = token.lower()
                    if token != '' and token not in self.stopwords:
                        self.vocabulary.setdefault(token, 0)
                        self.vocabulary[token] += 1
                        counts.setdefault(token, 0)
                        counts[token] += 1
                        total += 1
            f.close()
        return counts, total

    def classify(self, filename):
        results = {}
        for category in self.categories:
            results[category] = 0
        f = codecs.open(filename, 'r', 'iso8859-1')
        for line in f:
            tokens = line.split()
            for token in tokens:
                # print(token)
                token = token.strip('\'".,?:-').lower()
                if token in self.vocabulary:
                    for category in self.categories:
                        if self.prob[category][token] == 0:
                            print("%s %s" % (category, token))
                        results[category] += math.log(
                            self.prob[category][token])
        f.close()
        results = list(results.items())
        results.sort(key=lambda tuple_seq: tuple_seq[1], reverse=True)
        # for debugging I can change this to give me the entire list
        return results[0][0]

    def classify_text(self, search_text):
        results = {}
        for category in self.categories:
            results[category] = 0
        tokens = search_text.split()
        for token in tokens:
            # print(token)
            token = token.strip('\'".,?:-').lower()
            if token in self.vocabulary:
                for category in self.categories:
                    if self.prob[category][token] == 0:
                        print("%s %s" % (category, token))
                    results[category] += math.log(
                        self.prob[category][token])
        results = list(results.items())
        results.sort(key=lambda tuple_seq: tuple_seq[1], reverse=True)
        # for debugging I can change this to give me the entire list
        return results[0][0]

    def read_file_content(self, training_dir, category):
        current_dir = training_dir + category
        files = os.listdir(current_dir)
        content = ""
        for filename in files:
            # print(filename)
            f = codecs.open(current_dir + '/' + filename, 'r', 'iso8859-1')
            for line in f:
                content += line
            f.close()
        return content


if __name__ == '__main__':
    # change these to match your directory structure
    # trainingDir = "/Users/raz/Dropbox/guide/data/20news-bydate/20news-bydate-train/"
    # trainingDir = "./app/static/app/app-kb/app-kb-train/"
    trainingDir = "./app/static/app/app-kb/app-kb-train/"
    
    # (just create an empty file to use as a stoplist file.)
    # stoplistfile = "/Users/raz/Dropbox/guide/data/20news-bydate/emptyStoplist.txt"
    # stoplistfile = "./app/static/app/app-kb/emptyStoplist.txt"
    # stoplistfile = "./app/static/app/app-kb/stopwords174.txt"
    # stoplistfile = "./app/static/app/app-kb/stopwords174.txt"
    # The next has 100 words
    # stoplistfile = "./app/static/app/app-kb/stoplist.txt"
    # stoplistfile = "./app/static/app/app-kb/stopwords0.txt"
    # stoplistfile = "./app/static/app/app-kb/stopwords25.txt"
    stoplistfile = "./app/static/app/app-kb/stopwords174.txt"

    bT = BayesText(trainingDir, stoplistfile)
    print("Running Test ...")
    # result = bT.classify("/Users/raz/Dropbox/guide/data/20news-bydate/20news-bydate-test/rec.motorcycles/104673")
    # result =
    # bT.classify("./app/static/app/app-kb/app-kb-test/req.txt")
    # print(result)
    # result = bT.classify("/Users/raz/Dropbox/guide/data/20news-bydate/20news-bydate-test/sci.med/59246")
    # result = bT.classify("./app/static/app/app-kb/app-kb-test/req.txt")
    # print(result)
    # result = bT.classify("/Users/raz/Dropbox/guide/data/20news-bydate/20news-bydate-test/soc.religion.christian/21424")

    result = bT.classify("./app/static/app/app-kb/app-kb-test/req.txt")
    print(result)

    # category_result = bT.classify_text("Person Unique Identification Number")
    # print(category_result)
    # print(bT.read_file_content(trainingDir, category_result))
