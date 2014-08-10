select arow as row_num, bcol as col_num, sum(value) as value
from (
select A.row_num as arow, A.col_num as acol, B.row_num as brow,  B.col_num as bcol, A.value*B.value as value
from A
join B on B.row_num = A.col_num
)