import dataclasses
import pytest

from .templatetags.custom_filters import censor


########################
# TEST FOR CENSOR FILTER
########################


@dataclasses.dataclass
class Case:
    word: str
    censored_word: str

    def __str__(self) -> str:
        return f"censor_{self.word}"


TEST_CASES = [
    Case(word='Предложение со словом редис.', censored_word='Предложение со словом р****.'),
    Case(word='Редис в начале предложения', censored_word='Р**** в начале предложения'),
    Case(word='редиска, редиски и редисками', censored_word='р******, р****** и р********'),
    Case(word='заредись', censored_word='заредись'),
    Case(word='Предложение без цензуры', censored_word='Предложение без цензуры'),
    Case(word='рЕдИс', censored_word='р****')
]


@pytest.mark.parametrize("t", TEST_CASES, ids=str)
def test_name(t: Case) -> None:
    censured = censor(t.word)
    assert censured == t.censored_word
