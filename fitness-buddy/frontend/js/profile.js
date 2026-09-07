/**
 * profile.js – User profile management (read/write to localStorage).
 */

const Profile = (() => {
  const KEY = "fb_profile";

  const DEFAULTS = {
    name: "Friend",
    age: null,
    fitness_goal: "general fitness",
    experience_level: "beginner",
    workout_duration_minutes: 30,
    equipment: "none",
    dietary_preference: "balanced",
    activity_level: "sedentary",
  };

  function get() {
    try {
      const raw = localStorage.getItem(KEY);
      return raw ? { ...DEFAULTS, ...JSON.parse(raw) } : { ...DEFAULTS };
    } catch (_) {
      return { ...DEFAULTS };
    }
  }

  function save(data) {
    const profile = { ...DEFAULTS, ...data };
    localStorage.setItem(KEY, JSON.stringify(profile));
    return profile;
  }

  function exists() {
    return !!localStorage.getItem(KEY);
  }

  function clear() {
    localStorage.removeItem(KEY);
  }

  return { get, save, exists, clear, DEFAULTS };
})();
