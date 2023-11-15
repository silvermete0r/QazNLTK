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

    def __init__(self, stop_words_file="special_words/stop_words.txt") -> None:
        if not QazNLTK.stop_words:
            QazNLTK.stop_words = set(QazNLTK.load_words(stop_words_file))

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

if __name__ == "__main__":
    qnltk = QazNLTK()
    text = input('Enter text: ')
    tokenized_text = qnltk.tokenize(text)
    print(tokenized_text)