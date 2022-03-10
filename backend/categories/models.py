from django.db.models import *

from translation.translate import translate_model


@translate_model
class FinanceCategory(Model):
    name = CharField(max_length=63)

    class Meta:
        ordering = 'id',

    def __str__(self):
        return self.name


@translate_model
class GrantCategory(Model):
    name = CharField(max_length=63)

    class Meta:
        ordering = 'id',

    def __str__(self):
        return self.name


@translate_model
class PropagationIntendedForCategory(Model):
    name = CharField(max_length=63)

    class Meta:
        ordering = 'id',

    def __str__(self):
        return self.name


@translate_model
class DietCategory(Model):
    name = CharField(max_length=63)

    class Meta:
        ordering = 'id',

    def __str__(self):
        return self.name


@translate_model
class QualificationCategory(Model):
    name = CharField(max_length=63)
    description = CharField(max_length=255)
    parent = ForeignKey('QualificationCategory', on_delete=PROTECT, related_name='included_qualifications', blank=True,
                        null=True)

    class Meta:
        ordering = 'id',

    def __str__(self):
        return self.name