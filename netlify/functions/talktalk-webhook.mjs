// 네이버 톡톡 webhook (설명은 netlify/lib/talktalk.mjs 맨 위)
import { getStore } from "@netlify/blobs";
import { handleWebhook } from "../lib/talktalk.mjs";

export default async (req) =>
  handleWebhook(req, { store: getStore({ name: "talktalk", consistency: "strong" }), env: process.env });

export const config = { path: "/api/talktalk/webhook" };
