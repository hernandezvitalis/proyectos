from textblob import TextBlob 
from wordcloud import WordCloud
import pandas as pd 
import re
import matplotlib.pyplot as plt
import json

#Nombre del archivo que haremos el DF
with open('fibertel.json','r') as f:
    data = json.load(f)

df = pd.DataFrame(data)

df = pd.read_json ('fibertel.json', orient='columns')

result = df.to_json(orient = 'columns')
parsed = json.loads(result)

json.dumps(parsed, indent=30)

def get_subjectivity(text):
    return TextBlob(text).sentiment.subjectivity

def get_polarity(text):
    return TextBlob(text).sentiment.polarity


df['Subjectivity'] = df['Tweets: '].apply(get_subjectivity)
df['Polarity'] = df['Tweets: '].apply(get_polarity)

df

#Limpieza del texto
def clean_text(text):
    text = re.sub(r'@[A-Za-z09]+', '', text)
    text = re.sub(r'#', '', text)
    text = re.sub(r'RT[\s]+', '', text)
    text = re.sub(r'https?:\/\/?', '', text)
    return text

df['Tweets: '] = df['Tweets: '].apply(clean_text) #Columna que aplicaremos la limpieza

df

df.to_excel('fibertel.xlsx') #Pasado a excel

print(df.head(30))

#Creación de grafico con palabras predominantes en los tweets
all_words = ' '.join( [twts for twts in df['Tweets: ']])
word_Cloud = WordCloud(width=500, height=300, random_state=21, max_font_size=119).generate(all_words)

stopwords = set(all_words)
#Palabras excluidas del grafico
stopwords.update(["fibertel", "la", "y", "ahora", "con", "deja", "de", "lo", "_at", "ya", "en", "que", "es", "una", "el", "no", "se", "sin", "del", "se llama", "llama", "dejan", "te","me", "mi", "por", "tu", "las"])

wordcloud = WordCloud(stopwords=stopwords, background_color="white").generate(all_words)

plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

#Agregando sentiment analysis
def analysis(score):
    if score < 0:
        return 'Negative'
    elif score == 0:
          return 'Neutral'
        
    elif score > 0:
        return 'Positive'
    
    else:
          return 'Positive'
           
df['Analysis'] = df['Polarity'].apply(analysis) 

j=1
sortedDF = df.sort_values(by=['Polarity'])
for i in range(0, sortedDF.shape[0]):
    if(sortedDF['Analysis'][i] == 'Positive'):
        print(str(j) + ') ' + sortedDF['Tweets: '][i])
        print()
        j += 1

j=1
sortedDF = df.sort_values(by=['Polarity'], ascending=False)
for i in range(0, sortedDF.shape[0]):
    if(sortedDF['Analysis'][i] == 'Negative'):
        print(str(j) + ') ' + sortedDF['Tweets: '][i])
        print()
        j += 1

plt.figure(figsize=(8,6))
for i in range(0, df.shape[0]):
    plt.scatter(df['Polarity'][i], df['Subjectivity'][i], color='blue')

plt.title('Analisis de sentimientos')
plt.xlabel('polarity')
plt.ylabel('subjectivity')

plt.show()

ptweet = df[df.Analysis == 'Positive']
pteet = ptweet['Tweets: ']

round(ptweet.shape[0] / df.shape[0] * 100, 1)

ntweet = df[df.Analysis == 'Negative']
nteet = ntweet['Tweets: ']

round(ntweet.shape[0] / df.shape[0] * 100, 1)

df['Analysis'].value_counts()

plt.title('Sentiment Analysis')
plt.xlabel('Sentiment')
plt.ylabel('Counts')
df['Analysis'].value_counts().plot(kind='bar')
plt.show()
