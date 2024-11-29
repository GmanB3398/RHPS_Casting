from typing import List, Optional

from pydantic import BaseModel, model_validator


class Cast(BaseModel):
    cast_id: int
    Frank: str
    Brad: str
    Janet: str
    Riff: str
    Magenta: str
    Columbia: str
    Scott: str
    Rocky: str
    Eddie: str
    Crim: Optional[str]
    Trixie: str
    Host: str
    Crew: str
    preference_score: Optional[int]

    @model_validator(mode="after")
    def check_crew(self):
        """
        Checks that all crew members are not casted
        """
        if len(self.Crew) == 0:
            raise ValueError("Need at least 1 crew member!")
        unique_actors = [
            self.Riff,
            self.Brad,
            self.Janet,
            self.Columbia,
            self.Magenta,
            self.Frank,
            self.Crim,
            self.Rocky,
            self.Eddie,
            self.Scott,
        ]
        for crew in self.Crew:
            if crew in unique_actors:
                raise RuntimeError(f"{crew} is both in cast and on crew!")
        return self

    @model_validator(mode="after")
    def check_unique_characters(self):
        """
        Checks that all characters are played
        by unique actors and are not on Crew
        """
        unique_characters = [
            self.Riff,
            self.Brad,
            self.Janet,
            self.Columbia,
            self.Magenta,
            self.Frank,
            self.Crim,
            self.Rocky,
            self.Eddie,
            self.Scott,
        ]
        if len(set(unique_characters)) != len(unique_characters):
            # Check Eddie-Scott
            unique_characters_no_scott = [
                self.Riff,
                self.Brad,
                self.Janet,
                self.Columbia,
                self.Magenta,
                self.Frank,
                self.Crim,
                self.Rocky,
                self.Eddie,
            ]
            if len(set(unique_characters_no_scott)) != len(unique_characters_no_scott):
                raise RuntimeError("Characters are doubled up! Try a different Cast")
        return self


def cast_equal(cast1: Cast, cast2: Cast) -> bool:
    role_list = [
        "Riff",
        "Brad",
        "Janet",
        "Columbia",
        "Scott",
        "Eddie",
        "Magenta",
        "Frank",
        "Rocky",
        "Crim",
    ]
    cast1_dict = cast1.model_dump()
    cast2_dict = cast2.model_dump()

    cast1_dict = {role: cast1_dict.get(role) for role in role_list}
    cast2_dict = {role: cast2_dict.get(role) for role in role_list}

    return cast1_dict == cast2_dict
