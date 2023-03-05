import time
import datetime
import csv
import aylien_news_api
from aylien_news_api.rest import ApiException

def fetch_new_stories(params={}):
	fetched_stories = []
	stories = None

	while stories is None or len(stories) > 0:
		response = api_instance.list_stories(**params)
		stories = response.stories
	
		params['cursor'] = response.next_page_cursor

		fetched_stories += stories
		#print("Fetched %d stories. Total story count so far: %d" %(len(stories), len(fetched_stories)))
	return fetched_stories

# Configure API key authorization: app_id
aylien_news_api.configuration.api_key['X-AYLIEN-NewsAPI-Application-ID'] = 'e8dde0e8'
# Configure API key authorization: app_key
aylien_news_api.configuration.api_key['X-AYLIEN-NewsAPI-Application-Key'] = 'a423f70591dec161362d6dba626f2031'

# create an instance of the API class
api_instance = aylien_news_api.DefaultApi()

params = {
	#'title': 'aapl OR apple OR AAPL OR Apple',
	#'text':'AAPL or aapl',
	'categories_confident': True,
	'categories_taxonomy': 'iptc-subjectcode',
	'categories_id': ['04000000'],
	'entities_body_links_dbpedia':[
    'http://dbpedia.org/resource/Apple_Inc.'
	],
	'source_rankings_alexa_rank_max': 150,
	'sort_by': 'source.rankings.alexa.rank',
	'sort_direction': 'asc',
	'language': ['en'],
	'published_at_start': 'NOW-10DAY',
	'published_at_end': 'NOW',
	#'cursor': '*',
	#'per_page': 10
}

stories = fetch_new_stories(params)

sentimentv = float()

for story in stories:
	print(f'Title: {story.title}')
	print(f'Source: {story.source.name}')
	print(f'Date: {str(story.published_at.date())}')
	print(f'Title sentiment: {str(story.sentiment.title.score)}')
	print(f'Body sentiment: {str(story.sentiment.body.score)}')
	print(f'Link: {str(story.links.permalink)}' + '\n')
	sentimentv += story.sentiment.body.score

if (len(stories) > 0):
	sentimentv = sentimentv / len(stories)
	print(f'Average body sentiment: {str(sentimentv)}' + '\n')

print('************')
print("Fetched %d stories published between %s and %s" %(len(stories), params['published_at_start'], params['published_at_end']))