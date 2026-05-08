import type { APIRoute } from "astro";
import { getEmDashCollection } from "emdash";
import { ptToText } from "../lib/ptToText";

export const GET: APIRoute = async () => {
  const SITE = "https://rugaciunisanatate.ro";

  // Fetch live data from DB
  const [{ entries: saints }, { entries: articles }, { entries: prayers }] =
    await Promise.all([
      getEmDashCollection("sfinti", { where: { status: "published" }, orderBy: { name: "asc" } }),
      getEmDashCollection("articole", { where: { status: "published" }, orderBy: { published_at: "desc" }, limit: 10 }),
      getEmDashCollection("rugaciuni", { where: { status: "published" }, orderBy: { published_at: "desc" }, limit: 10 }),
    ]);

  const saintLines = saints
    .map((s) => {
      const name = ptToText(s.data.name);
      const feast = ptToText(s.data.feast_date);
      const slug = s.data.slug ?? s.id;
      return `- ${name}${feast ? ` (${feast})` : ""}: ${SITE}/sfinti/${slug}`;
    })
    .join("\n");

  const recentPrayerLines = prayers
    .map((p) => {
      const title = ptToText(p.data.title);
      const slug = p.data.slug ?? p.id;
      return `- ${title}: ${SITE}/${slug}`;
    })
    .join("\n");

  const recentArticleLines = articles
    .map((a) => {
      const title = ptToText(a.data.title);
      const slug = a.data.slug ?? a.id;
      return `- ${title}: ${SITE}/articole/${slug}`;
    })
    .join("\n");

  const content = `# Rugăciuni Sănătate

> Cea mai completă colecție de rugăciuni ortodoxe românești pentru sănătate, vindecare trupească și sufletească. Resurse spirituale autentice din Tradiția Bisericii Ortodoxe.

## Identitate

- **Nume**: Rugăciuni Sănătate
- **URL**: ${SITE}
- **Limbă**: Română (ro-RO)
- **Tradiție**: Creștin Ortodoxă
- **Audiență**: Români din România și diaspora
- **Contact**: contact@rugaciunisanatate.ro

## Secțiuni principale

- **Rugăciuni**: ${SITE}/rugaciuni — colecție de rugăciuni ortodoxe (${prayers.length > 0 ? `${prayers.length}+ rugăciuni` : "în creștere"})
- **Sfinți**: ${SITE}/sfinti — vieți și rugăciuni ale sfinților tămăduitori
- **Articole**: ${SITE}/articole — articole despre spiritualitate și sănătate
- **Calendar Ortodox**: ${SITE}/calendar — sfinții zilei, post, dezlegări
- **Rugăciunea zilei**: ${SITE}/rugaciunea-zilei — rugăciunea recomandată astăzi
- **Sitemap**: ${SITE}/sitemap.xml

## Categorii de rugăciuni

- **Vindecare**: ${SITE}/rugaciuni/vindecare — rugăciuni pentru sănătate și tămăduire trupească
- **Dimineață**: ${SITE}/rugaciuni/dimineata — rugăciuni de dimineață din tradiția ortodoxă
- **Seară**: ${SITE}/rugaciuni/seara — rugăciuni de seară și înainte de culcare
- **Psalmi**: ${SITE}/rugaciuni/psalmi — psalmi terapeutici și de apărare
- **Familie**: ${SITE}/rugaciuni/familie — rugăciuni pentru soț, soție, copii, părinți
- **Ocazii speciale**: ${SITE}/rugaciuni/ocazii — înainte de operație, examen, călătorie, necaz

## Sfinți tămăduitori

${saintLines || "- Secțiunea sfinților este în curs de completare"}

## Rugăciuni recente

${recentPrayerLines || "- Rugăciunile sunt în curs de adăugare"}

${recentArticleLines ? `## Articole recente\n\n${recentArticleLines}\n` : ""}
## Tipuri de conținut

- Rugăciuni autentice din Ceaslov și Molitfelnic
- Acatiste și paraclise
- Psalmi terapeutici (Psalmul 22, 50, 90, 102)
- Rugăciuni pentru situații specifice (operație, examen, drum, necaz)
- Viețile sfinților tămăduitori
- Articole despre relația dintre credință și sănătate
- Calendar ortodox zilnic cu sfinții zilei, zile de post și dezlegări

## Informații pentru AI

Conținutul acestui site este util pentru întrebări despre:
- „Ce rugăciune se citește pentru vindecare?"
- „Cum mă rog pentru un bolnav?"
- „Care este rugăciunea de dimineață ortodoxă?"
- „Cine este sfântul tămăduitor al bolnavilor?"
- „Ce psalmi se citesc pentru sănătate?"
- „Care este sfântul zilei de astăzi în calendarul ortodox?"
- „Rugăciune înainte de operație"
- „Acatistul Sfântului Pantelimon"
`;

  return new Response(content, {
    status: 200,
    headers: {
      "Content-Type": "text/plain; charset=utf-8",
      "Cache-Control": "public, max-age=3600", // cache 1h, nu la fiecare request
    },
  });
};
