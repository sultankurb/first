from sqlalchemy import ForeignKey, Integer, UniqueConstraint, BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base


class CourseSub(Base):
    __table_args__ = (
        UniqueConstraint(
            'course_id',
            'user_id',
            name='idx_unique_course_user',
        ),
    )
    course_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(column="courses.pk", ondelete="CASCADE"),
    )
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        default=0
    )
