const apiBaseUrl = window.PORTFOLIO_API_BASE_URL.replace(/\/$/, "");
const status = document.querySelector("#status");
const portfolioValue = document.querySelector("#portfolio-value");

async function loadDashboard() {
  try {
    const [healthResponse, portfolioResponse] = await Promise.all([
      fetch(`${apiBaseUrl}/health`),
      fetch(`${apiBaseUrl}/portfolio`),
    ]);
    if (!healthResponse.ok || !portfolioResponse.ok) throw new Error("API unavailable");
    const portfolio = await portfolioResponse.json();
    status.textContent = "API connected. Import your broker data in Sprint 2 to begin analysis.";
    if (portfolio.holdings_count > 0) {
      portfolioValue.textContent = new Intl.NumberFormat("en-IN", { style: "currency", currency: "INR" })
        .format(portfolio.total_value);
    }
  } catch {
    status.textContent = "The dashboard is waiting for its API. Check the deployment configuration.";
  }
}

loadDashboard();
