from sqlmodel import Field, SQLModel, create_engine, Session, select
from typing import Optional
from datetime import datetime
from typing import List
from sqlmodel import select

# Data model
class Battlecard(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    company: str
    extract: str
    keywords: str
    strengths: str
    weaknesses: str
    differentiators: str
    action: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# Setup DB engine
sqlite_file_name = "battlecards.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=False)

# Create tables
def create_db():
    SQLModel.metadata.create_all(engine)

# Save new battlecard
def save_battlecard(card: Battlecard):
    with Session(engine) as session:
        session.add(card)
        session.commit()


def get_all_battlecards() -> List[Battlecard]:
    with Session(engine) as session:
        statement = select(Battlecard).order_by(Battlecard.timestamp.desc())
        return session.exec(statement).all()
