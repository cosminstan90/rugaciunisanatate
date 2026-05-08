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

# (id, slug, name, saint_type, icon, subtitle, feast_date, life_dates, patron_of, description_paragraphs)
saints = [
  ("01KRTQ00000000000000000S01",
   "sfantul-pantelimon",
   "Sfântul Mare Mucenic și Tămăduitor Pantelimon",
   "Mare Mucenic",
   "✝️",
   "Doctorul fără de arginți, ocrotitorul bolnavilor",
   "27 iulie",
   "circa 275–305 d.Hr.",
   "Medici, bolnavi, spitale",
   ["Sfântul Pantelimon s-a născut în orașul Nicomidia, în vremea împăratului Maximian. Fiul unui om bogat, Eustorgiu, a primit o educație aleasă și a urmat medicina, devenind unul dintre cei mai iscusiți doctori ai vremii sale.",
    "Convertit la creștinism de preotul Ermolae, Pantelimon a început să vindece bolnavii nu numai cu mijloace omenești, ci și prin rugăciune și invocarea numelui lui Hristos. El tămăduia gratuit pe cei săraci și neputincioși, de unde i-a venit și numele de Doctor fără de arginți.",
    "Denunțat ca creștin, a fost supus la chinuri groaznice și, în cele din urmă, decapitat în 27 iulie 305. Trupul său a rămas intact, iar sângele care a curs s-a transformat în lapte, semn al sfințeniei sale. Moaștele sale sunt venerate la Mănăstirea Sfântul Pantelimon din Muntele Athos.",
    "Sfântul Pantelimon este unul dintre cei mai iubiți sfinți tămăduitori ai lumii ortodoxe. Milioane de credincioși aleargă la el cu rugăciuni pentru vindecarea bolilor trupești și sufletești."]),

  ("01KRTQ00000000000000000S02",
   "sfantul-nectarie",
   "Sfântul Ierarh Nectarie din Eghina",
   "Ierarh",
   "✝️",
   "Taumaturghul veacului nostru, vindecătorul bolnavilor de cancer",
   "9 noiembrie",
   "1846–1920 d.Hr.",
   "Bolnavi de cancer, cei suferinzi",
   ["Sfântul Nectarie s-a născut în 1846 în Silyvria, Tracia. Educat la Atena și Constantinopol, a devenit călugăr la maturitate și a ajuns Mitropolit al Pentapolei. Prigonit de invidioși și calomniat, a fost îndepărtat din scaun și a trăit în smerenie și răbdare.",
    "Stabilit în Grecia, a înființat o mănăstire de maici pe insula Eghina, unde a trăit în rugăciune, post și lucrare duhovnicească. Iubirea sa față de oameni și sfințenia vieții sale au atras mulțimi de credincioși care căutau tămăduire și mângâiere.",
    "Decedat în 1920, trupul său a fost mutat în patul unui bolnav, care s-a vindecat instantaneu la atingerea cu hainele sfântului. Canonizat în 1961, Sfântul Nectarie este venerat în toată lumea ortodoxă ca taumaturgh, adică făcător de minuni.",
    "Numeroase vindecări miraculoase, mai ales ale bolnavilor de cancer, au fost atribuite mijlocirii sale. El este socotit sfântul veacului nostru, cel mai apropiat de sufletele creștinilor contemporani."]),

  ("01KRTQ00000000000000000S03",
   "sfantul-luca-al-crimeei",
   "Sfântul Ierarh Luca al Crimeei",
   "Ierarh",
   "✝️",
   "Chirurgul și arhiepiscopul, vindecătorul prin credință și știință",
   "11 iunie",
   "1877–1961 d.Hr.",
   "Medici, chirurgi, bolnavi",
   ["Sfântul Luca — pe numele laic Valentin Felixovici Voino-Iasențchi — s-a născut în 1877 în Kerci. Medic chirurg de renume, și-a dedicat viața bolnavilor și cercetării medicale, publicând lucrări importante de chirurgie purulentă.",
    "Rămas văduv, a primit hirotonia în preot și mai apoi în episcop, continuând simultan activitatea medicală. Persecutat de regimul sovietic, a trecut prin mai multe deportări în Siberia și lagăre de muncă, fără să-și abandoneze credința sau profesia medicală.",
    "Chiar în gulag opera pe bolnavi, adesea în condiții primitive, realizând intervenții chirurgicale care par imposibile fără ajutorul divin. Eliberat după cel de-al Doilea Război Mondial, a primit titlul de Arhiepiscop al Crimeei.",
    "Canonizat în 1996, Sfântul Luca este un simbol al îmbinării credinței cu știința. El este patron al medicilor și chirurgilor și mijlocitor pentru toți bolnavii care apelează la rugăciunile sale."]),

  ("01KRTQ00000000000000000S04",
   "sfantul-mina",
   "Sfântul Mare Mucenic Mina",
   "Mare Mucenic",
   "✝️",
   "Ocrotitorul celor nedreptățiți și al celor pierduți",
   "11 noiembrie",
   "sec. III–IV d.Hr.",
   "Cei nedreptățiți, cei care caută lucruri pierdute",
   ["Sfântul Mina s-a născut în Egipt și a slujit ca soldat în armata romană. Nemaiputând asista la persecuțiile creștinilor, a mărturisit public credința sa creștină și a părăsit armata, retrăgându-se în pustie pentru rugăciune și asceză.",
    "Întors în cetatea Cotuas din Frigia în vremea unui spectacol public, Mina și-a mărturisit din nou credința în fața mulțimii. Arestat, a fost torturat cu cruzime pentru a-l face să se lepede de Hristos, dar a rămas neînduplecat.",
    "Decapitat în jurul anului 296, sfântul Mina a devenit unul dintre cei mai venerați mucenici ai Bisericii de Răsărit. Moaștele sale, aduse la Alexandria, au dat loc unor nenumărate minuni de vindecare.",
    "Tradiția îl socotește mijlocitor pentru cei nedreptățiți și pentru cei care caută lucruri pierdute sau oameni dispăruți. Rugăciunea sa este invocată și pentru vindecarea bolilor și apărarea de vrăjmași."]),

  ("01KRTQ00000000000000000S05",
   "cosma-si-damian",
   "Sfinții Doctori fără de Arginți Cosma și Damian",
   "Doctori fără de Arginți",
   "✝️",
   "Gemenii tămăduitori, ocrotitorii medicinei creștine",
   "1 noiembrie (apuseni) / 1 iulie (răsăriteni)",
   "sec. III d.Hr.",
   "Medici, farmaciști, bolnavi",
   ["Sfinții Cosma și Damian au fost frați gemeni, născuți în Arabia sau Asia Mică, în familia unei creștine evlavioase pe nume Teodota. Orfani de tată de mici, au fost crescuți în frica lui Dumnezeu și au urmat studii de medicină.",
    "Cei doi frați practicau medicina fără a cere plată, vindecând atât oameni cât și animale, și au primit de aceea titlul de Anargyri — Fără de Arginți. Minunile săvârșite de ei, inclusiv transplantul miraculos al unui picior, i-au făcut vestiți în toată lumea creștină.",
    "Martirizați în timpul persecuțiilor lui Dioclețian, cei doi frați au rămas împreună și în moarte. Venerați de Biserică ca ocrotitori ai medicinei, ei sunt chemați în ajutor de medici, farmaciști și de toți cei bolnavi.",
    "Numeroase biserici și spitale din lumea ortodoxă le poartă numele. Ei simbolizează idealul medicinei creștine: vindecarea trupului în slujba sufletului, fără urmărirea câștigului material."]),

  ("01KRTQ00000000000000000S06",
   "sfanta-parascheva",
   "Sfânta Cuvioasă Parascheva",
   "Cuvioasă",
   "✝️",
   "Ocrotitoarea Moldovei și a Munteniei, ajutătoarea bolnavilor",
   "14 octombrie",
   "sec. X–XI d.Hr.",
   "Femei, bolnavi, cei năpăstuiți",
   ["Sfânta Parascheva s-a născut în Epivata, lângă Constantinopol, într-o familie creștină evlavioasă. Îndrăgostită de viața duhovnicească de la vârstă fragedă, a renunțat la confortul lumesc și a dus o viață de asceză și rugăciune.",
    "A trăit o vreme în Constantinopol, apoi în Palestina, la locurile sfinte, și în cele din urmă s-a stabilit în pustia din apropierea Jordanului, unde a trăit în post și rugăciune continuă până la moartea sa.",
    "Moaștele sale, descoperite în mod minunat, au fost aduse la Târnovo (Bulgaria), apoi la Belgrad și, în 1641, la Iași, unde se află și astăzi în Catedrala Mitropolitană. Sfânta Parascheva este ocrotitoarea Moldovei și a întregii Românii.",
    "Milioane de credincioși vin în fiecare an la Iași pentru a se închina moaștelor sale, aducând rugăciuni pentru sănătate, dezlegare de boli și ajutor în necazuri. Ea este una dintre cele mai iubite sfinte ale poporului român."]),
]

rows = []
for s in saints:
    id_, slug, name, stype, icon, subtitle, feast_date, life_dates, patron_of, desc_texts = s
    desc_json = pt(desc_texts)
    ts = "2026-05-08 10:00:00+00"

    def sql_str(v):
        return v.replace("'", "''")

    row = (
        f"('{id_}', '{slug}',\n"
        f" 'published', 'ro',\n"
        f" '{sql_str(name)}',\n"
        f" '{sql_str(stype)}',\n"
        f" '{sql_str(icon)}',\n"
        f" '{sql_str(subtitle)}',\n"
        f" '{sql_str(feast_date)}',\n"
        f" '{sql_str(life_dates)}',\n"
        f" '{sql_str(patron_of)}',\n"
        f" '{sql_str(desc_json)}',\n"
        f" '{ts}', '{ts}', '{ts}')"
    )
    rows.append(row)

output = "-- Seed 6 sfinți — generat cu gen_sfinti.py\n"
output += "BEGIN;\n\n"
output += (
    "INSERT INTO ec_sfinti "
    "(id, slug, status, locale, name, saint_type, icon, subtitle, feast_date, life_dates, patron_of, description, created_at, updated_at, published_at)\n"
    "VALUES\n"
)
output += ",\n\n".join(rows)
output += ";\n\nCOMMIT;\n"

with open("scripts/seed-sfinti.sql", "w", encoding="utf-8") as f:
    f.write(output)

print(f"OK — {len(saints)} sfinti, {len(output)} bytes")
