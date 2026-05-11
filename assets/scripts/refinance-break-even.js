(() => {
  let chart = null;
  const ids = ["loanBalance", "currentRate", "remainingYears", "newRate", "newYears", "closingCosts", "plannedYears"];
  const el = ids.reduce((acc, id) => { acc[id] = document.getElementById(id); return acc; }, {});
  if (!el.loanBalance) return;
  const fmtMoney = (n) => new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 }).format(Number.isFinite(n) ? n : 0);
  const fmtMonths = (m) => `${m} month${m === 1 ? "" : "s"}`;
  function payment(principal, annualRate, years) {
    const n = years * 12;
    const r = annualRate / 100 / 12;
    if (principal <= 0 || n <= 0) return 0;
    if (r === 0) return principal / n;
    return principal * r / (1 - Math.pow(1 + r, -n));
  }
  function updateChart(monthlySavings, closingCosts, horizonMonths) {
    const ctx = document.getElementById("refiChart");
    if (!ctx || typeof Chart === "undefined") return;
    const months = Math.min(Math.max(horizonMonths, 12), 360);
    const labels = [];
    const values = [];
    const step = Math.max(1, Math.round(months / 24));
    for (let i = 0; i <= months; i += step) {
      labels.push(i);
      values.push((monthlySavings * i) - closingCosts);
    }
    if (chart) chart.destroy();
    chart = new Chart(ctx, {
      type: "line",
      data: { labels, datasets: [{ label: "Cumulative savings after closing costs", data: values, borderColor: "#1f6fff", backgroundColor: "rgba(31,111,255,0.12)", tension: 0.2, fill: true }]},
      options: {
        responsive: true,
        plugins: { tooltip: { callbacks: { label: (c) => `${c.dataset.label}: ${fmtMoney(c.parsed.y)}` } } },
        scales: { y: { ticks: { callback: (v) => fmtMoney(v) } }, x: { title: { display: true, text: "Months" } } }
      }
    });
  }
  function calculate() {
    const balance = Math.max(0, parseFloat(el.loanBalance.value) || 0);
    const currentRate = Math.max(0, parseFloat(el.currentRate.value) || 0);
    const remainingYears = Math.max(1, parseFloat(el.remainingYears.value) || 1);
    const newRate = Math.max(0, parseFloat(el.newRate.value) || 0);
    const newYears = Math.max(1, parseFloat(el.newYears.value) || 1);
    const closingCosts = Math.max(0, parseFloat(el.closingCosts.value) || 0);
    const plannedYears = Math.max(0, parseFloat(el.plannedYears.value) || 0);
    const oldPmt = payment(balance, currentRate, remainingYears);
    const newPmt = payment(balance, newRate, newYears);
    const monthlySavings = oldPmt - newPmt;
    const breakEvenMonths = monthlySavings > 0 ? Math.ceil(closingCosts / monthlySavings) : Infinity;
    const oldInterest = (oldPmt * remainingYears * 12) - balance;
    const newInterest = (newPmt * newYears * 12) - balance;
    document.getElementById("oldPayment").textContent = fmtMoney(oldPmt);
    document.getElementById("newPayment").textContent = fmtMoney(newPmt);
    document.getElementById("tableOldPayment").textContent = fmtMoney(oldPmt);
    document.getElementById("tableNewPayment").textContent = fmtMoney(newPmt);
    document.getElementById("oldInterest").textContent = fmtMoney(oldInterest);
    document.getElementById("newInterest").textContent = fmtMoney(newInterest);
    document.getElementById("tableClosingCosts").textContent = fmtMoney(closingCosts);
    const warning = document.getElementById("refiWarning");
    warning.hidden = true;
    if (!Number.isFinite(breakEvenMonths)) {
      document.getElementById("breakEven").textContent = "No monthly break-even";
      document.getElementById("breakEvenSub").textContent = "The new payment is not lower than the current payment.";
      warning.hidden = false;
      warning.textContent = "This refinance does not lower the estimated principal-and-interest payment. Review the offer carefully and confirm the Loan Estimate.";
      updateChart(monthlySavings, closingCosts, plannedYears * 12 || 120);
      return;
    }
    document.getElementById("breakEven").textContent = fmtMonths(breakEvenMonths);
    document.getElementById("breakEvenSub").textContent = `After that, estimated savings are ${fmtMoney(monthlySavings)}/month.`;
    const plannedMonths = plannedYears * 12;
    if (plannedMonths > 0 && plannedMonths < breakEvenMonths) {
      warning.hidden = false;
      warning.textContent = `Warning: your planned sale or next refinance is in ${plannedMonths} months \u2014 before the estimated break-even point of ${breakEvenMonths} months. This refinance may not recover closing costs through monthly savings.`;
    }
    updateChart(monthlySavings, closingCosts, plannedMonths || newYears * 12);
  }
  Object.values(el).forEach(input => input.addEventListener("input", calculate));
  calculate();
})();
