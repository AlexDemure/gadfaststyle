class ModuleDisabled(Exception):
    module: str

    def __str__(self) -> str:
        return f"{self.module} is disabled"
