export const API_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export type BulletRewrite = { original: string; rewritten: string };

export type AnalyzeResult = {
  score: number;
  matched_keywords: string[];
  missing_keywords: string[];
  rewrites: BulletRewrite[];
};

export async function analyze(
  resume: File,
  jobDescription: string,
  strictness: number,
): Promise<AnalyzeResult> {
  const form = new FormData();
  form.append("resume", resume);
  form.append("job_description", jobDescription);
  form.append("strictness", String(strictness));

  const res = await fetch(`${API_URL}/api/analyze`, {
    method: "POST",
    body: form,
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}
