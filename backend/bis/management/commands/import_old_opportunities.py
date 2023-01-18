from collections import OrderedDict

from dateutil.relativedelta import relativedelta
from dateutil.utils import today
from django.core.management.base import BaseCommand

from bis.models import User
from opportunities.models import Opportunity
from other.models import DashboardItem

data = [OrderedDict([('id', 10), ('name', 'Budkování v Mikulčickém luhu'), ('start', '2022-09-09'), ('end', '2023-03-15'), ('on_web_start', '2022-09-09'), ('on_web_end', '2023-02-15'), ('introduction', '<p>Brontosauři na Podluž&iacute; jsou po torn&aacute;du dosti zaměstn&aacute;ni pracemi na obnově zeleně, opravami klubovny apod. a uv&iacute;taj&iacute; pomoc s peč&iacute; o hn&iacute;zdn&iacute; budky pro ptactvo v lužn&iacute;ch les&iacute;ch na Podluž&iacute; a s jejich doplňov&aacute;n&iacute;m.</p>\r\n<p>&nbsp;</p>'), ('description', '<p>Uv&iacute;t&aacute;me tak v&iacute;kendov&eacute; i jednodenn&iacute; akce na či&scaron;těn&iacute;, opravy, evidenci stavaj&iacute;c&iacute;ch budek a na vyvě&scaron;ov&aacute;n&iacute; nov&yacute;ch. Budky v les&iacute;ch, jež jsou poznamen&aacute;ny hospod&aacute;řskou činnost&iacute;, kompenzuj&iacute; ptactvu nedostatek přirozen&yacute;ch hn&iacute;zdn&iacute;ch dutin.</p>\r\n<p>K akc&iacute;m nab&iacute;z&iacute;me, jak z&aacute;zem&iacute; kluboven v bl&iacute;zk&yacute;ch ob&iacute;ch či maringotky v lužn&iacute;m lese, tak n&aacute;řad&iacute; a ve&scaron;ker&eacute; podklady a pomůcky pro dobrovolnickou pomoc. Um&iacute;me nab&iacute;dnout i odborn&yacute; v&yacute;klad v př&iacute;nosu dan&eacute; dobrovolnick&eacute; č&iacute;nnosti či exkuze nebo předn&aacute;&scaron;ky k m&iacute;stn&iacute; př&iacute;rodě a jej&iacute; ochraně a jej&iacute;ch ohrožen&iacute;ch.</p>\r\n<p>Dle zad&aacute;n&iacute; v map&aacute;ch a GPS se po skupink&aacute;ch proch&aacute;z&iacute; lužn&iacute; les a kontroluj&iacute; se, eviduj&iacute; a př&iacute;padně opravuj&iacute; st&aacute;vaj&iacute;c&iacute; budky a jejich obsazenost. Ve vybran&yacute;ch &uacute;sec&iacute;ch se doplňuj&iacute; budky nov&eacute; pro různ&eacute; druhy ptactva.</p>'), ('location_benefits', '<p>Lužn&iacute; lesy na soutoku Moravy a Dyje jsou jednou z př&iacute;rodně nejbohat&scaron;&iacute;ch a nejceněj&scaron;&iacute;ch lokalit ve středn&iacute; Evropě. Druhovou pestrost po&scaron;kozuje v&scaron;ak dlouhodob&aacute; nevhodně veden&aacute; hospod&aacute;řsk&aacute; činnost v les&iacute;ch, odkud miz&iacute; star&eacute; porosty, odum&iacute;raj&iacute;c&iacute; stromy apod. Ve vznikaj&iacute;c&iacute;ch mlad&yacute;ch stejnověk&yacute;ch monokulturn&iacute;ch porostech chyb&iacute; např&iacute;klad star&eacute; doupn&eacute; stromy. Vyvě&scaron;ov&aacute;n&iacute;m budek kompenzujeme pr&aacute;vě nedostatek hn&iacute;zdn&iacute;ch dudit pro mnoh&eacute; druhy ptactva - s&yacute;kory, lejsky, brhl&iacute;ky, sovy aj.</p>'), ('personal_benefits', '<p><span style="font-weight: 400;">Zejm&eacute;na dobr&yacute; pocit, že zpěv ptactva v brněnsk&yacute;ch parc&iacute;ch zn&iacute; i d&iacute;ky tobě! Taky se dozv&iacute;&scaron; o tom, jak a proč se budky vyvě&scaron;uj&iacute;, jac&iacute; pt&aacute;ci v nich hn&iacute;zdn&iacute;, apod. Inspirovat tě budou obdobn&eacute; brontosauř&iacute; projekty po cel&eacute; ČR. Rozvine&scaron; si organizačn&iacute; dovednosti, přiuč&iacute;&scaron; se něco ochraně př&iacute;rody.<br /></span></p>'), ('requirements', '<p><span style="font-weight: 400;">Nic speci&aacute;ln&iacute;ho nen&iacute; třeba umět. Předpokl&aacute;d&aacute;me, že dovednostmi pr&aacute;ci na PC a stoup&aacute;n&iacute; po žebři vl&aacute;dne&scaron;. Hod&iacute; se umět pracovat s GPS navigac&iacute;, ale to když tak vysvětl&iacute;me :)</span></p>'), ('contact_name', 'Dalimil Toman'), ('contact_phone', '+420 605 763 112'), ('contact_email', 'podluzi@brontosaurus.cz'), ('image', '/media/opportunity_images/023_-_Budkovani-Uroboros_2017_kopie.jpg'), ('category_id', 3), ('location_id', 2176), ('contact_person_id', None)]), OrderedDict([('id', 11), ('name', 'Koordinátor/koordinátorka péče o budky v Brně'), ('start', '2022-09-09'), ('end', '2023-03-15'), ('on_web_start', '2022-09-09'), ('on_web_end', '2023-01-01'), ('introduction', '<p><span style="font-weight: 400;">Brontosauři v Brně dlouhodobě pečuj&iacute; o ptactvo a instalac&iacute; ptač&iacute;ch budek doplňuj&iacute; chyběj&iacute;c&iacute; možnosti hn&iacute;zděn&iacute; pro s&yacute;kory, lejsky i dal&scaron;&iacute; druhy pt&aacute;ků. Zapoj se s n&aacute;mi do koordinace p&eacute;če o ptač&iacute; budky.&nbsp;</span></p>\r\n<p>&nbsp;</p>'), ('description', '<p><span style="font-weight: 400;">Aktu&aacute;lně m&aacute;me vyvě&scaron;eno na 200 budek. Budky každoročně doplňujeme, opravujeme, čist&iacute;me a monitorujeme jejich obsazenost. K tomu poř&aacute;d&aacute;me vět&scaron;inou odpoledn&iacute; dobrovolnick&eacute; akce pro ty, co chtěj&iacute; pomoci.</span></p>\r\n<p><span style="font-weight: 400;">Hled&aacute;me nad&scaron;ence/nad&scaron;enkyni, kter&yacute;/kter&aacute; by p&eacute;či o budky koordinoval/koordinovala. To spoč&iacute;v&aacute; ve:</span></p>\r\n<ul>\r\n<li style="font-weight: 400;" aria-level="1"><span style="font-weight: 400;">spr&aacute;vě jednoduch&eacute; datab&aacute;ze budek</span></li>\r\n<li style="font-weight: 400;" aria-level="1"><span style="font-weight: 400;">př&iacute;pravě podkladů k p&eacute;či o budky v jednotliv&yacute;ch lokalit&aacute;ch (mapa a seznam budek z datab&aacute;ze)</span></li>\r\n<li style="font-weight: 400;" aria-level="1"><span style="font-weight: 400;">př&iacute;pravě nov&yacute;ch budek na vyvě&scaron;en&iacute;, popř. zaji&scaron;těn&iacute; drobn&eacute;ho materi&aacute;lu</span></li>\r\n<li style="font-weight: 400;" aria-level="1"><span style="font-weight: 400;">pomoc se zaji&scaron;těn&iacute;m 3-5 akc&iacute; během roku na monitoring, či&scaron;těn&iacute; a &uacute;držbu budek (mohou je organizovat i dal&scaron;&iacute; dobrovoln&iacute;ci)</span></li>\r\n<li style="font-weight: 400;" aria-level="1"><span style="font-weight: 400;">zad&aacute;n&iacute; obsazenosti budek do datab&aacute;ze</span></li>\r\n</ul>'), ('location_benefits', '<p><span style="font-weight: 400;">Podpoř&iacute;&scaron; p&eacute;či o ptactvo v mnoha lokalit&aacute;ch Brna, biodiverzitu městk&eacute; př&iacute;rody apod.<br /></span></p>'), ('personal_benefits', '<p><span style="font-weight: 400;">Zejm&eacute;na dobr&yacute; pocit, že zpěv ptactva v brněnsk&yacute;ch parc&iacute;ch zn&iacute; i d&iacute;ky tobě! Taky se dozv&iacute;&scaron; o tom, jak a proč se budky vyvě&scaron;uj&iacute;, jac&iacute; pt&aacute;ci v nich hn&iacute;zdn&iacute;, apod. Inspirovat tě budou obdobn&eacute; brontosauř&iacute; projekty po cel&eacute; ČR. Rozvine&scaron; si organizačn&iacute; dovednosti, přiuč&iacute;&scaron; se něco k propagaci akc&iacute;. A zejm&eacute;na pozn&aacute;&scaron; dal&scaron;&iacute; inspirativn&iacute; lidi na Dobrovolnick&eacute;m centru Hnut&iacute; Brontosaurus.</span></p>'), ('requirements', '<p><span style="font-weight: 400;">Uv&iacute;t&aacute;me dovednosti pr&aacute;ce s GPS navigac&iacute; a z&aacute;kladn&iacute; organizačn&iacute; schopnosti. Znalost v&yacute;znamu budek a problematiky ochrany ptactva v&yacute;hodou. <br /></span></p>'), ('contact_name', 'Tereza Opravilová'), ('contact_phone', '+420 736 720 568'), ('contact_email', 'akce-priroda@brontosaurus.cz'), ('image', '/media/opportunity_images/IMG_6549.jpg'), ('category_id', 2), ('location_id', 100), ('contact_person_id', None)]), OrderedDict([('id', 12), ('name', 'Technické zázemí pro organizátorské setkání REFRESH'), ('start', '2022-10-01'), ('end', '2022-12-04'), ('on_web_start', '2022-09-09'), ('on_web_end', '2022-10-20'), ('introduction', '<p>Skvěl&yacute; t&yacute;m velk&eacute;ho organiz&aacute;torsk&eacute;ho setk&aacute;n&iacute; Hnut&iacute; Brontosaurus REFRESH do sv&yacute;ch řad r&aacute;d přijme dal&scaron;&iacute; členy a členky, co by chtěli pomoci v z&aacute;zem&iacute; akce, s koordinac&iacute; j&iacute;del, př&iacute;pravou občerstven&iacute; pro &uacute;častn&iacute;ky, př&iacute;pravou materi&aacute;lu apod.</p>'), ('description', '<p>Hled&aacute;me:</p>\r\n<p>Ty, jež by uměli koordinovat př&iacute;pravu coffe breaků, čajovny a dal&scaron;&iacute;ho občerstven&iacute; na akci.</p>\r\n<p>Ty, jež by uměli komunikovat s m&iacute;stn&iacute; kuchyn&iacute; a kuchařkami, napl&aacute;novat a ře&scaron;it j&iacute;deln&iacute;ček apod.</p>\r\n<p>Ty, jež by uměli schrom&aacute;ždit, nakoupit, sehnat a na m&iacute;stě spravovat a chystat materi&aacute;l potřebn&yacute; na jednotliv&eacute; programy.</p>'), ('location_benefits', '<p>&Scaron;tastn&iacute; &uacute;častn&iacute;ci akce :-)</p>'), ('personal_benefits', '<p>Pozn&aacute;n&iacute; z&aacute;kulis&iacute; př&iacute;pravy jedn&eacute; z největ&scaron;&iacute;ch akc&iacute; Hnut&iacute; Brontosaurus pro organiz&aacute;tory. Z&iacute;sk&aacute;n&iacute; organiz&aacute;torsk&yacute;ch zku&scaron;enost&iacute; při př&iacute;pravě. Nov&eacute; kontakty.</p>\r\n<p>Radost z toho, že jsme společně připravili akci, kter&aacute; Brontosaura posune zase d&aacute;l, namotivuje nov&eacute; organiz&aacute;tory a pote&scaron;&iacute; ty st&aacute;vaj&iacute;c&iacute;.</p>'), ('requirements', '<p>Na akci a před n&iacute; uv&iacute;t&aacute;me dobrou n&aacute;ladu, nadhled, organizačn&iacute; dovednosti, flexibilitu v ře&scaron;en&iacute; probl&eacute;mů... :-)</p>\r\n<p>Bude potřeba věnovat čas př&iacute;pravě i před akc&iacute;. Cca min. 2-3 schůzky, t&yacute;movky, př&iacute;prava materi&aacute;lu dle potřeb, jež vyplynou.</p>'), ('contact_name', 'Rozálie Jandová'), ('contact_phone', ''), ('contact_email', ''), ('image', '/media/opportunity_images/P1020127.jpg'), ('category_id', 1), ('location_id', 60), ('contact_person_id', None)]), OrderedDict([('id', 16), ('name', 'Výsadba stromů v Hruškách'), ('start', '2022-12-02'), ('end', '2022-12-18'), ('on_web_start', '2022-10-10'), ('on_web_end', '2022-12-11'), ('introduction', '<p>Vesnice Hru&scaron;ky nedaleko Slavkova je vesnic&iacute; plnou ovoce. Za v&yacute;sadbami stoj&iacute; klub Spadl&iacute; z Hru&scaron;ky v čele s Dominikem Grohmannem. Na několika dobrovolnick&yacute;ch akc&iacute;ch se zde od roku 2018 vys&aacute;zelo na stovku ovocn&yacute;ch stromů, o kter&eacute; se každoročně pečuje a dal&scaron;&iacute; se st&aacute;le s&aacute;z&iacute;.</p>\r\n<p>V současn&eacute; době zde v&scaron;ak chyb&iacute; dobrovoln&iacute;ci a dobrovolnice, kteř&iacute; by o tyto v&yacute;sadby pečovali a na nov&yacute;ch v&yacute;sadb&aacute;ch se pod&iacute;leli. <strong>Hled&aacute;me organiz&aacute;tory či organiz&aacute;torsk&eacute; t&yacute;my</strong>, kteř&iacute; zde na zač&aacute;tku prosince uspoř&aacute;daj&iacute; dobrovolnicko z&aacute;žitkovou akci na v&yacute;sadby stromů!</p>'), ('description', '<p>Uspoř&aacute;dej dobrovolnickou jednodenn&iacute; akci nebo dobrovolnicko z&aacute;žitkovou v&iacute;kendovku v Hru&scaron;k&aacute;ch. N&aacute;pln&iacute; dobrovolnick&eacute; pr&aacute;ce bude dosadba ovocn&yacute;ch stromů do v&yacute;sadeb po okol&iacute; a p&eacute;če o vysazen&eacute; stromy, kter&aacute; bude prob&iacute;hat ve spolupr&aacute;ci s Dominikem či něk&yacute;m z ovocn&aacute;řsk&eacute;ho t&yacute;mu.</p>\r\n<p>Na tobě tak bude <strong>realizace akce</strong> ve smyslu z&aacute;zem&iacute;, propagace, programu, komunikace s &uacute;častn&iacute;ky apod.&nbsp;</p>\r\n<p>Pro kon&aacute;n&iacute; akce lze využ&iacute;t prostory hasičky př&iacute;mo v obci, kter&aacute; je vybaven&aacute; kuchyn&iacute;, koupelnou, span&iacute; je na karimatk&aacute;ch.</p>'), ('location_benefits', '<p>Pomůže&scaron; s p&eacute;č&iacute; o ovocn&eacute; stromy a jejich n&aacute;vratem do krajiny.</p>'), ('personal_benefits', '<p>Pod veden&iacute;m zku&scaron;en&yacute;ch sadařů a sadařek se nauč&iacute;&scaron;, jak spr&aacute;vně s&aacute;zet stromy a pečovat o ně. Kromě samotn&eacute; dobrovolnick&eacute; pr&aacute;ce je možn&eacute; se domluvit na workshopu k ovocn&yacute;m stromům, určov&aacute;n&iacute; odrůd ovoce či rukoděln&yacute;m workshopům.</p>\r\n<p>Jinak z&iacute;sk&aacute;&scaron; dal&scaron;&iacute; cenn&eacute; zku&scaron;enosti z organizace dobrovolnicko z&aacute;žitkov&eacute; akce.</p>'), ('requirements', '<p>Nad&scaron;en&iacute; a odhodl&aacute;n&iacute; do organizace dobrovolnick&eacute; v&iacute;kendovky nebo jednodenn&iacute; akce.</p>'), ('contact_name', 'Terka'), ('contact_phone', '+420 736 720 568'), ('contact_email', 'akce-priroda@brontosaurus.cz'), ('image', '/media/opportunity_images/IMG_5913.JPG'), ('category_id', 3), ('location_id', 1973), ('contact_person_id', None)]), OrderedDict([('id', 17), ('name', 'Biokoridor Přerov Hvězdárna'), ('start', '2023-01-15'), ('end', '2023-09-30'), ('on_web_start', '2023-01-01'), ('on_web_end', '2023-09-24'), ('introduction', '<p>Vznikaj&iacute;c&iacute; biokoridor Přerov - Hvězd&aacute;rna se nach&aacute;z&iacute; v zemědělsk&eacute; krajině na v&yacute;chodn&iacute;m okraji města. Je opatřen&iacute;m pro podporu biodiverzity a pro adaptaci krajiny na změnu klimatu. Za jeho vznikem stoj&iacute; přerovsk&yacute; <strong>spolek Na&scaron;e společn&aacute; krajina</strong>, kter&yacute; biokoridor navrhnul, vytvořil a pravidelně se o něj star&aacute;. P&eacute;če je na několik m&aacute;lo členů spolku mnoho a dal&scaron;&iacute; zapojen&iacute; dobrovoln&iacute;ků by tak mohlo s p&eacute;č&iacute; o biokoridor ulehčil a pomohli by pustit se do dal&scaron;&iacute;ch projektů jako např&iacute;klad realizace naučn&eacute; stezky přes biokoridor.</p>'), ('description', '<p>Hled&aacute;me jednotliv&eacute; organiz&aacute;tory nebo organiz&aacute;torsk&eacute; t&yacute;my, kteř&iacute; by r&aacute;di ve spolupr&aacute;ci s m&iacute;stn&iacute;m spolkem na tomto m&iacute;stě poř&aacute;dali jednodenn&iacute; nebo v&iacute;kendov&eacute; dobrovolnick&eacute; akce. N&aacute;pln&iacute; dobrovolnick&eacute; pr&aacute;ce by byla dle ročn&iacute;ho obdob&iacute; v&yacute;pomoc s p&eacute;č&iacute; o biokoridor (např&iacute;klad stavba a opravy oplocenek, sečen&iacute; a kosen&iacute; porostu, odstraňov&aacute;n&iacute; nepůvodn&iacute;ch n&aacute;letů, v&yacute;roba a instalace hmyz&iacute;ch domečků a ptač&iacute;ch budek, zal&eacute;v&aacute;n&iacute; a o&scaron;etřov&aacute;n&iacute; v&yacute;sadeb dřevin, s&aacute;zen&iacute; nov&yacute;ch keřů a stromů, &uacute;držba informačn&iacute;ch prvků, a dal&scaron;&iacute;).</p>'), ('location_benefits', '<p>Biokoridor a dal&scaron;&iacute; navazuj&iacute;c&iacute; prvky vytvoř&iacute; až sedm kilometrů dlouh&yacute; p&aacute;s zeleně kolem v&yacute;chodn&iacute;ho okraje Přerova. M&iacute;sto bude sloužit jako uk&aacute;zkov&yacute; postup pro obnovu zemědělsk&eacute; krajiny a jako oblast bohat&eacute;ho v&yacute;skytu poln&iacute;ch druhů rostlin a živočichů. Krajinou bude proch&aacute;zet ekoturistick&aacute; stezka, kterou může veřejnost &scaron;etrně nahl&eacute;dnout do tajů př&iacute;rody kulturn&iacute; stepi. Bude zde možnost pozorovat nespočet vz&aacute;cn&yacute;ch kvetouc&iacute;ch plevelů, denn&iacute;ch i nočn&iacute;ch mot&yacute;lů a poln&iacute;ch pt&aacute;ků. O lokalitě Biokoridor Přerov Hvězd&aacute;rna se může&scaron; v&iacute;c doč&iacute;st v <a href="https://www.mapotic.com/lokality-hnuti-brontosaurus/1478925-biokoridor-prerov-hvezdarna">datab&aacute;zi lokalit</a>.&nbsp;</p>'), ('personal_benefits', '<p>Z&iacute;sk&aacute;&scaron; cenn&eacute; zku&scaron;enosti s poř&aacute;d&aacute;n&iacute;m dobrovolnick&yacute;ch nebo dobrovolnicko z&aacute;žitkov&yacute;ch akc&iacute; a <strong>praktick&eacute; zku&scaron;enosti s p&eacute;č&iacute; o př&iacute;rodn&iacute; lokalitu</strong>, dozv&iacute;&scaron; se mnoho nov&yacute;ch věc&iacute; o <strong>současn&eacute; zemědělsk&eacute; krajině</strong>, možn&yacute;ch ře&scaron;en&iacute; probl&eacute;mů krajiny, nauč&iacute;&scaron; se nov&eacute; typy činnost&iacute; v př&iacute;rodě.&nbsp;</p>\r\n<p>Pro samotn&eacute; poř&aacute;d&aacute;n&iacute; akc&iacute; je na lokalitě v&yacute;hodu spolupr&aacute;ce se spolkem Na&scaron;e společn&aacute; krajina, kter&yacute;<strong> prakticky i odborně za&scaron;t&iacute;t&iacute; dobrovolnickou činnost</strong>, pomůže s hled&aacute;n&iacute;m z&aacute;zem&iacute; ve městě a může nab&iacute;dnout bohat&yacute; doprovodn&yacute; program v podobě exkurz&iacute; po okol&iacute;.&nbsp;</p>'), ('requirements', '<p>Zku&scaron;enost s dobrovolnick&yacute;mi akcemi pro př&iacute;rodu (alespoň v podobě &uacute;časti), komunikačn&iacute; schopnosti a t&yacute;mvov&aacute; spolupr&aacute;ce, v př&iacute;padě organizace v&iacute;kendov&eacute; akce kvalifikace Organiz&aacute;tor v&iacute;kendovek HB alespoň jednoho člena t&yacute;mu.&nbsp;</p>'), ('contact_name', 'Petr Rejzek'), ('contact_phone', ''), ('contact_email', 'info@koroptvicky.cz'), ('image', '/media/opportunity_images/a_lokalita4d.jpg'), ('category_id', 3), ('location_id', 329), ('contact_person_id', None)]), OrderedDict([('id', 18), ('name', 'Ekofarma Šardice'), ('start', '2023-01-16'), ('end', '2023-08-30'), ('on_web_start', '2023-01-01'), ('on_web_end', '2023-06-30'), ('introduction', '<p>Chce&scaron; se dozvědět něco o tom, jak můžeme v zemědělsk&eacute; krajině zadržovat vodu, podporovat biodiverzitu a navracet život? Chce&scaron; na vlastn&iacute; oči vidět jak to v&scaron;echno může fungovat a chce&scaron; se zapojit do p&eacute;če o takov&aacute; m&iacute;sta?</p>\r\n<p>Zapoj se do pomoci na Ekofarmě v &Scaron;ardic&iacute;ch, vyraž sem s kamar&aacute;dy v men&scaron;&iacute; skupině nebo zde uspoř&aacute;dej akci pro dal&scaron;&iacute; dobrovoln&iacute;ky a dobrovolnice!&nbsp;</p>'), ('description', '<p>Prvotn&iacute;m z&aacute;měrem zemědělce a pedagoga Petra Marady byla ochrana &uacute;zem&iacute; před nepř&iacute;zniv&yacute;m a ničiv&yacute;m dopadem př&iacute;valov&yacute;ch de&scaron;ťů. Kromě obnovy vodn&iacute;ho režimu krajiny jeho opatřen&iacute; ale tak&eacute; podporuj&iacute; biodiverzitu a zaji&scaron;ťuj&iacute; prostupnost krajiny. Jeho aktivity rozv&iacute;j&iacute; fungov&aacute;n&iacute; komunity a jsou tak&eacute; zdrojem odborn&eacute; a informačn&iacute; činnosti. Postupn&yacute;m roz&scaron;iřov&aacute;n&iacute;m obhospodařovan&yacute;ch pozemků vznikla vzorov&aacute; ekofarma, na kter&eacute; m&aacute;&scaron; možnost zapojit se do p&eacute;če o př&iacute;rodu i ty a kromě toho se dozvědět spoustu informac&iacute; a nahl&eacute;dnout do toho, jak zdej&scaron;&iacute; ekosyst&eacute;m funguje.&nbsp;</p>\r\n<p>Do &Scaron;ardic může&scaron; vyrazit pom&aacute;hat a vzděl&aacute;vat se s kamar&aacute;dy v men&scaron;&iacute; skupině nebo zde může&scaron; uspoř&aacute;dat jednodenn&iacute; nebo v&iacute;cedenn&iacute; dobrovolnickou akci. N&aacute;pln&iacute; dobrovolnick&eacute; činnosti na ekofarmě je pomoc s p&eacute;č&iacute; o v&yacute;znamn&eacute; krajinotvorn&eacute; prvky zemědělsk&eacute; krajiny - sečen&iacute; tr&aacute;vobylinn&eacute;ho patra, odstraňov&aacute;n&iacute; oplocenek, odstraňov&aacute;n&iacute; letorostů z kmene ovocn&yacute;ch stromů apod.&nbsp;</p>'), ('location_benefits', '<p>Chceme dos&aacute;hnout uk&aacute;zky spr&aacute;vn&eacute; praxe - dosažen&iacute; vzorov&eacute; - demonstračn&iacute; p&eacute;če o krajinn&eacute; prvky.</p>'), ('personal_benefits', '<p>Dostane&scaron; př&iacute;ležitost dovz&iacute;dat se nov&eacute; věci a zkoumat o adaptac&iacute;ch krajiny na klimatickou změnu. Uvid&iacute;&scaron;, jak tyto prvky v krajině funguj&iacute; a jak&eacute; možnosti jako jednotlivci m&aacute;me.&nbsp;</p>'), ('requirements', '<p>Chuť zaj&iacute;mat se o fungov&aacute;n&iacute; krajiny a ře&scaron;en&iacute; aktu&aacute;ln&iacute;ch environment&aacute;ln&iacute;ch probl&eacute;mů. V př&iacute;padě poř&aacute;d&aacute;n&iacute; akc&iacute; zku&scaron;enost s dobrovolnick&yacute;mi akcemi (alespoň na &uacute;rovni &uacute;častnick&eacute;).</p>'), ('contact_name', 'Petr Marada'), ('contact_phone', ''), ('contact_email', 'marada@mendelu.cz'), ('image', '/media/opportunity_images/210616_02_petr-marada_09_2500px_1.jpg'), ('category_id', 3), ('location_id', 2178), ('contact_person_id', None)]), OrderedDict([('id', 19), ('name', 'Kutiny na Tišnovsku'), ('start', '2023-01-16'), ('end', '2023-08-30'), ('on_web_start', '2023-01-01'), ('on_web_end', '2023-01-16'), ('introduction', '<p>Přidejte se k ochraně stepn&iacute; př&iacute;rodn&iacute; pam&aacute;tky pln&eacute; jalovců, prořez&aacute;vce březov&eacute;ho lesa a večerům u ohně. Zapoj se do obnovy svažit&eacute; stepn&iacute; vegetace Př&iacute;rodn&iacute; pam&aacute;tky Pl&aacute;ně a světl&yacute;ch lesů na Ti&scaron;novsku. Ček&aacute; na tebe smyslupln&aacute; pr&aacute;ce, span&iacute; na seně a klidn&aacute; př&iacute;roda v &uacute;dol&iacute; kousek za Brnem.&nbsp;&nbsp;</p>'), ('description', '<p>Uspoř&aacute;dej v&iacute;kendovku nebo jednodenn&iacute; akci na ochranu př&iacute;rody cenn&eacute;ho stanovi&scaron;tě mnoha bezobratl&yacute;ch živoč&iacute;chů a rostlin. M&iacute;stn&iacute; znalci tě zasvět&iacute; do zdej&scaron;&iacute; př&iacute;rody a v&yacute;znamu dobrovolnick&eacute; činnosti.</p>\r\n<p>K z&aacute;zem&iacute; akce lze využ&iacute;t star&scaron;&iacute; dům v nedalek&eacute; osadě Kutiny. Přehnan&eacute;ho luxusu se ale neob&aacute;vej, span&iacute; je na seně ve stodole nebo na louce pod &scaron;ir&aacute;kem. Z&aacute;zem&iacute; domu s kadibudkou, studenou vodou z hadice a teplo z kamen.&nbsp;</p>'), ('location_benefits', '<p>Pomůžete s p&eacute;č&iacute; o lokalitu, kter&aacute; m&aacute; potenci&aacute;l st&aacute;t se &uacute;toči&scaron;těm mnoha vz&aacute;cn&yacute;ch brzobratl&yacute;ch živočichů a rostlin. Vedle p&eacute;če o př&iacute;rodn&iacute; pam&aacute;tku je možnost zapojit se do přeměny smrkov&eacute;ho lesa ve světl&yacute; pařezinov&yacute; les, č&iacute;mž opět podpoř&iacute;me m&iacute;stn&iacute; biodiverzitu a stabilitu ekosyst&eacute;mu.&nbsp;</p>'), ('personal_benefits', '<p>Z&iacute;sk&aacute;&scaron; cenn&eacute; zku&scaron;enosti s poř&aacute;d&aacute;n&iacute;m dobrovolnick&yacute;ch nebo dobrovolnicko z&aacute;žitkov&yacute;ch akc&iacute; a&nbsp;<strong>praktick&eacute; zku&scaron;enosti s p&eacute;č&iacute; o př&iacute;rodn&iacute; lokalitu.</strong></p>\r\n<p>Pro samotn&eacute; poř&aacute;d&aacute;n&iacute; akc&iacute; je na lokalitě v&yacute;hodu spolupr&aacute;ce se spr&aacute;vcem lokality a spolkem ČSOP, kter&yacute; se o lokalitu star&aacute; a může prakticky i odborně za&scaron;t&iacute;tit dobrovolnickou činnost.&nbsp;</p>'), ('requirements', '<p>Zku&scaron;enost s dobrovolnick&yacute;mi akcemi pro př&iacute;rodu (alespoň v podobě &uacute;časti), komunikačn&iacute; schopnosti a t&yacute;mvov&aacute; spolupr&aacute;ce, v př&iacute;padě organizace v&iacute;kendov&eacute; akce kvalifikace Organiz&aacute;tor v&iacute;kendovek HB alespoň jednoho člena t&yacute;mu.&nbsp;</p>'), ('contact_name', 'Tereza Opravilová'), ('contact_phone', '+420 736 720 568'), ('contact_email', 'akce-priroda@brontosaurus.cz'), ('image', '/media/opportunity_images/AF1QipMiyDLYA_z1B8hiqUwpivJUy1Aa4eqJSwpzYYhcw4032-h3024.jpg'), ('category_id', 3), ('location_id', 729), ('contact_person_id', None)]), OrderedDict([('id', 20), ('name', 'Organizátorský tým pro mezinárodní dobrovolnický tábor'), ('start', '2023-01-16'), ('end', '2023-07-30'), ('on_web_start', '2023-01-01'), ('on_web_end', '2023-07-30'), ('introduction', '<p><span style="font-weight: 400;">Klasick&eacute; letn&iacute; dobrovolnick&eacute; t&aacute;bory Hnut&iacute; Brontosaurus jsme roz&scaron;&iacute;řili o 3 nov&eacute;, mezin&aacute;rodn&iacute; t&aacute;bory i pro &uacute;častn&iacute;ky ze zahranič&iacute;. Zapoj se do jedinečn&eacute; př&iacute;ležitosti pr&aacute;vě teď!</span></p>'), ('description', '<p><span style="font-weight: 400;">Přes l&eacute;to 2023 pl&aacute;nujeme zorganizovat 3 mezin&aacute;rodn&iacute; letn&iacute; t&aacute;bory a aktu&aacute;lně hled&aacute;me </span><strong>organiz&aacute;torsk&yacute; t&yacute;m</strong><span style="font-weight: 400;"> (3 nad&scaron;en&eacute; lidi) pro jeden z nich.&nbsp;</span></p>\r\n<p><span style="font-weight: 400;">Organiz&aacute;torsk&yacute; t&yacute;m společně s pomoc&iacute; na&scaron;ich zahraničn&iacute;ch ESC dobrovoln&iacute;ků zorganizuje </span><strong>14 denn</strong><span style="font-weight: 400;">&iacute; </span><strong>dobrovolnick&yacute; t&aacute;bo</strong><span style="font-weight: 400;">r pro celkem </span><strong>20 &uacute;častn&iacute;ků</strong><span style="font-weight: 400;"> (13 z Česka a 7 ze zahranič&iacute;). T&aacute;bor zat&iacute;m nem&aacute; přesn&yacute; datum ani lokalitu, nech&aacute;v&aacute;me to pr&aacute;vě na v&aacute;s a va&scaron;e časov&eacute; možnosti, měl by v&scaron;ak b&yacute;t v druh&eacute; polovině července (16.7. - 2.8.) nebo někdy na konci srpna (17.8. - 10.9.).&nbsp;</span></p>\r\n<p><span style="font-weight: 400;">Tvoje činnost bude spoč&iacute;vat zejm&eacute;na:&nbsp;</span></p>\r\n<ul>\r\n<li style="font-weight: 400;" aria-level="1"><span style="font-weight: 400;">&Uacute;čast na t&yacute;movk&aacute;ch</span></li>\r\n<li style="font-weight: 400;" aria-level="1"><span style="font-weight: 400;">Aktivn&iacute; př&iacute;prava programu&nbsp;</span></li>\r\n<li style="font-weight: 400;" aria-level="1"><span style="font-weight: 400;">Př&iacute;tomnost na t&aacute;boře na cel&yacute;ch 14 dn&iacute;</span></li>\r\n<li style="font-weight: 400;" aria-level="1"><span style="font-weight: 400;">Koordinace pr&aacute;ce, komunikace s &uacute;častn&iacute;ky, realizace programu&hellip;</span></li>\r\n</ul>'), ('location_benefits', '<p><span style="font-weight: 400;">Lokalita je zcela na v&yacute;běru organiz&aacute;torsk&eacute;ho t&yacute;mu. Př&iacute;nos bude velk&yacute;, pracovat budeme nejm&eacute;ně 7 dn&iacute; po dobu 4 - 8 hodin/den. </span></p>'), ('personal_benefits', '<p><span style="font-weight: 400;">Dobrovolnick&yacute; t&aacute;bor Evropsk&eacute;ho sboru solidarity přin&aacute;&scaron;&iacute; množstvo v&yacute;hod pro jednotlivce z organiz&aacute;torsk&eacute;ho t&yacute;mu i pro ZČ kter&yacute; zastupuje&scaron;</span></p>\r\n<ul>\r\n<li style="font-weight: 400;" aria-level="1"><span style="font-weight: 400;">Dobr&yacute; pocit z pomoci na lokalitě</span></li>\r\n<li style="font-weight: 400;" aria-level="1"><span style="font-weight: 400;">Potk&aacute;&scaron; nov&eacute; lidi z Česka ale i ze zahranič&iacute;&nbsp;</span></li>\r\n<li style="font-weight: 400;" aria-level="1"><span style="font-weight: 400;">Zlep&scaron;&iacute;&scaron; svoji angličtinu</span></li>\r\n<li style="font-weight: 400;" aria-level="1"><span style="font-weight: 400;">Za sv&eacute; nasazen&iacute; z&iacute;sk&aacute;&scaron; evropsk&yacute; certifik&aacute;t &ldquo;Youth Pass&rdquo;</span></li>\r\n<li style="font-weight: 400;" aria-level="1"><span style="font-weight: 400;">Dostane&scaron; kapesn&eacute; a stravn&eacute; na každ&yacute; den</span></li>\r\n<li style="font-weight: 400;" aria-level="1"><span style="font-weight: 400;">Stane&scaron; se souč&aacute;st&iacute; t&yacute;mu organiz&aacute;torů a organiz&aacute;torek mezin&aacute;rodn&iacute;ch aktivit Hnut&iacute; Brontosaurus</span></li>\r\n<li style="font-weight: 400;" aria-level="1"><span style="font-weight: 400;">Podpoř&iacute;me tě men&scaron;&iacute; finančn&iacute; kompenzac&iacute; za čas str&aacute;ven&yacute; na př&iacute;prav&aacute;ch</span></li>\r\n<li style="font-weight: 400;" aria-level="1"><span style="font-weight: 400;">Rovnako podpoř&iacute;me tvůj ZČ nov&yacute;m vybaven&iacute;m a materi&aacute;lem</span></li>\r\n<li style="font-weight: 400;" aria-level="1"><span style="font-weight: 400;">Nauč&iacute;&scaron; se postupy důležit&eacute; pro organizov&aacute;n&iacute; mezin&aacute;rodn&iacute;ch eventov</span></li>\r\n<li style="font-weight: 400;" aria-level="1"><span style="font-weight: 400;">A mnoho dal&scaron;&iacute;ho :)&nbsp;</span></li>\r\n</ul>'), ('requirements', '<ul>\r\n<li style="font-weight: 400;" aria-level="1"><span style="font-weight: 400;">Alespoň z&aacute;kladn&iacute; znalost angličtiny</span></li>\r\n<li style="font-weight: 400;" aria-level="1"><span style="font-weight: 400;">Chuť pomoci a aktivn&iacute;ho zapojen&iacute;</span></li>\r\n<li style="font-weight: 400;" aria-level="1"><span style="font-weight: 400;">Př&iacute;tomnost na t&aacute;boře na cel&yacute;ch 14 dn&iacute;&nbsp;</span></li>\r\n<li style="font-weight: 400;" aria-level="1"><span style="font-weight: 400;">&Uacute;čast na velk&eacute;m společn&eacute;m pl&aacute;nov&aacute;n&iacute; v&scaron;ech tř&iacute; t&aacute;borů o v&iacute;kendu 10.-12.3.2023&nbsp;</span></li>\r\n<li style="font-weight: 400;" aria-level="1"><span style="font-weight: 400;">Nad&scaron;en&iacute;, spolupr&aacute;ce skrz cel&eacute; Hnut&iacute; Brontosaurus</span></li>\r\n</ul>'), ('contact_name', 'Veronika Vlačuhová'), ('contact_phone', '+420 734 392 735'), ('contact_email', 'international@brontosaurus.cz'), ('image', '/media/opportunity_images/20220704_135028.jpg'), ('category_id', 1), ('location_id', 100), ('contact_person_id', None)]), OrderedDict([('id', 21), ('name', 'Pomoc s organizací výstavy celostátní soutěže Máme rádi přírodu'), ('start', '2023-01-17'), ('end', '2023-01-28'), ('on_web_start', '2023-01-01'), ('on_web_end', '2023-01-28'), ('introduction', '<p><span style="font-weight: 400;">Chce&scaron; se zapojit do organiz&aacute;torsk&eacute;ho t&yacute;mu a l&aacute;k&aacute; tě vět&scaron;&iacute; akce? Co třeba rovnou akce celost&aacute;tn&iacute;ho rozměru? Nem&aacute;&scaron; čas se zapojit do dlouhodoběj&scaron;&iacute;ho spolupr&aacute;ce? Pojď n&aacute;m pomoci s organizac&iacute; v&yacute;stavy a slavnostn&iacute;ho před&aacute;v&aacute;n&iacute; cen v r&aacute;mci celost&aacute;tn&iacute; soutěže M&Aacute;ME R&Aacute;DI PŘ&Iacute;RODU!</span></p>'), ('description', '<p><span style="font-weight: 400;">Bl&iacute;ž&iacute; se vyhl&aacute;&scaron;en&iacute; v&yacute;sledků kreativn&iacute; soutěže M&aacute;me r&aacute;di př&iacute;rodu. M&aacute;me r&aacute;di př&iacute;rodu&ldquo; je celost&aacute;tn&iacute; soutěž pro děti a ml&aacute;dež do 19 let, kterou poř&aacute;d&aacute; Hnut&iacute; Brontosaurus. Soutěž m&aacute; dlouholetou tradici, je organizov&aacute;na již od roku 1992. Soutěž si klade za &uacute;kol v prvn&iacute; řadě podpořit z&aacute;jem o př&iacute;rodu a p&eacute;či o ni. Je určena pro v&scaron;echny milovn&iacute;ky př&iacute;rody, kteř&iacute; z&aacute;roveň i r&aacute;di něco tvoř&iacute;. Se sv&yacute;mi v&yacute;tvarn&yacute;mi a liter&aacute;rn&iacute;mi d&iacute;ly, fotografiemi a bezva ekof&oacute;ry se j&iacute; &uacute;častn&iacute; děti a ml&aacute;dež (od M&Scaron; po S&Scaron;) z cel&eacute; ČR. Letos se se&scaron;lo neuvěřiteln&yacute;ch </span><span style="font-weight: 400;">&nbsp;2 150 děl. Teď n&aacute;s ček&aacute; slavnostn&iacute; </span><span style="font-weight: 400;">vyhl&aacute;&scaron;en&iacute; v&yacute;sledků a před&aacute;v&aacute;n&iacute;&nbsp; cen, na kter&eacute; se sjedou &uacute;častn&iacute;ci soutěže z cel&eacute; republiky. </span></p>\r\n<p><span style="font-weight: 400;">Nev&aacute;hej a přidej se do organiz&aacute;torsk&eacute;ho t&yacute;mu! Hled&aacute;me pomocn&iacute;ky, kteř&iacute; pomůžou na m&iacute;stě při slavnostn&iacute;m vyhl&aacute;&scaron;en&iacute; v&yacute;sledků a před&aacute;v&aacute;n&iacute;&nbsp; cen.&nbsp;</span></p>\r\n<p><span style="font-weight: 400;">&nbsp;</span></p>\r\n<p><span style="font-weight: 400;">Možnosti zapojen&iacute;:</span></p>\r\n<ul>\r\n<li style="font-weight: 400;" aria-level="1"><span style="font-weight: 400;">pomoc s organizov&aacute;n&iacute;m vyhl&aacute;&scaron;en&iacute; v&yacute;sledků&nbsp;</span></li>\r\n<li style="font-weight: 400;" aria-level="1"><span style="font-weight: 400;">pomoc s doprovodn&yacute;m programem - d&iacute;lny pro děti</span></li>\r\n<li style="font-weight: 400;" aria-level="1"><span style="font-weight: 400;">pomoc s před&aacute;v&aacute;n&iacute;m cen&nbsp;</span></li>\r\n<li style="font-weight: 400;" aria-level="1"><span style="font-weight: 400;">komunikace s rodiči, dětmi a učiteli</span></li>\r\n<li style="font-weight: 400;" aria-level="1"><span style="font-weight: 400;">fotograf</span></li>\r\n</ul>'), ('location_benefits', ''), ('personal_benefits', '<p><span style="font-weight: 400;">Načerp&aacute;&scaron; zku&scaron;enosti z organizace akce celost&aacute;tn&iacute;ho rozměru.&nbsp;</span></p>\r\n<p><span style="font-weight: 400;">Podpoř&iacute;&scaron; z&aacute;jem o př&iacute;rodu a p&eacute;či o ni u dět&iacute; a ml&aacute;deže např&iacute;č celou republikou.</span></p>\r\n<p><span style="font-weight: 400;">Stane&scaron; se souč&aacute;st&iacute; zku&scaron;en&eacute;ho t&yacute;mu organiz&aacute;torů.</span></p>\r\n<p><span style="font-weight: 400;">Z&iacute;sk&aacute;&scaron; přehled v dal&scaron;&iacute; činnosti v r&aacute;mci Hnut&iacute; Brontosaurus.&nbsp;</span></p>\r\n<p><span style="font-weight: 400;">Organizaci soutěže může&scaron; pojmout jako praxi při studiu na v&scaron;.</span></p>\r\n<p><span style="font-weight: 400;">Pozn&aacute;&scaron; nov&eacute; lidi. </span></p>'), ('requirements', '<p><span style="font-weight: 400;">Chuť pomoci a aktivn&iacute; zapojen&iacute; :) </span></p>'), ('contact_name', 'Jitka Rajmonová'), ('contact_phone', '+420 732 882 032'), ('contact_email', 'mrp@brontosaurus.cz'), ('image', '/media/opportunity_images/DSC_0400.JPG'), ('category_id', 2), ('location_id', 100), ('contact_person_id', None)]), OrderedDict([('id', 22), ('name', 'Organizátorský tým pro celostátní soutěž Máme rádi přírodu'), ('start', '2023-01-17'), ('end', '2023-01-28'), ('on_web_start', '2023-01-01'), ('on_web_end', '2023-01-28'), ('introduction', '<p><span style="font-weight: 400;">Chce&scaron; se zapojit do organiz&aacute;torsk&eacute;ho t&yacute;mu a l&aacute;k&aacute; tě vět&scaron;&iacute; akce? Co třeba rovnou akce celost&aacute;tn&iacute;ho rozměru?Pojď n&aacute;m pomoci s organizac&iacute; celost&aacute;tn&iacute; soutěže M&Aacute;ME R&Aacute;DI PŘ&Iacute;RODU!</span></p>'), ('description', '<p><span style="font-weight: 400;">M&aacute;me r&aacute;di př&iacute;rodu&ldquo; je celost&aacute;tn&iacute; soutěž pro děti a ml&aacute;dež do 19 let, kterou poř&aacute;d&aacute; Hnut&iacute; Brontosaurus. Soutěž m&aacute; dlouholetou tradici, je organizov&aacute;na již od roku 1992. Soutěž si klade za &uacute;kol v prvn&iacute; řadě podpořit z&aacute;jem o př&iacute;rodu a p&eacute;či o ni. Je určena pro v&scaron;echny milovn&iacute;ky př&iacute;rody, kteř&iacute; z&aacute;roveň i r&aacute;di něco tvoř&iacute;.</span></p>\r\n<p><span style="font-weight: 400;">Nev&aacute;hej a přidej se do organiz&aacute;torsk&eacute;ho t&yacute;mu! Může&scaron; se zapojit do komunikace s &uacute;častn&iacute;ky soutěže, organizace slavnostn&iacute;ho vyhl&aacute;&scaron;en&iacute; v&yacute;sledků, hodnocen&iacute; př&iacute;choz&iacute;ch děl, vym&yacute;&scaron;len&iacute; oceněn&iacute; pro &uacute;častn&iacute;ky soutěže nebo vymy&scaron;len&iacute; t&eacute;matu a konceptu dal&scaron;&iacute;ho ročn&iacute;ku.</span></p>'), ('location_benefits', ''), ('personal_benefits', '<p><span style="font-weight: 400;">Načerp&aacute;&scaron; zku&scaron;enosti z organizace akce celost&aacute;tn&iacute;ho rozměru.&nbsp;</span></p>\r\n<p><span style="font-weight: 400;">Podpoř&iacute;&scaron; z&aacute;jem o př&iacute;rodu a p&eacute;či o ni u dět&iacute; a ml&aacute;deže např&iacute;č celou republikou.</span></p>\r\n<p><span style="font-weight: 400;">Z&iacute;sk&aacute;&scaron; možnost pro vlastn&iacute; seberealizaci v r&aacute;mci vym&yacute;&scaron;len&iacute; dal&scaron;&iacute;ho ročn&iacute;ku soutěže.</span></p>\r\n<p><span style="font-weight: 400;">Stane&scaron; se souč&aacute;st&iacute; zku&scaron;en&eacute;ho t&yacute;mu organiz&aacute;torů.</span></p>\r\n<p><span style="font-weight: 400;">Z&iacute;sk&aacute;&scaron; přehled v dal&scaron;&iacute; činnosti v r&aacute;mci Hnut&iacute; Brontosaurus.&nbsp;</span></p>\r\n<p><span style="font-weight: 400;">Organizaci soutěže může&scaron; pojmout jako praxi při studiu na v&scaron;.</span></p>\r\n<p><span style="font-weight: 400;">Pozn&aacute;&scaron; nov&eacute; lidi.&nbsp;</span></p>'), ('requirements', '<p><span style="font-weight: 400;">Chuť pomoci a aktivn&iacute; zapojen&iacute; :) </span></p>'), ('contact_name', 'Jitka Rajmonová'), ('contact_phone', '+420 732 882 032'), ('contact_email', 'mrp@brontosaurus.cz'), ('image', '/media/opportunity_images/DSC_0423.JPG'), ('category_id', 2), ('location_id', 100), ('contact_person_id', None)])]

class Command(BaseCommand):
    def handle(self, *args, **options):
        for item in data:
            item['contact_person_id'] = User.objects.get_or_create(all_emails__email=item['contact_email'], defaults={
                'email': item['contact_email'],
                'first_name': 'Prázdný',
                'last_name': 'User',
            })[0].id
            Opportunity.objects.create(**item)
