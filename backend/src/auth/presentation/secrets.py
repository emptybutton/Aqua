from src.shared.infrastructure.envs import Env, existing


jwt_secret = existing(Env.jwt_secret.value)
