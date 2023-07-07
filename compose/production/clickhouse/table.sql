create table if not exists db1.watching_movies/*ON CLUSTER cluster*/(
    id UInt32,
    user_id UUID,
    film_id UUID,
    frameno UInt32,
    timestamp DATETIME
)
engine = MergeTree
order by id
partition by toMonth(timestamp);
