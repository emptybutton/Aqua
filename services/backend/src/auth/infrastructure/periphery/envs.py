import typenv


_env = typenv.Env()
_env.read_env(".env")


is_dev = _env.bool("AUTH_DEV")

postgres_database = _env.str("AUTH_POSTGRES_DATABASE")
postgres_username = _env.str("AUTH_POSTGRES_USERNAME")
postgres_password = _env.str("AUTH_POSTGRES_PASSWORD")
postgres_host = _env.str("AUTH_POSTGRES_HOST")
postgres_port = _env.int("AUTH_POSTGRES_PORT")
postgres_echo = _env.bool("AUTH_POSTGRES_ECHO")
