/**
 * nutrition.js – Nutrition suggestions UI.
 */

const Nutrition = (() => {
  function renderMeal(meal) {
    const tags = (meal.dietary_tags || [])
      .map((t) => `<span class="meal-tag">${escHtml(t)}</span>`)
      .join("");
    const ingredients = (meal.ingredients || []).map(escHtml).join(", ");

    return `
      <div class="meal-card">
        <div class="meal-name">🍽️ ${escHtml(meal.name)}</div>
        ${tags ? `<div class="meal-tags">${tags}</div>` : ""}
        <p style="font-size:.85rem;color:var(--text-muted);margin-bottom:.4rem">
          <strong>Ingredients:</strong> ${ingredients}
        </p>
        <div class="meal-prep">${escHtml(meal.preparation)}</div>
        ${meal.nutritional_highlights ? `<div class="meal-highlights">📊 ${escHtml(meal.nutritional_highlights)}</div>` : ""}
      </div>`;
  }

  function render(data, containerId) {
    const el = document.getElementById(containerId);
    if (!el) return;

    const meals = (data.suggestions || []).map(renderMeal).join("");
    el.innerHTML = `
      ${meals || "<p class='text-muted'>No suggestions returned.</p>"}
      <div class="disclaimer mt-2">ℹ️ ${escHtml(data.disclaimer || "These are general wellness suggestions only.")}</div>`;
  }

  async function load(containerId, mealType = "any") {
    const el = document.getElementById(containerId);
    if (!el) return;

    el.innerHTML = `<div class="flex-center" style="padding:2rem"><span class="spinner"></span>&nbsp; Loading meal ideas…</div>`;

    try {
      const profile = Profile.get();
      const data = await API.getNutrition({ profile, meal_type: mealType });
      render(data, containerId);
    } catch (err) {
      el.innerHTML = `<div class="alert alert-error">Could not load nutrition: ${escHtml(err.message)}</div>`;
    }
  }

  return { load, render };
})();
