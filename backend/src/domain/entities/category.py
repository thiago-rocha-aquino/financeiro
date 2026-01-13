from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class Category:
    """Entidade de domínio que representa uma categoria de transação."""

    name: str
    user_id: UUID
    color: str = "#6366f1"
    icon: str = "tag"
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    def update(self, name: Optional[str] = None, color: Optional[str] = None, icon: Optional[str] = None) -> None:
        if name:
            self.name = name
        if color:
            self.color = color
        if icon:
            self.icon = icon
        self.updated_at = datetime.utcnow()
