from aqua.domain.framework.fp.env import Env, env


def test_env() -> None:
    wrapped = env("context")

    result = wrapped(4)

    assert result == Env("context", 4)
