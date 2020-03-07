from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django import template
register=template.Library()
# Create your models here.
import misaka
from django.contrib.auth import get_user_model
User = get_user_model()

class Group(models.Model):
    name = models.CharField(max_length=256,unique=True)
    slug = models.SlugField(allow_unicode=True,unique=True)
    description = models.TextField(blank=True,defualt='')
    description_html = models.TextField(editable =False,defualt='',blank=True)
    members = models.ManyToManyField(User,through='GroupMember')

    def __str__(self):
        return self.name

    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        self.description_html = misaka.html(self.description)
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('groups:single',kwargs={'slug':self.slug})

    class Meta():
        ordering = ['name']


class GroupMembers(models.Model):

    group = models.ForeignKey(Group,related_name='memberships')
    user = models.ForeignKey(User,related_name='user_groups')

    def __str__(self):
        self.user.username

    class Meta():
        unique_together = ('group','user')
