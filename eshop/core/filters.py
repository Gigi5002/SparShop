from .models import Product
import django_filters
from .forms import DatePicker


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        lookup_expr="icontains",
        label="Название"
    )
    price__gte = django_filters.NumberFilter(
        field_name='price',
        lookup_expr="gte",
        label="Цена, от"
    )
    price__lte = django_filters.NumberFilter(
        field_name='price',
        lookup_expr="lte",
        label="Цена, до"
    )

    guarantee__lt = django_filters.DateFilter(
        field_name='guarantee',
        lookup_expr='lt',
        widget=DatePicker,
    )

    class Meta:
        model = Product
        fields = [
            'name', 'category',
            'price__gte', 'price__lte',
            'guarantee__lt',
        ]

