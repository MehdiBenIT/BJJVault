import { useEffect, useState } from "react";

import { apiFetch } from "../api/client";

interface TrainingEntry {
  id: number;
  session_date: string;
  is_gi: boolean;
  techniques_practiced: string | null;
  notes: string | null;
}

const EMPTY = { session_date: new Date().toISOString().slice(0, 10), is_gi: true, techniques_practiced: "", notes: "" };

export default function TrainingJournal() {
  const [entries, setEntries] = useState<TrainingEntry[]>([]);
  const [form, setForm] = useState(EMPTY);

  function load() {
    apiFetch<TrainingEntry[]>("/training-entries").then(setEntries);
  }

  useEffect(load, []);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    await apiFetch("/training-entries", { method: "POST", body: JSON.stringify(form) });
    setForm(EMPTY);
    load();
  }

  async function handleDelete(id: number) {
    await apiFetch(`/training-entries/${id}`, { method: "DELETE" });
    load();
  }

  return (
    <div className="page">
      <h1>Training Journal</h1>
      <form onSubmit={handleSubmit} className="form">
        <label>
          Date
          <input
            type="date"
            value={form.session_date}
            onChange={(e) => setForm({ ...form, session_date: e.target.value })}
            required
          />
        </label>
        <label>
          <input type="checkbox" checked={form.is_gi} onChange={(e) => setForm({ ...form, is_gi: e.target.checked })} />
          Gi
        </label>
        <label>
          Techniques Practiced
          <textarea
            value={form.techniques_practiced}
            onChange={(e) => setForm({ ...form, techniques_practiced: e.target.value })}
          />
        </label>
        <label>
          Notes
          <textarea value={form.notes} onChange={(e) => setForm({ ...form, notes: e.target.value })} />
        </label>
        <button type="submit">Add Entry</button>
      </form>

      <ul className="entry-list">
        {entries.map((entry) => (
          <li key={entry.id}>
            <strong>{entry.session_date}</strong> — {entry.is_gi ? "Gi" : "No-Gi"}
            <p>{entry.techniques_practiced}</p>
            <p>{entry.notes}</p>
            <button onClick={() => handleDelete(entry.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
