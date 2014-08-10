import MapReduce
import sys

"""
Assignment: Inverted Index in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()


def mapper(record):
    # key: order identifier
    # value: attributes in the table
    key = record[1]
    value = record
    mr.emit_intermediate(key, value)

def reducer(key, list_of_recs):
    # key: order identifier
    # value: list of attributes in the table
    recs = []
    orders = [o for o in list_of_recs if o[0] == 'order']
    items = [i for i in list_of_recs if i[0] == 'line_item']
    for o in orders:
        for i in items:
            mr.emit(o + i)

if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
