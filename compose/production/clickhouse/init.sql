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
    movie_id UUID,
    user_id UUID,
    score UInt32,
    timestamp DATETIME
)
engine = MergeTree
order by timestamp
partition by toMonth(timestamp);

SET allow_experimental_inverted_index = true;

create table if not exists movix_db.reviews_movies/*ON CLUSTER cluster*/(
    review_id UUID,
    user_id UUID,
    movie_id UUID,
    text String,
    timestamp DATETIME,
    score UInt32,
    INDEX inv_idx(text) TYPE inverted(0) GRANULARITY 1
)
engine = MergeTree
order by timestamp
partition by toMonth(timestamp);

create table if not exists movix_db.likes_reviews/*ON CLUSTER cluster*/(
    review_id UUID,
    user_id UUID,
    score UInt32,
    timestamp DATETIME
)
engine = MergeTree
order by timestamp
partition by toMonth(timestamp);

create table if not exists movix_db.bookmarks_movies/*ON CLUSTER cluster*/(
    movie_id UUID,
    user_id UUID,
    timestamp DATETIME
)
engine = MergeTree
order by timestamp
partition by toMonth(timestamp);
