from datetime import datetime, timezone
from enum import Enum

from sqlmodel import Field, Relationship, SQLModel


# ---------- Team ----------
class TeamBase(SQLModel):
    name: str = Field(index=True, unique=True)
    headquarters: str


class Team(TeamBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    heroes: list["Hero"] = Relationship(back_populates="team")


class TeamCreate(TeamBase):
    pass


class TeamPublic(TeamBase):
    id: int


# ---------- Hero <-> Mission link (many-to-many) ----------
class HeroMissionLink(SQLModel, table=True):
    hero_id: int | None = Field(default=None, foreign_key="hero.id", primary_key=True)
    mission_id: int | None = Field(default=None, foreign_key="mission.id", primary_key=True)


# ---------- Hero ----------
def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class HeroStatus(str, Enum):
    active = "active"
    retired = "retired"

class HeroBase(SQLModel):
    name: str = Field(index=True, min_length=1, max_length=100)
    age: int | None = Field(default=None, ge=0, le=150)
    power: str | None = Field(default=None, max_length=200)
    team_id: int | None = Field(default=None, foreign_key="team.id")
    status: HeroStatus = HeroStatus.active

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "name": "Tony",
                "age": 45,
                "power": "powered armor",
                "team_id": 1,
                "status": "active",
                "secret_name": "Iron Man",
            }]
        }
    }


class Hero(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    secret_name: str

    team: Team | None = Relationship(back_populates="heroes")
    missions: list["Mission"] = Relationship(back_populates="heroes",
                                             link_model=HeroMissionLink)
    created_at: datetime = Field(default_factory=utc_now)


class HeroCreate(HeroBase):
    secret_name: str


class HeroPublic(HeroBase):
    id: int
    created_at: datetime


class HeroUpdate(SQLModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    age: int | None = Field(default=None, ge=0, le=150)
    power: str | None = Field(default=None, max_length=200)
    team_id: int | None = None
    secret_name: str | None = None
    status: HeroStatus | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "name": "Tony Stark",
                "age": 46,
                "status": "retired",
            }]
        }
    }


# ---------- Mission ----------
class MissionBase(SQLModel):
    title: str


class Mission(MissionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    heroes: list[Hero] = Relationship(back_populates="missions",
                                      link_model=HeroMissionLink)


class MissionCreate(MissionBase):
    pass


class MissionPublic(MissionBase):
    id: int
