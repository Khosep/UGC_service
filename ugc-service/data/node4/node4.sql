-- NODE 4 (replica)
CREATE DATABASE replica;
CREATE TABLE replica.film_views (user_id UUID, film_id UUID, film_ts Int64, event_time DateTime DEFAULT now()) Engine=ReplicatedMergeTree('/clickhouse/tables/shard2/film_views', 'replica_2') PARTITION BY toYYYYMMDD(event_time) ORDER BY film_id;