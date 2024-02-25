-- NODE 1 (shard)
CREATE DATABASE shard;
CREATE TABLE shard.film_views (user_id Nullable(UUID), film_id UUID, film_timestamp_sec Int64, roles Array(String), email String, username String, first_name String, last_name String, event_time DateTime DEFAULT now()) Engine=ReplicatedMergeTree('/clickhouse/tables/shard1/film_views', 'replica_1') PARTITION BY toYYYYMMDD(event_time) ORDER BY film_id;
CREATE TABLE default.film_views (user_id Nullable(UUID), film_id UUID, film_timestamp_sec Int64, roles Array(String), email String, username String, first_name String, last_name String, event_time DateTime DEFAULT now()) ENGINE = Distributed('company_cluster', '', film_views, rand());
