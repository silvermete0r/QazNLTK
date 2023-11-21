<div align="center">
  <img src="https://sun9-11.userapi.com/impg/L_xiLxzenYgyzCVPJtXRCb-A1PTpHvIOSLmzcQ/XWD4xSHW5Vw.jpg?size=1280x440&quality=95&sign=efe38d48a22e0ca8ca8729a89ea0d401&type=album"><br>
</div>

-----------------

# QazNLTK: a package for working with Kazakh language text processing.

[![PyPI Latest Release](https://img.shields.io/pypi/v/qaznltk.svg)](https://pypi.org/project/qaznltk/) [![PyPI Downloads](https://img.shields.io/pypi/dm/qaznltk.svg?label=PyPI%20downloads)](https://pypi.org/project/qaznltk/)


## What is it?

**QazNLTK** provides developers with a fast and convenient tool for processing text in the Kazakh language. Tailored for the unique linguistic characteristics of Kazakh, this library offers a comprehensive set of tools for natural language processing, like: tokenization, sentence segmentation, evaluation similarity score and tranliteration of kazakh language cyrillic-latin.

## Table of Contents

- [Main Features](#main-features)
- [Where to get it](#where-to-get-it)
- [Dependencies](#dependencies)
- [License](#license)
- [Getting Help](#getting-help)
- [Contributing to QazNLTK](#contributing-to-qaznltk)

## Main Features
Here are just a few of the things that qaznltk does well:

1) Kazakh language Text Tokenizing by keyword frequencies:
``` Python
from qaznltk import qaznltk as qnltk
qn = qnltk.QazNLTK()

text = input("Enter text: ")
tokens = qn.tokenize(text)
print(tokens)

# Input: Біздің өміріміз үлкен өзен іспетті. Сіздің қайығыңыздың қиындықтардан жеңіл өтіп, махаббат иірімінде басқаруын жоғалтпай, бақыт сарқырамасына жетуін тілеймін!
# Output: [('өміріміз', 1), ('үлкен', 1), ('өзен', 1), ('іспетті', 1), ('сіздің', 1), ('қайығыңыздың', 1), ('қиындықтардан', 1), ('жеңіл', 1), ('өтіп', 1), ('махаббат', 1), ('иірімінде', 1), ('басқаруын', 1), ('жоғалтпай', 1), ('бақыт', 1), ('сарқырамасына', 1), ('жетуін', 1), ('тілеймін', 1)]
```

2) Kazakh language Text Segmentation into sentences:
``` Python
from qaznltk import qaznltk as qnltk
qn = qnltk.QazNLTK()

text = input("Enter text: ")
sent_tokens = qn.sent_tokenize(text)
print(sent_tokens)

# Input: Біздің өміріміз үлкен өзен іспетті. Сіздің қайығыңыздың қиындықтардан жеңіл өтіп, махаббат иірімінде басқаруын жоғалтпай, бақыт сарқырамасына жетуін тілеймін!
# Output: ['Біздің өміріміз үлкен өзен іспетті.', 'Сіздің қайығыңыздың қиындықтардан жеңіл өтіп, махаббат иірімінде басқаруын жоғалтпай, бақыт сарқырамасына жетуін тілеймін!']
```

3) Evaluate Difference score between 2 text:
``` Python
from qaznltk import qaznltk as qnltk
qn = qnltk.QazNLTK()

textA = input("Enter text A: ")
textB = input("Enter text B: ")
similarity_score = qn.calc_similarity(textA, textB)
print(similarity_score)

# Input: textA = "Еңбегіне қарай — құрмет, Жасына қарай — ізет.", textB = "Еңбегіне қарай табысы, Ерлігіне қарай дабысы."
# Output: 0.2222222222222222
```

4) Convert Kazakh language Text from Cyrillic to Latin using ISO-9 Standard:
``` Python
from qaznltk import qaznltk as qnltk
qn = qnltk.QazNLTK()

text = input("Enter text: ")
latin_text = qn.convert2latin(text)
print(latin_text)

# Input: Бүгін қандай керемет күн! 
# Output: Bùgìn k̦andaj keremet kùn!
```

5) Convert Kazakh language Text from Latin to Cyrillic using ISO-9 Standard:
``` Python
from qaznltk import qaznltk as qnltk
qn = qnltk.QazNLTK()

text = input("Enter text: ")
cyrillic_text = qn.convert2cyrillic(text)
print(cyrillic_text)

# Input: Bùgìn k̦andaj keremet kùn!
# Output: Бүгін қандай керемет күн!
```

6) Sentiment Analysis of Kazakh language text [`negative: -1`, `neutral: 0`, `positive: 1`]:
``` Python
from qaznltk import qaznltk as qnltk
qn = qnltk.QazNLTK()

text = input("Enter text: ")
sentimize_score = qnltk.sentimize(text)
print(sentimize_score)

# Input: Бұл мақала өте нашар жазылған.
# Output: -1 (negative)
```

7) Converting any number `N` into kazakh language number words [`N <= 10^31`]:
``` Python
from qaznltk import qaznltk as qnltk
qn = qnltk.QazNLTK()

n = int(input())
print(qnltk.num2word(n))

# Input: N = 9827
# Output: тоғыз мың сегіз жүз жиырма жеті
```

* **Test Samples:** https://vk.com/club121755042

## Where to get it
The source code is currently hosted on GitHub at: https://github.com/silvermete0r/QazNLTK.git

Binary installers for the latest released version are available at the [Python
Package Index (PyPI)](https://pypi.org/project/qaznltk).

```sh
pip install qaznltk
```
![image](https://github.com/silvermete0r/QazNLTK/assets/108217670/b1e8eaa1-f25f-4019-9d75-dee8d25d6a28)


The list of changes to pandas between each release can be found
[here](https://pandas.pydata.org/pandas-docs/stable/whatsnew/index.html). For full
details, see the commit logs at https://github.com/pandas-dev/pandas.

## Dependencies
- Package was developed on built-in python functions; 


## License
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Getting Help

📧 [supwithproject@gmail.com](https://gmail.com/)

## Contributing to qaznltk

All contributions, bug reports, bug fixes, documentation improvements, enhancements, and ideas are welcome.

<hr>

[Go to Top](#table-of-contents)