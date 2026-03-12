# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  space_crew.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: stmaire <stmaire@student.42.fr>           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/11 17:32:30 by stmaire         #+#    #+#               #
#  Updated: 2026/03/11 17:46:45 by stmaire         ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from enum import Enum
from typing import List
from pydantic import ValidationError, BaseModel, model_validator, Field
from datetime import datetime


class Rank(Enum):
    CADET = 'cadet'
    OFFICER = 'officer'
    LIEUTENANT = 'lieutenant'
    CAPTAIN = 'captain'
    COMMANDER = 'commander'


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = True


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: List[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = "planned"
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode='after')
    def validate_mission(self) -> 'SpaceMission':
        if not self.mission_id.startswith('M'):
            raise ValueError("Mission ID must start with 'M'")

        comm_or_captain: bool = False
        for crew_member in self.crew:
            if (
                crew_member.rank == Rank.COMMANDER
                or crew_member.rank == Rank.CAPTAIN
            ):
                comm_or_captain = True
        if not comm_or_captain:
            raise ValueError("Mission must have "
                             "at least one Commander or Captain")
        if self.duration_days > 365:
            xp_crew_member = 0
            for crew_member in self.crew:
                if crew_member.years_experience >= 5:
                    xp_crew_member += 1
            if not xp_crew_member >= len(self.crew) / 2:
                raise ValueError("Long missions "
                                 "(> 365 days) need 50% "
                                 "experienced crew (5+ years)")
        for crew_member in self.crew:
            if not crew_member.is_active:
                raise ValueError("All crew members must be active")

        return self


def main() -> None:
    print("Space Mission Crew Validation")
    print("=========================================")

    try:
        sconnor = CrewMember(
            member_id="M001",
            name="Sarah Connor",
            rank=Rank.COMMANDER,
            age=32,
            specialization="Mission Command",
            years_experience=10,
            is_active=True
        )

        jsmith = CrewMember(
            member_id="M002",
            name="John Smith",
            rank=Rank.LIEUTENANT,
            age=28,
            specialization="Navigation",
            years_experience=8,
            is_active=True
        )

        ajohnson = CrewMember(
            member_id="M003",
            name="Alice Johnson",
            rank=Rank.OFFICER,
            age=41,
            specialization="Engineering",
            years_experience=20,
            is_active=True
        )

        crew_members = [sconnor, jsmith, ajohnson]

        mission = SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date=datetime(2024, 3, 22),
            duration_days=900,
            crew=crew_members,
            budget_millions=2500.0
        )

        print("Valid mission created:")
        print(f"Mission: {mission.mission_name}")
        print(f"ID: {mission.mission_id}")
        print(f"Destination: {mission.destination}")
        print(f"Duration: {mission.duration_days} days")
        print(f"Budget: ${mission.budget_millions:.1f}M")
        print(f"Crew size: {len(mission.crew)}")
        print("Crew members:")
        for member in mission.crew:
            print(f"- {member.name} ({member.rank.value}) "
                  f"- {member.specialization}")

    except ValidationError as e:
        print(f"Unexpected error: {e}")

    print("\n=========================================")
    print("Expected validation error:")
    try:
        sconnor.rank = Rank.OFFICER

        crew_members = [sconnor, jsmith, ajohnson]

        SpaceMission(
                mission_id="M2024_MARS",
                mission_name="Mars Colony Establishment",
                destination="Mars",
                launch_date=datetime(2024, 3, 22),
                duration_days=900,
                crew=crew_members,
                budget_millions=2500.0
            )

    except ValidationError as e:
        msg = e.errors()[0]['msg']
        clean_msg = msg.replace("Value error, ", "")
        print(clean_msg)


if __name__ == "__main__":
    main()
