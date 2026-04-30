import { defineMiddleware } from "astro:middleware";
import { getEmDashCollection } from "emdash";

// Cache redirects in memory — refreshed every 5 minutes
let redirectCache: Map<string, string> = new Map();
let cacheLoadedAt = 0;
const CACHE_TTL = 5 * 60 * 1000;

async function loadRedirects() {
  const now = Date.now();
  if (redirectCache.size > 0 && now - cacheLoadedAt < CACHE_TTL) return;
  try {
    const { entries } = await getEmDashCollection("redirecturi", {
      where: { activ: true },
    });
    const map = new Map<string, string>();
    for (const r of entries) {
      const from = (r.data.from as string).replace(/\/$/, "").toLowerCase();
      map.set(from, r.data.to as string);
    }
    redirectCache = map;
    cacheLoadedAt = now;
  } catch {
    // Collection doesn't exist yet — skip silently
  }
}

export const onRequest = defineMiddleware(async (context, next) => {
  const pathname = context.url.pathname.replace(/\/$/, "").toLowerCase();

  // Only check redirects for non-asset, non-admin paths
  if (
    !pathname.startsWith("/_emdash") &&
    !pathname.startsWith("/api") &&
    !pathname.match(/\.(js|css|png|jpg|svg|ico|webp|woff2?)$/)
  ) {
    await loadRedirects();
    const target = redirectCache.get(pathname);
    if (target) {
      return context.redirect(target, 301);
    }
  }

  return next();
});
