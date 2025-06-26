TORTOISE_ORM = {
    "connections": {
        "default": "postgres://postgres:postgres@localhost:5432/aio",
    },
    "apps": {
        "models": {
            "models": ["models"],
            "default_connection": "default",
        },
    },
}