from pytest import fixture

from aqua.domain.model.core.aggregates.user.root import User
from aqua.infrastructure.periphery.pymongo.document import Document


@fixture
def users(user1: User, user2: User) -> list[User]:
    return [user1, user2]


@fixture
def user_documents(
    user1_document: Document,
    user2_document: Document,
) -> list[Document]:
    return [user1_document, user2_document]
