from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
import os

class Post(models.Model):
	title = models.CharField(max_length=100)
	file = models.FileField(null=True,blank=True,upload_to='Files')
	content = models.TextField()
	date_posted = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.title

	def extension(self):
		name, extension = os.path.splitext(self.file.name)
		return extension

	def get_absolute_url(self):
		return reverse('post-detail', kwargs={'pk': self.pk})
	
	@property
	def has_approved_request(self):
		# Check if there's an approved download request for this post by the current user
		return self.download_requests.filter(requester=self.author, status='Approved').exists()


class DownloadRequest(models.Model):
    PENDING = 'Pending'
    APPROVED = 'Approved'
    DECLINED = 'Declined'
    
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (DECLINED, 'Declined')
    ]
    
    requester = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    
    def __str__(self):
        return f'Request for {self.post.title} by {self.requester.username}'

