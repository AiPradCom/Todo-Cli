from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class Todo:
    """A single todo item"""
    id: int
    title: str
    done: bool
    created_at: str

    @classmethod
    def create(cls, id, title):
        """Create a new todo with the current timestamp"""
        return cls(
            id=id,
            title=title,
            done=False,
            created_at=datetime.now().isoformat()
        )

    def to_dict(self):
        """Convert to dictionary for JSON storage"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        """Load from dictionary"""
        return cls(**data)
