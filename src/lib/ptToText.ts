export function ptToText(blocks: unknown): string {
  if (!Array.isArray(blocks)) return typeof blocks === "string" ? blocks : "";
  return blocks
    .map((b: any) => (b?.children ?? []).map((c: any) => c.text ?? "").join(""))
    .join(" ")
    .trim();
}
