create table if not exists movix_db.watching_movies/*ON CLUSTER cluster*/(
    id UInt32,
    user_id UUID,
    film_id UUID,
    frameno UInt32,
    timestamp DATETIME
)
engine = MergeTree
order by id
partition by toMonth(timestamp);

create table if not exists movix_db.likes_movies/*ON CLUSTER cluster*/(
    id UInt32,
    movie_id UUID,
    user_id UUID,
    score UInt32,
    timestamp DATETIME
)
engine = MergeTree
order by id
partition by toMonth(timestamp);
