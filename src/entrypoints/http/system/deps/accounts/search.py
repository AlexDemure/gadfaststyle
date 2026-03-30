from src.application.usecases.accounts.search import Usecase


def dependency() -> Usecase:
    return Usecase()
