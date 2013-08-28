from django.db import models
from django.template.defaultfilters import slugify

class ExampleModel(models.Model):
    name = models.CharField(max_length=50)

class AnotherExampleModel(models.Model):
    title = models.CharField(max_length=500)
    slug = models.SlugField(max_length=128, unique=True)
    author = models.CharField(max_length=500)
    region = models.ManyToManyField(ExampleModel)
    # status = models.ForeignKey(ExampleModel, null=True, blank=True)
    long_field = models.TextField()
    published = models.BooleanField(default=False)
    published_date = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='sr_imgs')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title[:128])
            existing = AnotherExampleModel.objects.filter(slug=self.slug).count()
            if existing:
                self.slug = "%s-%d" % (self.slug, existing+1)
        super(AnotherExampleModel, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('sr_details', (), { 'pk': self.pk })

    def get_abbr(self):
        return "sr"
