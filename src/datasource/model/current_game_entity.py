from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from datasource.database import Base
from datetime import datetime


class CurrentGameEntity(Base):
    __tablename__ = "current_games"

    id = Column(Integer, primary_key=True, autoincrement=True)
    game_id = Column(String(36), unique=True, nullable=False, index=True)
    game_field_id = Column(Integer, ForeignKey("game_fields.id"), nullable=False)

    game_type = Column(String(10), nullable=False)
    game_state = Column(String(30), nullable=False)

    player1_id = Column(PG_UUID(as_uuid=True), nullable=False)
    player2_id = Column(PG_UUID(as_uuid=True), nullable=True)
    player1_symbol = Column(Integer, nullable=False)
    player2_symbol = Column(Integer, nullable=False)

    current_player_id = Column(PG_UUID(as_uuid=True), nullable=True)
    winner_id = Column(PG_UUID(as_uuid=True), nullable=True)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    game_field = relationship("GameFieldEntity", lazy="joined")

    def __repr__(self):
        return (
            f"<CurrentGameEntity(game_id='{self.game_id}', "
            f"game_type='{self.game_type}', game_state='{self.game_state}')>"
        )
