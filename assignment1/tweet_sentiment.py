import sys
import json
import re

def getAfinnDicts(afinnFile):
    # build 2 dictionaries of scores from AFINN file:
    # one with single words, one for 2 words
    single_words = {}
    double_words = {}
    for line in afinnFile:
        term, score = line.split('\t')
        if re.findall(r'\w+ \w+', term):
            double_words[term] = int(score)
        else:
            single_words[term] = int(score)

    return (single_words, double_words)

def getTweetScore(tweet, single_words, double_words):
    tweet_score = []
    
    # get scores for single-word term (ex: "fun")
    tweet_score = [ single_words.get(s, 0) for s in re.split(r'\W+', tweet) if s ]

    # append scores for multi-word term (ex: "no fun")
    for term, score in double_words.items():
        tweet_score = tweet_score + [ score for d in re.findall(r'\b%s\b' % term, tweet) ]

    return sum(tweet_score)

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    
    # get dictionaries of sentiment scores
    single_words, double_words = getAfinnDicts(sent_file)

    # parse twitter output
    for line in tweet_file.readlines():
        text = None
        sent_score = 0

        # decode json and get the text part of the tweet
        try:
            tweet = json.loads(line)
            text = tweet.get('text', None)
        except:
            text = None

        # if tweet is valid, compute score
        if text:
            tweet_score = getTweetScore(text.encode('utf-8').lower(), single_words, double_words)
            print tweet_score


if __name__ == '__main__':
    main()
