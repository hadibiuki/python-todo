from core.db import Base, engine

# مهم: import کردن مدل‌ها تا SQLAlchemy آن‌ها را register کند
from modules.tasks.model import Task  # noqa: F401


def init_db() -> None:
    Base.metadata.create_all(bind=engine)