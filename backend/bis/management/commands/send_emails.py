from django.core.management.base import BaseCommand
from vokativ import vokativ

from bis.models import User
from ecomail import ecomail

table_contacts = """\
suska@seznam.cz
rostislav.konupka@centrum.cz
karel.jilek@seznam.cz
hanka.ondrakova@seznam.cz
drazil.jiri@seznam.cz
vera.konupkova@centrum.cz
dalimil.toman@seznam.cz
hjilkova1@seznam.cz
bedlicka@centrum.cz
terca.op@seznam.cz
martinkadala@gmail.com
tom.hradil@jeseniky-brontosaurus.cz
josefina.skopova@gmail.com
nelsondufek@gmail.com
kristina.studena@gmail.com
michalsmid@gmail.com
aja@email.cz
rizek.vodak@seznam.cz
2012markle@gmail.com
radim.cenek@gmail.com
fr.novotny@email.cz
honza@krivonozka.cz
radim.pechal@gmail.com
michalo.lb@seznam.cz
tomas.stec@gmail.com
katerina.ruzickova@centrum.cz
jsvec.bota@seznam.cz
hlucil.m@seznam.cz
kdesivlesi@seznam.cz
pina@email.cz
diego.plzen@seznam.cz
vmartinkos@gmail.com
oli.korinkova@centrum.cz
veronika.frelichova@gmail.com
pike1@centrum.cz
vladimira@brontosaurus.cz
brontosaurus.uroboros@gmail.com
astragoth@seznam.cz
lamedko@seznam.cz

h.svatosova@seznam.cz
montytedatady@seznam.cz
benakr@seznam.cz
jezi@centrum.cz
nrogara@seznam.cz
j.jedounek.lyrika@seznam.cz
sarka.ondrackova@centrum.cz
tovrabec@email.cz
helesicova.leona@gmail.com
barbora.veclova@seznam.cz
vavrinova.aa@gmail.com
zdenek_f@email.cz
vasek.havlicek2@seznam.cz
ostadalradim@seznam.cz
roman.haken@cpkp.cz
ctibor.brancik@gmail.com
pavelpracny@gmail.com
cerny.honza@centrum.cz
vilhelm.petr@seznam.cz
zuzka.skvorova@centrum.cz
pavel@cernyp.cz
ja.filip@seznam.cz
radek.vondra@gmail.com
drevokocka@seznam.cz
s.daienn@gmail.com
kaludr@seznam.cz
zblebt@slunovrat.info
pavlakriz@seznam.cz
rcieslarova@gmail.com
cusblus@seznam.cz
jiri.bobrik@seznam.cz
ivana.cenkova@gmail.com
novotnaa.markeetka@gmail.com
vlasticka.f@gmail.com
f.benatzky@seznam.cz
petr.kurz@seznam.cz
maleda10@seznam.cz
ada.zavadova@gmail.com
jzemlik@email.cz
roza188@seznam.cz
ardea.breclav@brontosaurus.cz
jenda.kubata@gmail.com
gabka.rekova@gmail.com
lubosjanku@seznam.cz


iv-b@email.cz
flasar.tomas@email.cz
janca@slunovrat.info
ingrid.cejkova@gmail.com
dedkova.bara@gmail.com
h.pupikova@gmail.com
amormi.wyvern@gmail.com
nadenikovalucie@gmail.com
anicka.kulikova@gmail.com
jiri.gazarek@esb-rozvadece.cz
kacafilk@gmail.com
hornova.monika@seznam.cz
akcilkuk@seznam.cz
kostirv@seznam.cz
jermar.jakub@gmail.com
farkacdan@seznam.cz
lenkaolbertova@seznam.cz
vmkamel@seznam.cz
ksanda2001@seznam.cz
miramikovec@seznam.cz
jonas.prochazka@seznam.cz
rjakubstepanek@email.cz
mar.bejdova@gmail.com
malunka@email.cz
v12h2@seznam.cz
jkrivonozka@gmail.com
simi.fab@seznam.cz
janapavkova@seznam.cz
safarikova.h@gmail.com
robin.remes@seznam.cz
nomon@seznam.cz
martinzrcek@gmail.com
marketa.bulvova@gmail.com
leones.petr@seznam.cz
marketapodhraska@seznam.cz
cokynek@post.cz
hnuti@brontosaurus.cz
pavel.cejnar@centrum.cz
vomotom@gmail.com
capkova.karoli@gmail.com
vzdelavani@brontosaurus.cz
kesulik@seznam.cz
zuzulka123@seznam.cz
totocanka@seznam.cz
girafka.sro@seznam.cz
misa.mikovcova@email.cz
pavla.srbova@gmail.com
dashb@mushca.com
m@centrum.cz
caterina.drazilova@seznam.cz
grohmann.dominik@gmail.com
rjanik@freepoint.cz
michal.svarny@brontosaurus.cz
kuba@slunovrat.info
mariehradilova@post.cz
sigmar@slunovrat.info


biolik@seznam.cz
helca.23@seznam.cz
bockova.zdenka@gmail.com
lenka.rajmonova@seznam.cz
amfiser@seznam.cz
holumar@gmail.com
papa17@seznam.cz
mojzis.pavel@centrum.cz
lukas.linha@gmail.com
velpole@volny.cz
adela.cechovicova@gmail.com
pavelholubec@centrum.cz
director@brontosaurivhimalajich.cz
doskova.tereza@gmail.com
miropanek@seznam.cz
alenabulvova2@gmail.com
karolina.kozlovska@seznam.cz
hana.rosova@gmail.com
zelenydum@brontosaurus.cz
jana.kabatova@teatime.cz
martin.dyma@brontosaurus.cz
jupicert@seznam.cz
jan.cap.zak@gmail.com
chroaza@gmail.com
zdenek.ott@seznam.cz
yenour@seznam.cz
blanka.dobesova@centrum.cz
lida.valaskova@seznam.cz
siprj@seznam.cz
daniela.syrovatkova@seznam.cz
xhouskar@centrum.cz
frantalskoda@seznam.cz
ivauhrova@seznam.cz
pikuloval@centrum.cz
aleschramosta@seznam.cz
krenkovaanna@seznam.cz
sladkovsky.jakub@gmail.com
katekf@seznam.cz
burianova.lucie@seznam.cz
marek1.jr@gmail.com
evikskarabeus@seznam.cz
martaspavelkova@gmail.com
vanek.mojmir@seznam.cz
loskot.jan@post.cz
xpiratx@centrum.cz
klara.vrtelova@seznam.cz
poldam@seznam.cz
radka@slunovrat.info
petr@slunovrat.info
nela.jancalkova@seznam.cz
slanyj@centrum.cz
sindle.mi@seznam.cz
ondra@skvor.cz
pavel.simecek@gmail.com
adriana.valkovska@gmail.com
petravav@email.cz
honzik.stransky@gmail.com
sapient@centrum.cz
korcakova.m@centrum.cz
gal.pavlik@seznam.cz
mkoudy@centrum.cz
janula.bohmova@gmail.com
ifka.balackova@gmail.com
barunka79@seznam.cz
evakrasenska@centrum.cz
pilnikcgp@seznam.cz
halali@centrum.cz
klarka.vankova@seznam.cz
jsvobodo@antonio.cz
tereza.louckova8@gmail.com
houskova.lenka@gmail.com
s.poucova@gmail.com
marlosk@post.cz
gajanku@volny.cz
david@karban.eu
premysl.bejda@gmail.com
zidonp@atlas.cz
paik@email.cz
vranis4@seznam.cz
tjen.welion@seznam.cz
zorouska@seznam.cz
miroslava.sutnarova@seznam.cz
gavento@gmail.com
jaroslav.spac@seznam.cz
backova.karin@gmail.com
honza.hok@gmail.com
stranska.kata@gmail.com
brenmi@seznam.cz
kocurv@seznam.cz
sonik.mh@seznam.cz
mirobest@post.cz
saurinka166@seznam.cz
michal.krejci.olomouc@centrum.cz
olgavacula@centrum.cz
sedlacekt@gmail.com
t.fantasy@seznam.cz
wawi68@seznam.cz
monacasper@seznam.cz
cmelda@halahoj.org
l.balacek@seznam.cz
ondrejxcerny@seznam.cz
lennerova@seznam.cz
jiri.knapil@email.cz
marys.parak@seznam.cz
mkrivonozkova@seznam.cz
m.chlebounova@gmail.com
luc8kos@gmail.com
ondra.svobi@seznam.cz
zdenka.pavkova@gmail.com
marie.hulkova99@gmail.com
pavel.rimak@seznam.cz
vasek.kaplan@gmail.com
joe.rypar@email.cz
romanaslizova@email.cz
kjezkova@volny.cz
stolinka@email.cz
ajdam.d@seznam.cz
novakovavera9@gmail.com
betka@kurowsti.cz
kroca@centrum.cz


dianka.dom@gmail.com
lukesipek@seznam.cz
f.tamara@seznam.cz
vacpodlesak@gmail.com
jiri.cerny89@seznam.cz
vh.piff@atlas.cz
aldavanek@seznam.cz
lada.kopia@centrum.cz
peterbuchta@seznam.cz
j.dvorakova98@seznam.cz

tolman@seznam.cz
av2436337@gmail.com
zemlikovat@gmail.com
kekuna@seznam.cz
livnanska.pavlina@gmail.com
zouhar.jiri@gmail.com
pavelkok@seznam.cz
novotny.pavlik@seznam.cz
kisac.l@seznam.cz
lindazajickova@seznam.cz
jeny.n@email.cz
petr_vesely@atlas.cz
pa.kral@gmail.com
dancale@seznam.cz
dusan.renat@gmail.com
hajkovakristy@seznam.cz
elsa.sebkova@centrum.cz
tomaskorab25@seznam.cz
hanulatko.brontatko@centrum.cz
tibor.vansa@seznam.cz
pavli.kuch@seznam.cz
petrkus@email.cz
ppevny@seznam.cz

vodnik92@gmail.com
aajina@centrum.cz
polasek.martin@seznam.cz
sandovahanka@gmail.com
lamanchy@gmail.com
petapravdova@seznam.cz
evamagulova@gmail.com
mon.grossova@seznam.cz
klara.cihakova@seznam.cz

taluk@email.cz
paninka@centrum.cz
tomas.dado@gmail.com
bradshawpetr@gmail.com
jaroslav.dytrych@centrum.cz
holy164@seznam.cz
aja@slunovrat.info
lucik.sebek@gmail.com
sarka.brazdova@email.cz
malchikovaev13@gmail.com
milada.dobiasova@ekologickavychova.cz
jcdevil@post.cz
luca.hlavackova@seznam.cz
stefkova.eva@seznam.cz
frantiska.sylva1@gmail.com
vit.dohnal@seznam.cz
alice.filkova@seznam.cz

la.special@post.cz
milos.marek@no-dimensions.cz
lenka.belcherova@seznam.cz
kriz@pf.jcu.cz
silarova.j@seznam.cz
hanajanku@centrum.cz
mbilik@seznam.cz
kuriatko@slunovrat.info
st.dadak@seznam.cz
petra.simakova@gmail.com
m.slamena@seznam.cz
dvorakova.barunka@gmail.com
cejvik@seznam.cz
zikmund11@seznam.cz
k.synek@seznam.cz
slanymarek@seznam.cz
jpavlita@seznam.cz
michal.domansky@seznam.cz
lukas.cerovsky@seznam.cz
vierik@slunovrat.info
brozova.b@gmail.com
pavel44211130@hotmail.com
jozef.klopacka@centrum.sk
mipetru@centrum.cz
midonat@gmail.com
elle.b@seznam.cz
neottia@seznam.cz
petraopltova@seznam.cz
eliska.plotena@seznam.cz
antz@centrum.cz
nikolahrebackova@seznam.cz
janahrdlicka@centrum.cz
elisabettruhlarova@gmail.com
market.petr@seznam.cz
honzaher@centrum.cz
w.marusjenka@seznam.cz

ivana.rumpelova@seznam.cz
rundova@seznam.cz
risa.necas@centrum.cz
jita.ola.sevcikova@gmail.com
jiri_c@email.cz
jakub.hajekj@gmail.com
jana.svacina@seznam.cz
josefina.hlavacova@seznam.cz
hana.cernikova@seznam.cz
blejk@centrum.cz
katka.vilhelmova@gmail.com
hanasekerkova@gmail.com
epavliko@gmail.com
vavrinovah@seznam.cz
fandazajic@gmail.com
damned.me@seznam.cz
marcelina.med@email.cz
ap79@volny.cz
mariana.jandourkova@gmail.com
braham@centrum.cz
pavel.kucharik@volny.cz
abcvanicek@seznam.cz
petr.drazil@email.cz
p.nani@seznam.cz
zaotom@centrum.cz

"""


class Command(BaseCommand):
    def handle(self, *args, **options):
        our_contacts = """\
Dan Farkač, Dane, farkacdan@seznam.cz
Káťa Růžičková, Káťo, katerina.ruzickova@centrum.cz
Terka Opravilová, Terko, terca.op@seznam.cz
Hanka Šafaříková, Hanko, safarikova.h@gmail.com
Johny Kuchař, Johny, john.yy@seznam.cz
Halka Vašinková, Halko, v12h2@seznam.cz
Péťa Novotny, Péťo a Alčo, leones.petr@seznam.cz
Kryštof Synek, Kryštofe, k.synek@seznam.cz
Cody, Cody, dalimil.toman@seznam.cz
Rózi Jandová, Rózi, roza188@seznam.cz
Petr Kus, Peťo, petrkus@email.cz
Mojmír Vaněk, Mojmíre, vanek.mojmir@seznam.cz
Dušan Vrána, Dušane, vranis4@seznam.cz
Monika Grossova, Mončo, mon.grossova@seznam.cz
Roman Szomolai, Romane, szomolai.roman@gmail.com
Jakub Jedounek, Jakube, j.jedounek.lyrika@seznam.cz
Tereza Křivská, Terko, krivskatereza3@gmail.com
Michal Švarný, Šváro, michal.svarny@seznam.cz
Tomáš Vrabec, Basty, tovrabec@email.cz
Martin Polášek, Martine, polasek.martin@seznam.cz 
Jan Strapek, Johny, honstrap@gmail.com
Marťa Pavelková, Marťo, martaspavelkova@gmail.com
Ajdam, Ajdame, ajdam.d@seznam.cz
Martin Rexa, Martine, martinrexa@seznam.cz
Jakub Vojtíšek, Jakube, davias@email.cz
Marta Šiborová, Marto, msiborova@seznam.cz
Ester Koňařová, Ester, konarovae@gmail.com
Michal Malý, Michale, maly.michal@outlook.com
Adéla Svobodová, Adélo, adelajonakova01@seznam.cz
David Svoboda, Davide, svoboda989@gmail.com
Radka Sedláková, Ráďo, rada.sedlakova@gmail.com
Martin Hájek, Jariku, xjarik@seznam.cz
Pavel Nani, Pavle, p.nani@seznam.cz
Marek Slaný, Marku, slanymarek@seznam.cz	
Sorondil, Sorondile, slanyj@centrum.cz
Michal Šmíd, Majky, michalsmid@gmail.com
Martina Bejdová , Marťo, mar.bejdova@gmail.com
Michal Polanský, Poldo, poldam@seznam.cz
Anna Kučerová, Rusalko, anicka.kulikova@gmail.com
Daniela Syrovátková, Dani, daniela.syrovatkova@seznam.cz
Martin Rehuš, Mates, martin.rehus8@gmail.com 
Jupíčert, Jupí, jupicert@seznam.cz	
Finn, Finne, pavel.simecek@gmail.com"""

        to_whom = {}
        contacts = our_contacts.splitlines()
        for contact in contacts:
            full_name, nick, email = contact.split(",")
            to_whom[email.strip()] = nick.strip()

        for email in table_contacts.splitlines():
            if email:
                to_whom[email] = vokativ(User.objects.get(email=email).first_name.split(' ')[0]).capitalize()

        exclude = [
            "michal.svarny@brontosaurus.cz", "brontosaurus.uroboros@gmail.com", "vzdelavani@brontosaurus.cz"
        ]

        for email in exclude:
            del to_whom[email]

        for email, vok in to_whom.items():
            print(User.objects.get(email=email))
            print(email)
            print(vok)
            print()

        for user in sorted([User.objects.get(email=email) for email in to_whom.keys()], key=lambda u: u.last_name):
            print(user.last_name, user.first_name, "\t", user.email)

        to_whom2 = {
            'petrkus@email.cz': "Peťo"
        }
        for email, vok in to_whom2.items():
            ecomail.send_email(
                'bis@brontosaurus.cz', 'BIS',
                "Brontosauří fond her",
                '175',
                [email],
                variables={'VOK': vok}
            )
