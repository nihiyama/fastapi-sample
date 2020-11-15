import logging

from app.db.init_db import init_db
from app.db.database import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    db = SessionLocal()
    init_db(db)


def main() -> None:
    logger.info("Creating superuser")
    init()
    logger.info("superuser created")


if __name__ == "__main__":
    main()
