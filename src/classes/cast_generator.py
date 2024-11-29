import pandas as pd
import logging
import json
from typing import List, Dict
import tqdm
import copy
from pydantic import ValidationError
import numpy as np
from src.classes.cast import Cast, cast_equal


class CastGenerator:

    def __init__(self, available_members: List[str] = []):
        self.roles = pd.read_csv("data/roles_example.csv")
        self.preferences = pd.read_csv(
            "data/pref_example.csv"
        )  # Will eventually be related to show date
        self.available_members = available_members
        self.roles = self.roles[self.roles.member.isin(self.available_members)]
        roles_long = pd.melt(self.roles, id_vars="member", var_name="role")
        roles_long = roles_long.loc[roles_long.value == 1]
        self.roles_long = roles_long

        self.preferences = self.preferences[
            self.preferences.member.isin(self.available_members)
        ]
        self.preferences = self.preferences.set_index("member")
        self.base_cast = {
            "Riff": "",
            "Brad": "",
            "Janet": "",
            "Columbia": "",
            "Scott": "",
            "Eddie": "",
            "Magenta": "",
            "Frank": "",
            "Crim": "",
            "Trixie": "",
            "Rocky": "",
        }
        self.roles_list = list(self.base_cast.keys())

    def eligible_members(self, role: str) -> List:
        return (
            self.roles["member"][self.roles[role] == 1]
            .rename(index=role, inplace=False)
            .to_list()
        )

    def assign_Sceddie(self, cast: Dict[str, str], role: str) -> Dict:
        anti_role = "Scott" if role == "Eddie" else "Eddie"
        actors = self.eligible_members(role)
        valid = False
        it = 0
        anti_actor = cast.pop(anti_role)
        while (not valid) and it < 100:
            actor = str(np.random.choice(actors))
            if actor not in cast.values():
                cast[role] = actor
                cast[anti_role] = anti_actor
                valid = True
            else:
                it += 1
        if valid:
            return cast
        elif anti_actor != "":
            cast[role] = anti_actor
            cast[anti_role] = anti_actor
        else:
            raise LookupError

    def assign_standard_role(self, cast: Dict[str, str], role: str) -> Dict:
        actors = self.eligible_members(role)
        valid = False
        it = 0
        while (not valid) and it < 100:
            actor = str(np.random.choice(actors))
            if actor not in cast.values():
                cast[role] = actor
                valid = True
            else:
                it += 1
        if valid:
            return cast
        else:
            raise LookupError

    def assign_extra_role(self, cast: Dict[str, str], role: str) -> Dict:
        actors = self.eligible_members(role)
        actor = str(np.random.choice(actors))
        cast[role] = actor
        return cast

    def cast_in_casts(self, cast: Cast, casts: List[Cast]):
        for old_cast in casts:
            equal = cast_equal(cast, old_cast)
            if equal:
                return True
        return False

    def get_all_casts(self, it: int = 5000):
        """ """

        # Choose In order of Least Represented Role
        # (likely smallest constraint)
        roles_by_amount = list(
            self.roles_long.groupby("role")
            .sum("value")
            .loc[self.roles_list]
            .sort_values("value", ascending=True)
            .index
        )
        casts: List = []
        for i in tqdm.trange(it):
            try:
                if i > round(it / 2):
                    np.random.shuffle(roles_by_amount)
                cast = copy.copy(self.base_cast)
                cast["cast_id"] = i
                for role in roles_by_amount:
                    # Get All Members who Can play that role
                    if role in ["Crim", "Crew", "Trixie", "Host"]:
                        continue
                    if role in ["Eddie", "Dr. Scott"]:
                        cast = self.assign_Sceddie(cast, role)
                    else:
                        cast = self.assign_standard_role(cast, role)
                # Assign Crim at the End
                try:
                    cast = self.assign_standard_role(cast, "Crim")
                except LookupError:
                    logging.debug("Creating Crimless Cast")
                    pass
                cast = self.assign_extra_role(cast, "Trixie")
                cast["Crew"] = [
                    member
                    for member in self.available_members
                    if member not in cast.values()
                ]
                cast["Crew"] = ", ".join(cast["Crew"])
                cast = self.assign_extra_role(cast, "Host")
                cast = self.get_preference_for_cast(cast)
                cast = Cast(**cast)
                if not self.cast_in_casts(cast, casts):
                    casts.append(cast)
                    final_it = i

            except ValidationError as val:
                logging.error(
                    f"Invalid Cast Passed to Validator. Validation Error: {val}"
                )
                with open("data/error_cast.json", "w+") as err:
                    json.dump(cast, fp=err, indent=4)
            except LookupError:
                logging.debug(f"Could not find an Actor to play {role}")

        self.all_casts = casts
        logging.info(f"Last Unique Cast after {final_it} iterations.")

        return (
            pd.DataFrame([c.model_dump() for c in casts])
            .drop(columns=["cast_id", "Host"])
            .sort_values("preference_score", ascending=False)
        )

    def get_preference_for_cast(self, cast: Dict[str, str]) -> Dict[str, str]:

        # match preference_df to Cast
        score = 0
        for role, actor in cast.items():
            if role == "cast_id":
                continue
            if actor == "":  # Crimless case
                continue  # TODO: Ask laurel if we should penalize a crimless cast
            try:
                if type(actor) is list:
                    for crew in actor:
                        score += int(self.preferences.loc[actor, role].iloc[0])
                else:
                    score += int(self.preferences.loc[actor, role])
            except KeyError:
                logging.debug("Score Not Found")

        # sum up preferences
        # return Cast with sum object
        cast["preference_score"] = score
        return cast
