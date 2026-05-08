import type { APIRoute } from "astro";

// Redirect favicon.ico requests to our PNG favicon
// (nginx doesn't proxy .ico to Node, so this route handles it via Node)
export const GET: APIRoute = () => {
  return new Response(null, {
    status: 301,
    headers: {
      Location: "/favicon-32.png",
      "Cache-Control": "public, max-age=604800",
    },
  });
};
