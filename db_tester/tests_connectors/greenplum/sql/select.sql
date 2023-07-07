select * from public.regular_table
order by id
offset %(offset)s
limit %(limit)s;
