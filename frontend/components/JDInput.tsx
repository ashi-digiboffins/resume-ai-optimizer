"use client";

export function JDInput({
  value,
  onChange,
}: {
  value: string;
  onChange: (v: string) => void;
}) {
  return (
    <label className="block">
      <span className="mb-1 block text-sm font-medium text-gray-700">
        Job description
      </span>
      <textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        rows={10}
        placeholder="Paste the job description here…"
        className="w-full resize-y rounded-xl border bg-white p-3 text-sm"
      />
    </label>
  );
}
