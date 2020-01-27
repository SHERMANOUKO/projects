from django.db import models

# Create your models here.
class Category(models.Model):
    categoryID = models.AutoField(primary_key=True)
    categoryName = models.CharField(max_length=100,unique=True)
    

class Books(models.Model):
    bookID = models.IntegerField(primary_key=True)
    bookName = models.CharField(max_length=100,unique=True)
    bookAuthor = models.CharField(max_length=100)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)


