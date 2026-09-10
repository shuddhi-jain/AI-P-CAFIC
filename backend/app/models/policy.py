from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import DateTime, Enum as SQLEnum, ForeignKey, Numeric, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class PolicyType(str,PyEnum):
    HEALTH = "health"
    LIFE = "life"

class PolicyStatus(str,PyEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class Policy(Base):
    __tablename__ = "policies"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    policy_number: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    policy_type: Mapped[PolicyType] = mapped_column(SQLEnum(PolicyType, name="policy_type"), nullable=False, default=PolicyType.HEALTH)
    insurer_name: Mapped[str] = mapped_column(String(100), nullable=False)
    insurer_id: Mapped[str] = mapped_column(String(100), nullable=True)
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    coverage_amount: Mapped[float] = mapped_column(Numeric(precision=12, scale=2),nullable=False)
    policy_document_url: Mapped[str] = mapped_column(String(200), nullable=True)
    status: Mapped[PolicyStatus] = mapped_column(SQLEnum(PolicyStatus, name="policy_status"), nullable=False, default=PolicyStatus.ACTIVE)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

