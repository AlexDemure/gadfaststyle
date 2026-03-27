from src.application.usecases.accounts.delete import Usecase


def dependency() -> Usecase:
    return Usecase()
