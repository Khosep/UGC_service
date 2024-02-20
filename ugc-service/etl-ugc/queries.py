INSERT_BUTCH = """
INSERT INTO shard.film_views (user_id, film_id, film_ts, event_time) VALUES
"""
COUNT_ROWS = """
SELECT COUNT(*) from shard.film_views"""