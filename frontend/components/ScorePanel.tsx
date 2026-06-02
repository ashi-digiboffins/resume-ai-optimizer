"use client";

export function ScorePanel({
  score,
  matched,
  missing,
}: {
  score: number;
  matched: string[];
  missing: string[];
}) {
  const color =
    score >= 70 ? "text-green-600" : score >= 40 ? "text-amber-600" : "text-red-600";

  return (
    <div className="rounded-xl border bg-white p-5">
      <div className="flex items-baseline gap-2">
        <span className={`text-4xl font-bold ${color}`}>{score}</span>
        <span className="text-sm text-gray-400">/ 100 ATS match</span>
      </div>

      <div className="mt-4">
        <h3 className="text-xs font-semibold uppercase text-gray-400">Matched</h3>
        <div className="mt-1 flex flex-wrap gap-1">
          {matched.map((k) => (
            <span key={k} className="rounded-full bg-green-100 px-2 py-0.5 text-xs text-green-700">
              {k}
            </span>
          ))}
        </div>
      </div>

      <div className="mt-3">
        <h3 className="text-xs font-semibold uppercase text-gray-400">Missing</h3>
        <div className="mt-1 flex flex-wrap gap-1">
          {missing.map((k) => (
            <span key={k} className="rounded-full bg-red-100 px-2 py-0.5 text-xs text-red-700">
              {k}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}
