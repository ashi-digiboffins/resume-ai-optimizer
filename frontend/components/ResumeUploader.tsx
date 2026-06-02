"use client";

import { useRef } from "react";

export function ResumeUploader({
  file,
  onSelect,
}: {
  file: File | null;
  onSelect: (file: File | null) => void;
}) {
  const inputRef = useRef<HTMLInputElement>(null);

  return (
    <div
      onDragOver={(e) => e.preventDefault()}
      onDrop={(e) => {
        e.preventDefault();
        onSelect(e.dataTransfer.files?.[0] ?? null);
      }}
      className="rounded-xl border-2 border-dashed border-gray-300 bg-white p-6 text-center"
    >
      <p className="text-sm text-gray-500">
        {file ? `📄 ${file.name}` : "Drop your resume (PDF / DOCX / TXT)"}
      </p>
      <button
        onClick={() => inputRef.current?.click()}
        className="mt-3 rounded-lg bg-black px-4 py-2 text-sm text-white"
      >
        {file ? "Change file" : "Choose file"}
      </button>
      <input
        ref={inputRef}
        type="file"
        accept=".pdf,.docx,.txt"
        className="hidden"
        onChange={(e) => onSelect(e.target.files?.[0] ?? null)}
      />
    </div>
  );
}
