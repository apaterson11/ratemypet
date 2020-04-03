from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=250)
    views = models.IntegerField(default=0)
    slug = models.SlugField(max_length=250, unique=True)
    
    types = [
        ('DO', 'Dog'),
        ('CA', 'Cat'),
        ('FI', 'Fish'),
        ('RE', 'Reptile'),
        ('RO', 'Rodent'),
        ('OT', 'Other'),
    ]
    
    animalType = models.CharField(max_length=2, choices=types, primary_key = True, default = 'OT')
    
    def save(self, *args, **kwargs):
        for t in self.types:
            if t[0] == self.animalType:
                name = t[1]
        print(name)
        if name == 'fish' or name == 'other':
            self.slug = slugify(name)
        else:
            self.slug = slugify(name + 's')
        super(Category, self).save(*args, **kwargs)
    
    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_absoulte_url(self):
        return reverse('purrfectpets:list_of_post_by_category', args=[self.slug])

    
    def __str__(self):
        return self.slug
        
 
class Pet(models.Model):            
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default='OT', null=True)
    MAX_LENGTH = 128
    owner = models.ForeignKey(User,on_delete=models.CASCADE, related_name="owner", null=True)
    name = models.CharField(max_length=MAX_LENGTH, null=True)
    breed = models.CharField(max_length=MAX_LENGTH, null=True)
    bio = models.TextField(max_length=1000, null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    slug = models.SlugField(max_length = MAX_LENGTH, unique = True)

    views = models.IntegerField(default=0)
    
    awwSenders = models.ManyToManyField(User, related_name="awwSenders",blank = True)
    
    awwCount = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Pet, self).save(*args, **kwargs)

class PetPhoto(models.Model):

    pet = models.ForeignKey(Pet, on_delete = models.CASCADE, related_name="pet", parent_link = True, null=True)
    
    photo = models.ImageField(upload_to = 'uploads/')


"""
This is a model for storing the comments made by users on the site. It stores the pet which has had a comment made of, 
this is a foreign key which links to the Pet model. The model also stores the name of the user who made the comment, 
the body which is the actual comment and the date which the comment was written on.
"""

class Comment(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='comments')
    name = models.ForeignKey(User,on_delete=models.CASCADE, related_name="commenter", null=True)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    #The most recent comments are displayed first 
    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return "Comment {} by {}".format(self.body, self.name)

    