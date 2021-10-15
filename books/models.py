from django.db import models
from django.urls import reverse

TOPIC_CHOICES = (
 ('general', 'General enquiry'),
 ('bug', 'Bug report'),
 ('suggestion', 'Suggestion'),
)


class Publisher(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    website = models.URLField()

    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("books:publisher_detail",kwargs={"pk":self.id})


class Author(models.Model):
    salutation = models.CharField(max_length=10)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    headshot = models.ImageField(upload_to="author_headshots")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("books:author_detail",kwargs={"pk":self.id})

class Book(models.Model):
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField("Author")
    publisher = models.ForeignKey(Publisher,on_delete=models.CASCADE)
    book = models.FileField(null=True,blank=True,upload_to="books")
    publication_date = models.DateField()


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("books:book_detail",kwargs={"pk":self.id})


class Contact(models.Model):
    topic = models.CharField(choices=TOPIC_CHOICES,max_length=40)
    message = models.CharField(max_length=200)
    sender = models.EmailField(null=True,blank=True)

    def __str__(self):
        return self.topic






