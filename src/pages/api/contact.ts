import type { APIRoute } from "astro";
import { Resend } from "resend";

// Simple in-memory rate limiter: max 3 requests per IP per 10 minutes
const rateLimitMap = new Map<string, { count: number; resetAt: number }>();

function checkRateLimit(ip: string): boolean {
  const now = Date.now();
  const windowMs = 10 * 60 * 1000; // 10 minutes
  const maxRequests = 3;

  const entry = rateLimitMap.get(ip);
  if (!entry || now > entry.resetAt) {
    rateLimitMap.set(ip, { count: 1, resetAt: now + windowMs });
    return true;
  }
  if (entry.count >= maxRequests) return false;
  entry.count++;
  return true;
}

// Clean up old entries periodically
setInterval(() => {
  const now = Date.now();
  for (const [ip, entry] of rateLimitMap.entries()) {
    if (now > entry.resetAt) rateLimitMap.delete(ip);
  }
}, 5 * 60 * 1000);

export const POST: APIRoute = async ({ request }) => {
  const json = (data: object, status = 200) =>
    new Response(JSON.stringify(data), {
      status,
      headers: { "Content-Type": "application/json" },
    });

  // Rate limit by IP
  const ip =
    request.headers.get("x-forwarded-for")?.split(",")[0]?.trim() ??
    request.headers.get("x-real-ip") ??
    "unknown";

  if (!checkRateLimit(ip)) {
    return json({ error: "Prea multe cereri. Încercați din nou în 10 minute." }, 429);
  }

  // Parse form data
  let formData: FormData;
  try {
    formData = await request.formData();
  } catch {
    return json({ error: "Date invalide." }, 400);
  }

  const name = (formData.get("name") as string | null)?.trim() ?? "";
  const email = (formData.get("email") as string | null)?.trim() ?? "";
  const subject = (formData.get("subject") as string | null)?.trim() ?? "";
  const message = (formData.get("message") as string | null)?.trim() ?? "";
  // Honeypot field — bots fill this, humans don't see it
  const honeypot = (formData.get("website") as string | null) ?? "";

  // Spam check
  if (honeypot) {
    // Silently succeed to not tip off bots
    return json({ ok: true });
  }

  // Validation
  if (!name || name.length < 2) return json({ error: "Introduceți un nume valid." }, 422);
  if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return json({ error: "Adresă de email invalidă." }, 422);
  if (!subject) return json({ error: "Alegeți un subiect." }, 422);
  if (!message || message.length < 10) return json({ error: "Mesajul este prea scurt." }, 422);
  if (message.length > 5000) return json({ error: "Mesajul depășește 5000 de caractere." }, 422);

  const apiKey = import.meta.env.RESEND_API_KEY;
  if (!apiKey) {
    console.error("RESEND_API_KEY not set");
    return json({ error: "Serviciul de email nu este configurat momentan." }, 503);
  }

  const subjectLabels: Record<string, string> = {
    sugestie: "Sugestie rugăciune",
    corectie: "Corecție / eroare",
    colaborare: "Colaborare",
    altele: "Altele",
  };
  const subjectLabel = subjectLabels[subject] ?? subject;

  const resend = new Resend(apiKey);

  try {
    const { error } = await resend.emails.send({
      from: "Rugăciuni Sănătate <noreply@rugaciunisanatate.ro>",
      to: ["contact@rugaciunisanatate.ro"],
      replyTo: email,
      subject: `[Contact] ${subjectLabel} — ${name}`,
      html: `
        <div style="font-family:Georgia,serif;max-width:600px;margin:0 auto;color:#2c1810">
          <div style="background:#2c1810;padding:24px;text-align:center">
            <span style="color:#c4973a;font-size:1.4rem">✦ Rugăciuni Sănătate ✦</span>
          </div>
          <div style="padding:32px;background:#fffdf8;border:1px solid #e8d5a3">
            <h2 style="color:#2c1810;margin-top:0">Mesaj nou din formularul de contact</h2>
            <table style="width:100%;border-collapse:collapse;margin-bottom:24px">
              <tr>
                <td style="padding:8px 0;color:#8b7355;width:100px"><strong>Nume:</strong></td>
                <td style="padding:8px 0">${escapeHtml(name)}</td>
              </tr>
              <tr>
                <td style="padding:8px 0;color:#8b7355"><strong>Email:</strong></td>
                <td style="padding:8px 0"><a href="mailto:${escapeHtml(email)}">${escapeHtml(email)}</a></td>
              </tr>
              <tr>
                <td style="padding:8px 0;color:#8b7355"><strong>Subiect:</strong></td>
                <td style="padding:8px 0">${escapeHtml(subjectLabel)}</td>
              </tr>
            </table>
            <div style="background:#f5f0e8;padding:20px;border-left:3px solid #c4973a;border-radius:4px">
              <strong style="color:#8b7355;display:block;margin-bottom:8px">Mesaj:</strong>
              <p style="margin:0;line-height:1.8;white-space:pre-wrap">${escapeHtml(message)}</p>
            </div>
            <hr style="border:none;border-top:1px solid #e8d5a3;margin:24px 0" />
            <p style="color:#8b7355;font-size:0.85rem;margin:0">
              Trimis de pe rugaciunisanatate.ro · IP: ${escapeHtml(ip)}
            </p>
          </div>
        </div>
      `,
      text: `Mesaj nou din formularul de contact\n\nNume: ${name}\nEmail: ${email}\nSubiect: ${subjectLabel}\n\nMesaj:\n${message}\n\n---\nIP: ${ip}`,
    });

    if (error) {
      console.error("Resend error:", error);
      return json({ error: "Eroare la trimiterea emailului. Încercați din nou." }, 500);
    }

    return json({ ok: true });
  } catch (err) {
    console.error("Contact form error:", err);
    return json({ error: "Eroare internă. Încercați din nou." }, 500);
  }
};

function escapeHtml(str: string): string {
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#x27;");
}
