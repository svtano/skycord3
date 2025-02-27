"""Internal language utilities for the library."""

import inspect
from functools import cache
from pathlib import Path

from ..logs import log
from .config import SkyConfig
from .language.languages import load_lang


def plural_de(amount: int, word: str, relative: bool = True) -> str:
    """Pluralize a given word (German).

    Parameters
    ----------
    amount:
        The amount to check.
    word:
        The word to pluralize.
    relative:
        Whether to use relative time. Defaults to ``True``.

    Examples
    --------
    >>> plural_de(1, "Tag")
    'Tag'
    >>> plural_de(2, "Tag")  # Relative: "Seit 5 Tagen"
    'Tagen'
    >>> plural_de(2, "Tag", relative=False)  # Not relative: "5 Tage"
    'Tage'
    """
    if amount != 1:
        if not word.endswith("e"):
            word += "e"

        if relative:
            return f"{word}n"

    return word


def plural_en(amount: int, word: str) -> str:
    """Pluralize a given word (English).

    Parameters
    ----------
    amount:
        The amount to check.
    word:
        The word to pluralize.

    Returns
    -------
    :class:`str`
        The pluralized word.
    """
    if amount != 1:
        return f"{word}s"
    return word


def plural_es(amount: int, word: str) -> str:
    """Pluralize a given word in Spanish.

    Parameters
    ----------
    amount:
        The amount to check.
    word:
        The word to pluralize.

    Returns
    -------
    :class:`str`
        The pluralized word.
    """
    if amount != 1:
        if word.endswith("ión"):
            return f"{word[:-3]}iones"
        elif word.endswith("z"):
            return f"{word[:-1]}ces"
        else:
            return f"{word}s"
    return word


def plural_fr(amount: int, word: str) -> str:
    """Pluralize a given word in French.

    Parameters
    ----------
    amount:
        The amount to check.
    word:
        The word to pluralize.

    Returns
    -------
    :class:`str`
        The pluralized word.
    """
    if amount != 1:
        if word.endswith("al"):
            return f"{word}aux"
        elif word.endswith("ail"):
            return f"{word}s"
        else:
            return f"{word}s"
    return word


def tp(key: str, amount: int, *args: str, relative: bool = True) -> str:
    """Load a string in the selected language and pluralize it.

    Parameters
    ----------
    key:
        The text to load.
    amount:
        The amount to check.
    *args:
        The arguments to format the string with.
    relative:
        Whether to use relative time. Defaults to ``True``.
    """
    word = t(key, *args)
    lang = get_lang()

    if lang == "de":
        return plural_de(amount, word, relative)
    elif lang == "es":
        return plural_es(amount, word)
    elif lang == "fr":
        return plural_fr(amount, word)
    else:
        return plural_en(amount, word)


def t(key: str, *args: str):
    """Load a string in the selected language.

    Parameters
    ----------
    key:
        The text to load.
    *args:
        The arguments to format the string with.
    """
    n = 1
    origin_file = Path(inspect.stack()[n].filename).stem

    while origin_file == Path(__file__).stem:
        n += 1
        origin_file = Path(inspect.stack()[n].filename).stem

    lang = get_lang()

    try:
        string = load_lang(lang)[origin_file][key]
        if not string:
            return None
        return string.format(*args)
    except KeyError:
        # fallback to english if the key is not in the custom language file
        # provided by the user
        log.warn(f"Key '{key}' not found in language file '{lang}'. Falling back to 'en'.")
        return load_lang("en")[origin_file][key].format(*args)


@cache
def get_lang():
    """Get the language from the config class."""
    return SkyConfig.lang


def set_lang(lang: str):
    """Set the language for the bot.

    Parameters
    ----------
    lang:
        The language to set.
    """
    SkyConfig.lang = lang
