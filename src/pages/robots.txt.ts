import type { APIRoute } from "astro";

export const GET: APIRoute = () => {
  return new Response(
    `User-agent: *
Allow: /

Disallow: /_emdash/
Disallow: /api/

Sitemap: https://rugaciunisanatate.ro/sitemap.xml
`,
    {
      status: 200,
      headers: {
        "Content-Type": "text/plain; charset=utf-8",
        "Cache-Control": "public, max-age=86400",
      },
    }
  );
};
