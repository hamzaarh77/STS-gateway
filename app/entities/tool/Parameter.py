from dataclasses import dataclass


@dataclass
class Parameter:
    name: str
    type: str
    description: dict
    required: bool

    def __str__(self):
        return f"{self.name} {self.type} {self.description} {self.required}"
