import MapReduce
import sys

"""
Word Count Example in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

def mapper(record):
    # key: friend A
    # value: friend B
    matrix = record[0]
    i = record[1]
    j = record[2]
    value = record[3]
    for k in range(5):
        if matrix == "a":
            mr.emit_intermediate((i,k), record)
        else:
            mr.emit_intermediate((k,j), record)

def reducer(key, list_of_vals):
    # key: (i,k)
    # value: count (1)
    total = 0
    matrixA = [a for a in list_of_vals if a[0] == "a"]
    matrixB = [b for b in list_of_vals if b[0] == "b"]
    for a in matrixA:
        for b in matrixB:
            if a[2] == b[1]:
                total += a[3] * b[3]
    mr.emit((key[0], key[1], total))

if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
