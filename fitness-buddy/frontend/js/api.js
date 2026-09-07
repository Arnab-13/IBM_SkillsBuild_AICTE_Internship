/**
 * api.js – Centralised fetch wrappers for the Fitness Buddy backend.
 * All requests go to the same origin (served by FastAPI).
 */

const API = (() => {
  async function request(method, path, body = null) {
    const opts = {
      method,
      headers: { "Content-Type": "application/json" },
    };
    if (body !== null) opts.body = JSON.stringify(body);

    const res = await fetch(path, opts);
    if (!res.ok) {
      let msg = `HTTP ${res.status}`;
      try { const err = await res.json(); msg = err.detail || msg; } catch (_) {}
      throw new Error(msg);
    }
    return res.json();
  }

  return {
    saveProfile:  (profile)  => request("POST", "/api/profile",   profile),
    chat:         (payload)  => request("POST", "/api/chat",       payload),
    getWorkout:   (payload)  => request("POST", "/api/workout",    payload),
    getNutrition: (payload)  => request("POST", "/api/nutrition",  payload),
    getHabits:    ()         => request("GET",  "/api/habits"),
    getMotivation:()         => request("GET",  "/api/motivation"),
  };
})();
