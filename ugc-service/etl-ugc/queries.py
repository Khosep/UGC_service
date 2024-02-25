INSERT_BUTCH = """
INSERT INTO shard.film_views (user_id, film_id, film_timestamp_sec, username, roles, email, first_name, last_name, event_time) VALUES
"""
COUNT_ROWS = """
SELECT COUNT(*) from shard.film_views"""