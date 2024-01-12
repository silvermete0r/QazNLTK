import re
from typing import List
from collections import Counter

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

    stop_words = set()
    positive_words = set()
    negative_words = set()

    def __init__(self, stop_words_file="special_words/stop_words.txt", positive_words_file="special_words/positive_words.txt", negative_words_file="special_words/negative_words.txt") -> None:
        QazNLTK.stop_words = set(self.load_words(stop_words_file))
        QazNLTK.positive_words = set(self.load_words(positive_words_file))
        QazNLTK.negative_words = set(self.load_words(negative_words_file))

    @staticmethod
    def load_words(words_file: str) -> List[str]:
        try:
            with open(words_file, "r", encoding='utf-8') as f:
                return [line.strip() for line in f.readlines()]
        except FileNotFoundError:
            print(f"File {words_file} not found")
            return []
        except Exception as e:
            print(f"Error: {e}")
            return []
    
    @classmethod
    def convert2cyrillic(cls, text: str) -> str:
        # Convert kazakh latin to cyrillic
        cyrillic_text = ''
        reversed_mapping = {v: k for k, v in cls.cyrillic_to_iso_9_mapping.items()}
        
        for char in text:
            cyrillic_text += reversed_mapping.get(char, char)

        return cyrillic_text

    @classmethod
    def convert2latin(cls, text: str) -> str:
        # Convert kazakh cyrillic to latin
        latin_text = ''

        for char in text:
            latin_text += cls.cyrillic_to_iso_9_mapping.get(char, char)

        return latin_text

    @classmethod
    def tokenize(cls, text: str) -> List[tuple]:
        # Tokenize text
        tokens = re.findall(r'\w+', text)

        tokens = [token.lower() for token in tokens if token.lower() not in cls.stop_words]
        
        freqs = Counter(tokens)
        sorted_freqs = sorted(freqs.items(), key=lambda item: item[1], reverse=True)
        
        return sorted_freqs
    
    @classmethod
    def sent_tokenize(cls, text: str) -> List[str]:
        # Tokenize Kazakh text into sentences
        sentence_pattern = re.compile(r'(?<!\w\.\w.)(?<![A-ZА-ЯІЇҮӘҒЕЁНОҢУЎЫ])(?<=\.|\?|\!)\s')
        
        sentences = sentence_pattern.split(text)
        sentences = [sentence.strip() for sentence in sentences]

        return sentences
    
    @staticmethod
    def calc_similarity(textA: str, textB: str) -> float:
        # Jaccard Similarity Calculation
        setA = set(textA.split())
        setB = set(textB.split())

        intersection = len(setA.intersection(setB))
        union = len(setA) + len(setB) - intersection

        similarity_score = intersection / union if union != 0 else 0.0

        return similarity_score
    
    @classmethod
    def sentimize(cls, tokens) -> int:
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
            return 1
        elif positive_score < negative_score:
            return -1
        else:
            return 0
    
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

    # latin_text = qnltk.convert2latin(text)
    # print(latin_text)

    # cyrillic_text = qnltk.convert2cyrillic(text)
    # print(cyrillic_text)

    # sentimize_score = qnltk.sentimize(text)
    # print(sentimize_score)

    # n = int(input())
    # print(qnltk.num2word(n))