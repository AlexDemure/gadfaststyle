from src.application.usecases.accounts.update import Usecase


def dependency() -> Usecase:
    return Usecase()
