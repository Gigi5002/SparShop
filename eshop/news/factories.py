import factory
from .models import New


class NewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = New

    title = factory.Sequence(lambda n: f'test new {n}')
