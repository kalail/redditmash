from django.db import models


class Post(models.Model):
	id = models.CharField(max_length=32, primary_key=True)
	title = models.TextField()
	author = models.TextField()
	url = models.URLField()
	is_active = models.BooleanField()
	is_active_reddit = models.BooleanField()
	created_on = models.DateTimeField(auto_now_add=True)
	created_on_reddit = models.DateTimeField()

	def __unicode__(self):
		return self.title

class Choice(models.Model):
	post_1 = models.ForeignKey(Post, related_name='post_1')
	post_2 = models.ForeignKey(Post, related_name='post_2')
	times_completed = models.IntegerField()
	is_active = models.BooleanField()
	created_on = models.DateTimeField(auto_now_add=True)


class StatsReddit(models.Model):
	post = models.OneToOneField(Post)
	score = models.IntegerField()
	rank = models.IntegerField()
	edited_on = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return str(self.rank)

class Stats(models.Model):
	post = models.OneToOneField(Post)
	rating = models.FloatField()
	rank = models.IntegerField()
	edited_on = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return str(self.rating)

# class MediaType(models.Model):
# 	name = models.CharField(max_length=128)
# 	posts = models.ManyToManyField(Post)