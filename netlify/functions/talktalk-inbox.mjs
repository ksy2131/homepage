// 네이버 톡톡 inbox (설명은 netlify/lib/talktalk.mjs 맨 위)
import { getStore } from "@netlify/blobs";
import { handleInbox } from "../lib/talktalk.mjs";

export default async (req) =>
  handleInbox(req, { store: getStore({ name: "talktalk", consistency: "strong" }), env: process.env });

export const config = { path: "/api/talktalk/inbox" };
