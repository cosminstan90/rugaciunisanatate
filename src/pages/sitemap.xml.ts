import type { APIRoute } from "astro";
import { getEmDashCollection } from "emdash";

const SITE = "https://rugaciunisanatate.ro";

const STATIC_PAGES = [
  { url: "/", priority: "1.0", changefreq: "daily" },
  { url: "/rugaciuni", priority: "0.9", changefreq: "daily" },
  { url: "/rugaciuni/vindecare", priority: "0.85", changefreq: "weekly" },
  { url: "/rugaciuni/dimineata", priority: "0.85", changefreq: "weekly" },
  { url: "/rugaciuni/seara", priority: "0.85", changefreq: "weekly" },
  { url: "/rugaciuni/psalmi", priority: "0.8", changefreq: "weekly" },
  { url: "/rugaciuni/familie", priority: "0.8", changefreq: "weekly" },
  { url: "/rugaciuni/ocazii", priority: "0.75", changefreq: "weekly" },
  { url: "/sfinti", priority: "0.8", changefreq: "weekly" },
  { url: "/articole", priority: "0.8", changefreq: "daily" },
  { url: "/calendar", priority: "0.7", changefreq: "daily" },
  { url: "/despre", priority: "0.4", changefreq: "monthly" },
  { url: "/contact", priority: "0.3", changefreq: "monthly" },
];

function urlEntry(loc: string, lastmod?: string, changefreq = "weekly", priority = "0.6") {
  return `  <url>
    <loc>${SITE}${loc}</loc>
    ${lastmod ? `<lastmod>${lastmod}</lastmod>` : ""}
    <changefreq>${changefreq}</changefreq>
    <priority>${priority}</priority>
  </url>`;
}

export const GET: APIRoute = async () => {
  const [{ entries: rugaciuni }, { entries: sfinti }, { entries: articole }] =
    await Promise.all([
      getEmDashCollection("rugaciuni", { where: { status: "published" }, limit: 5000 }),
      getEmDashCollection("sfinti", { where: { status: "published" }, limit: 1000 }),
      getEmDashCollection("articole", { where: { status: "published" }, limit: 5000 }),
    ]);

  const staticUrls = STATIC_PAGES.map((p) => urlEntry(p.url, undefined, p.changefreq, p.priority));

  const rugaciuniUrls = rugaciuni.map((r) => {
    const lastmod = r.data.updated_at
      ? new Date(r.data.updated_at).toISOString().split("T")[0]
      : undefined;
    return urlEntry(`/${r.data.slug}`, lastmod, "monthly", "0.8");
  });

  const sfintiUrls = sfinti.map((s) => {
    const lastmod = s.data.updated_at
      ? new Date(s.data.updated_at).toISOString().split("T")[0]
      : undefined;
    return urlEntry(`/sfinti/${s.data.slug}`, lastmod, "monthly", "0.7");
  });

  const articoleUrls = articole.map((a) => {
    const lastmod = a.data.updated_at
      ? new Date(a.data.updated_at).toISOString().split("T")[0]
      : undefined;
    return urlEntry(`/articole/${a.data.slug}`, lastmod, "weekly", "0.7");
  });

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${[...staticUrls, ...rugaciuniUrls, ...sfintiUrls, ...articoleUrls].join("\n")}
</urlset>`;

  return new Response(xml, {
    headers: {
      "Content-Type": "application/xml; charset=utf-8",
      "Cache-Control": "public, max-age=3600",
    },
  });
};
