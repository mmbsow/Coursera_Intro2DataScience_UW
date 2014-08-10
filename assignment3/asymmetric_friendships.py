import MapReduce
import sys

"""
Word Count Example in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

def mapper(record):
    # key: friend A
    # value: friend B
    friendA = record[0]
    friendB = record[1]
    mr.emit_intermediate((friendA, friendB), 1)
    mr.emit_intermediate((friendB, friendA), -1)

def reducer(key, list_of_friends):
    # key: [friendA, friendB]
    # value: list of friend counts
    total = 0
    for f in list_of_friends:
        total += f
    if total != 0:
        mr.emit(key)

if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
