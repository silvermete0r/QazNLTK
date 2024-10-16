import re
from typing import List
from collections import Counter
import urllib3
from functools import lru_cache
from vectorizer import QazNLTKVectorizer, KNN

class QazNLTK:
    '''
        Kazakh Cyrillic is romanized for accessibility to readers familiar with the Latin alphabet.
        
        ISO 9:1995 (International Organization for Standardization), 1995, 
        an international system based on central European orthography 
        that uses a single unique character for each letter.

        Link: https://en.wikipedia.org/wiki/Kazakh_alphabets
    '''
    
    cyrillic_to_iso_9_mapping = {
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

    base = 'https://raw.githubusercontent.com/silvermete0r/QazNLTK/master/special_words'
    stop_words = set()
    positive_words = set()
    negative_words = set()

    @lru_cache(maxsize=None)
    def __init__(self, stop_words_file=f"{base}/stop_words.txt", positive_words_file=f"{base}/positive_words.txt", negative_words_file=f"{base}/negative_words.txt") -> None:
        QazNLTK.stop_words = set(self.load_words(stop_words_file))
        QazNLTK.positive_words = set(self.load_words(positive_words_file))
        QazNLTK.negative_words = set(self.load_words(negative_words_file))
    
    @staticmethod
    def __preprocess_text(text: str) -> str:
        return re.sub(r'\W+', '', text.lower())
    
    @staticmethod
    def __jaccard_similarity(str1: str, str2: str) -> float:
        # Calculate Jaccard similarity: https://en.wikipedia.org/wiki/Jaccard_index
        set1 = set(str1)
        set2 = set(str2)
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        return intersection / union if union != 0 else 0
    
    @staticmethod
    @lru_cache(maxsize=None)
    def __levenshtein_distance(s1: str, s2: str) -> int:
        # Calculate Levenshtein distance: https://en.wikipedia.org/wiki/Levenshtein_distance
        if len(s1) < len(s2):
            return QazNLTK.__levenshtein_distance(s2, s1)
        if len(s2) == 0:
            return len(s1)
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        return previous_row[-1]

    @staticmethod
    def load_words(words_link: str) -> List[str]:
        try:
            data = urllib3.PoolManager().request('GET', words_link).data.decode('utf-8')
            return data.split('\n')
        except FileNotFoundError:
            print(f"File {words_link} not found")
            return []
        except Exception as e:
            print(f"Error: {e}")
            return []
    
    @classmethod
    def convert2cyrillic_iso9(cls, text: str) -> str:
        return ''.join({v: k for k, v in cls.cyrillic_to_iso_9_mapping.items()}.get(char, char) for char in text)

    @classmethod
    def convert2latin_iso9(cls, text: str) -> str:
        return ''.join(cls.cyrillic_to_iso_9_mapping.get(char, char) for char in text)

    @classmethod
    def tokenize(cls, text: str) -> List[tuple]:
        # Tokenize text
        tokens = re.findall(r'\w+', text)

        tokens = [token.lower() for token in tokens if token.lower() not in cls.stop_words]
        
        freqs = Counter(tokens)
        sorted_freqs = sorted(freqs.items(), key=lambda item: item[1], reverse=True)
        
        return sorted_freqs
    
    @classmethod
    def sentimize(cls, tokens) -> float:
        # Sentiment analysis by tokens
        if isinstance(tokens, str):
            tokens = cls.tokenize(tokens)

        positive_score = sum(freq for token, freq in tokens if token in cls.positive_words)
        negative_score = sum(freq for token, freq in tokens if token in cls.negative_words)
        
        return 1.0 if positive_score > negative_score else -1.0 if positive_score < negative_score else 0.0

    @staticmethod
    def calc_similarity(textA: str, textB: str) -> float:
        # Calculate similarity between two texts
        str1 = QazNLTK.__preprocess_text(textA)
        str2 = QazNLTK.__preprocess_text(textB)
        if not str1 or not str2:
            return 0
        jaccard_similarity = QazNLTK.__jaccard_similarity(str1, str2) 
        levenshtein_distance = QazNLTK.__levenshtein_distance(str1, str2)
        return (jaccard_similarity + 1 / (levenshtein_distance + 1)) / 2

    @staticmethod
    def get_info_from_iin(iin: str) -> dict:
        # Get information from IIN
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

        return {
            "status": "success",
            "date_of_birth": birth_date.strftime("%d.%m.%Y"),
            "century_of_birth": f"{year // 100 + 1}",
            "gender": gender,
            "sequence_number": sequence_number,
            "control_discharge": control_discharge
        }

    @classmethod
    def sentimize(cls, tokens) -> float:
        # Sentiment analysis by tokens
        if type(tokens) == str:
            tokens = cls.tokenize(tokens)

        positive_score = 0
        negative_score = 0

        for token, freq in tokens:
            if token in cls.positive_words:
                positive_score += freq
            elif token in cls.negative_words:
                negative_score += freq
        
        if positive_score > negative_score:
            return 1.0
        elif positive_score < negative_score:
            return -1.0
        else:
            return 0.0
    
    @staticmethod
    def num2word(n):
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

if __name__ == "__main__":
    qnltk = QazNLTK()
    
    # text = input('Enter text: ')
    
    # tokens = qnltk.tokenize(text)
    # print(tokens)

    # sent_tokens = qnltk.sent_tokenize(text)
    # print(sent_tokens)

    # textA = input("Enter text A: ")
    # textB = input("Enter text B: ")
    # similarity_score = qnltk.calc_similarity(textA, textB)
    # print(similarity_score)

    # latin_text = qnltk.convert2latin_iso9(text)
    # print(latin_text)

    # cyrillic_text = qnltk.convert2cyrillic_iso9(text)
    # print(cyrillic_text)

    # sentimize_score = qnltk.sentimize(text)
    # print(sentimize_score)

    # n = int(input())
    # print(qnltk.num2word(n))

    # iin = input("Enter IIN: ")
    # print(qnltk.get_info_from_iin(iin))

    # Vectorizer and KNN search example:
    documents = [
        "Ер — елінде, гүл — жерінде.",
        "Өз елінде көртышқан да батыр.",
        "Өз елінің иті де қадірлі.",
        "Отан үшін күрес — ерге тиген үлес.",
        "Орағың өткір болса, қарың талмайды, Отаның берік болса, жауың алмайды.",
        "Елінен безген ер болмас, Көлінен безген қаз болмас.",
        "Сағынған елін аңсайды, Сары ала қаз көлін аңсайды.",
        "Жат жердің қаршығасынан, Өз еліңнің қарғасы артық.",
        "Егілмеген жер жетім, Елінен айырылған ер жетім.",
        "Ерінен айырылған көмгенше жылайды, Елінен айырылған өлгенше жылайды.",
        "Отан — отбасынан басталады.",
        "Опасызда oтан жоқ.",
        "Отан оттан да ыстық.",
        "Отансыз адам — ормансыз бұлбұл."
    ]

    vectorizer = QazNLTKVectorizer()
    tf_idf_matrix = vectorizer.fit_transform(documents)

    knn = KNN(tf_idf_matrix)

    query = "Еліміздің алтын күні жарық күн."

    query_vector = vectorizer.transform([query])[0]

    results = knn.search(query_vector, k=3)

    for idx, distance in results:
        print(f"Document: {documents[idx]}, Distance: {distance}")

    # Document: Орағың өткір болса, қарың талмайды, Отаның берік болса, жауың алмайды., Distance: 0.6740830490255459
    # Document: Жат жердің қаршығасынан, Өз еліңнің қарғасы артық., Distance: 0.7040525969511919
    # Document: Өз елінде көртышқан да батыр., Distance: 0.7453452762306501