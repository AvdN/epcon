import datetime

import factory
import factory.django
import factory.fuzzy

from django.template.defaultfilters import slugify

from django_factory_boy import auth as auth_factories

class AttendeeProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'conference.AttendeeProfile'

    user = factory.SubFactory(auth_factories.UserFactory)
    slug = factory.LazyAttribute(lambda a: slugify("%s %s" % (a.user.first_name, a.user.last_name)))
    uuid = factory.Faker('uuid4')

    birthday = factory.fuzzy.FuzzyDate(start_date=datetime.date(1950, 1, 1))
