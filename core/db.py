import sqlite3
import tempfile
from pathlib import Path
from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)


def _sqlite_url(path: Path) -> str:
    return f"sqlite:///{path.resolve().as_posix()}"


def _can_use_sqlite_path(path: Path) -> bool:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(path) as connection:
            connection.execute("PRAGMA user_version")
        return True
    except sqlite3.Error:
        return False


def _resolve_database_path() -> Path:
    default_path = DATA_DIR / "app.db"
    if _can_use_sqlite_path(default_path):
        return default_path

    fallback_dir = Path(tempfile.gettempdir()) / "todo"
    fallback_path = fallback_dir / "app.db"
    fallback_dir.mkdir(parents=True, exist_ok=True)
    return fallback_path


DATABASE_PATH = _resolve_database_path()
DATABASE_URL = _sqlite_url(DATABASE_PATH)


class Base(DeclarativeBase):
    pass


engine = create_engine(
    DATABASE_URL,
    echo=False,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    class_=Session,
)


@contextmanager
def get_session() -> Iterator[Session]:
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
