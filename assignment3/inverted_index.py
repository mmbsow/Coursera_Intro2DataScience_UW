import MapReduce
import sys

"""
Assignment: Inverted Index in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()


def mapper(record):
    # key: document identifier
    # value: document contents
    key = record[0]
    value = record[1]
    words = value.split()
    for w in words:
      mr.emit_intermediate(w, key)

def reducer(key, list_of_docs):
    # key: word
    # value: list of documents where the word appears
    docs = []
    for d in list_of_docs:
      docs += [d]
    mr.emit((key, list(set(docs))))

if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
