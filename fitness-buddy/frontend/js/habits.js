/**
 * habits.js – Habit tracker using localStorage.
 */

const Habits = (() => {
  const STORAGE_KEY  = "fb_habits";
  const STREAK_KEY   = "fb_streak";
  const LAST_DATE_KEY = "fb_last_date";

  // ---------- persistence ----------
  function todayStr() {
    return new Date().toISOString().slice(0, 10);
  }

  function loadState(catalogue) {
    // Reset completions each new day
    const lastDate = localStorage.getItem(LAST_DATE_KEY);
    const today    = todayStr();

    if (lastDate !== today) {
      // New day – update streak if all habits were done yesterday
      if (lastDate) {
        const prev = getSavedState();
        const allDone = prev && prev.every((h) => h.completed);
        if (allDone) incrementStreak();
        else resetStreakIfMissed(lastDate);
      }
      localStorage.setItem(LAST_DATE_KEY, today);
      const fresh = catalogue.map((h) => ({ ...h, completed: false }));
      localStorage.setItem(STORAGE_KEY, JSON.stringify(fresh));
      return fresh;
    }

    const saved = getSavedState();
    if (!saved || saved.length === 0) {
      const fresh = catalogue.map((h) => ({ ...h, completed: false }));
      localStorage.setItem(STORAGE_KEY, JSON.stringify(fresh));
      return fresh;
    }
    // Merge catalogue with saved completions
    return catalogue.map((cat) => {
      const s = saved.find((x) => x.id === cat.id);
      return { ...cat, completed: s ? s.completed : false };
    });
  }

  function getSavedState() {
    try { return JSON.parse(localStorage.getItem(STORAGE_KEY)) || []; } catch (_) { return []; }
  }

  function saveState(habits) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(habits));
  }

  // ---------- streak ----------
  function getStreak() { return parseInt(localStorage.getItem(STREAK_KEY) || "0", 10); }
  function incrementStreak() { localStorage.setItem(STREAK_KEY, String(getStreak() + 1)); }
  function resetStreakIfMissed(lastDate) {
    const yesterday = new Date(); yesterday.setDate(yesterday.getDate() - 1);
    const yStr = yesterday.toISOString().slice(0, 10);
    if (lastDate !== yStr) localStorage.setItem(STREAK_KEY, "0");
  }

  // ---------- render ----------
  function render(habits, containerId) {
    const el = document.getElementById(containerId);
    if (!el) return;

    const done  = habits.filter((h) => h.completed).length;
    const total = habits.length;
    const pct   = total ? Math.round((done / total) * 100) : 0;
    const streak = getStreak();

    const items = habits.map((h) => `
      <li class="habit-item${h.completed ? " completed" : ""}" data-id="${escHtml(h.id)}">
        <div class="habit-checkbox">${h.completed ? "✓" : ""}</div>
        <span class="habit-emoji">${escHtml(h.emoji)}</span>
        <span class="habit-label">${escHtml(h.label)}</span>
      </li>`).join("");

    el.innerHTML = `
      <div class="flex-between mb-2">
        <span class="streak-badge">🔥 ${streak}-day streak</span>
        <span class="text-muted" style="font-size:.85rem">${done}/${total} done</span>
      </div>
      <div class="progress-bar-wrap">
        <div class="progress-bar" style="width:${pct}%"></div>
      </div>
      <div class="progress-label">${pct}% complete</div>
      <ul class="habit-list mt-2">${items}</ul>`;

    el.querySelectorAll(".habit-item").forEach((li) => {
      li.addEventListener("click", () => toggle(li.dataset.id, habits, containerId));
    });
  }

  function toggle(id, habits, containerId) {
    const h = habits.find((x) => x.id === id);
    if (!h) return;
    h.completed = !h.completed;
    saveState(habits);
    render(habits, containerId);
  }

  // ---------- init ----------
  async function init(containerId) {
    const el = document.getElementById(containerId);
    if (!el) return;
    el.innerHTML = `<div class="flex-center" style="padding:1.5rem"><span class="spinner"></span></div>`;

    try {
      const catalogue = await API.getHabits();
      const habits    = loadState(catalogue);
      render(habits, containerId);
    } catch (err) {
      el.innerHTML = `<div class="alert alert-error">Could not load habits: ${escHtml(err.message)}</div>`;
    }
  }

  return { init };
})();
