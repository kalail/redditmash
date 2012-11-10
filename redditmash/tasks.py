import requests
import datetime
from django.core.cache import cache
from redditmash.models import Post, StatsReddit, Stats
from requests.exceptions import RequestException
from celery.task import task, periodic_task
from datetime import timedelta




@periodic_task(run_every = timedelta(seconds=10))
def get_posts():
	"""Get the latest 100 posts on the reddit homepage. Returns a list of raw un-parsed posts.
	"""

	url = 'http://www.reddit.com/.json?limit=1'
	headers = {
		'User-Agent': 'redditmash'
	}

	# Make request
	data = requests.get(url=url, headers=headers)

	# Check data for correct type
	if data.json['kind'] != 'Listing':
		print "ERROR: wrong type recieved from " + url
		return None

	# Contruct packet
	listing = data.json['data']['children']
	print 'Fetched ' + str(len(listing)) + ' posts'

	# Save listing in cache
	cache.set('new_listing', listing, 120)

	# Send parsing task
	parse_posts.delay()

	
@task
def parse_posts():
	# Get listing from cache
	listing = cache.get('new_listing')

	# Check for existence
	if not listing:
		return None

	# Send post save tasks
	for rank, post in enumerate(listing):
		pp = PostParser(post, rank)
		cache.set('parsed_' + str(pp.id), pp, 30)
		save_post.delay(pp.id)

	# Delete listing from cache
	cache.delete('new_listing')

@task
def save_post(parsed_post_id):
	# Get post from cache
	parsed_post = cache.get('parsed_' + parsed_post_id)
	# Check fror existence
	if not parsed_post:
		return None

	# Get or create post
	try:
		p = Post.objects.get(id=parsed_post.id)
		# Update attributes
		if parsed_post.edited == True:
			p.title = parsed_post.title
			p.url = parsed_post.url
			p.author = parsed_post.author
		stats_r = p.statsreddit

	except Post.DoesNotExist:
		# Create post
		p = Post(id=parsed_post.id, title=parsed_post.title, author=parsed_post.author, url=parsed_post.url, created_on_reddit=parsed_post.created_on)
		stats_r = StatsReddit(post=p)

	# Save updated models
	p.save()
	stats_r.score = parsed_post.score
	stats_r.rank = parsed_post.rank
	stats_r.save()

	# Delete post from cache
	cache.delete('parsed_' + parsed_post.id)


class PostParser(object):
	"""Provides a wrapper-based parser for reddit posts of type t3.
	"""

	def __init__(self, raw_post, rank):
		if raw_post['kind'] == 't3':
			self.post = raw_post['data']
			self.rank = rank

	@property
	def title(self):
		return self.post['title']

	@property
	def created_on(self):
		return datetime.datetime.utcfromtimestamp(self.post['created_utc'])

	@property
	def author(self):
		return self.post['author']

	@property
	def over_18(self):
		return self.post['over_18']

	@property
	def id(self):
		return self.post['id']

	@property
	def num_comments(self):
		return self.post['num_comments']

	@property
	def score(self):
		return self.post['score']

	@property
	def up_votes(self):
		return self.post['ups']

	@property
	def down_votes(self):
		return self.post['downs']

	@property
	def domain(self):
		return self.post['domain']
	
	@property
	def url(self):
		return self.post['url']

	@property
	def edited(self):
		return self.post['edited']
