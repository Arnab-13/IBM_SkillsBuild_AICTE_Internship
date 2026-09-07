/**
 * app.js – Shared utilities and page bootstrap.
 * Loaded on every page before other JS files.
 */

// -------------------------------------------------------
// Utility: HTML-escape to prevent XSS
// -------------------------------------------------------
function escHtml(str) {
  if (str === null || str === undefined) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

// -------------------------------------------------------
// Highlight active nav link
// -------------------------------------------------------
(function highlightNav() {
  const path = window.location.pathname;
  document.querySelectorAll(".nav-links a").forEach((a) => {
    const href = a.getAttribute("href");
    const active =
      (href === "/" && path === "/") ||
      (href !== "/" && path.startsWith(href));
    if (active) a.classList.add("active");
  });
})();

// -------------------------------------------------------
// Profile setup guard: redirect to /profile if missing
// (Only enforced on dashboard page)
// -------------------------------------------------------
(function profileGuard() {
  const isDashboard = window.location.pathname === "/dashboard";
  if (isDashboard && !Profile.exists()) {
    window.location.href = "/profile";
  }
})();
