import math
from collections import defaultdict, Counter
from typing import List, Dict, Tuple
import re

class QazNLTKVectorizer:
    def __init__(self):
        self.vocabulary = set()
        self.idf_values = {}
        self.tf_idf_matrix = []
    
    def fit_transform(self, documents: List[str]) -> List[List[float]]:
        # ~ build the vocabulary
        tokenized_documents = [self.__tokenize(doc) for doc in documents]
        self.vocabulary = set(token for doc in tokenized_documents for token in doc)
        
        # ~ compute document frequencies (DF)
        doc_freq = defaultdict(int)
        for doc in tokenized_documents:
            for token in set(doc): 
                doc_freq[token] += 1
        
        # ~ compute inverse document frequency (IDF)
        num_documents = len(documents)
        self.idf_values = {
            token: math.log(num_documents / (df + 1))
            for token, df in doc_freq.items()
        }
        
        # ~ compute TF-IDF for each document
        self.tf_idf_matrix = []
        for doc in tokenized_documents:
            tf = Counter(doc)
            doc_length = len(doc)
            tf_idf_vector = [
                (tf[token] / doc_length) * self.idf_values.get(token, 0) for token in self.vocabulary
            ]
            self.tf_idf_matrix.append(tf_idf_vector)
        
        return self.tf_idf_matrix
    
    def __tokenize(self, text: str) -> List[str]:
        # ~ tokenization function
        tokens = re.findall(r'\w+', text.lower())
        return [token for token in tokens]
    
    def transform(self, new_documents: List[str]) -> List[List[float]]:
        # ~ transform new documents into vectors using the existing vocabulary and IDF values
        tokenized_documents = [self.__tokenize(doc) for doc in new_documents]
        transformed_vectors = []
        
        for doc in tokenized_documents:
            tf = Counter(doc)
            doc_length = len(doc)
            tf_idf_vector = [
                (tf[token] / doc_length) * self.idf_values.get(token, 0) for token in self.vocabulary
            ]
            transformed_vectors.append(tf_idf_vector)
        
        return transformed_vectors

class KNN:
    def __init__(self, vectors: List[List[float]]):
        self.vectors = vectors
    
    def __euclidean_distance(self, vec1: List[float], vec2: List[float]) -> float:
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(vec1, vec2)))
    
    def search(self, query_vector: List[float], k: int = 5) -> List[Tuple[int, float]]:
        distances = []
        
        for idx, vector in enumerate(self.vectors):
            distance = self.__euclidean_distance(query_vector, vector)
            distances.append((idx, distance))
        
        # ~ sort by distance and return top k
        distances.sort(key=lambda x: x[1])
        return distances[:k]
    
if __name__ == '__main__':
    documents = [
        "Әйелі жоқ үй – жетім.",
        "Екі жарты – бір бүтін.",
        "Келін жаман емес, келген жері жаман.",
        "Қапқа түскен — қатындікі.",
        "Үйің жаман болса, күйің жаман.",
        "Үй іші толған жан — бір-біріне мейман.",
        "Үлкен үй ортақ, Кішкене үй бұлтақ.",
        "Малыңа сүйенбе, арыңа сүйен.",
        "Жігіттің құны – жүз жылқы, Ары – мың жылқы.",
        "Аянбаған жауды алар, Абайлаған дауды алар.",
        "Су жүрген жер береке, Ел жүрген жер мереке.",
        "Халыққа қарсы жүру - ағысқа қарсы жүзу",
        "Көптің қолы көкке жетеді",
        "Жолдастының жолы кең.",
        "Жолдасты жол айырады.",
        "Әңгіме жол қысқартады.",
        "Шошқаға ерген – балшыққа аунар.",
        "Жолдасын тастаған – жолда қалар.",
        "Досыңды мақтағаның - өзіңді жақтағаның.",
        "Қой егіз тапса, шөптің басы айыр шығады.",
        "Өнерлінің өзегі талмас.",
        "Өтпес пышақ қол кесер.",
        "Еңбек ептілікті сүйеді.",
        "Алтынды ала білген бөле де біледі.",
        "Болат біз қап түбінде қалмас.",
        "Өнерліге есік ашық.",
        "Қолы білген құм үстінен кеме жүргізер.",
        "Күшіңе сенбе, ісіңе сен.",
        "Білім арзан, білу қымбат.",
        "Мың малың болғанша, бір балаң ғалым болсын.",
        "Наданмен дос болғанша, Кітаппен дос бол.",
        "Азат елдің аспаны ашық.",
        "Атты қамшымен айдама, жеммен айда.",
        "Қыран құстың баласы ұшса келмес ұяға.",
        "Қыран құс шашып жейді, қара құс басып жейді.",
        "Тоты құс бойына қарап зорланады, аяғына қарап қорланады.",
        "Құс қанатымен ұшады, құйрығымен қонады.",
        "Алты бақан, ала ауыз.",
        "Бір жеңнен қол шығар, бір жағадан бас шығар.",
        "Бірлік бар жерде - тірлік бар.",
        "Бірлік байлық, байлық емес.",
        "Бірлікке жауапты бірлік.",
        "Байлық, байлық емес, бірлік байлық."
    ]
    
    qaznltk_vectorizer = QazNLTKVectorizer()
    tf_idf_matrix = qaznltk_vectorizer.fit_transform(documents)
    
    knn = KNN(tf_idf_matrix)
    
    query = "Білімнің басы - бейнет, соңы - зейнет."
    query_vector = qaznltk_vectorizer.transform([query])[0]
    
    results = knn.search(query_vector, k=3)
    for idx, distance in results:
        print(f"Document: {documents[idx]}, Distance: {distance}")

