/**
 * workout.js – Workout generator UI.
 */

const Workout = (() => {
  function renderExercise(ex) {
    const meta = [];
    if (ex.sets)             meta.push(`${ex.sets} sets`);
    if (ex.reps)             meta.push(`${ex.reps} reps`);
    if (ex.duration_seconds) meta.push(`${ex.duration_seconds}s`);
    if (ex.rest_seconds)     meta.push(`Rest: ${ex.rest_seconds}s`);

    return `
      <li class="exercise-item">
        <div class="exercise-name">${escHtml(ex.name)}</div>
        ${meta.length ? `<div class="exercise-meta">${meta.map(escHtml).join(" · ")}</div>` : ""}
        <div class="exercise-instructions">${escHtml(ex.instructions)}</div>
      </li>`;
  }

  function renderSection(label, items) {
    if (!items || items.length === 0) return "";
    return `
      <div class="workout-section-label">${escHtml(label)}</div>
      <ul class="exercise-list">${items.map(renderExercise).join("")}</ul>`;
  }

  function render(data, containerId) {
    const el = document.getElementById(containerId);
    if (!el) return;

    const diffColor = { beginner: "#2ecc71", intermediate: "#f39c12", advanced: "#e74c3c" };
    const color = diffColor[data.difficulty] || "#718096";

    el.innerHTML = `
      <div class="card-header">
        <span class="card-icon">🏋️</span>
        <div>
          <h3>${escHtml(data.title)}</h3>
          <span style="font-size:.8rem;color:${color};font-weight:700;text-transform:capitalize">${escHtml(data.difficulty)}</span>
        </div>
      </div>
      <p class="text-muted" style="font-size:.9rem">${escHtml(data.summary)}</p>
      ${renderSection("🔥 Warm-Up", data.warm_up)}
      ${renderSection("💪 Exercises", data.exercises)}
      ${renderSection("🧘 Cool-Down", data.cool_down)}
      <div class="disclaimer mt-2">⚠️ ${escHtml(data.safety_note)}</div>`;
  }

  async function generate(containerId, overrides = {}) {
    const el = document.getElementById(containerId);
    if (!el) return;

    el.innerHTML = `<div class="flex-center" style="padding:2rem"><span class="spinner"></span>&nbsp; Generating your workout…</div>`;

    try {
      const profile = Profile.get();
      const payload = { profile, ...overrides };
      const data = await API.getWorkout(payload);
      render(data, containerId);
    } catch (err) {
      el.innerHTML = `<div class="alert alert-error">Could not load workout: ${escHtml(err.message)}</div>`;
    }
  }

  return { generate, render };
})();
