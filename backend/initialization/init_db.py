from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from persistent.db.celebrity import Celebrity
from settings.settings import settings


with open(settings.paths.name_list, 'r') as file:
    DEFAULT_NAMES = [row.strip() for row in file.readlines()]

def init_db(names: list):
    engine = create_engine(f"sqlite:///{settings.paths.database}")
    
    with engine.begin() as conn:
        Celebrity.metadata.create_all(conn)
        conn.execute(text("INSERT INTO celebrities (id, name) VALUES (0, :name)"), {"name": names[0]})

    with Session(engine) as session:
        celebrities = [Celebrity(name=name) for name in names[1:]]
        session.add_all(celebrities)
        session.commit()

if __name__ == "__main__":
    init_db(DEFAULT_NAMES)
    print("База данных создана и заполнена!")