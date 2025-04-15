from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
#from django_jalali.db import models as jmodels
from django.urls import reverse
from django_resized import ResizedImageField
from django.template.defaultfilters import slugify

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Costumer.Status.PUBLISHED)


class Costumer(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
        REJECTED = 'RJ', 'Rejected'

    CATEGORY_CHOICES = (
        ('برنامه غذایی', 'برنامه غذایی'),
        ('برنامه ورزشی', 'برنامه ورزشی'),
        ('این بادی', 'این بادی'),
        ('اطلاعات پرداخت', 'اطلاعات پرداخت'),
        ('سایر', 'سایر'),
    )


    user_c = models.ForeignKey(User, on_delete=models.CASCADE, related_name="costum_posts", verbose_name="مشتری")
    title = models.CharField(max_length=250, verbose_name="عنوان")
    description = models.TextField(verbose_name="توضیحات")
    publish = models.DateTimeField(default=timezone.now, verbose_name="تاریخ انتشار")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.PUBLISHED, verbose_name="وضعیت")
    objects = models.Manager()
    published = PublishedManager() 
    category = models.CharField( verbose_name="دسته بندی", max_length=20, choices=CATEGORY_CHOICES, default='سایر')


    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish'])
        ]
        verbose_name = "اطلاعات جدید"
        verbose_name_plural = "اطلاعات جدید"

    def __str__(self):
       return self.title
    
    def get_absolute_url(self):
        return reverse('gym:post_detail', args=[self.id])
    

    def delete(self, *args, **kwargs):
        for img in self.images.all():
            storage, path = img.image_file.storage , img.image_file.path
            storage.delete(path)
        super().delete(*args, **kwargs)


    
class Image(models.Model):

    post = models.ForeignKey(Costumer, related_name='images',on_delete=models.CASCADE,verbose_name='تصویر')
    image_file = ResizedImageField(upload_to='post_image/', height_field=None, width_field=None, max_length=None)
    title =  models.CharField(max_length=250,verbose_name ='عنوان',null=True,blank=True )
    description = models.TextField(verbose_name = "توضیحات",null=True,blank=True )
    created = models.DateTimeField(auto_now_add =True,verbose_name='تاریخ ایجاد')

    def __str__(self):
        return self.title if self.post else 'None'

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created'])
        ]
        verbose_name = "تصویر"
        verbose_name_plural = 'تصاویر' 

    def delete(self, *args, **kwargs):
        storage, path = self.image_file.storage , self.image_file.path
        storage.delete(path)
        super().delete(*args, **kwargs)
    def __str__(self):
        return self.title if self.title else "None"
 


class Ticket(models.Model):
    message = models.TextField(verbose_name="پیام")
    name = models.CharField(max_length=250, verbose_name="نام")
    email = models.EmailField(verbose_name="ایمیل")
    phone = models.CharField(max_length=11, verbose_name="شماره تماس")
    subject = models.CharField(max_length=250, verbose_name="موضوع")

    class Meta:
        verbose_name = "تیکت"
        verbose_name_plural = "تیکت ها"

    def __str__(self):
        return self.subject

class Account(models.Model):
    user = models.OneToOneField(User, related_name="account", on_delete=models.CASCADE)
    date_of_birth = models.DateField(verbose_name="تاریخ تولد", blank=True, null=True)
    bio = models.TextField(verbose_name="بایو", null=True, blank=True)
    photo = ResizedImageField(verbose_name="تصویر", upload_to="account_images/", size=[500, 500], quality=60, crop=['middle', 'center'], blank=True, null=True)
    job = models.CharField(max_length=250, verbose_name="شغل", null=True, blank=True)

    def __str__(self):
        return self.user.username
    class Meta:
        verbose_name = "اکانت"
        verbose_name_plural = "اکانت ها"
