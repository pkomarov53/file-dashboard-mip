# services/text_analysis.py
import os
import re
from collections import Counter
import pandas as pd
import pymorphy3
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Инициализация морфологического анализатора
morph = pymorphy3.MorphAnalyzer()

STOPWORDS_FILE = "data/stopwords.txt"

# Базовый набор стоп-слов на случай отсутствия внешнего файла
DEFAULT_STOPWORDS = {
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
    "всегда", "конечно", "всю", "между", "это", "который", "очень", "просто", "спасибо", 
    "хотелось", "модуль", "курс"
}

def load_stopwords() -> set:
    """
    Загружает стоп-слова из внешнего файла data/stopwords.txt.
    Если файл отсутствует, возвращает дефолтный набор.
    """
    if os.path.exists(STOPWORDS_FILE):
        try:
            with open(STOPWORDS_FILE, "r", encoding="utf-8") as f:
                custom_words = {line.strip().lower() for line in f if line.strip()}
                return custom_words.union(DEFAULT_STOPWORDS)
        except Exception:
            return DEFAULT_STOPWORDS
    return DEFAULT_STOPWORDS

STOPWORDS = load_stopwords()

def lemmatize_word(word: str) -> str:
    """Приводит слово к нормальной словарной форме."""
    return morph.parse(word)[0].normal_form

def clean_and_tokenize(text_series: pd.Series) -> list:
    """
    Очищает текст, выполняет токенизацию, лемматизацию 
    и фильтрацию по стоп-словам.
    """
    text = " ".join(text_series.dropna().astype(str).tolist()).lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    raw_words = text.split()
    
    clean_lemmas = []
    for w in raw_words:
        if len(w) <= 2 or w in STOPWORDS:
            continue
        
        lemma = lemmatize_word(w)
        
        # Повторная проверка леммы по стоп-словам
        if len(lemma) > 2 and lemma not in STOPWORDS:
            clean_lemmas.append(lemma)
            
    return clean_lemmas

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