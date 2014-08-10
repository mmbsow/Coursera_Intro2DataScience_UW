import MapReduce
import sys

"""
Word Count Example in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

def mapper(record):
    # key: friend A
    # value: friend B
    key = record[0]
    value = 1 if record[1] else 0
    mr.emit_intermediate(key, value)

def reducer(key, list_of_friends):
    # key: person
    # value: list of friend counts
    total = 0
    for f in list_of_friends:
      total += f
    mr.emit((key, total))

if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
