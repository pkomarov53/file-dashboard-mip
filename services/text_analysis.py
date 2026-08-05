import pandas as pd
import re
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Базовый список стоп-слов для очистки текста
STOPWORDS = set([
    "и", "в", "во", "не", "что", "он", "на", "я", "с", "со", "как", "а", "то", 
    "все", "она", "так", "его", "но", "да", "ты", "к", "у", "же", "вы", "за", 
    "бы", "по", "только", "ее", "мне", "было", "вот", "от", "меня", "еще", "нет", 
    "о", "из", "ему", "теперь", "когда", "даже", "ну", "вдруг", "ли", "если", "уже", 
    "или", "ни", "быть", "был", "него", "до", "вас", "нибудь", "опять", "уж", "вам", 
    "ведь", "там", "потом", "себя", "ничего", "ей", "может", "они", "тут", "где", 
    "есть", "надо", "ней", "для", "мы", "тебя", "их", "чем", "была", "сам", "чтоб", 
    "без", "будто", "чего", "раз", "тоже", "себе", "под", "будет", "ж", "тогда", 
    "кто", "этот", "того", "потому", "этого", "какой", "совсем", "ним", "здесь", 
    "этом", "один", "почти", "мой", "тем", "чтобы", "нее", "сейчас", "были", "куда", 
    "зачем", "всех", "никогда", "можно", "при", "наконец", "два", "об", "другой", 
    "хоть", "после", "над", "больше", "тот", "через", "эти", "нас", "про", "всего", 
    "них", "какая", "много", "разве", "три", "эту", "моя", "впрочем", "хорошо", "свою", 
    "этой", "перед", "иногда", "лучше", "чуть", "том", "нельзя", "такой", "им", "более", 
    "всегда", "конечно", "всю", "между", 
    # Специфичные слова, которые не несут смысла для анализа
    "модуль", "модуля", "модуле", "курс", "курса", "очень", "просто", "спасибо", "хотелось", "бы"
])

def clean_and_tokenize(text_series: pd.Series) -> list:
    # Отбрасываем пустые значения и переводим в нижний регистр
    text = " ".join(text_series.dropna().astype(str).tolist()).lower()
    # Убираем всю пунктуацию
    text = re.sub(r'[^\w\s]', ' ', text)
    words = text.split()
    # Фильтруем слова
    words = [w for w in words if w not in STOPWORDS and len(w) > 2]
    return words

def get_top_words_df(text_series: pd.Series, top_n: int = 15) -> pd.DataFrame:
    words = clean_and_tokenize(text_series)
    if not words:
        return pd.DataFrame(columns=["Слово", "Частота"])
    
    counter = Counter(words).most_common(top_n)
    return pd.DataFrame(counter, columns=["Слово", "Частота"])

def create_wordcloud_fig(text_series: pd.Series):
    words = clean_and_tokenize(text_series)
    text = " ".join(words)
    
    if not text.strip():
        return None
        
    wordcloud = WordCloud(
        width=800, 
        height=400, 
        background_color='white', 
        colormap='Blues',
        max_words=100
    ).generate(text)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    return fig