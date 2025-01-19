import logging
from typing import Dict, List

import pandas as pd


class CastGenerator:

    def __init__(
        self, available_members: List[str], roles: pd.DataFrame, preferences: pd.DataFrame
    ):
        self.available_members = available_members
        self.roles = roles[roles.member.isin(self.available_members)]
        roles_long = pd.melt(self.roles, id_vars=["member"], var_name="role")
        roles_long = roles_long.loc[roles_long.value == 1]
        self.roles_long = roles_long

        self.preferences = preferences[preferences.member.isin(self.available_members)]
        self.preferences = self.preferences.set_index("member")
        self.roles_list = [
            "Frank",
            "Janet",
            "Brad",
            "Riff",
            "Magenta",
            "Columbia",
            "Scott",
            "Rocky",
            "Eddie",
            "Crim",
            "Trixie",
        ]
        self.full_casts: List[Dict] = []

    def get_all_casts(self):
        """ """
        # Choose In order of Least Represented Role
        # (likely smallest constraint)
        roles_by_amount = list(
            self.roles_long.groupby("role")
            .sum()
            .loc[self.roles_list]
            .sort_values("value", ascending=True)
            .index
        )
        for role in roles_by_amount:
            if role in ["Crim", "Crew", "Trixie", "Host"]:
                continue
            if role in ["Eddie", "Scott"]:
                self.assign_Sceddie(role)
            else:
                self.assign_standard_role(role)
        # Assign Crim, Trixie at the End
        self.assign_Crim()
        self.assign_Trixie()
        self.assign_Crew()
        self.get_preferences_for_casts()
        return pd.DataFrame(self.full_casts).sort_values("preference_score", ascending=False)

    def eligible_members(self, role: str) -> List:
        return (
            self.roles["member"][self.roles[role] == 1].rename(index=role, inplace=False).to_list()
        )

    def assign_Sceddie(self, role: str) -> None:
        casts: List[Dict[str, str]] = []
        anti_role = "Scott" if role == "Eddie" else "Eddie"
        actors = self.eligible_members(role)
        for actor in actors:
            if len(self.full_casts) == 0:
                casts.append({role: actor})
            else:
                for cast_ref in self.full_casts:
                    cast = cast_ref.copy()
                    if actor not in cast.values() or actor == cast.get(anti_role):
                        cast.update({role: actor})
                        casts.append(cast)
        self.full_casts = casts

    def assign_standard_role(self, role: str) -> None:
        casts: List[Dict[str, str]] = []
        actors = self.eligible_members(role).copy()
        for actor in actors:
            if len(self.full_casts) == 0:
                casts.append({role: actor})
            else:
                for cast_ref in self.full_casts:
                    cast = cast_ref.copy()
                    if actor not in cast.values():
                        cast.update({role: actor})
                        casts.append(cast)
        self.full_casts = casts

    def assign_Crim(self) -> None:
        casts: List[Dict[str, str]] = []
        actors = self.eligible_members("Crim").copy()
        for cast_ref in self.full_casts:
            cast = cast_ref.copy()
            for actor in actors:
                if actor not in cast.values():
                    cast.update({"Crim": actor})
                    casts.append(cast)
            cast.update({"Crim": ""})
            casts.append(cast)

        self.full_casts = casts

    def assign_Trixie(self):
        casts: List[Dict[str, str]] = []
        actors = self.eligible_members(role="Trixie")
        for actor in actors:
            for cast_ref in self.full_casts:
                cast = cast_ref.copy()
                if actor not in (cast["Brad"], cast["Janet"]):
                    cast.update({"Trixie": actor})
                    casts.append(cast)
        self.full_casts = casts

    def assign_Crew(self):
        for cast in self.full_casts:
            crew: List[str] = [
                member for member in self.available_members if member not in cast.values()
            ]
            cast.update({"Crew": crew})

    def get_preferences_for_casts(self):
        # match preference_df to Cast
        for cast in self.full_casts:
            score = 0.0
            for role, actor in cast.items():
                mult: float
                if role == "Crew":
                    mult = 0.25
                elif role in ("Eddie", "Scott"):
                    mult = 0.5
                elif role in ("Crim", "Trixie"):
                    mult = 0.75
                else:
                    mult = 1

                if actor == "":  # Crimless case
                    score -= 1.0
                try:
                    if isinstance(actor, list):
                        for crew in actor:
                            score += pd.to_numeric(self.preferences.loc[crew, role]) * mult
                    else:
                        score += pd.to_numeric(self.preferences.loc[actor, role]) * mult
                except KeyError:
                    logging.debug("Score Not Found")

            # sum up preferences
            # return Cast with sum object
            cast.update({"preference_score": score})
