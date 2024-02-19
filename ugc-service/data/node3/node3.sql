-- NODE 3 (shard)
CREATE DATABASE shard;
CREATE TABLE shard.film_views (user_id UUID, film_id UUID, film_ts Int64, event_time DateTime DEFAULT now()) Engine=ReplicatedMergeTree('/clickhouse/tables/shard2/film_views', 'replica_1') PARTITION BY toYYYYMMDD(event_time) ORDER BY film_id;
CREATE TABLE default.film_views (user_id UUID, film_id UUID, film_ts Int64, event_time DateTime DEFAULT now()) ENGINE = Distributed('company_cluster', '', film_views, rand());
