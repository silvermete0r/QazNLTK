<div align="center">
  <img src="https://sun9-11.userapi.com/impg/L_xiLxzenYgyzCVPJtXRCb-A1PTpHvIOSLmzcQ/XWD4xSHW5Vw.jpg?size=1280x440&quality=95&sign=efe38d48a22e0ca8ca8729a89ea0d401&type=album">
</div>

# QazNLTK

A Python library for Kazakh language text processing.

[![PyPI](https://img.shields.io/pypi/v/qaznltk.svg)](https://pypi.org/project/qaznltk/) [![Downloads](https://img.shields.io/pypi/dm/qaznltk.svg)](https://pypi.org/project/qaznltk/)

```sh
pip install qaznltk
```

---

## Features
 
| # | Feature | Method |
|---|---------|--------|
| 1 | Tokenization by frequency | `tokenize(text)` |
| 2 | Sentence segmentation | `sent_tokenize(text)` |
| 3 | Text similarity score | `calc_similarity(a, b)` |
| 4 | Cyrillic → Latin (ISO-9) | `convert2latin_iso9(text)` |
| 5 | Latin → Cyrillic (ISO-9) | `convert2cyrillic_iso9(text)` |
| 6 | Sentiment analysis | `sentimize(text)` → `-1 / 0 / 1` |
| 7 | Number to words | `num2word(n)` |
| 8 | IIN parser | `get_info_from_iin(iin)` |
| 9 | Stop words list | `get_stop_words()` |
| 10 | Kazakh alphabet | `get_kaz_alphabet()` |
| 11 | TF-IDF + KNN search | `QazNLTKVectorizer` + `KNN` |
| 12 | Kazakh LLM (QazPerry) | via HuggingFace |

---

## Usage
 
```python
from qaznltk import QazNLTK
qn = QazNLTK()
```
 
**Tokenize**
```python
qn.tokenize("Біздің өміріміз үлкен өзен іспетті.")
# [('өміріміз', 1), ('үлкен', 1), ('өзен', 1), ('іспетті', 1)]
```
 
**Sentence split**
```python
qn.sent_tokenize("Сәлем. Қалайсың?")
# ['Сәлем.', 'Қалайсың?']
```
 
**Similarity**
```python
qn.calc_similarity("Еңбегіне қарай — құрмет.", "Еңбегіне қарай табысы.")
# 0.368
```
 
**Transliteration**
```python
qn.convert2latin_iso9("Бүгін керемет күн!")   # Bùgìn keremet kùn!
qn.convert2cyrillic_iso9("Bùgìn keremet kùn!")  # Бүгін керемет күн!
```
 
**Sentiment** (`-1` negative, `0` neutral, `1` positive)
```python
qn.sentimize("Бұл мақала өте нашар жазылған.")  # -1.0
```
 
**Number to words**
```python
qn.num2word(1465)  # 'бір мың төрт жүз алпыс бес'
```
 
**IIN parser**
```python
qn.get_info_from_iin("990408482390")
# {'status': 'success', 'date_of_birth': '08.04.1999', 'gender': 'female', ...}
```
 
**Stop words**
```python
qn.get_stop_words()
# ['біздің', 'бұл', 'және', 'мен', 'не', ...]
```
 
**Kazakh alphabet**
```python
qn.get_kaz_alphabet()
# ['а', 'ә', 'б', 'в', 'г', 'ғ', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й',
#  'к', 'қ', 'л', 'м', 'н', 'ң', 'о', 'ө', 'п', 'р', 'с', 'т', 'у',
#  'ү', 'ұ', 'ф', 'х', 'һ', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'і', 'ь', 'э', 'ю', 'я']
```
 
**TF-IDF + KNN**
```python
from qaznltk import QazNLTKVectorizer
 
vectorizer = QazNLTKVectorizer()
matrix = vectorizer.fit_transform(documents)
knn = vectorizer.KNN(matrix)
 
query_vector = vectorizer.transform(["Еліміздің алтын күні жарық күн."])[0]
results = knn.search(query_vector, k=3)
# [(idx, distance), ...]
```
 
**QazPerry (Kazakh LLM)**
```bash
pip install keras-nlp huggingface_hub
```
```python
from huggingface_hub import hf_hub_download
import keras, keras_nlp
 
model_path = hf_hub_download("silvermete0r/Gemma2_2B_QazPerry", "Gemma2_2B_QazPerry.keras")
model = keras.models.load_model(model_path, custom_objects={"GemmaCausalLM": keras_nlp.models.GemmaCausalLM})
 
print(model.generate("Instruction:\nҚазақша бірдеңе айтшы?\n\nResponse:\n"))
```
 
> HuggingFace: [silvermete0r/Gemma2_2B_QazPerry](https://huggingface.co/silvermete0r/Gemma2_2B_QazPerry)
 
---
 
## License
 
* [MIT](LICENSE)
*  Built at [Skillset School](https://skillset.edu.kz/)