from django.contrib import admin

from .models import Country
from .models import CountryDivision
from .models import CountryDivisionType
from .models import PostalZone


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    fieldsets = [
        ('General',  {
            'classes': ('wide',),
            'fields': [
                ('id',), ('iso2',), ('iso3',), ('isoN',),
                ('fips',), ('continent',), ('tld',), ('currency_code',),
                ('phone_number_prefix',), ('phone_number_regex',),
                ('postal_code_format',), ('postal_code_regex',),
                ('geoname_id',)]
        }),
    ]
    list_display = ['id', 'iso2', 'iso3', 'name']
    ordering = ['iso3']
    search_fields = ['iso2', 'iso3', 'phone_prefix']


@admin.register(PostalZone)
class PostalZoneAdmin(admin.ModelAdmin):
    fieldsets = [
        ('General',  {
            'classes': ('wide',),
            'fields': [('country',), ('code',)]
        }),
    ]
    list_display = ['id', 'country', 'code']
    list_filter = ['country']
    ordering = ['code']
    search_fields = ['code']


@admin.register(CountryDivisionType)
class CountryDivisionTypeAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        queryset = super(CountryDivisionTypeAdmin, self).get_queryset(request)
        queryset = queryset.prefetch_related(
            '_name_localizations',
            'country___name_localizations')

        return queryset

    fieldsets = [
        ('General',  {
            'classes': ('wide',),
            'fields': [('country',), ('code',)]
        }),
    ]
    list_display = ['id', 'country', 'code', 'name']
    list_filter = ['country__iso3']
    ordering = ['code']
    search_fields = ['code']


@admin.register(CountryDivision)
class CountryDivisionAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        queryset = super(CountryDivisionAdmin, self).get_queryset(request)
        queryset = queryset.prefetch_related(
            '_name_localizations',
            'country_division_type___name_localizations',
            'country___name_localizations')

        return queryset

    fieldsets = [
        ('General',  {
            'classes': ('wide',),
            'fields': [
                ('country',), ('country_division_type',), ('parent',), ('postal_zone',), ('code',),
                ('latitude_min',), ('latitude_max',), ('longitude_min',), ('longitude_max',),
                ('geoname_id',)]
        }),
    ]
    list_display = ['id', 'country', 'country_division_type', 'parent', 'postal_zone', 'code', 'name', 'geoname_id']
    list_filter = ['country_division_type__code', 'country__iso3']
    ordering = ['code']
    search_fields = ['code', 'country__code', 'postal_zone__code']
