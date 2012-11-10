import requests
import datetime
import random
import math
from django.core.cache import cache
from redditmash.models import Post, StatsReddit, Stats, Choice
from requests.exceptions import RequestException
from celery.task import task, periodic_task
from datetime import timedelta


choices_limit = 10



# PROCESS / PREPARE LOCAL RANKS
# 
# ==============================================================================

@periodic_task
def update_queue_manager():
	new_posts = Post.objects.filter(is_active=False).filter(is_active_reddit=True)
	old_posts = Post.objects.filter(is_active=True).filter(is_active_reddit=False)
	current_posts = Post.objects.filter(is_active=True).filter(is_active_reddit=True)

	# Just started
	if not old_posts and not current_posts:
		posts_to_compete = random.sample(new_posts, 2)
		create_choice(posts_to_compete[0].id, posts_to_compete[1].id)



def choice_consumer():
	try:
		choice = Choice.objects.filter(is_active=True).order_by('times_completed')[0]
	except IndexError:
		return

	winner = random.choice([choice.post_1, choice.post_2])
	process_decision.delay(winner.id, choice.id)

@task
def process_decision(winner_id, choice_id):
	"""Make, process and save decision to database
	"""
	# Get objects
	winner = Post.objects.get(id=winner_id)
	choice = Choice.objects.get(id=choice_id)
	loser = choice.post_2 if winner_id == choice.post_1.id else choice.post_1

	# Update choice
	choice.times_completed = choice.times_completed + 1
	choice.save()

	# Run algorithm
	results = ELOResultCalculator(winner, loser)

	winner.rating = results.winner_rating
	loser.rating = results.loser_rating

	# Save results
	winner.save()
	loser.save()

	# Recalculate rank
	calculate_rank.delay()


class ELOResultCalculator(object):
	def __init__(self, winner, loser):
		self.winner = winner
		self.loser = loser
		self.k = 20.0

	def winner_win_probability(self):
		return 1.0 / (10.0**((self.loser.rating - self.winner.rating) / 400.0) + 1.0)

	def loser_win_probability(self):
		return 1.0 / (10.0**((self.winner.rating - self.loser.rating) / 400.0) + 1.0)

	@property
	def winner_rating(self):
		return self.winner.rating + (self.k * (1.0 - self.winner_win_probability()))

	@property
	def loser_rating(self):
		return self.loser.rating + (self.k * (0.0 - self.loser_win_probability()))

@task
def calculate_rank():
	posts = Post.objects.filter(is_active=True).order_by('-stats__rating')
	for idx, p in enumerate(posts):
		s = p.stats
		s.rank = idx
		s.save()


@periodic_task(run_every = timedelta(seconds=60))
def delete_unused_posts():
	unused_posts = Post.objects.filter(is_active=False).filter(is_active_reddit=False)
	unused_posts.delete()
# 
# ==============================================================================



# UPDATE POSTS FROM REDDIT
#
# ==============================================================================
@periodic_task(run_every = timedelta(seconds=30))
def get_posts():
	"""Get the latest 25 posts on the reddit homepage. Returns a list of raw un-parsed posts.
	"""

	url = 'http://www.reddit.com/r/pics/.json?limit=100'
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
	rank = 0
	for post in listing:
		pp = PostParser(post, rank)
		if pp.is_image():
			cache.set('parsed_' + str(pp.id), pp, 30)
			save_post.delay(pp.id)
			rank = rank + 1

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
		p.is_active_reddit = True
		if parsed_post.edited == True:
			p.title = parsed_post.title
			p.url = parsed_post.url
			p.author = parsed_post.author
		stats_r = p.statsreddit

	except Post.DoesNotExist:
		# Create post
		p = Post(id=parsed_post.id, title=parsed_post.title, author=parsed_post.author, url=parsed_post.url, created_on_reddit=parsed_post.created_on, is_active=False, is_active_reddit=True)
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

	def is_image(self):
		if ('jpg' or 'png' or 'gif') in self.url[-5:]:
			return True
		return False
# 
# ==============================================================================