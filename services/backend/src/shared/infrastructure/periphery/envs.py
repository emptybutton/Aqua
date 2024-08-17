import typenv


_env = typenv.Env()
_env.read_env(".env")


class Env:
    postgres_database = _env.str("POSTGRES_DATABASE")
    postgres_username = _env.str("POSTGRES_USERNAME")
    postgres_password = _env.str("POSTGRES_PASSWORD")
    postgres_host = _env.str("POSTGRES_HOST")
    postgres_port = _env.int("POSTGRES_PORT")
    postgres_echo = _env.bool("POSTGRES_ECHO")
