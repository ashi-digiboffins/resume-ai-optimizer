"use client";

import { useState } from "react";
import { analyze, AnalyzeResult } from "@/lib/api";
import { ResumeUploader } from "@/components/ResumeUploader";
import { JDInput } from "@/components/JDInput";
import { ScorePanel } from "@/components/ScorePanel";
import { DiffView } from "@/components/DiffView";

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [jd, setJd] = useState("");
  const [strictness, setStrictness] = useState(0.5);
  const [result, setResult] = useState<AnalyzeResult | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function run() {
    if (!file || !jd.trim()) return;
    setBusy(true);
    setError(null);
    try {
      setResult(await analyze(file, jd, strictness));
    } catch (e) {
      setError(e instanceof Error ? e.message : "analysis failed");
    } finally {
      setBusy(false);
    }
  }

  return (
    <main className="mx-auto max-w-5xl px-6 py-12">
      <h1 className="text-3xl font-semibold">Resume AI Optimizer</h1>
      <p className="mt-2 text-gray-500">
        Tailor your resume to a job description — with an ATS score and
        hallucination-guarded rewrites.
      </p>

      <div className="mt-8 grid gap-8 md:grid-cols-2">
        <div className="space-y-4">
          <ResumeUploader file={file} onSelect={setFile} />
          <JDInput value={jd} onChange={setJd} />
          <label className="block text-sm">
            <span className="text-gray-700">
              Rewrite strictness: {strictness.toFixed(2)}
            </span>
            <input
              type="range"
              min={0}
              max={1}
              step={0.05}
              value={strictness}
              onChange={(e) => setStrictness(Number(e.target.value))}
              className="mt-1 w-full"
            />
          </label>
          <button
            onClick={run}
            disabled={busy || !file || !jd.trim()}
            className="w-full rounded-lg bg-black px-4 py-2 text-white disabled:opacity-50"
          >
            {busy ? "Analyzing…" : "Analyze"}
          </button>
          {error && <p className="text-sm text-red-500">{error}</p>}
        </div>

        <div className="space-y-4">
          {result ? (
            <>
              <ScorePanel
                score={result.score}
                matched={result.matched_keywords}
                missing={result.missing_keywords}
              />
              <DiffView rewrites={result.rewrites} />
            </>
          ) : (
            <p className="text-sm text-gray-400">
              Results will appear here after you analyze.
            </p>
          )}
        </div>
      </div>
    </main>
  );
}
