import typing

from src.domain.models import Account


def serialize(account: object) -> Account:
    return Account.model_validate(account, from_attributes=True)


def decrypt(decrypter: typing.Callable[..., typing.Any], account: Account) -> Account:
    for key, value in Account.decrypt(
        decrypter=decrypter,
        external_id=account.external_id,
    ).items():
        setattr(account, key, value)

    return account
