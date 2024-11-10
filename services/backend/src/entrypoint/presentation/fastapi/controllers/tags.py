from enum import Enum


class Tag(Enum):
    current_user_endpoints = "me"
    other_users_endpoints = "others"
    access_endpoints = "access"
