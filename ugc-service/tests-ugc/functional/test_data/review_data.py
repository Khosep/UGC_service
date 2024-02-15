reviews = (
    {
        "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "film_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "review": "first",
        "score": 1,
    },
    {
        "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "film_id": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
        "review": "second",
        "score": 2,
    },
    {
        "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
        "film_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "review": "third",
        "score": 3,
    },
    {
        "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
        "film_id": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
        "review": "four",
        "score": 4,
    },
)

error_reviews = (
    {},
    {
        "film_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "review": "first",
        "score": 1,
    },
    {
        "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "review": "second",
        "score": 2,
    },
    {
        "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
        "film_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "score": 3,
    },
    {
        "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
        "film_id": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
        "review": "four",
    },
)

check_reviews_in_db_sql = """select * from user_film_review;"""
