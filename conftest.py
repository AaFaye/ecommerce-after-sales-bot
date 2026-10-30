"""测试全局配置：所有测试使用独立的内存数据库，不落盘、不污染本地 after_sales.db。"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db import Base, engine as _orig_engine, SessionLocal as _orig_sessionlocal
import main as app_main
from api import main as api_main


@pytest.fixture(autouse=True)
def _isolate_db(monkeypatch):
    """每个测试启动一张全新的内存表，并让所有模块的 Session 引用指向它。"""
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    Base.metadata.create_all(bind=engine)

    # 替换全局对象（含 api.main 在模块加载时拷贝的引用）
    monkeypatch.setattr(app_main, "engine", engine)
    monkeypatch.setattr(app_main, "SessionLocal", SessionLocal)
    monkeypatch.setattr(api_main, "SessionLocal", SessionLocal)
    monkeypatch.setattr("db.engine", engine)
    monkeypatch.setattr("db.SessionLocal", SessionLocal)

    yield SessionLocal

    Base.metadata.drop_all(bind=engine)
