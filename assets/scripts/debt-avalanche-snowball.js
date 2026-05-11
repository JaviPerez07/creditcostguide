(() => {
  const MAX_DEBTS = 5;
  const MAX_MONTHS = 600;
  let debtChart = null;
  const debtRows = document.getElementById("debtRows");
  if (!debtRows) return;
  const addDebtBtn = document.getElementById("addDebtBtn");
  const totalPaymentInput = document.getElementById("totalPayment");
  const warning = document.getElementById("debtWarning");
  const fmtMoney = (n) => new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 }).format(Number.isFinite(n) ? n : 0);
  const fmtMonths = (m) => `${m} month${m === 1 ? "" : "s"}`;
  const defaultDebts = [
    { name: "Credit card", balance: 4200, apr: 24.99 },
    { name: "Personal loan", balance: 8000, apr: 12.5 },
    { name: "Store card", balance: 1200, apr: 28.99 }
  ];
  function addDebtRow(debt = { name: "Debt", balance: 1000, apr: 18 }) {
    if (debtRows.children.length >= MAX_DEBTS) return;
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td><input class="debt-name" type="text" value="${debt.name}" aria-label="Debt name"></td>
      <td><input class="debt-balance" type="number" inputmode="decimal" min="0" step="50" value="${debt.balance}" aria-label="Debt balance"></td>
      <td><input class="debt-apr" type="number" inputmode="decimal" min="0" max="99" step="0.01" value="${debt.apr}" aria-label="Debt APR"></td>
      <td><button type="button" class="ccg-button ccg-button--ghost ccg-button--small remove-button">Remove</button></td>
    `;
    debtRows.appendChild(tr);
    tr.querySelectorAll("input").forEach(input => input.addEventListener("input", calculate));
    tr.querySelector(".remove-button").addEventListener("click", () => { tr.remove(); calculate(); });
    calculate();
  }
  function getDebts() {
    return Array.from(debtRows.querySelectorAll("tr"))
      .map(row => ({
        name: row.querySelector(".debt-name").value.trim() || "Debt",
        balance: Math.max(0, parseFloat(row.querySelector(".debt-balance").value) || 0),
        apr: Math.max(0, parseFloat(row.querySelector(".debt-apr").value) || 0)
      }))
      .filter(d => d.balance > 0);
  }
  function simulate(strategy, debts, totalPayment) {
    let balances = debts.map(d => ({ ...d }));
    let totalInterest = 0;
    let months = 0;
    const timeline = [balances.reduce((s, d) => s + d.balance, 0)];
    while (balances.some(d => d.balance > 0.01) && months < MAX_MONTHS) {
      months += 1;
      let monthlyInterest = 0;
      balances.forEach(d => {
        if (d.balance <= 0) return;
        const interest = d.balance * (d.apr / 100 / 12);
        d.balance += interest;
        monthlyInterest += interest;
      });
      totalInterest += monthlyInterest;
      let paymentLeft = totalPayment;
      const active = balances.filter(d => d.balance > 0.01);
      active.sort((a, b) => strategy === "avalanche" ? (b.apr - a.apr || a.balance - b.balance) : (a.balance - b.balance || b.apr - a.apr));
      for (const debt of active) {
        if (paymentLeft <= 0) break;
        const payment = Math.min(paymentLeft, debt.balance);
        debt.balance -= payment;
        paymentLeft -= payment;
      }
      timeline.push(balances.reduce((s, d) => s + Math.max(0, d.balance), 0));
    }
    return { months, totalInterest, timeline, amortizes: months < MAX_MONTHS };
  }
  function debtFreeDate(months) {
    const d = new Date();
    d.setMonth(d.getMonth() + months);
    return d.toLocaleDateString("en-US", { month: "short", year: "numeric" });
  }
  function updateChart(avalanche, snowball) {
    const ctx = document.getElementById("debtChart");
    if (!ctx || typeof Chart === "undefined") return;
    const len = Math.max(avalanche.timeline.length, snowball.timeline.length);
    const labels = Array.from({ length: len }, (_, i) => i);
    if (debtChart) debtChart.destroy();
    debtChart = new Chart(ctx, {
      type: "line",
      data: { labels, datasets: [
        { label: "Avalanche balance", data: avalanche.timeline, borderColor: "#1f6fff", backgroundColor: "rgba(31,111,255,0.12)", tension: 0.25 },
        { label: "Snowball balance", data: snowball.timeline, borderColor: "#e65100", backgroundColor: "rgba(230,81,0,0.12)", tension: 0.25 }
      ]},
      options: {
        responsive: true,
        interaction: { mode: "index", intersect: false },
        plugins: { tooltip: { callbacks: { label: (c) => `${c.dataset.label}: ${fmtMoney(c.parsed.y)}` } } },
        scales: { y: { ticks: { callback: (v) => fmtMoney(v) } }, x: { title: { display: true, text: "Months" } } }
      }
    });
  }
  function calculate() {
    const debts = getDebts();
    const totalPayment = Math.max(0, parseFloat(totalPaymentInput.value) || 0);
    const monthlyInterest = debts.reduce((s, d) => s + d.balance * (d.apr / 100 / 12), 0);
    warning.hidden = true;
    warning.textContent = "";
    if (!debts.length || totalPayment <= 0) return;
    if (totalPayment <= monthlyInterest) {
      warning.hidden = false;
      warning.textContent = "Your monthly payment may not cover estimated monthly interest across all debts. The balance can grow under these assumptions. Try a larger monthly payment.";
    }
    const avalanche = simulate("avalanche", debts, totalPayment);
    const snowball = simulate("snowball", debts, totalPayment);
    const interestSaved = snowball.totalInterest - avalanche.totalInterest;
    const monthDiff = snowball.months - avalanche.months;
    document.getElementById("avalancheMonths").textContent = avalanche.amortizes ? fmtMonths(avalanche.months) : "600+ months";
    document.getElementById("avalancheInterest").textContent = `${fmtMoney(avalanche.totalInterest)} interest`;
    document.getElementById("snowballMonths").textContent = snowball.amortizes ? fmtMonths(snowball.months) : "600+ months";
    document.getElementById("snowballInterest").textContent = `${fmtMoney(snowball.totalInterest)} interest`;
    document.getElementById("avalancheTableMonths").textContent = avalanche.amortizes ? avalanche.months : "600+";
    document.getElementById("snowballTableMonths").textContent = snowball.amortizes ? snowball.months : "600+";
    document.getElementById("avalancheDate").textContent = avalanche.amortizes ? debtFreeDate(avalanche.months) : "Not estimated";
    document.getElementById("snowballDate").textContent = snowball.amortizes ? debtFreeDate(snowball.months) : "Not estimated";
    document.getElementById("avalancheTableInterest").textContent = fmtMoney(avalanche.totalInterest);
    document.getElementById("snowballTableInterest").textContent = fmtMoney(snowball.totalInterest);
    if (interestSaved > 0) document.getElementById("methodVerdict").textContent = `Avalanche saves ${fmtMoney(interestSaved)}`;
    else if (interestSaved < 0) document.getElementById("methodVerdict").textContent = `Snowball saves ${fmtMoney(Math.abs(interestSaved))}`;
    else document.getElementById("methodVerdict").textContent = "Both methods cost the same";
    document.getElementById("methodVerdictSub").textContent = monthDiff > 0 ? `Avalanche is ${monthDiff} month${monthDiff === 1 ? "" : "s"} faster.` : monthDiff < 0 ? `Snowball is ${Math.abs(monthDiff)} month${Math.abs(monthDiff) === 1 ? "" : "s"} faster.` : "Same payoff time.";
    updateChart(avalanche, snowball);
  }
  addDebtBtn.addEventListener("click", () => addDebtRow());
  totalPaymentInput.addEventListener("input", calculate);
  defaultDebts.forEach(addDebtRow);
})();
