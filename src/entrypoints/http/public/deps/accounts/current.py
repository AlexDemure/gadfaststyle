from src.application.usecases.accounts.current import Usecase


def dependency() -> Usecase:
    return Usecase()
