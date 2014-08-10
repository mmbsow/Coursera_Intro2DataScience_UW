import MapReduce
import sys

"""
Word Count Example in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

def mapper(record):
    # key: friend A
    # value: friend B
    sequence_id = record[0]
    nucleotide = record[1][:-10]
    if nucleotide:
        mr.emit_intermediate(nucleotide, 1)

def reducer(key, list_of_nucs):
    # key: nucleotide
    # value: count (1)
    mr.emit(key)

if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
