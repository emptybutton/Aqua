import typenv


_env = typenv.Env()
_env.read_env(".env")


is_dev = _env.bool("AQUA_DEV")
mongo_uri = _env.str("AQUA_MONGO_URI")
