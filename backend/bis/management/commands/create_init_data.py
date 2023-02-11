from django.core.management.base import BaseCommand

from bis.models import Location
from categories.models import DietCategory, EventIntendedForCategory, QualificationCategory, \
    AdministrationUnitCategory, MembershipCategory, EventProgramCategory, \
    EventCategory, GrantCategory, DonationSourceCategory, OrganizerRoleCategory, TeamRoleCategory, OpportunityCategory, \
    LocationProgramCategory, LocationAccessibilityCategory, RoleCategory, HealthInsuranceCompany, SexCategory, \
    EventGroupCategory
from game_book_categories.models import Tag, PhysicalCategory, MentalCategory, LocationCategory, \
    ParticipantNumberCategory, ParticipantAgeCategory, GameLengthCategory, PreparationLengthCategory, \
    OrganizersNumberCategory, MaterialRequirementCategory
from translation.translate import _


class Command(BaseCommand):
    help = "Creates categories etc."

    def create_event_categories(self, data, prefix='', name_prefix=''):
        if len(prefix):
            prefix += '__'
        if len(name_prefix):
            name_prefix += ' - '

        for key, value in data.items():
            slug = prefix + key
            name = name_prefix + _(f'event_categories.{slug}')
            if value is None:
                EventCategory.objects.update_or_create(
                    slug=slug,
                    defaults=dict(name=name)
                )
            else:
                self.create_event_categories(value, slug, name)

    def handle(self, *args, **options):
        DietCategory.objects.update_or_create(slug='meat', defaults=dict(name='s masem'))
        DietCategory.objects.update_or_create(slug='vege', defaults=dict(name='vegetariánská'))
        DietCategory.objects.update_or_create(slug='vegan', defaults=dict(name='veganská'))

        EventIntendedForCategory.objects.update_or_create(slug='for_all', defaults=dict(name='pro všechny'))
        EventIntendedForCategory.objects.update_or_create(slug='for_young_and_adult',
                                                          defaults=dict(name='pro mládež a dospělé'))
        EventIntendedForCategory.objects.update_or_create(slug='for_kids', defaults=dict(name='pro děti'))
        EventIntendedForCategory.objects.update_or_create(slug='for_parents_with_kids',
                                                          defaults=dict(name='pro rodiče s dětmi'))
        EventIntendedForCategory.objects.update_or_create(slug='for_first_time_participant',
                                                          defaults=dict(name='pro prvoúčastníky'))

        QualificationCategory.objects.update_or_create(slug='consultant', defaults=dict(name='Konzultant'))
        QualificationCategory.objects.update_or_create(slug='instructor', defaults=dict(name='Instruktor'))
        QualificationCategory.objects.update_or_create(slug='organizer', defaults=dict(name='Organizátor (OHB)'))
        QualificationCategory.objects.update_or_create(slug='weekend_organizer',
                                                       defaults=dict(name='Organizátor víkendovek (OvHB)'))
        QualificationCategory.objects.update_or_create(slug='consultant_for_kids',
                                                       defaults=dict(name='Konzultant Brďo'))
        QualificationCategory.objects.update_or_create(slug='kids_leader', defaults=dict(name='Vedoucí Brďo'))
        QualificationCategory.objects.update_or_create(slug='kids_intern', defaults=dict(name='Praktikant Brďo'))
        QualificationCategory.objects.update_or_create(slug='main_leader_of_kids_camps',
                                                       defaults=dict(name='Hlavní vedoucí dětských táborů (HVDT)'))
        QualificationCategory.objects.update_or_create(slug='organizer_without_education',
                                                       defaults=dict(name='Organizátor nevzdělaný'))

        qualification_parents = {
            'instructor': ['consultant'],
            'organizer': ['instructor'],
            'weekend_organizer': ['organizer'],
            'kids_leader': ['consultant_for_kids'],
            'kids_intern': ['kids_leader'],
            'organizer_without_education': ['weekend_organizer', 'kids_intern'],
        }
        for slug, parent_slugs in qualification_parents.items():
            QualificationCategory.objects.get(slug=slug).parents.set(
                [QualificationCategory.objects.get(slug=parent_slug) for parent_slug in parent_slugs]
            )

        qualification_can_approve = {
            'instructor': ['main_leader_of_kids_camps', 'weekend_organizer'],
            'consultant': ['organizer'],
            'consultant_for_kids': ['main_leader_of_kids_camps', 'kids_leader', 'kids_intern'],
        }
        for slug, can_approve_slugs in qualification_can_approve.items():
            QualificationCategory.objects.get(slug=slug).can_approve.set(
                [QualificationCategory.objects.get(slug=can_approve_slug) for can_approve_slug in can_approve_slugs]
            )

        AdministrationUnitCategory.objects.update_or_create(slug="basic_section", defaults=dict(name='Základní článek'))
        AdministrationUnitCategory.objects.update_or_create(slug="headquarter", defaults=dict(name='Ústředí'))
        AdministrationUnitCategory.objects.update_or_create(slug="regional_center",
                                                            defaults=dict(name='Regionální centrum'))
        AdministrationUnitCategory.objects.update_or_create(slug="club", defaults=dict(name='Klub'))

        MembershipCategory.objects.update_or_create(slug='family', defaults=dict(name='rodinné'))
        MembershipCategory.objects.update_or_create(slug='family_member', defaults=dict(name='rodinný příslušník'))
        MembershipCategory.objects.update_or_create(slug='kid', defaults=dict(name='dětské do 15 let'))
        MembershipCategory.objects.update_or_create(slug='student', defaults=dict(name='individuální 15-26 let'))
        MembershipCategory.objects.update_or_create(slug='adult', defaults=dict(name='individuální nad 26 let'))
        MembershipCategory.objects.update_or_create(slug='member_elsewhere', defaults=dict(name='platil v jiném ZČ'))

        EventGroupCategory.objects.update_or_create(slug='camp', defaults=dict(name='Tábor'))
        EventGroupCategory.objects.update_or_create(slug='weekend_event', defaults=dict(name='Víkendovka'))
        EventGroupCategory.objects.update_or_create(slug='other', defaults=dict(name='Ostatní'))

        EventProgramCategory.objects.update_or_create(slug='monuments', defaults=dict(name='Akce památky'))
        EventProgramCategory.objects.update_or_create(slug='nature', defaults=dict(name='Akce příroda'))
        EventProgramCategory.objects.update_or_create(slug='kids', defaults=dict(name='BRĎO'))
        EventProgramCategory.objects.update_or_create(slug='eco_tent', defaults=dict(name='Ekostan'))
        EventProgramCategory.objects.update_or_create(slug='holidays_with_brontosaurus', defaults=dict(
            name='PsB (Prázdniny s Brontosaurem = vícedenní letní akce)'))
        EventProgramCategory.objects.update_or_create(slug='education', defaults=dict(name='Vzdělávání'))
        EventProgramCategory.objects.update_or_create(slug='international', defaults=dict(name='Mezinárodní'))
        EventProgramCategory.objects.update_or_create(slug='none', defaults=dict(name='Žádný'))

        event_categories = {
            'internal': {
                'general_meeting': None,
                'volunteer_meeting': None,
                'section_meeting': None,
            },
            'public': {
                'volunteering': None,
                'only_experiential': None,
                'educational': {
                    'lecture': None,
                    'course': None,
                    'ohb': None,
                    'educational': None,
                    'educational_with_stay': None,
                },
                'club': {
                    'lecture': None,
                    'meeting': None,
                },
                'other': {
                    'for_public': None,
                    'exhibition': None,
                    'eco_tent': None,
                }
            }
        }

        self.create_event_categories(event_categories)

        GrantCategory.objects.update_or_create(slug='msmt', defaults=dict(name='mšmt'))
        GrantCategory.objects.update_or_create(slug='other', defaults=dict(name='z jiných projektů'))

        DonationSourceCategory.objects.update_or_create(slug='bank_transfer', defaults=dict(name='bankovním převodem'))

        OrganizerRoleCategory.objects.update_or_create(slug='program', defaults=dict(name='Tvorba a vedení her'))
        OrganizerRoleCategory.objects.update_or_create(slug='material',
                                                       defaults=dict(name='Materiálně-technické zajištění'))
        OrganizerRoleCategory.objects.update_or_create(slug='cook', defaults=dict(name='Kuchař/ka'))
        OrganizerRoleCategory.objects.update_or_create(slug='photo', defaults=dict(name='Fotograf/ka'))
        OrganizerRoleCategory.objects.update_or_create(slug='propagation', defaults=dict(name='Propagace akcí'))
        OrganizerRoleCategory.objects.update_or_create(slug='communication',
                                                       defaults=dict(name='Komunikace s účastníky/lektory/lokalitou'))
        OrganizerRoleCategory.objects.update_or_create(slug='manager', defaults=dict(name='Hospodář/ka'))
        OrganizerRoleCategory.objects.update_or_create(slug='medic', defaults=dict(name='Zdravotník/ce'))
        OrganizerRoleCategory.objects.update_or_create(slug='singer', defaults=dict(name='Hudebník/ce'))
        OrganizerRoleCategory.objects.update_or_create(slug='generic', defaults=dict(name='Všeuměl / podržtaška'))

        TeamRoleCategory.objects.update_or_create(slug='lector', defaults=dict(name='Lektor'))
        TeamRoleCategory.objects.update_or_create(slug='lecturer', defaults=dict(name='Přednášející'))
        TeamRoleCategory.objects.update_or_create(slug='graphic', defaults=dict(name='Grafik'))
        TeamRoleCategory.objects.update_or_create(slug='translator', defaults=dict(name='Překladatel'))
        TeamRoleCategory.objects.update_or_create(slug='copywriter', defaults=dict(name='Copywriter'))
        TeamRoleCategory.objects.update_or_create(slug='marketing', defaults=dict(name='Markeťák'))
        TeamRoleCategory.objects.update_or_create(slug='web', defaults=dict(name='Webař'))
        TeamRoleCategory.objects.update_or_create(slug='manager', defaults=dict(name='Hospodář'))

        OpportunityCategory.objects.update_or_create(slug='organizing', defaults=dict(
            name='Organizování akcí',
            description='Příležitosti organizovat či pomáhat s pořádáním našich akcí.'))
        OpportunityCategory.objects.update_or_create(slug='collaboration', defaults=dict(
            name='Spolupráce',
            description='Příležitosti ke spolupráci na chodu a rozvoji Hnutí Brontosaurus.'))
        OpportunityCategory.objects.update_or_create(slug='location_help', defaults=dict(
            name='Pomoc lokalitě',
            description='Příležitosti k pomoci dané lokalitě, která to aktuálně potřebuje.'))

        LocationProgramCategory.objects.update_or_create(slug='nature', defaults=dict(name='AP - Akce příroda'))
        LocationProgramCategory.objects.update_or_create(slug='monuments', defaults=dict(name='APAM - Akce památky'))

        LocationAccessibilityCategory.objects.update_or_create(slug='good', defaults=dict(name='Snadná (0-1,5h)'))
        LocationAccessibilityCategory.objects.update_or_create(slug='ok',
                                                               defaults=dict(name='Středně obtížná (1,5-3h)'))
        LocationAccessibilityCategory.objects.update_or_create(slug='bad', defaults=dict(name='Obtížná (více než 3h)'))

        RoleCategory.objects.update_or_create(slug='director', defaults=dict(name='Ředitel'))
        RoleCategory.objects.update_or_create(slug='admin', defaults=dict(name='Admin'))
        RoleCategory.objects.update_or_create(slug='office_worker', defaults=dict(name='Kancl'))
        RoleCategory.objects.update_or_create(slug='auditor', defaults=dict(name='KRK'))
        RoleCategory.objects.update_or_create(slug='executive', defaults=dict(name='VV'))
        RoleCategory.objects.update_or_create(slug='education_member', defaults=dict(name='EDU'))
        RoleCategory.objects.update_or_create(slug='chairman', defaults=dict(name='Předseda'))
        RoleCategory.objects.update_or_create(slug='vice_chairman', defaults=dict(name='Místopředseda'))
        RoleCategory.objects.update_or_create(slug='manager', defaults=dict(name='Hospodář'))
        RoleCategory.objects.update_or_create(slug='board_member', defaults=dict(name='Člen představenstva'))
        RoleCategory.objects.update_or_create(slug='main_organizer', defaults=dict(name='Hlavní organizátor'))
        RoleCategory.objects.update_or_create(slug='organizer', defaults=dict(name='Organizátor'))
        RoleCategory.objects.update_or_create(slug='qualified_organizer',
                                              defaults=dict(name='Organizátor s kvalifikací'))
        RoleCategory.objects.update_or_create(slug='any', defaults=dict(name='Kdokoli'))

        HealthInsuranceCompany.objects.update_or_create(slug='VZP', defaults=dict(
            name='Všeobecná zdravotní pojišťovna České republiky'))
        HealthInsuranceCompany.objects.update_or_create(slug='VOZP', defaults=dict(
            name='Vojenská zdravotní pojišťovna České republiky'))
        HealthInsuranceCompany.objects.update_or_create(slug='CPZP', defaults=dict(
            name='Česká průmyslová zdravotní pojišťovna'))
        HealthInsuranceCompany.objects.update_or_create(slug='OZP', defaults=dict(
            name='Oborová zdravotní pojišťovna zaměstnanců bank, pojišťoven a stavebnictví'))
        HealthInsuranceCompany.objects.update_or_create(slug='ZPS', defaults=dict(
            name='Zaměstnanecká pojišťovna Škoda'))
        HealthInsuranceCompany.objects.update_or_create(slug='ZPMV', defaults=dict(
            name='Zdravotní pojišťovna ministerstva vnitra České republiky'))
        HealthInsuranceCompany.objects.update_or_create(slug='RBP', defaults=dict(
            name='RBP, zdravotní pojišťovna'))

        SexCategory.objects.update_or_create(slug='woman', defaults=dict(name='Žena'))
        SexCategory.objects.update_or_create(slug='man', defaults=dict(name='Muž'))
        SexCategory.objects.update_or_create(slug='other', defaults=dict(name='Jiné'))

        Location.objects.update_or_create(name='Online', defaults=dict(
            for_beginners=True,
            accessibility_from_prague=LocationAccessibilityCategory.objects.get(slug='good'),
            accessibility_from_brno=LocationAccessibilityCategory.objects.get(slug='good'),
        ))


        tags = ['icebreaker', 'seznamka', 'dynamix', 'důvěrovka', 'simulační', 'strategie', 'drobnička', 'eko',
                'diskuzní', 'orvo', 'larp', 'team building', 'kreativní', 'psycho', 'reflexe', 'noční']
        for tag in tags:
            Tag.objects.get_or_create(name=tag)

        PhysicalCategory.objects.update_or_create(slug="minimal", defaults=dict(
            name="Na místě", description="Programy sedící či s minimem pohybu mezi účasníky"))
        PhysicalCategory.objects.update_or_create(slug="moving", defaults=dict(
            name="Chodící", description="Během programu něco nachodím, zahřeji se, ale nezpotím"))
        PhysicalCategory.objects.update_or_create(slug="running", defaults=dict(
            name="Běhací", description="Unavím se, ale nezničím se"))
        PhysicalCategory.objects.update_or_create(slug="hardcore", defaults=dict(
            name="Náročná", description="Po skončení někam odpadnu"))

        MentalCategory.objects.update_or_create(slug="minimal", defaults=dict(
            name="Nenáročná", description="Odpočinkové programy, u kterých můžu vypnout hlavu"))
        MentalCategory.objects.update_or_create(slug="thinking", defaults=dict(
            name="Mozek potřeba", description="Trochu kreativity to chce, ale nic náročného"))
        MentalCategory.objects.update_or_create(slug="logically_demanding", defaults=dict(
            name="Analyticky náročná", description="Plánování strategie, řešení šifer, komunikace v časovém presu"))
        MentalCategory.objects.update_or_create(slug="emotionally_demanding", defaults=dict(
            name="Emočně náročná", description="Přemýšlecí otázky, řešení hodnot, pocitů, sdílení"))
        MentalCategory.objects.update_or_create(slug="hardcore", defaults=dict(
            name="Psycho", description="Kombinace náročných prvků, narušování komforní zóny, nutnost aktivně řešit psychickou bezpečnost"))

        LocationCategory.objects.update_or_create(slug="tearoom", defaults=dict(
            name="Čajovna", description="Klidné a komfortní místo s hezkou atmosférou, omezené množství pohybu"))
        LocationCategory.objects.update_or_create(slug="hall", defaults=dict(
            name="Větší místnost", description="Sál či místnost dostatkem prostoru, relativní teplo"))
        LocationCategory.objects.update_or_create(slug="in_a_circle", defaults=dict(
            name="V kruhu (kolem ohně)", description="Všichi na sebe vidí, tepelný komfort, omezený pohyb"))
        LocationCategory.objects.update_or_create(slug="field", defaults=dict(
            name="Louka", description="Louka či park, dost prostoru na sezení či běhání"))
        LocationCategory.objects.update_or_create(slug="forest", defaults=dict(
            name="Les", description="Kousek lesa se stromy"))
        LocationCategory.objects.update_or_create(slug="village", defaults=dict(
            name="Vesnice", description="Či město, výskyt lidí v okolí"))
        LocationCategory.objects.update_or_create(slug="water", defaults=dict(
            name="Voda", description="Nutno větší množství vody, na koupání či čvachtání"))
        LocationCategory.objects.update_or_create(slug="at_road", defaults=dict(
            name="K cestě", description="Možno hrát během putování či přesunu"))
        LocationCategory.objects.update_or_create(slug="specific", defaults=dict(
            name="Specifické umístění", description="K programu třeba specifické místo (ať konkrétní či zřídké)"))

        ParticipantNumberCategory.objects.update_or_create(slug="individual", defaults=dict(
            name="Pro jednotlivce", description="Každý hraje sám, lib. množství účastníků"))
        ParticipantNumberCategory.objects.update_or_create(slug="small", defaults=dict(
            name="Malá skupinka (4-6)", description="Skupinka 4-6 lidí"))
        ParticipantNumberCategory.objects.update_or_create(slug="few", defaults=dict(
            name="Skupina lidí (10+)", description="Zepár lidí, přes 10"))
        ParticipantNumberCategory.objects.update_or_create(slug="big", defaults=dict(
            name="Větší skupina (20+)", description="Kolem 20 lidí"))
        ParticipantNumberCategory.objects.update_or_create(slug="a_log", defaults=dict(
            name="Hromada lidí", description="Pro velká skupiny lidí"))

        ParticipantAgeCategory.objects.update_or_create(slug="parents_with_kids", defaults=dict(
            name="Rodiče s dětmi", description=""))
        ParticipantAgeCategory.objects.update_or_create(slug="preschool", defaults=dict(
            name="Předškoláci", description=""))
        ParticipantAgeCategory.objects.update_or_create(slug="elementary", defaults=dict(
            name="Školáci", description=""))
        ParticipantAgeCategory.objects.update_or_create(slug="teen", defaults=dict(
            name="Středoškoláci", description=""))
        ParticipantAgeCategory.objects.update_or_create(slug="university", defaults=dict(
            name="Vysokoškoláci", description=""))
        ParticipantAgeCategory.objects.update_or_create(slug="adult", defaults=dict(
            name="Dospělí", description=""))
        ParticipantAgeCategory.objects.update_or_create(slug="old", defaults=dict(
            name="Vyspělí", description=""))


        GameLengthCategory.objects.update_or_create(slug="short", defaults=dict(
            name="Rychlé (do 10 minut)", description="Krátké programy, jednuché seznamky, rozcvičky, pro vyplnění prostoje"))
        GameLengthCategory.objects.update_or_create(slug="an_hour", defaults=dict(
            name="Střední (do hodiny)", description="Nějakou chvíli účastníky zabaví, dvě tři takové naplní odpoledne"))
        GameLengthCategory.objects.update_or_create(slug="long", defaults=dict(
            name="Dlouhé (pár hodin)", description="Odpolední program, noční hra"))
        GameLengthCategory.objects.update_or_create(slug="multiple_days", defaults=dict(
            name="Vícedenní, celotáborové", description="Programy rozprostřené přes několik dní, většinou na pozadí jiných programů"))

        PreparationLengthCategory.objects.update_or_create(slug="enough_to_read", defaults=dict(
            name="Stačí přečíst", description="Zkušený org přečte, a program rovnou uvede"))
        PreparationLengthCategory.objects.update_or_create(slug="need_to_study", defaults=dict(
            name="Třeba chvíle klidu", description="Netriviální, potřeba pořádně přečíst a pochopit"))
        PreparationLengthCategory.objects.update_or_create(slug="training", defaults=dict(
            name="Potřeba se připravit", description="Příprava zabere pár hodin, chystání materiálů, předání dalším orgům"))
        PreparationLengthCategory.objects.update_or_create(slug="multiple_sessions", defaults=dict(
            name="Velmi náročné", description="Rozsáhle rozpracovaný či naopak nedokončený program, nutno věnovat značné úsilí k uvedení"))

        OrganizersNumberCategory.objects.update_or_create(slug="one", defaults=dict(
            name="Zvládnu sám", description="Uvedení programu zvládne jeden org"))
        OrganizersNumberCategory.objects.update_or_create(slug="few", defaults=dict(
            name="Potřebuji pomocnou ruku", description="Na program je potřeba dva či tři orgové"))
        OrganizersNumberCategory.objects.update_or_create(slug="group", defaults=dict(
            name="Skupinka orgů", description="Potřeba kolem pěti orgů"))
        OrganizersNumberCategory.objects.update_or_create(slug="a_lot", defaults=dict(
            name="Spousta orgů", description="Velké hry vyžadující B-tým, atp."))

        MaterialRequirementCategory.objects.update_or_create(slug="none", defaults=dict(
            name="Nic není potřeba", description="Stačí účastníci"))
        MaterialRequirementCategory.objects.update_or_create(slug="simple", defaults=dict(
            name="Stačí základ", description="Šátky, tužka a papír, provázek"))
        MaterialRequirementCategory.objects.update_or_create(slug="get_some", defaults=dict(
            name="Potřeba nachystat", description="Tisk pár stránek, kostým, potřeba specifický materiál k programu"))
        MaterialRequirementCategory.objects.update_or_create(slug="complicated", defaults=dict(
            name="Kdo se s tím potáhne?", description="Velké množství či velmi specifický materiál"))
