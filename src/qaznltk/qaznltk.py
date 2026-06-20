import os
import re
from typing import List

from .exceptions import InvalidInputError
from .legacy import convert2cyrillic_iso9, convert2latin_iso9
from .metrics import calc_cer, calc_wer
from .utils import compute_jaccard_similarity, frequency_tokens, levenshtein_distance, normalize_text, tokenize_words

class QazNLTK:
    def __init__(cls) -> None:
        base = os.path.join(os.path.dirname(__file__), "..", "special_words")
        cls.stop_words = set(cls.load_words(f"{base}/stop_words.txt"))
        cls.positive_words = set(cls.load_words(f"{base}/positive_words.txt"))
        cls.negative_words = set(cls.load_words(f"{base}/negative_words.txt"))

    @staticmethod
    def load_words(words_path: str) -> List[str]:
        try:
            with open(words_path, "r", encoding="utf-8") as f:
                return [w.strip() for w in f.readlines() if w.strip()]
        except Exception as e:
            print(f"Error while loading {words_path}: {e}")
            return []

    def get_stop_words(cls) -> List[str]:
        return sorted(list(cls.stop_words))
    
    def get_positive_words(cls) -> List[str]:
        return sorted(list(cls.positive_words))
    
    def get_negative_words(cls) -> List[str]:
        return sorted(list(cls.negative_words))
    
    def convert2latin_iso9(cls, text: str) -> str:
        return convert2latin_iso9(text)

    def convert2cyrillic_iso9(cls, text: str) -> str:
        return convert2cyrillic_iso9(text)

    def tokenize(self, text: str) -> List[tuple]:
        if not isinstance(text, str):
            raise InvalidInputError("text must be a string")
        tokens = [token for token in tokenize_words(text) if token not in self.stop_words]
        return frequency_tokens(tokens)

    def sentimize(self, text) -> float:
        if isinstance(text, str):
            tokens = self.tokenize(text)
        else:
            tokens = text

        positive_score = 0
        negative_score = 0
        for token, freq in tokens:
            if token in self.positive_words:
                positive_score += freq
            elif token in self.negative_words:
                negative_score += freq

        if positive_score > negative_score:
            return 1.0
        if positive_score < negative_score:
            return -1.0
        return 0.0

    @staticmethod
    def calc_similarity(text_a: str, text_b: str) -> float:
        if not isinstance(text_a, str) or not isinstance(text_b, str):
            raise InvalidInputError("text_a and text_b must be strings")

        str1 = normalize_text(text_a)
        str2 = normalize_text(text_b)
        if not str1 or not str2:
            return 0.0
        
        jaccard_similarity = compute_jaccard_similarity(str1, str2)
        levenshtein = levenshtein_distance(str1, str2)
        if levenshtein == 0:
            return 1.0
        similarity = (jaccard_similarity + (1 / (levenshtein + 1))) / 2
        sim_score = float(max(0.0, min(1.0, similarity)))
        return sim_score
    
    @staticmethod
    def calc_cer(true_text: str, pred_text: str) -> float:
        return calc_cer(true_text, pred_text)

    @staticmethod
    def calc_wer(true_text: str, pred_text: str) -> float:
        return calc_wer(true_text, pred_text)

    @staticmethod
    def sent_tokenize(text: str) -> List[str]:
        if not isinstance(text, str):
            raise InvalidInputError("text must be a string")
        return re.split(r'(?<=[.!?]) +', text)
    
    @staticmethod
    def get_kaz_alphabet() -> List[str]:
        return list("аәбвгғдеёжзийкқлмнңоөпрстуүұфхһцчшщъыіьэюя")

    @staticmethod
    def num2word(n: int) -> str:
        # Convert number to word
        w = {
            "1": "бір",
            "2": "екі",
            "3": "үш",
            "4": "төрт",
            "5": "бес",
            "6": "алты",
            "7": "жеті",
            "8": "сегіз",
            "9": "тоғыз",
            "10": 'он',
            "20": "жиырма",
            "30": "отыз",
            "40": "қырық",
            "50": "елу",
            "60": "алпыс",
            "70": "жетпіс",
            "80": "сексен",
            "90": "тоқсан"
        }
        mp = {
            0: "нөл",
            1: "он",
            2: "жүз",
            3: "мың",
            6: "миллион",
            9: "миллиард",
            12: "триллион",
            15: "квадриллион",
            18: "квинтиллион",
            21: "секстиллион",
            24: "септиллион",
            27: "октиллион",
            30: "нониллион"
        }
        s = str(n)
        v = []
        c = []
        cur = ''

        for i in range(len(s) - 1, -1, -1):
            if i == len(s) - 1:
                if s[i] > '0':
                    v.append(w[s[i]])
                continue
            x = len(s) - i - 1
            if x in mp:
                if x == 1:
                    if s[i] > '0':
                        cur = w[s[i] + '0']
                else:
                    cur = mp[x]
            else:
                if x % 3 == 1:
                    if s[i] > '0':
                        cur = w[s[i] + '0']
                    if mp[x - x % 3] not in c:
                        cur += ' '
                        cur += mp[x - x % 3]
                else:
                    cur = mp[x % 3]
                    if mp[x - x % 3] not in c:
                        cur += ' '
                        cur += mp[x - x % 3]
                        c.append(mp[x - x % 3])
            if s[i] > '0':
                c.append(cur)
                v.append(cur)
                if x % 3 == 2 and s[i] < '2':
                    continue
                if x % 3 != 1:
                    v.append(w[s[i]])

        if n < 0:
            v.append('минус')

        v.reverse()
        return ' '.join(v)

    @staticmethod
    def get_info_from_iin(iin: str) -> dict:
        if len(iin) != 12 or not iin.isdigit():
            return {"status": "error", "message": "Incorrect IIN. The length of the IIN must be 12 digits."}

        year = int(iin[:2])
        month = int(iin[2:4])
        day = int(iin[4:6])
        sequence_number = int(iin[7:11])
        control_discharge = int(iin[11:12])
        gender_code = int(iin[6])

        if gender_code in [1, 2]:
            year += 1800
        elif gender_code in [3, 4]:
            year += 1900
        elif gender_code in [5, 6]:
            year += 2000
        else:
            return {"status": "error", "message": "Incorrect IIN. The first digit of the IIN must be in the range [1, 6]."}

        gender = "male" if gender_code % 2 == 1 else "female"

        try:
            from datetime import datetime
            birth_date = datetime(year, month, day)
        except ValueError:
            return {"status": "error", "message": "Incorrect IIN. The date of birth is incorrect."}

        weights = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        total = sum(int(iin[i]) * weights[i] for i in range(11))
        mod = total % 11
        if mod == 10:
            weights = [3, 4, 5, 6, 7, 8, 9, 10, 11, 1, 2]
            total = sum(int(iin[i]) * weights[i] for i in range(11))
            mod = total % 11
        if mod != control_discharge:
            return {"status": "error", "message": "Incorrect IIN. Control discharge does not match."}

        return {
            "status": "success",
            "date_of_birth": birth_date.strftime("%d.%m.%Y"),
            "century_of_birth": f"{year // 100 + 1}",
            "gender": gender,
            "sequence_number": sequence_number,
            "control_discharge": control_discharge,
        }