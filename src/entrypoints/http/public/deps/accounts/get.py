from src.application.usecases.accounts.get.jwt import Usecase


def dependency() -> Usecase:
    return Usecase()
