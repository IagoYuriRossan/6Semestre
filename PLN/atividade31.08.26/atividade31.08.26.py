import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
stop_words_pt = stopwords.words('portuguese')

textos = [
    "Aplicativos facilitam a comunicação entre pessoas distantes.",
    "A tecnologia transforma a forma como estudamos e trabalhamos.",
    "Celulares conectam pessoas, notícias e serviços em poucos segundos.",
    "Usar tecnologia com responsabilidade melhora a vida em sociedade."
]

print("--- Vetorização Bag-of-Words (BoW) ---")
vetorizador_bow = CountVectorizer(stop_words=stop_words_pt)
matriz_bow = vetorizador_bow.fit_transform(textos)
df_bow = pd.DataFrame(matriz_bow.toarray(), columns=vetorizador_bow.get_feature_names_out())
print(df_bow)
print("\n")

print("--- Vetorização TF-IDF ---")
vetorizador_tfidf = TfidfVectorizer(stop_words=stop_words_pt)
matriz_tfidf = vetorizador_tfidf.fit_transform(textos)
df_tfidf = pd.DataFrame(matriz_tfidf.toarray(), columns=vetorizador_tfidf.get_feature_names_out())
print(df_tfidf)
print("\n")

print("--- Análise de Frequências (BoW) ---")
frequencias = matriz_bow.toarray().sum(axis=0)
palavras = vetorizador_bow.get_feature_names_out()

tabela_frequencias = pd.DataFrame({'Termo': palavras, 'Ocorrências': frequencias})
tabela_frequencias = tabela_frequencias.sort_values(by='Ocorrências', ascending=False)
print(tabela_frequencias)

tabela_frequencias.plot(x='Termo', y='Ocorrências', kind='bar', legend=False, title="Termos mais frequentes no corpus")
plt.ylabel('Número de ocorrências')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()