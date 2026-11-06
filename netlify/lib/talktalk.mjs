// 네이버 톡톡 챗봇 API 연결 (11/6). 공식 문서: https://github.com/navertalk/chatbot-api
// - 웹훅: 톡톡이 보내는 이벤트를 받아 저장만 한다. 자동 답장은 하지 않는다.
// - 받은함: AI 직원이 새 메시지를 읽고, 답장 초안을 저장한다.
// - 보내기: 사장님이 확인한 초안만 보낸다(초안 id 필요, 한 번만).
// 손님 톡톡 user 값은 서버 저장소 안에만 두고, 밖으로는 임의 대화 번호(thread)만 내보낸다.
// 비밀 값은 모두 Netlify 환경 변수에서만 읽는다:
//   TALKTALK_WEBHOOK_KEY  웹훅 주소 ?k= 에 붙이는 비밀 값
//   TALKTALK_AUTH_TOKEN   톡톡 파트너센터 > 개발자도구 > API 설정 > 보내기 API 에서 만든 Authorization 값
//   SMILE_INBOX_KEY       받은함 읽기·읽음 표시·초안 저장용 (헤더 x-smile-key)
//   SMILE_SEND_KEY        보내기용 (헤더 x-smile-key). 받은함 키와 다른 값

import { createHash, randomBytes, timingSafeEqual } from "node:crypto";

export const SEND_URL = "https://gw.talk.naver.com/chatbot/v1/event";
const MAX_TEXT = 1000; // 문서 한도는 10,000자. 답장은 짧게 쓰도록 1,000자로 막음

export function keyOk(given, expected) {
  if (!expected || !given) return false;
  const a = Buffer.from(String(given));
  const b = Buffer.from(String(expected));
  return a.length === b.length && timingSafeEqual(a, b);
}

const hashUser = (user) => createHash("sha256").update("talktalk:" + user).digest("hex");
const newId = () => Date.now().toString(36).padStart(9, "0") + "-" + randomBytes(4).toString("hex");
const nowIso = () => new Date().toISOString();

// 손님 user 값 → 임의 대화 번호. 같은 손님은 늘 같은 번호.
async function threadFor(store, user) {
  const uk = "users/" + hashUser(user);
  const found = await store.get(uk, { type: "json" });
  if (found && found.thread) return found.thread;
  const thread = "t-" + randomBytes(6).toString("hex");
  await store.setJSON(uk, { thread });
  await store.setJSON("threads/" + thread, { user, createdAt: nowIso() });
  return thread;
}

// 이벤트에서 화면에 보여 줄 내용만 뽑음 (user 값은 넣지 않음)
function pickContent(ev) {
  const out = {};
  if (ev.textContent) {
    out.text = String(ev.textContent.text || "");
    if (ev.textContent.inputType) out.inputType = ev.textContent.inputType;
  }
  if (ev.imageContent && ev.imageContent.imageUrl) out.imageUrl = String(ev.imageContent.imageUrl);
  if (ev.compositeContent) out.composite = true;
  return out;
}

// ── 1. 웹훅 ─────────────────────────────────────────────
export async function handleWebhook(req, { store, env }) {
  const url = new URL(req.url);
  if (!keyOk(url.searchParams.get("k"), env.TALKTALK_WEBHOOK_KEY)) return new Response(null, { status: 404 });
  if (req.method !== "POST") return new Response(null, { status: 200 });

  let ev = null;
  try { ev = await req.json(); } catch (e) { ev = null; }
  try {
    if (ev && typeof ev.user === "string" && ev.user) {
      const kind = ev.event;
      // send = 손님이 보낸 메시지, echo = 상담원(사장님)·챗봇이 보낸 메시지 기록
      if (kind === "send" || kind === "echo") {
        const thread = await threadFor(store, ev.user);
        const id = newId();
        const msg = {
          id, thread, at: nowIso(),
          from: kind === "send" ? "customer" : "partner",
          ...pickContent(ev),
        };
        if (kind === "send" && ev.standby === true) msg.standby = true; // 핸드오버 사용 시: 상담원이 대화를 맡고 있음
        if (kind === "echo" && ev.echoedEvent) msg.echoedEvent = String(ev.echoedEvent);
        await store.setJSON("msg/" + id, msg);
        if (kind === "send") await store.setJSON("new/" + id, { at: msg.at });
      } else if (kind === "open" || kind === "leave" || kind === "friend") {
        const thread = await threadFor(store, ev.user);
        const id = newId();
        const msg = { id, thread, at: nowIso(), from: "system", event: kind };
        if (kind === "open" && ev.options && ev.options.inflow) msg.inflow = String(ev.options.inflow);
        if (kind === "friend" && ev.options && ev.options.set) msg.set = String(ev.options.set);
        await store.setJSON("msg/" + id, msg);
      }
    }
  } catch (e) {
    console.log("talktalk-webhook 저장 실패:", e && e.name); // 손님 내용·user 값은 로그에 남기지 않음
  }
  // 항상 200, 본문 없음 = 자동 답장 없음 (문서: 200 이 아니면 실패로 기록, 읽기 제한 5초)
  return new Response(null, { status: 200 });
}

// ── 2. 받은함 ───────────────────────────────────────────
// GET  /api/talktalk/inbox            → 아직 안 읽은 손님 메시지
// GET  /api/talktalk/inbox?thread=t-… → 그 대화의 지난 메시지 전부(초안 포함)
// POST /api/talktalk/inbox {read:[id…]}                → 읽음 표시
// POST /api/talktalk/inbox {draft:{thread, text}}      → 답장 초안 저장(보내지 않음) → draftId
export async function handleInbox(req, { store, env }) {
  if (!keyOk(req.headers.get("x-smile-key"), env.SMILE_INBOX_KEY)) return new Response(null, { status: 404 });
  const url = new URL(req.url);

  if (req.method === "GET") {
    const thread = url.searchParams.get("thread");
    if (thread) {
      if (!/^t-[0-9a-f]{12}$/.test(thread)) return Response.json({ error: "thread" }, { status: 400 });
      const { blobs } = await store.list({ prefix: "msg/" });
      const all = [];
      for (const b of blobs) {
        const m = await store.get(b.key, { type: "json" });
        if (m && m.thread === thread) all.push(m);
      }
      const { blobs: dblobs } = await store.list({ prefix: "draft/" });
      const drafts = [];
      for (const b of dblobs) {
        const d = await store.get(b.key, { type: "json" });
        if (d && d.thread === thread) drafts.push(d);
      }
      all.sort((a, b) => a.id.localeCompare(b.id));
      drafts.sort((a, b) => a.id.localeCompare(b.id));
      return Response.json({ thread, messages: all, drafts }, { headers: { "Cache-Control": "no-store" } });
    }
    const { blobs } = await store.list({ prefix: "new/" });
    const items = [];
    for (const b of blobs) {
      const m = await store.get("msg/" + b.key.slice(4), { type: "json" });
      if (m) items.push(m);
    }
    items.sort((a, b) => a.id.localeCompare(b.id));
    return Response.json({ count: items.length, messages: items }, { headers: { "Cache-Control": "no-store" } });
  }

  if (req.method === "POST") {
    let body = {};
    try { body = await req.json(); } catch (e) {}
    if (Array.isArray(body.read)) {
      let n = 0;
      for (const id of body.read.slice(0, 200)) {
        if (typeof id === "string" && /^[0-9a-z]{9}-[0-9a-f]{8}$/.test(id)) { await store.delete("new/" + id); n++; }
      }
      return Response.json({ ok: true, read: n });
    }
    if (body.draft && typeof body.draft === "object") {
      const thread = String(body.draft.thread || "");
      const text = String(body.draft.text || "").trim();
      if (!/^t-[0-9a-f]{12}$/.test(thread) || !(await store.get("threads/" + thread, { type: "json" })))
        return Response.json({ error: "thread" }, { status: 400 });
      if (!text || text.length > MAX_TEXT) return Response.json({ error: "text" }, { status: 400 });
      const id = "d-" + newId();
      const draft = { id, thread, text, status: "draft", createdAt: nowIso() };
      await store.setJSON("draft/" + id, draft);
      return Response.json({ ok: true, draft });
    }
    return Response.json({ error: "body" }, { status: 400 });
  }
  return new Response(null, { status: 405 });
}

// ── 3. 보내기 ───────────────────────────────────────────
// POST /api/talktalk/send {draftId} (헤더 x-smile-key = SMILE_SEND_KEY)
// 저장된 초안만, 한 번만 보낸다. 글을 직접 받아 보내는 길은 없다.
// 사장님이 사무실 페이지에서 '보내기' 확인을 누른 초안만 이 함수를 부르도록 예약 작업 설명서에 적는다.
export async function handleSend(req, { store, env, fetchFn = fetch }) {
  if (!keyOk(req.headers.get("x-smile-key"), env.SMILE_SEND_KEY)) return new Response(null, { status: 404 });
  if (req.method !== "POST") return new Response(null, { status: 405 });
  if (!env.TALKTALK_AUTH_TOKEN) return Response.json({ error: "no-token" }, { status: 500 });
  let body = {};
  try { body = await req.json(); } catch (e) {}
  const draftId = String(body.draftId || "");
  if (!/^d-[0-9a-z]{9}-[0-9a-f]{8}$/.test(draftId)) return Response.json({ error: "draftId" }, { status: 400 });
  const draft = await store.get("draft/" + draftId, { type: "json" });
  if (!draft) return Response.json({ error: "no-draft" }, { status: 404 });
  if (draft.status !== "draft") return Response.json({ error: "already", status: draft.status }, { status: 409 });
  const t = await store.get("threads/" + draft.thread, { type: "json" });
  if (!t || !t.user) return Response.json({ error: "thread" }, { status: 400 });

  // 두 번 보내기 막기: 먼저 '보내는 중'으로 바꿈
  draft.status = "sending";
  draft.sendingAt = nowIso();
  await store.setJSON("draft/" + draftId, draft);

  let result = null;
  try {
    const r = await fetchFn(SEND_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json;charset=UTF-8", Authorization: env.TALKTALK_AUTH_TOKEN },
      body: JSON.stringify({ event: "send", user: t.user, textContent: { text: draft.text } }),
    });
    result = await r.json().catch(() => ({ success: false, resultCode: "http-" + r.status }));
  } catch (e) {
    result = { success: false, resultCode: "network" };
  }
  const ok = result && result.success === true;
  draft.status = ok ? "sent" : "failed";
  draft.resultCode = String((result && result.resultCode) || "");
  if (!ok && result && result.resultMessage) draft.resultMessage = String(result.resultMessage).slice(0, 200);
  draft[ok ? "sentAt" : "failedAt"] = nowIso();
  await store.setJSON("draft/" + draftId, draft);
  return Response.json({ ok, draft }, { status: ok ? 200 : 502 });
}
