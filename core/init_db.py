from core.db import Base, engine

# مهم: مدل‌ها باید import شوند تا در metadata ثبت شوند
from modules.tasks.model import Task  # noqa: F401


def init_db() -> None:
    Base.metadata.create_all(bind=engine)