#Importar librerias
import tweepy
import credentials
import json

#Credenciales asociadas al archivo credentials.py
consumer_key = credentials.API_KEY
consumer_secret_key = credentials.API_SECRET_KEY
access_token = credentials.ACCESS_TOKEN
access_token_secret = credentials.ACCESS_TOKEN_SECRET

auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

#Buscador de tweet
search_terms = ['fibertel'] #Aqui la palabra buscada.
def stream_tweets(search_term):
    data = [] 
    counter = 0 
    for tweet in tweepy.Cursor(api.search_tweets, q='\"{}\"'.format(search_term), count=5, lang='es', tweet_mode='extended').items():
        tweet_details = {}
        tweet_details['Nombre: '] = tweet.user.screen_name
        tweet_details['Tweets: '] = tweet.full_text
        tweet_details['RT: '] = tweet.retweet_count
        tweet_details['Ubicación: '] = tweet.user.location
        tweet_details['Creado: '] = tweet.created_at.strftime("%d-%b-%Y")
        tweet_details['Seguidores: '] = tweet.user.followers_count
        tweet_details['Verificación: '] = tweet.user.verified
        data.append(tweet_details)
        
        counter += 1
        if counter == 5: #Cantidad de tweets
            break
        else:
            pass
    with open('fibertel.json'.format(search_term), 'w') as f: #Nombre del archivo 
        data = json.dump(data, f)


print('hecho!')


if __name__ == "__main__":
    print('Comienzo...')
    for search_term in search_terms:
        stream_tweets(search_term)

print('finalizado!')



