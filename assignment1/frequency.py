import sys
import json
import re


def main():
    tweet_file = open(sys.argv[1])

    # total number of occurrences for all tweets
    countAllTerms = 0.0
    termsDict = {}
        
    # parse twitter output
    for line in tweet_file.readlines():
        text = None

        # decode json and get the text part of the tweet
        try:
            tweet = json.loads(line)
            text = tweet.get('text', None)
        except:
            text = None

        # if tweet is valid, compute score
        if text:
            text = text.encode('utf-8').lower()
            terms = [ t for t in re.split(r'\W+', text) if t ] # get rid of empty terms

            for t in terms:
                termsDict[t] = termsDict.get(t, 0.0) + 1.0
                countAllTerms = countAllTerms + 1.0


    for term, count in termsDict.items():
        freq = count / countAllTerms
        print '%s %f' % (term, freq)


if __name__ == '__main__':
    main()
