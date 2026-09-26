import { useEffect, useState } from "react";

import { apiFetch } from "../api/client";

const BELTS = ["white", "blue", "purple", "brown", "black"];

interface AthleteProfile {
  name: string;
  belt: string;
  weight_class: string | null;
  academy: string | null;
  country: string | null;
}

const EMPTY_PROFILE: AthleteProfile = { name: "", belt: "white", weight_class: "", academy: "", country: "" };

export default function Profile() {
  const [profile, setProfile] = useState<AthleteProfile>(EMPTY_PROFILE);
  const [status, setStatus] = useState<"idle" | "saving" | "saved" | "error">("idle");

  useEffect(() => {
    apiFetch<AthleteProfile>("/profile")
      .then(setProfile)
      .catch(() => setProfile(EMPTY_PROFILE));
  }, []);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setStatus("saving");
    try {
      const saved = await apiFetch<AthleteProfile>("/profile", {
        method: "PUT",
        body: JSON.stringify(profile),
      });
      setProfile(saved);
      setStatus("saved");
    } catch {
      setStatus("error");
    }
  }

  return (
    <div className="page">
      <h1>Athlete Profile</h1>
      <form onSubmit={handleSubmit} className="form">
        <label>
          Name
          <input value={profile.name} onChange={(e) => setProfile({ ...profile, name: e.target.value })} required />
        </label>
        <label>
          Belt
          <select value={profile.belt} onChange={(e) => setProfile({ ...profile, belt: e.target.value })}>
            {BELTS.map((belt) => (
              <option key={belt} value={belt}>
                {belt}
              </option>
            ))}
          </select>
        </label>
        <label>
          Weight Class
          <input
            value={profile.weight_class ?? ""}
            onChange={(e) => setProfile({ ...profile, weight_class: e.target.value })}
          />
        </label>
        <label>
          Academy
          <input value={profile.academy ?? ""} onChange={(e) => setProfile({ ...profile, academy: e.target.value })} />
        </label>
        <label>
          Country
          <input value={profile.country ?? ""} onChange={(e) => setProfile({ ...profile, country: e.target.value })} />
        </label>
        <button type="submit" disabled={status === "saving"}>
          {status === "saving" ? "Saving..." : "Save"}
        </button>
        {status === "saved" && <span>Saved.</span>}
        {status === "error" && <span>Something went wrong.</span>}
      </form>
    </div>
  );
}
