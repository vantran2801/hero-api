from fastapi import APIRouter, HTTPException, status

from app.database import SessionDep
from app.models import Hero, Mission, MissionCreate, MissionPublic


router = APIRouter(tags=["missions"])


@router.post(
    "/missions",
    response_model=MissionPublic,
    status_code=status.HTTP_201_CREATED,
    summary="Create a mission",
)
def create_mission(mission_in: MissionCreate, session: SessionDep):
    mission = Mission.model_validate(mission_in)
    session.add(mission)
    session.commit()
    session.refresh(mission)
    return mission


@router.post(
    "/heroes/{hero_id}/missions/{mission_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Assign a mission to a hero",
    responses={404: {"description": "Hero or mission not found"}},
)
def assign_mission(hero_id: int, mission_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    mission = session.get(Mission, mission_id)
    if not hero or not mission:
        raise HTTPException(status_code=404, detail="Hero or mission not found")
    if mission not in hero.missions:
        hero.missions.append(mission)
        session.add(hero)
        session.commit()


@router.get(
    "/heroes/{hero_id}/missions",
    response_model=list[MissionPublic],
    summary="List a hero's missions",
    responses={404: {"description": "Hero not found"}},
)
def list_hero_missions(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero.missions
