from src.application.usecases.accounts.create import Usecase


def dependency() -> Usecase:
    return Usecase()
