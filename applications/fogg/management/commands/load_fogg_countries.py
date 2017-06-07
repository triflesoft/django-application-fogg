from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        from ...models import Country
        from json import load
        from os.path import abspath
        from os.path import dirname
        from os.path import join

        json_path = dirname(abspath(__file__))

        with open(join(json_path, 'fogg_countries.json'), 'r') as file:
            country_data = load(file)

        country_objects = []

        for country_datum in country_data:
            country = Country(
                id=country_datum['id'],
                iso2=country_datum['iso2'],
                iso3=country_datum['iso3'],
                isoN=country_datum['isoN'],
                fips=country_datum['fips'],
                continent=country_datum['continent'],
                tld=country_datum['tld'],
                currency_code=country_datum['currency_code'],
                phone_number_prefix=country_datum['phone_number_prefix'],
                phone_number_regex=country_datum['phone_number_regex'],
                postal_code_format=country_datum['postal_code_format'],
                postal_code_regex=country_datum['postal_code_regex'],
                geoname_id=country_datum['geoname_id'],
                _name_localizations=country_datum['name'])
            country_objects.append(country)

        Country.objects.bulk_create(country_objects)
