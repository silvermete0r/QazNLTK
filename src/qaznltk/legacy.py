from __future__ import annotations

from .exceptions import InvalidInputError


CYRILLIC_TO_ISO9_MAPPING = {
    'А': 'A', 'а': 'a',
    'Ә': 'A̋', 'ә': 'a̋',
    'Б': 'B', 'б': 'b',
    'В': 'V', 'в': 'v',
    'Г': 'G', 'г': 'g',
    'Ғ': 'Ġ', 'ғ': 'ġ',
    'Д': 'D', 'д': 'd',
    'Е': 'E', 'е': 'e',
    'Ё': 'Ë', 'ё': 'ë',
    'Ж': 'Ž', 'ж': 'ž',
    'З': 'Z', 'з': 'z',
    'И': 'I', 'и': 'i',
    'Й': 'J', 'й': 'j',
    'К': 'K', 'к': 'k',
    'Қ': 'K̦', 'қ': 'k̦',
    'Л': 'L', 'л': 'l',
    'М': 'M', 'м': 'm',
    'Н': 'N', 'н': 'n',
    'Ң': 'N̦', 'ң': 'n̦',
    'О': 'O', 'о': 'o',
    'Ө': 'Ô', 'ө': 'ô',
    'П': 'P', 'п': 'p',
    'Р': 'R', 'р': 'r',
    'С': 'S', 'с': 's',
    'Т': 'T', 'т': 't',
    'У': 'U', 'у': 'u',
    'Ұ': 'U̇', 'ұ': 'u̇',
    'Ү': 'Ù', 'ү': 'ù',
    'Ф': 'F', 'ф': 'f',
    'Х': 'H', 'х': 'h',
    'Һ': 'Ḥ', 'һ': 'ḥ',
    'Ц': 'C', 'ц': 'c',
    'Ч': 'Č', 'ч': 'č',
    'Ш': 'Š', 'ш': 'š',
    'Щ': 'Ŝ', 'щ': 'ŝ',
    'Ъ': 'ʺ', 'ъ': 'ʺ',
    'Ы': 'Y', 'ы': 'y',
    'І': 'Ì', 'і': 'ì',
    'Ь': 'ʹ', 'ь': 'ʹ',
    'Э': 'È', 'э': 'è',
    'Ю': 'Û', 'ю': 'û',
    'Я': 'Â', 'я': 'â'
}

ISO9_TO_CYRILLIC_MAPPING = {value: key for key, value in CYRILLIC_TO_ISO9_MAPPING.items()}


def convert2latin_iso9(text: str) -> str:
    """Convert Kazakh Cyrillic text to ISO-9 Latin representation."""
    if not isinstance(text, str):
        raise InvalidInputError("text must be a string")
    return ''.join(CYRILLIC_TO_ISO9_MAPPING.get(char, char) for char in text)


def convert2cyrillic_iso9(text: str) -> str:
    """Convert ISO-9 Latin text back to Cyrillic representation."""
    if not isinstance(text, str):
        raise InvalidInputError("text must be a string")
    return ''.join(ISO9_TO_CYRILLIC_MAPPING.get(char, char) for char in text)
