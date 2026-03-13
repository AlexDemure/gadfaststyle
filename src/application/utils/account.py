import typing

from src.domain.models import Account


def decrypt(decrypter: typing.Callable[..., typing.Any], account: Account) -> Account:
    for key, value in Account.decrypt(
        decrypter=decrypter,
        external_id=account.external_id,
    ).items():
        setattr(account, key, value)

    return account
