select adocid as docid, bterm as term, sum(product) as totalCount
from (
select A.docid as adocid, A.term as aterm, B.docid as bdocid,  B.term as bterm, A.count*B.count as product
from Frequency A
join Frequency B on B.term = A.term
where A.docid < B.docid
and A.docid = '10080_txt_crude'
and B.docid = '17035_txt_earn'
)