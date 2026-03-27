from src.application.usecases.accounts.list import Usecase


def dependency() -> Usecase:
    return Usecase()
