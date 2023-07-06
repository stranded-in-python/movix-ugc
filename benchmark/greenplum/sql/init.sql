drop table if exists public.regular_table;

create table public.regular_table(
    id bigserial,
    user_id bigint not null,
    filem_id bigint not null,
    timestamp timestamp without time zone not null
) with (
    appendoptimized = true,
    ORIENTATION=column,
    compresstype = zstd,
    compresslevel = 3,
    fillfactor = 100 )
distributed by (id);

CREATE INDEX idx_regular_table_id ON public.regular_table (id);
/*Не помогает :)*/
