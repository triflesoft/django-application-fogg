from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def _load_country(self):
        from ...models import Country

        self._country = Country.objects.get(id=268)

    def _load_division_type_data(self, path):
        from json import load
        from collections import OrderedDict

        with open(path, 'r') as file:
            self._division_type_data = load(file, object_pairs_hook=OrderedDict)

    def _parse_division_type_data(self):
        from ...models import CountryDivisionType

        self._division_type_id = 26800000
        self._division_type_objects = []
        self._division_type_name_objects = []
        self._division_type_map = {}

        division_type_name_model = CountryDivisionType._meta._sazed_localization_models['name']

        for datum in self._division_type_data:
            self._division_type_id += 1
            division_type = CountryDivisionType(id=self._division_type_id, country=self._country, code=datum['code'])
            self._division_type_objects.append(division_type)
            self._division_type_map[datum['code']] = division_type

            for language_code, value in datum['name'].items():
                division_type_name = division_type_name_model(target=division_type, language_code=language_code, value=value)
                self._division_type_name_objects.append(division_type_name)

    def _create_division_type_objects(self):
        from ...models import CountryDivisionType

        division_type_name_model = CountryDivisionType._meta._sazed_localization_models['name']

        CountryDivisionType.objects.bulk_create(self._division_type_objects)
        division_type_name_model.objects.bulk_create(self._division_type_name_objects)

    def _load_division_data(self, path):
        from json import load
        from collections import OrderedDict

        with open(path, 'r') as file:
            self._division_data = load(file, object_pairs_hook=OrderedDict)

    def _parse_division_data_tree(self, name_model, parent, data):
        from ...models import CountryDivision
        from ...models import PostalZone
        from uuid import uuid4

        for datum in data:
            if 'postal_code' in datum:
                postal_zone_code = datum['postal_code']

                if postal_zone_code in self._postal_zone_objects:
                    postal_zone = self._postal_zone_objects[postal_zone_code]
                else:
                    postal_zone = PostalZone(id=268000000 + int(postal_zone_code), country=self._country, code=postal_zone_code)
                    self._postal_zone_objects[postal_zone_code] = postal_zone
            else:
                postal_zone = None

            self._division_id += 1

            division = CountryDivision(
                id=self._division_id,
                country=self._country,
                country_division_type=self._division_type_map[datum['type']],
                parent=parent,
                postal_zone=postal_zone,
                code=datum['code'] if 'code' in datum else str(uuid4()),
                latitude_min=0,
                latitude_max=0,
                longitude_min=0,
                longitude_max=0,
                geoname_id=None)

            self._division_objects.append(division)

            for language_code, value in datum['name'].items():
                division_name = name_model(target=division, language_code=language_code, value=value)
                self._division_name_objects.append(division_name)

            if 'children' in datum:
                self._parse_division_data_tree(name_model, division, datum['children'])

    def _parse_division_data(self):
        from ...models import CountryDivision

        self._division_id = 268000000
        self._division_objects = []
        self._division_name_objects = []
        self._postal_zone_objects = {}

        division_name_model = CountryDivision._meta._sazed_localization_models['name']

        self._parse_division_data_tree(division_name_model, None, self._division_data)

    def _create_division_objects(self):
        from ...models import CountryDivision
        from ...models import PostalZone

        division_name_model = CountryDivision._meta._sazed_localization_models['name']

        PostalZone.objects.bulk_create(self._postal_zone_objects.values())
        CountryDivision.objects.bulk_create(self._division_objects)
        division_name_model.objects.bulk_create(self._division_name_objects)

    def handle(self, *args, **options):
        from os.path import abspath
        from os.path import dirname
        from os.path import join

        json_path = dirname(abspath(__file__))

        self._load_country()
        self._load_division_type_data(join(json_path, 'fogg_ge_division_types.json'))
        self._parse_division_type_data()
        self._create_division_type_objects()
        self._load_division_data(join(json_path, 'fogg_ge_divisions.json'))
        self._parse_division_data()
        self._create_division_objects()
