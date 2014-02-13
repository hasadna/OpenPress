from django.db import models
from django.conf.global_settings import LANGUAGES

gettext_noop = lambda s: s

# Create your models here.

# Logical-Physical Models


class Archive(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(null=True)
    archive_owner = models.CharField(max_length=128, default='NLI')  # Name of organization
    # archive_admin = models.ForeignKey('User')

    def __unicode__(self):
        return unicode(self.name)


class Title(models.Model):
    archive = models.ForeignKey('Archive')
    name = models.CharField(max_length=128)
    display_name = models.CharField(max_length=128)
    description = models.TextField(null=True)
    Founder = models.CharField(max_length=128)  # TODO: Change to ForeignKey, person
    country_of_publication = models.CharField(max_length=128)  # TODO: Change to django-countries

    def __unicode__(self):
        return unicode(self.name)


class Volume(models.Model):
    title = models.ForeignKey('Title')
    serial = models.CharField(max_length=128)
    standardized_serial = models.CharField(max_length=128)  # TODO: Create as True standardized serial
    date_of_publication = models.DateTimeField()
    volume_of_distribution = models.IntegerField()
    language = models.CharField(max_length=128, choices=LANGUAGES, default=('he', gettext_noop('Hebrew')))
    is_weekend = models.BooleanField(default=False)  # TODO: Calculate from date_of_publication?
    is_unique_publication = models.BooleanField(default=False)  # TODO:  Change to ForeignKey, events

    def __unicode__(self):
        return unicode(self.title) + '_' + unicode(self.serial)

    class Meta:
        unique_together = ('title', 'serial')


class Staff(models.Model):
    volume = models.OneToOneField('Volume', related_name='staff')
    chief_editor = models.CharField(max_length=128)  # TODO: Change to ForeignKey, person
    owner_of_title_at_time_of_publication = models.CharField(max_length=128)  # TODO: Change to ForeignKey, person
    contributors = models.TextField(max_length=128)  # TODO: Change to OneToMany Relation


class Section(models.Model):
    volume = models.ForeignKey('Volume')
    name = models.CharField(max_length=128)
    section_editor = models.CharField(max_length=128)  # TODO: Change to ForeignKey, person
    section_staff = models.TextField(max_length=128)  # TODO: Change to OneToMany Relation

    def __unicode__(self):
        return unicode(self.volume) + '_' + unicode(self.name)

    class Meta:
        unique_together = ('volume', 'name')


# Logical Model

class Article(models.Model):
    section = models.ForeignKey('Section')
    description = models.TextField(null=True)
    title = models.TextField()
    secondary_title = models.TextField()
    contributor = models.CharField(max_length=128)  # TODO: Change to ForeignKey, person
    is_commercial = models.BooleanField(default=False)

    def __unicode__(self):
        return unicode(self.section) + '_' + unicode(self.title)


# Physical Model
class Page(models.Model):
    section = models.ForeignKey('Section')
    articles = models.ManyToManyField(Article, related_name='pages')
    page_number = models.IntegerField()
    is_back_cover = models.BooleanField(default=False)
    is_front_cover = models.BooleanField(default=False)
    width = models.IntegerField()
    height = models.IntegerField()

    class Meta:
        unique_together = ('section', 'page_number')

    def __unicode__(self):
        return unicode(self.section) + '_' + unicode(self.page_number)


# Logical-Physical Models
class Paragraph(models.Model):
    article = models.ForeignKey('Article', related_name='paragraphs')
    page = models.ForeignKey('Page')
    paragraph_number = models.IntegerField()
    title = models.CharField(max_length=128)  # TODO: Separate model?
    image_source = models.URLField()  # TODO: Separate model?, change to ImageField
    extracted_text = models.TextField()  # TODO: Separate model? OCR

    class Meta:
        unique_together = ('article', 'paragraph_number')

    def __unicode__(self):
        return unicode(self.article) + '_' + unicode(self.paragraph_number)
