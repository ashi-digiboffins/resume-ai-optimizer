"use client";

import { BulletRewrite } from "@/lib/api";

export function DiffView({ rewrites }: { rewrites: BulletRewrite[] }) {
  if (!rewrites.length) {
    return <p className="text-sm text-gray-400">No bullet rewrites yet.</p>;
  }

  return (
    <div className="space-y-4">
      {rewrites.map((r, i) => (
        <div key={i} className="rounded-xl border bg-white p-4">
          <p className="mb-2 text-sm text-gray-400 line-through">{r.original}</p>
          <p className="text-sm font-medium text-gray-900">{r.rewritten}</p>
        </div>
      ))}
    </div>
  );
}
