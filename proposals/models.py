from django.db import models
from django.contrib.auth.models import User

class Proposal(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    industry = models.CharField(max_length=100)
    client_email = models.EmailField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class ProposalDocument(models.Model):
    proposal = models.ForeignKey(Proposal, related_name='documents', on_delete=models.CASCADE)
    file = models.FileField(upload_to='proposals/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name

