# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  space_station.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: stmaire <stmaire@student.42.fr>           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/11 13:14:32 by stmaire         #+#    #+#               #
#  Updated: 2026/03/11 15:06:08 by stmaire         ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from pydantic import BaseModel, Field, ValidationError, ConfigDict
from datetime import datetime
from typing import Optional


class SpaceStation (BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = True
    notes: Optional[str] = Field(None, max_length=200)


def main() -> None:
    print("Space Station Data Validation")
    print("========================================")

    try:
        iss = SpaceStation(
            station_id="ISS001",
            name="International Space Station",
            crew_size=6,
            power_level=85.5,
            oxygen_level=92.3,
            is_operational=True,
            last_maintenance=datetime.now(),
            notes=None
            )

        print("Valid station created:")
        print(f"ID: {iss.station_id}")
        print(f"Name: {iss.name}")
        print(f"Crew: {iss.crew_size} people")
        print(f"Power: {iss.power_level}%")
        print(f"Oxygen: {iss.oxygen_level}%")
        status = "Operational" if iss.is_operational else "Non operational"
        print(f"Status: {status}")

    except ValidationError as e:
        print(f"Unexpected error: {e}")

    print("\n========================================")

    try:
        SpaceStation(
            station_id="ISS002",
            name="International Space Station",
            crew_size=22,
            power_level=85.5,
            oxygen_level=92.3,
            is_operational=True,
            last_maintenance=datetime.now(),
            notes=None
        )

    except ValidationError as e:
        print("Expected validation error:")
        print(e.errors()[0]['msg'])


if __name__ == "__main__":
    main()
