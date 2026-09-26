import { useEffect, useState } from "react";

import { apiFetch } from "../api/client";

interface CompetitionEntry {
  id: number;
  event_date: string;
  tournament: string;
  opponent: string | null;
  result: "win" | "loss" | "draw";
  video_link: string | null;
  notes: string | null;
}

const EMPTY = {
  event_date: new Date().toISOString().slice(0, 10),
  tournament: "",
  opponent: "",
  result: "win" as const,
  video_link: "",
  notes: "",
};

export default function CompetitionJournal() {
  const [entries, setEntries] = useState<CompetitionEntry[]>([]);
  const [form, setForm] = useState(EMPTY);

  function load() {
    apiFetch<CompetitionEntry[]>("/competition-entries").then(setEntries);
  }

  useEffect(load, []);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    await apiFetch("/competition-entries", { method: "POST", body: JSON.stringify(form) });
    setForm(EMPTY);
    load();
  }

  async function handleDelete(id: number) {
    await apiFetch(`/competition-entries/${id}`, { method: "DELETE" });
    load();
  }

  return (
    <div className="page">
      <h1>Competition Journal</h1>
      <form onSubmit={handleSubmit} className="form">
        <label>
          Date
          <input
            type="date"
            value={form.event_date}
            onChange={(e) => setForm({ ...form, event_date: e.target.value })}
            required
          />
        </label>
        <label>
          Tournament
          <input value={form.tournament} onChange={(e) => setForm({ ...form, tournament: e.target.value })} required />
        </label>
        <label>
          Opponent
          <input value={form.opponent} onChange={(e) => setForm({ ...form, opponent: e.target.value })} />
        </label>
        <label>
          Result
          <select value={form.result} onChange={(e) => setForm({ ...form, result: e.target.value as "win" | "loss" | "draw" })}>
            <option value="win">Win</option>
            <option value="loss">Loss</option>
            <option value="draw">Draw</option>
          </select>
        </label>
        <label>
          Video Link
          <input value={form.video_link} onChange={(e) => setForm({ ...form, video_link: e.target.value })} />
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
            <strong>{entry.event_date}</strong> — {entry.tournament} ({entry.result})
            {entry.opponent && <p>vs {entry.opponent}</p>}
            {entry.video_link && (
              <p>
                <a href={entry.video_link} target="_blank" rel="noreferrer">
                  Video
                </a>
              </p>
            )}
            <p>{entry.notes}</p>
            <button onClick={() => handleDelete(entry.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
