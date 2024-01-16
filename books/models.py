from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class BookAbstractModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Category(BookAbstractModel):
    title = models.CharField(max_length=100)


class AbstractReview(BookAbstractModel):
    rating = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=100)
    comment = models.TextField()

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()


class ProductInformation(BookAbstractModel):
    upc = models.CharField(max_length=100)
    product_type = models.CharField(max_length=100)
    price = models.FloatField()
    tax = models.FloatField()
    is_available = models.BooleanField(default=True)
    available_quantity = models.IntegerField(default=1)


class Book(BookAbstractModel):
    name = models.CharField(max_length=256)
    image = models.ImageField(upload_to="", default='images/default_book.png')
    description = models.TextField()

    abstract_review = GenericRelation(AbstractReview)
    product_information = models.OneToOneField(ProductInformation, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category)
