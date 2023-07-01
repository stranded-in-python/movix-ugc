with test_table as (
    select * from public.regular_table
--     order by id
    offset %(offset)s
    limit %(limit)s
)
select count(*) from test_table;
