import typenv


_env = typenv.Env()
_env.read_env(".env")


is_dev = _env.bool("ENTRYPOINT_DEV")
