// 조회수 세기 (화면에는 숫자를 보여 주지 않음). 전기 상식 목록의 '많이 찾는 글' 순위에만 씀.
import { getStore } from "@netlify/blobs";

const OK = /^(guide|case)-[a-z0-9-]{3,80}$/;

export default async (req) => {
  const store = getStore("views");
  const counts = (await store.get("counts", { type: "json" })) || {};
  if (req.method === "POST") {
    let p = "";
    try { p = String((await req.json()).p || ""); } catch (e) {}
    const ua = req.headers.get("user-agent") || "";
    if (!OK.test(p) || /bot|crawl|spider|slurp|yeti/i.test(ua)) return new Response(null, { status: 204 });
    counts[p] = (counts[p] || 0) + 1;
    await store.setJSON("counts", counts);
    return new Response(null, { status: 204 });
  }
  const kind = new URL(req.url).searchParams.get("kind");
  const out = {};
  for (const [k, v] of Object.entries(counts)) if (!kind || k.startsWith(kind + "-")) out[k] = v;
  return Response.json(out, { headers: { "Cache-Control": "public, max-age=300" } });
};

export const config = { path: "/api/views" };
