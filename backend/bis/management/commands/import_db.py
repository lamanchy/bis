import json
import re
from datetime import timedelta
from os import mkdir
from os.path import join, exists
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import urlretrieve
from zoneinfo import ZoneInfo

from django.core.management.base import BaseCommand
from django.utils.datetime_safe import date, datetime
from django.utils.timezone import now

from administration_units.models import AdministrationUnit, AdministrationUnitAddress, BrontosaurusMovement
from bis.models import User, UserAddress, Qualification, Location, Membership, UserEmail
from categories.models import MembershipCategory, EventCategory, EventProgramCategory, QualificationCategory, \
    AdministrationUnitCategory, PropagationIntendedForCategory, DietCategory, GrantCategory
from event.models import Event, EventPropagation, EventRegistration, EventRecord, EventFinance, VIPEventPropagation, \
    EventPropagationImage
from project.settings import BASE_DIR


def parse_date(data):
    if data:
        year, month, day = data.split('-')
        year, month, day = int(year), int(month), int(day)
        if not month: month = 1
        if not day: day = 1
        if not year: return
        data = date(year, month, day)

    return data


def parse_int(data):
    if data: data = int(data)
    return data


def get_event_start(item):
    start = parse_date(item['od'])
    if start:
        start = datetime(year=start.year, month=start.month, day=start.day, tzinfo=ZoneInfo(key='Europe/Prague'))
        if item['sraz']:
            time = item['sraz']
            time = time.replace('.', ':')
            if len(time.split(':')) > 1:
                hours, minutes = time.split(':', 1)
                hours = ''.join([i for i in hours if i in '0123456789'])
                minutes = ''.join([i for i in minutes if i in '0123456789'])
                if hours and minutes:
                    hours = int(hours) % 24
                    minutes = int(minutes) % 60
                    start += timedelta(hours=hours, minutes=minutes)

    if not start:
        start = parse_date(item['do'])
        if start:
            start = datetime(year=start.year, month=start.month, day=start.day, tzinfo=ZoneInfo(key='Europe/Prague'))
    return start


class Command(BaseCommand):
    help = "Import old BIS's database, exported as json from https://phpmyadmin.brontosaurus.cz/, user: bis_ro"
    file_path = join(BASE_DIR, 'old_database_dump', 'db.json')
    id_table_names = ['adresa', 'akce', 'akce_typ', 'clen', 'clen_typ', 'dar', 'darce', 'dar_divne', 'klub',
                      'lokalita', 'program', 'tabor', 'zc', 'qual_typ', 'ohb_instruktor', 'ohb_konzultant', 'qal']

    # TODO akce, dar, darce, dar_divne, tabor, prihlaska, ucastnik

    director_id = "2780"
    headquarters_id = "179"
    admin_ids = ['27987', '17371']

    membership_category_map = {
        "1": MembershipCategory.objects.get(slug='adult'),
        "2": MembershipCategory.objects.get(slug='family'),
        "3": MembershipCategory.objects.get(slug='family_member'),
        "4": MembershipCategory.objects.get(slug='kid'),
        "5": MembershipCategory.objects.get(slug='member_elsewhere'),
        "6": MembershipCategory.objects.get(slug='student'),
    }

    event_category_map = {
        "1": EventCategory.objects.get(slug="public__volunteering__with_experience"),
        "2": EventCategory.objects.get(slug="public__only_experiential"),
        "6": EventCategory.objects.get(slug="public__educational__course"),
        "7": EventCategory.objects.get(slug="internal__general_meeting"),
        "12": EventCategory.objects.get(slug="public__educational__educational"),
        "13": EventCategory.objects.get(slug="public__educational__educational_with_stay"),
        "14": EventCategory.objects.get(slug="public__other__exhibition"),
        "17": EventCategory.objects.get(slug="internal__volunteer_meeting"),
        "18": EventCategory.objects.get(slug="public__educational__lecture"),
        "19": EventCategory.objects.get(slug="public__club__meeting"),
        "5": EventCategory.objects.get(slug="public__sports"),
        "21": EventCategory.objects.get(slug="public__educational__ohb"),
        "20": EventCategory.objects.get(slug="internal__section_meeting"),
        "22": EventCategory.objects.get(slug="public__other__eco_tent"),
        "10": EventCategory.objects.get(slug="public__other__for_public"),
        "25": EventCategory.objects.get(slug="public__club__lecture"),
    }

    event_program_category_map = {
        "1": EventProgramCategory.objects.get(slug='nature'),
        "2": EventProgramCategory.objects.get(slug='monuments'),
        "3": EventProgramCategory.objects.get(slug='holidays_with_brontosaurus'),
        "4": EventProgramCategory.objects.get(slug='kids'),
        "5": EventProgramCategory.objects.get(slug='eco_tent'),
        "6": EventProgramCategory.objects.get(slug='education'),
        None: EventProgramCategory.objects.get(slug='none'),
    }

    qualification_category_map = {
        "1": QualificationCategory.objects.get(slug="OHB"),
        "4": QualificationCategory.objects.get(slug="HVDT"),
        "5": QualificationCategory.objects.get(slug="ODHB"),
        "6": QualificationCategory.objects.get(slug="VP"),
        "7": QualificationCategory.objects.get(slug="OpDHB"),
        "9": QualificationCategory.objects.get(slug="OvHB"),
        "Konzultant": QualificationCategory.objects.get(slug="Konzultant"),
        "Instruktor": QualificationCategory.objects.get(slug="Instruktor"),
    }

    administration_unit_category_map = {
        "1": AdministrationUnitCategory.objects.get(slug='club'),
        "2": AdministrationUnitCategory.objects.get(slug='basic_section'),
        "3": AdministrationUnitCategory.objects.get(slug='regional_center'),
        "4": AdministrationUnitCategory.objects.get(slug='headquarter'),
    }

    propagation_indented_for_category_map = {
        "1": PropagationIntendedForCategory.objects.get(slug='for_all'),
        "2": PropagationIntendedForCategory.objects.get(slug='for_young_and_adult'),
        "3": PropagationIntendedForCategory.objects.get(slug='for_kids'),
        "4": PropagationIntendedForCategory.objects.get(slug='for_parents_with_kids'),
        "5": PropagationIntendedForCategory.objects.get(slug='for_first_time_participant'),
    }

    diet_category_map = {
        "0": DietCategory.objects.get(slug='meat'),
        "3": DietCategory.objects.get(slug='meat'),
        "1": DietCategory.objects.get(slug='vege'),
        "2": DietCategory.objects.get(slug='meat'),
        None: DietCategory.objects.get(slug='no_food'),
    }

    grant_category_map = {
        "0": GrantCategory.objects.get(slug='none'),
        "1": GrantCategory.objects.get(slug='msmt'),
        "2": GrantCategory.objects.get(slug='other'),
        "3": GrantCategory.objects.get(slug='other'),
    }

    progresses = {}

    def print_progress(self, slug, i, total):
        if slug not in self.progresses:
            self.progresses[slug] = now()

        if (now() - self.progresses[slug]).seconds > 1:
            print(f"importing {slug}, progress {100 * i / total:.2f}%")
            self.progresses[slug] = now()

    def load_data(self):
        if not exists(self.file_path):
            print(self.file_path, 'does not exists')
            return

        with open(self.file_path, 'r', encoding='utf-8') as file:
            raw_data = json.loads(file.read())

        data = {}
        for item in raw_data:
            if item['type'] != 'table':
                continue

            name = item['name']

            if name not in self.id_table_names:
                data[name] = item['data']
                continue

            data[name] = {}
            for obj in item['data']:
                data[name][obj['id']] = obj

        return data

    user_map = {u._import_id: u for u in User.objects.all()}

    def import_users(self, data):
        for item in data['falesne_duplicity']:
            if item['adr1'] not in data['adresa'] or item['adr2'] not in data['adresa']:
                continue
            if data['adresa'][item['adr2']]['email']:
                data['adresa'][item['adr1']]['email'] = data['adresa'][item['adr2']]['email']
            if data['adresa'][item['adr1']]['email']:
                data['adresa'][item['adr2']]['email'] = data['adresa'][item['adr1']]['email']

        for i, (id, item) in enumerate(data['adresa'].items()):
            self.print_progress('users', i, len(data['adresa']))

            birthday = parse_date(item['datum_narozeni'])

            user = User.objects.update_or_create(_import_id=id, defaults=dict(
                first_name=item['jmeno'],
                last_name=item['prijmeni'],
                nickname=item['prezdivka'] or '',
                phone=item['telefon'] or '',
                birthday=birthday,
                is_active=True,
            ))[0]
            if item['email']:
                UserEmail.objects.update_or_create(email=item['email'], defaults=dict(user=user))

            street = item["ulice"]
            city = item["mesto"]
            zip_code = item["psc"]

            if street and city and zip_code:
                UserAddress.objects.update_or_create(user=user, defaults=dict(
                    street=street,
                    city=city,
                    zip_code=zip_code
                ))

            self.user_map[id] = user

    def import_qualifications(self, data):
        print('importing qualifications')
        for id, item in data['qal'].items():
            if not item['od']: continue

            if not item['schvalil']:
                item['schvalil'] = self.director_id

            since = parse_date(item['od'])
            till = parse_date(item['do'])
            if not till: till = since + timedelta(days=365)

            Qualification.objects.update_or_create(
                _import_id=id,
                defaults=dict(
                    user=self.user_map[item['kdo']],
                    category=self.qualification_category_map[item['druh']],
                    valid_since=since,
                    valid_till=till,
                    approved_by=self.user_map[item['schvalil']],
                )
            )

        for id, item in data['ohb_instruktor'].items():
            Qualification.objects.update_or_create(
                _import_id=id,
                defaults=dict(
                    user=self.user_map[item['kdo']],
                    category=self.qualification_category_map['Instruktor'],
                    valid_since=parse_date(item['od']),
                    valid_till=parse_date(item['do']),
                    approved_by=self.user_map[self.director_id],
                )
            )

        for id, item in data['ohb_konzultant'].items():
            Qualification.objects.update_or_create(
                _import_id=id,
                defaults=dict(
                    user=self.user_map[item['kdo']],
                    category=self.qualification_category_map['Konzultant'],
                    valid_since=parse_date(item['od']),
                    valid_till=parse_date(item['do']),
                    approved_by=self.user_map[self.director_id],
                )
            )

    administration_unit_map = {au._import_id: au for au in AdministrationUnit.objects.all()}

    def import_administration_units(self, data):
        print('importing administration units')
        for id, item in data['klub'].items():
            since, till = item['reg_od'], item['reg_do']
            if since: since += '-01-01'
            if till: till += '-12-31'
            chairman = None
            if item['predseda']:
                chairman = self.user_map[item['predseda']]

            manager = None
            board_members = []
            ic = None
            bank_account_number = None
            if id in data['zc']:
                if data['zc'][id]['hospodar'] in self.user_map:
                    manager = self.user_map[data['zc'][id]['hospodar']]

                if data['zc'][id]['statutar'] in self.user_map:
                    board_members.append(self.user_map[data['zc'][id]['statutar']])
                if data['zc'][id]['statutar2'] in self.user_map:
                    board_members.append(self.user_map[data['zc'][id]['statutar2']])

                ic = data['zc'][id]['ic']
                bank_account_number = data['zc'][id]['ucet']

            administration_unit = AdministrationUnit.objects.update_or_create(
                _import_id=id,
                defaults=dict(
                    name=item['nazev'],
                    abbreviation=item['zkratka'],
                    is_for_kids=item['brdo'] == '1',
                    phone=item['telefon'],
                    email=item['email'],
                    www=item['www'],
                    existed_since=parse_date(since),
                    existed_till=parse_date(till),
                    chairman=chairman,
                    manager=manager,
                    category=self.administration_unit_category_map[item['uroven']],
                    ic=ic,
                    bank_account_number=bank_account_number,
                )
            )[0]

            for board_member in board_members:
                administration_unit.board_members.add(board_member)

            street, city = item['ulice'], item['mesto']
            if not street:
                street, city = item['adresa'].rsplit(' ', 1)

            AdministrationUnitAddress.objects.update_or_create(
                administration_unit=administration_unit,
                defaults=dict(
                    street=street,
                    city=city,
                    zip_code=item['psc'],
                )
            )

            self.administration_unit_map[id] = administration_unit

    location_map = {l._import_id: l for l in Location.objects.all()}

    def import_locations(self, data):
        print('importing locations')
        for id, item in data['lokalita'].items():
            location = Location.objects.update_or_create(
                _import_id=id,
                defaults=dict(
                    name=item['nazev'],
                    patron=self.user_map.get(item['patron'], None),
                    address=item['misto'],
                    gps_location=None,
                )
            )[0]
            self.location_map[id] = location

    def import_memberships(self, data):
        for i, (id, item) in enumerate(data['clen'].items()):
            self.print_progress('memberships', i, len(data['clen']))

            if item['klub'] not in self.administration_unit_map or item['adresa'] not in self.user_map:
                continue

            Membership.objects.update_or_create(
                _import_id=id,
                defaults=dict(
                    user=self.user_map[item['adresa']],
                    category=self.membership_category_map[item['typ']],
                    administration_unit=self.administration_unit_map[item['klub']],
                    year=parse_date(item['od']).year,
                )
            )

    def get_attachments(self, item):
        attachments = set()
        for i in range(10):
            attachment = item.get(f"priloha_{i}")
            if attachment:
                attachments.add(attachment)

        return attachments

    event_map = {e._import_id: e for e in Event.objects.all()}

    def import_events(self, data):
        event_organizer_map = {}
        for item in data['porada']:
            # throw away M2M, since there are only few events (200/10000)
            # that had multiple organizing units
            event_organizer_map[item['akce']] = item['klub']

        for i, (id, item) in enumerate(data['akce'].items()):
            self.print_progress('events', i, len(data['akce']))
            attachments = self.get_attachments(item)
            if id in data['tabor']:
                attachments = attachments.union(self.get_attachments(data['tabor'][id]))
                item.update(data['tabor'][id])

            start = get_event_start(item)
            end = parse_date(item['do'])
            is_canceled = False
            if not start:
                start = datetime(2000, 1, 1, tzinfo=ZoneInfo(key='Europe/Prague'))
                end = datetime(2000, 1, 1, tzinfo=ZoneInfo(key='Europe/Prague'))
                is_canceled = True

            contact = None
            if item['kontakt_email']:
                contact = User.objects.filter(emails__email=item['kontakt_email']).first()

            location = None
            if item['lokalita']:
                location = self.location_map[item['lokalita']]
            elif item['lokalita_jina']:
                location = Location.objects.filter(name=item['lokalita_jina']).first()
                if not location:
                    location = Location.objects.create(name=item['lokalita_jina'])
                if not location.address and item['gps']:
                    location.address = item['gps']
                    location.save()

            event = Event.objects.update_or_create(_import_id=id, defaults=dict(
                name=item['nazev'][:63],
                start=start,
                end=end,
                is_canceled=is_canceled,
                location=location,
                category=self.event_category_map[item['typ']],
                program=self.event_program_category_map[item['program']],
                administration_unit=self.administration_unit_map[event_organizer_map.get(id, self.headquarters_id)],
                main_organizer=self.user_map.get(item.get('odpovedna')),
                is_internal=item['zamereno_na_cleny'] == '1',
                number_of_sub_events=item['pocet'],
                internal_note=item['poznamka'] or '',
            ))[0]

            self.event_map[id] = event

            EventFinance.objects.update_or_create(event=event, defaults=dict(
                grant_category=self.grant_category_map[item['dotace']],
                # grant_amount
                # total_event_cost
                # budget
            ))
            event_propagation = EventPropagation.objects.update_or_create(event=event, defaults=dict(
                is_shown_on_web=item['zverejnit'] == '1',
                minimum_age=parse_int(item['vek_od']),
                maximum_age=parse_int(item['vek_do']),
                cost=re.split(r'\D+', item['poplatek'] or '')[0] or 0,
                intended_for=self.propagation_indented_for_category_map[item['prokoho']],
                accommodation=item.get('ubytovani') or '',
                diet=self.diet_category_map[item.get('strava')],
                organizers=item['org'] or '',
                web_url=item['web'] or '',
                _contact_url=item['kontakt_url'] or '',
                invitation_text_introduction=item['text_uvod'] or '',
                invitation_text_practical_information=item['text_info'] or '',
                invitation_text_work_description=item['text_dobr'] or '',
                invitation_text_about_us=item['text_mnam'] or '',
                contact_person=contact,
                contact_name=item['kontakt'] or '',
                contact_phone=item['kontakt_telefon'] or '',
                contact_email=item['kontakt_email'] or '',
            ))[0]
            if item.get('vip') == '1':
                VIPEventPropagation.objects.update_or_create(event_propagation=event_propagation, defaults=dict(
                    goals_of_event=item['popis_programu'] or '',
                    program=item['tema'] or '',
                    short_invitation_text=item['text_kratsi'] or '',
                    rover_propagation=item.get('rover') == '1',
                    working_hours=item['pracovni_doba'],
                    working_days=item['pracovni_dny'],

                ))
            EventRegistration.objects.update_or_create(event=event, defaults=dict(
                is_registration_required=item['prihlaska'] == '4',
                is_event_full=item['prihlaska'] == '5',
                # 'add_info_title': None,
                # 'add_info_title_2': None,
                # 'add_info_title_3': None,
            ))
            EventRecord.objects.update_or_create(event=event, defaults=dict(
                total_hours_worked=item['odpracovano'],
                comment_on_work_done=item['prace_jine'] or '',
                has_attendance_list=item['adresar'] == '1',
                number_of_participants=item['lidi'],
                number_of_participants_under_26=item['lidi_do26'],
            ))

            for attachment in attachments:
                file_path = join(BASE_DIR, 'media', 'event_propagation_images', attachment)
                if not exists(file_path):
                    try:
                        urlretrieve(f"https://bis.brontosaurus.cz/files/psb/{quote(attachment)}", file_path)
                    except HTTPError:
                        pass
                if exists(file_path):
                    EventPropagationImage.objects.get_or_create(
                        propagation=event_propagation,
                        image=join('event_propagation_images', attachment),
                        defaults=dict(order=0)
                    )

    def import_participants(self, data):
        for i, item in enumerate(data['ucastnik']):
            self.print_progress('participants', i, len(data['ucastnik']))
            event = self.event_map[item['akce']]
            person = self.user_map.get(item['adresa'])
            if not person: continue
            if item['org'] == '1' or item['org2'] == '1':
                event.other_organizers.add(person)
            else:
                event.record.participants.add(person)

    def handle(self, *args, **options):
        images_dir = join(BASE_DIR, 'media', 'event_propagation_images')
        if not exists(images_dir):
            mkdir(images_dir)

        data = self.load_data()

        for id in data['zc']:
            assert id in data['klub']

        for id in data['tabor']:
            assert id in data['akce']

        # to_print = [item for item in data['akce'].values()]
        #
        # print(json.dumps(to_print, indent=2, ensure_ascii=False))

        self.import_users(data)
        self.import_qualifications(data)
        self.import_administration_units(data)
        self.import_locations(data)
        self.import_memberships(data)
        self.import_events(data)
        self.import_participants(data)

        director = self.user_map[self.director_id]

        b = BrontosaurusMovement.objects.get_or_create(defaults=dict(director=director))[0]
        b.bis_administrators.set([self.user_map[id] for id in self.admin_ids])