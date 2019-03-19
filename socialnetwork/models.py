from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    content       = models.CharField(max_length=300)
    post_creator    = models.ForeignKey(User, related_name="post_creators", on_delete=models.CASCADE)
    post_time = models.DateTimeField()
    def __str__(self):
    	return 'id=' + str(self.id) 


class Profile(models.Model):
	picture = models.FileField(blank=True)
	pic_saved = models.FileField(blank=True)
	user_bio     = models.CharField(max_length=200)
	content_type = models.CharField(max_length=50)
	user = models.ForeignKey(User,default=None, null=True,on_delete=models.PROTECT, related_name="profile_creators")
	followlist = models.ManyToManyField(User, related_name='follow', symmetrical=False)
	def __str__(self):
		return 'id=' + str(self.id)

class Comment(models.Model):
    content       = models.CharField(max_length=300)
    comment_creator    = models.ForeignKey(User, related_name="comment_creators", on_delete=models.CASCADE)
    comment_time = models.DateTimeField()
    post_id = models.CharField(max_length=100)
    creator_id=models.CharField(max_length=100)

    def __str__(self):
    	return 'id=' + str(self.id)
