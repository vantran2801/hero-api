from fastapi import APIRouter, HTTPException, Query, status
from sqlmodel import Session, select

from app.database import SessionDep
from app.models import Hero, HeroCreate, HeroPublic, HeroUpdate, Team


router = APIRouter(prefix="/heroes", tags=["heroes"])

NOT_FOUND = {404: {"description": "Hero not found"}}


def get_hero_or_404(session: Session, hero_id: int) -> Hero:
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero


def check_team_exists(session: Session, team_id: int | None) -> None:
    if team_id is not None and not session.get(Team, team_id):
        raise HTTPException(status_code=400, detail=f"Team {team_id} does not exist")


@router.post(
    "",
    response_model=HeroPublic,
    status_code=status.HTTP_201_CREATED,
    summary="Create a hero",
    responses={400: {"description": "Team does not exist"}},
)
def create_hero(hero_in: HeroCreate, session: SessionDep):
    check_team_exists(session, hero_in.team_id)
    hero = Hero.model_validate(hero_in)
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero


@router.get("", response_model=list[HeroPublic], summary="List heroes")
def list_heroes(
    session: SessionDep,
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    min_age: int | None = None,
    team_id: int | None = None,
    name: str | None = None,
):
    statement = select(Hero).order_by(Hero.id)
    if min_age is not None:
        statement = statement.where(Hero.age >= min_age)
    if team_id is not None:
        statement = statement.where(Hero.team_id == team_id)
    if name:
        statement = statement.where(Hero.name.ilike(f"%{name}%"))
    return session.exec(statement.offset(offset).limit(limit)).all()


@router.get(
    "/{hero_id}",
    response_model=HeroPublic,
    summary="Get one hero",
    responses=NOT_FOUND,
)
def read_hero(hero_id: int, session: SessionDep):
    return get_hero_or_404(session, hero_id)


@router.patch(
    "/{hero_id}",
    response_model=HeroPublic,
    summary="Update a hero partially",
    responses={**NOT_FOUND, 400: {"description": "Team does not exist"}},
)
def update_hero(hero_id: int, hero_in: HeroUpdate, session: SessionDep):
    hero = get_hero_or_404(session, hero_id)
    data = hero_in.model_dump(exclude_unset=True)
    check_team_exists(session, data.get("team_id"))
    hero.sqlmodel_update(data)
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero


@router.delete(
    "/{hero_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a hero",
    responses=NOT_FOUND,
)
def delete_hero(hero_id: int, session: SessionDep):
    hero = get_hero_or_404(session, hero_id)
    session.delete(hero)
    session.commit()
