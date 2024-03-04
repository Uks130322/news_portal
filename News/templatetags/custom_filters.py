from django import template
import re

BAD_WORD = 'редис'

register = template.Library()


class CensorException(Exception):
    pass


def censor_repl(word: (re.Match, str)) -> (re.Match, str):
    """Replace all letters but first with *"""

    if isinstance(word, re.Match):
        return word.group()[0] + '*' * (word.end() - word.start() - 1)
    elif isinstance(word, str):
        return word[0] + '*' * (len(word) - 1)
    else:
        raise CensorException('Filter can work only with str format')


@register.filter()
def censor(value: str) -> str:
    """Find all coincidences and replace it with censor_repl function"""

    try:
        if not isinstance(value, str):
            raise CensorException('Filter can work only with str format')
        pattern = re.compile(fr"\b{BAD_WORD}[а-я]{{0,5}}\b", re.IGNORECASE)
        result = re.sub(pattern, censor_repl, value)
        return result
    except CensorException as error:
        print(error)
        pass

