import json

def pt(texts):
    blocks = []
    for i, text in enumerate(texts):
        blocks.append({
            "_type": "block",
            "_key": f"blk{i+1}",
            "style": "normal",
            "children": [{
                "_type": "span",
                "_key": f"spn{i+1}",
                "text": text,
                "marks": []
            }]
        })
    return json.dumps(blocks, ensure_ascii=False)

# (id, slug, title, excerpt, category, reading_time, date, content_paragraphs)
articles = [
  ("01KRTQ00000000000000000A01",
   "puterea-rugaciunii-in-vindecare",
   "Puterea rugăciunii în vindecare — ce spune știința și credința",
   "Rugăciunea nu este doar o practică religioasă — studii medicale recente arată că ea influențează pozitiv sănătatea trupului și a minții. Descoperă ce spun cercetătorii și ce învață Biserica Ortodoxă despre tămăduire.",
   "Vindecare spirituală",
   6,
   "2026-03-01",
   ["De-a lungul veacurilor, creștinii ortodocși au știut că rugăciunea vindecă. Dar abia în ultimele decenii, medicina modernă a început să cerceteze serios această legătură dintre credință și sănătate, descoperind rezultate surprinzătoare.",
    "Studii realizate la Universitatea Harvard și la Duke University au arătat că persoanele care se roagă regulat au un sistem imunitar mai puternic, se recuperează mai rapid după operații și trăiesc, în medie, cu 7-14 ani mai mult decât cei care nu practică nicio formă de spiritualitate.",
    "Din perspectiva ortodoxă, rugăciunea nu este o tehnica psihologică, ci o întâlnire reală cu Dumnezeu, Izvorul vieții și al sănătății. Sfântul Ioan Gură de Aur spunea: rugăciunea este rădăcina, izvorul și mama tuturor bunătăților.",
    "Sfântul Luca al Crimeei, el însuși chirurg de renume, mărturisea că în operațiile dificile simțea o forță care îi ghida mâna dincolo de cunoștințele sale medicale. El nu vedea nicio contradicție între știință și credință — dimpotrivă, le considera complementare.",
    "Practica rugăciunii zilnice — chiar și câteva minute dimineața și seara — creează o stabilitate emoțională care se reflectă direct în sănătatea fizică. Cortizolul scade, tensiunea arterială se normalizează, somnul se îmbunătățește.",
    "Concluzia este simplă: rugăciunea face bine. Nu ca magie, nu ca auto-sugestie, ci ca o relație vie cu Cel care ne-a creat și care dorește vindecarea noastră — trupească și sufletească. Rugați-vă cu credință și lăsați-L pe Dumnezeu să lucreze."]),

  ("01KRTQ00000000000000000A02",
   "cum-sa-te-rogi-pentru-un-bolnav",
   "Cum să te rogi pentru un om bolnav — ghid practic ortodox",
   "Când cineva drag este bolnav, nu știm uneori cum să ne rugăm și ce să cerem de la Dumnezeu. Acest ghid practic ortodox îți arată cum să faci rugăciunea de mijlocire mai eficientă și mai plină de credință.",
   "Ghid spiritual",
   5,
   "2026-03-15",
   ["Unul dintre cele mai dureroase momente din viață este atunci când un om drag zace bolnav și nu putem face nimic. Medicina are limitele ei. Dar rugăciunea nu are limite — ea ajunge acolo unde medicii nu pot.",
    "Prima regulă a rugăciunii de mijlocire este: roagă-te cu credință, nu cu îndoială. Nu înseamnă că trebuie să fii sigur de rezultat — înseamnă să crezi că Dumnezeu te aude și că Îi pasă. Sfântul Iacov spune limpede: rugăciunea cu credință va vindeca pe cel bolnav.",
    "A doua regulă: roagă-te regulat, nu doar o dată. Rugăciunea de mijlocire este un act de perseverență. Hristos însuși a spus pilda cu văduvă stăruitoare pentru a ne arăta că Dumnezeu răspunde la rugăciunile insistente.",
    "A treia regulă: combină rugăciunea cu postul. Tradiția ortodoxă leagă strâns postul de rugăciune mai ales atunci când cerem ceva important. Chiar și un post parțial — renunțarea la ceva anume — însoțind rugăciunea sporește puterea ei.",
    "A patra regulă: lasă rezultatul lui Dumnezeu. Aceasta este cea mai grea parte. Rugăciunea adevărată nu dictează lui Dumnezeu ce să facă — Îi prezintă nevoile și se încrede în înțelepciunea Sa. Uneori Dumnezeu vindecă imediat; alteori îngăduie suferința ca pe o cale spre sfințenie.",
    "Rugați Sfântul Pantelimon, Sfântul Nectarie și Sfânta Parascheva să mijlocească pentru bolnavul vostru drag. Lor le-a dat Dumnezeu un dar special al tămăduirii, iar rugăciunile lor ajung direct la Tronul Celui Atotputernic."]),

  ("01KRTQ00000000000000000A03",
   "psalmii-in-viata-crestinului-ortodox",
   "Psalmii în viața creștinului ortodox — comoara uitată a rugăciunii",
   "Cele 150 de psalmi ale lui David sunt cea mai veche și mai bogată colecție de rugăciuni din istoria omenirii. Descoperă cum să introduci psalmii în rugăciunea ta zilnică și ce beneficii aduc sufletului tău.",
   "Spiritualitate",
   7,
   "2026-03-28",
   ["Cartea Psalmilor este inima Bibliei. Timp de trei mii de ani, evreii și creștinii au cântat și au rostit aceste texte în rugăciunile lor de zi și de noapte, în bucurie și în suferință, la naștere și la moarte.",
    "Psalmii exprimă tot spectrul emoțiilor omenești: bucurie, tristețe, frică, nădejde, mânie, recunoștință, disperare și exultare. Nu există stare sufletească pe care un psalm să n-o fi exprimat deja, cu cuvinte mai bune decât am putea găsi noi.",
    "Sfântul Atanasie cel Mare scria: psalmii sunt o oglindă a sufletului. Cel care îi citește cu atenție se vede pe sine, cunoaște mișcările inimii sale și află cuvintele potrivite pentru orice stare.",
    "În tradiția ortodoxă, Psaltirea se citea integral în fiecare săptămână în mănăstiri și în fiecare două săptămâni de creștinii mai râvnitori. Astăzi, putem începe mai simplu: câte un psalm pe zi, dimineața sau seara.",
    "Psalmul 50 este psalmul pocăinței — ideal pentru dimineață, ca o curățire a sufletului. Psalmul 90 este psalmul apărării — recomandat seara, pentru paza nopții. Psalmul 22 este psalmul nădejdii — de citit în orice moment de frică sau îndoială.",
    "Nu citiți psalmii în grabă, ca pe o obligație. Citiți-i încet, savurând fiecare cuvânt, oprindu-vă la versetele care vă ating inima. Rugăciunea psalmilor nu este performanță — este conversație vie cu Dumnezeu."]),

  ("01KRTQ00000000000000000A04",
   "sfantul-pantelimon-viata-si-minuni",
   "Sfântul Pantelimon — viața, minunile și cum să-i cerem ajutorul",
   "Sfântul Mare Mucenic și Tămăduitor Pantelimon este cel mai iubit sfânt al bolnavilor în lumea ortodoxă. Descoperă viața sa fascinantă, minunile atribuite mijlocirii sale și cum să te rogi lui cu credință.",
   "Sfinți",
   8,
   "2026-04-10",
   ["Sfântul Pantelimon trăiește în inimile a milioane de creștini ortodocși din întreaga lume ca cel mai mare tămăduitor dintre sfinți. Prăznuit pe 27 iulie, el este invocat zilnic de bolnavi, de medici și de familiile celor suferinzi.",
    "Povestea vieții sale este una dintre cele mai fascinante din hagiografia creștină. Fiu al unui senator păgân din Nicomidia, Pantelimon a primit o educație aleasă și a studiat medicina sub îndrumarea unui medic de curte. Era destinat unei cariere strălucite.",
    "Convertirea sa la creștinism a venit printr-o întâlnire providențială cu preotul Ermolae, care l-a catehizat în credința creștină. Semnul care i-a pecetluit credința a fost vindecarea miraculoasă a unui copil orbit de o viperă — vindecare pe care Pantelimon a săvârșit-o invocând numele lui Hristos.",
    "De atunci, viitorul sfânt a început să trateze bolnavii fără plată, mai ales pe cei săraci pe care doctorii plătiți nu-i îngrijeau. Faima sa a crescut rapid, atrăgând invidia altor medici care l-au denunțat autorităților ca creștin.",
    "Chinuit cu cruzime — ars cu torțe aprinse, aruncat în mare cu o piatră de gât, expus la fiare sălbatice — sfântul a ieșit nevătămat din toate, convertind mulți martori la credința creștină. A fost în cele din urmă decapitat, iar din trupul său a curs lapte în loc de sânge.",
    "Moaștele sale se află astăzi la Mănăstirea Sfântul Pantelimon din Muntele Athos, Grecia, unde pelerini din toată lumea vin să se roage. Rugăciunea lui este invocată mai ales pentru boli grave, operații și vindecări pe care medicina le consideră imposibile."]),

  ("01KRTQ00000000000000000A05",
   "rugaciunea-de-dimineata-cum-si-de-ce",
   "Rugăciunea de dimineață — cum și de ce să începi ziua cu Dumnezeu",
   "Dimineața dă tonul întregii zile. Descoperă de ce rugăciunea de dimineață este cea mai importantă rugăciune a zilei, cum să o faci corect și ce schimbări vei observa în viața ta după 30 de zile de practică.",
   "Viață duhovnicească",
   5,
   "2026-04-22",
   ["Există o lege simplă a vieții duhovnicești: cum îți începi ziua, așa o trăiești. Dacă prima ta acțiune dimineața este să verifici telefonul, ziua va fi dominată de zgomotul lumii. Dacă prima ta acțiune este rugăciunea, ziua va fi ancorată în Dumnezeu.",
    "Sfinții Părinți au acordat o importanță deosebită rugăciunii de dimineață. Sfântul Ioan Gură de Aur spunea că cel care nu se roagă dimineața lasă casa fără strajă — orice duh rău poate intra. Rugăciunea de dimineață sfințește ziua și o pune sub protecția lui Dumnezeu.",
    "Cum se face rugăciunea de dimineață în tradiția ortodoxă? Tradiționalmente, ea include: Rugăciunea Sfântului Macarie, Rugăciunea Sfântului Vasile cel Mare, câțiva psalmi și Crezul. Dar pentru un începător, e suficient să înceapă cu Tatăl Nostru și câteva cuvinte din inimă.",
    "Locul rugăciunii contează. Amenajați un colț de rugăciune în casă — cu o icoană și o candelă sau lumânare. Acest spațiu sfânt va deveni un reper vizual care vă cheamă la rugăciune și creează o atmosferă potrivită.",
    "Durata rugăciunii de dimineață pentru un laic poate fi de 5-15 minute. Nu cantitatea contează, ci calitatea și regularitatea. Mai bine 5 minute zilnic decât o oră o dată pe săptămână.",
    "Provocare practică: timp de 30 de zile, rugați-vă dimineața înainte de a verifica telefonul sau de a face orice altceva. La final, evaluați ce s-a schimbat în starea voastră sufletească, în relațiile cu ceilalți și în modul în care faceți față greutăților zilei."]),

  ("01KRTQ00000000000000000A06",
   "credinta-si-medicina-complement-nu-conflict",
   "Credință și medicină — complement, nu conflict",
   "Un subiect delicat dar important: relația dintre rugăciune și tratamentul medical. Ce spune Biserica Ortodoxă? Trebuie să alegem între medic și rugăciune? Răspunsul surprinzător al tradiției creștine.",
   "Sănătate și credință",
   6,
   "2026-05-01",
   ["Unii creștini cred că a apela la medic înseamnă lipsă de credință. Alții cred că rugăciunea este o practică superstițioasă incompatibilă cu medicina modernă. Ambele extreme sunt greșite și dăunătoare.",
    "Biserica Ortodoxă a avut dintotdeauna o atitudine echilibrată față de medicină. Sfântul Luca Evanghelistul era el însuși medic. Sfântul Luca al Crimeei era chirurg. Sfântul Cosma și Sfântul Damian practicau medicina. Medicina este văzută ca un dar al lui Dumnezeu pentru binele omului.",
    "Sfântul Vasile cel Mare, întemeietorul primului spital din istoria omenirii, scria: nu este lipsă de credință să cauți ajutorul artei medicale. Medicina este un dar dumnezeiesc, dar nu îl uita pe Dătătorul darurilor.",
    "Atitudinea corectă este să folosim ambele: medicina pentru vindecare trupească și rugăciunea pentru harul lui Dumnezeu care sfințește și potențează tratamentul. Nu sunt alternative — sunt complementare.",
    "Practic: mergi la medic, urmează tratamentul prescris, ia medicamentele, fă investigațiile recomandate. Și în același timp: roagă-te, cere ungerea cu Sfântul Maslu, invocă sfinții tămăduitori, participă la Sfânta Liturghie.",
    "Există mărturii documentate de vindecări care depășesc explicațiile medicale — minuni săvârșite prin mijlocirea sfinților. Dar aceste minuni nu neagă medicina; ele o completează acolo unde medicina ajunge la limitele ei. Dumnezeu lucrează și prin medici, și dincolo de medici."]),
]

rows = []
for a in articles:
    id_, slug, title, excerpt, category, rt, date, texts = a
    ts = f"{date} 10:00:00+00"
    content_json = pt(texts)

    def sql_str(v):
        return v.replace("'", "''")

    row = (
        f"('{id_}', '{slug}',\n"
        f" 'published', 'ro',\n"
        f" '{sql_str(title)}',\n"
        f" '{sql_str(excerpt)}',\n"
        f" '{sql_str(category)}',\n"
        f" '{sql_str(content_json)}',\n"
        f" {rt},\n"
        f" '{ts}', '{ts}', '{ts}',\n"
        f" '')"
    )
    rows.append(row)

output = "-- Seed 6 articole — generat cu gen_articole.py\n"
output += "BEGIN;\n\n"
output += (
    "INSERT INTO ec_articole "
    "(id, slug, status, locale, title, excerpt, category, content, reading_time, published_at, created_at, updated_at, og_image)\n"
    "VALUES\n"
)
output += ",\n\n".join(rows)
output += ";\n\nCOMMIT;\n"

with open("scripts/seed-articole.sql", "w", encoding="utf-8") as f:
    f.write(output)

print(f"OK — {len(articles)} articole, {len(output)} bytes")
