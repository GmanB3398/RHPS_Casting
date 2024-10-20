from unittest import TestCase
import pytest

from pydantic import ValidationError

from src.classes.cast import Cast


class TestCastObject(TestCase):

    # @pytest.mark.unit_test
    def test_happy_path(self):
        data = {
            "cast_id": 1,
            "Riff": "Riff",
            "Brad": "Brad",
            "Janet": "Janet",
            "Columbia": "Columbia",
            "Scott": "Scott",
            "Eddie": "Eddie",
            "Magenta": "Magenta",
            "Frank": "Frank",
            "Crim": "Crim",
            "Trixie": "Trixie",
            "Rocky": "Rocky",
            "Host": "Host",
            "Crew": ["T1", "T2", "T3"],
        }
        test_cast = Cast(**data)
        assert test_cast.model_dump() == data

    # @pytest.mark.unit_test
    def overlapping_host_trixie(self):
        data = {
            "cast_id": 2,
            "Riff": "Riff",
            "Brad": "Brad",
            "Janet": "Janet",
            "Columbia": "Columbia",
            "Scott": "Scott",
            "Eddie": "Eddie",
            "Magenta": "Magenta",
            "Frank": "Frank",
            "Crim": "Crim",
            "Trixie": "Trixie",  # Allowed to overlap
            "Rocky": "Trixie",
            "Host": "Trixie",
            "Crew": ["T1", "T2", "T3"],
        }
        test_cast = Cast(**data)
        assert test_cast.model_dump() == data

    # @pytest.mark.unit_test
    def overlapping_eddie_scott(self):
        data = {
            "cast_id": 3,
            "Riff": "Riff",
            "Brad": "Brad",
            "Janet": "Janet",
            "Columbia": "Columbia",
            "Scott": "Eddie",
            "Eddie": "Eddie",
            "Magenta": "Magenta",
            "Frank": "Frank",
            "Crim": "Crim",
            "Trixie": "Trixie",  # Allowed to overlap
            "Rocky": "Trixie",
            "Host": "Trixie",
            "Crew": ["T1", "T2", "T3"],
        }
        test_cast = Cast(**data)
        assert test_cast.model_dump() == data

    # @pytest.mark.unit_test
    def crew_on_cast(self):
        data = {
            "cast_id": 4,
            "Riff": "Riff",
            "Brad": "Brad",
            "Janet": "Janet",
            "Columbia": "Columbia",
            "Scott": "Eddie",
            "Eddie": "Eddie",
            "Magenta": "Magenta",
            "Frank": "Frank",
            "Crim": "Crim",
            "Trixie": "Trixie",  # Allowed to overlap
            "Rocky": "Trixie",
            "Host": "Trixie",
            "Crew": ["Columbia", "T2", "T3"],
        }
        with pytest.raises(ValidationError):
            Cast(**data)

    # @pytest.mark.unit_test
    def doubled_cast_member(self):
        data = {
            "cast_id": 5,
            "Riff": "Riff",
            "Brad": "Brad",
            "Janet": "Janet",
            "Columbia": "Janet",
            "Scott": "Eddie",
            "Eddie": "Eddie",
            "Magenta": "Magenta",
            "Frank": "Frank",
            "Crim": "Crim",
            "Trixie": "Trixie",
            "Rocky": "Trixie",
            "Host": "Trixie",
            "Crew": ["T1", "T2", "T3"],
        }
        with pytest.raises(ValidationError):
            Cast(**data)

    # @pytest.mark.unit_test
    def no_crew(self):
        data = {
            "cast_id": 5,
            "Riff": "Riff",
            "Brad": "Brad",
            "Janet": "Janet",
            "Columbia": "Columbia",
            "Scott": "Eddie",
            "Eddie": "Eddie",
            "Magenta": "Magenta",
            "Frank": "Frank",
            "Crim": "Crim",
            "Trixie": "Trixie",
            "Rocky": "Rocky",
            "Host": "Trixie",
            "Crew": [],
        }
        with pytest.raises(ValidationError):
            Cast(**data)
