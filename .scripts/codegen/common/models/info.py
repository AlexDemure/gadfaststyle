import dataclasses


@dataclasses.dataclass(frozen=True)
class ModelInfo:
    model: str
    table: str
    collection: str

    @property
    def title(self) -> str:
        return f"{self.model} -> /{self.collection}"
