import requests




# urlindia = ('http://newsapi.org/v2/top-headlines?'
#         'country=in&'
#         'q=coronavirus&'
#         'from=2020-03-21&'
#         'sortBy=popularity&'
#         'apiKey=55d55abffe3c48298169fd84576a8d48')

def NewsFromApi(url):
    news = []
    response= requests.get(url).json()
    if(response['status']=='ok'):
        for art in response['articles']:
            lsf = {'title':art['title'],
                   'description':art['description'],
                   'author':art['author'],
                   'publishedAt':art['publishedAt'],
                   'urlToImage':art['urlToImage'],
                   'content':art['content'],
                   'url':art['url']}
            news.append(lsf)
    else:
        return "api-error"
    return news
