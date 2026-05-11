(() => {
  const MAX_MONTHS = 720;
  let chart = null;
  const fields = ["ccBalance", "ccApr", "minPct", "minFloor", "extraPayment"].reduce((acc, id) => { acc[id] = document.getElementById(id); return acc; }, {});
  if (!fields.ccBalance) return;
  const fmtMoney = (n) => new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 }).format(Number.isFinite(n) ? n : 0);
  const fmtYearsMonths = (months) => {
    const y = Math.floor(months / 12);
    const m = months % 12;
    if (y <= 0) return `${m} month${m === 1 ? "" : "s"}`;
    return `${y} year${y === 1 ? "" : "s"}${m ? `, ${m} month${m === 1 ? "" : "s"}` : ""}`;
  };
  function simulate(balance, apr, minPct, minFloor, extra) {
    let current = balance;
    let months = 0;
    let interestPaid = 0;
    const monthlyRate = apr / 100 / 12;
    while (current > 0.01 && months < MAX_MONTHS) {
      months += 1;
      const interest = current * monthlyRate;
      current += interest;
      interestPaid += interest;
      const minPayment = Math.max(current * (minPct / 100), minFloor);
      const payment = Math.min(current, minPayment + extra);
      if (payment <= interest && monthlyRate > 0) return { months: MAX_MONTHS, interestPaid, amortizes: false };
      current -= payment;
    }
    return { months, interestPaid, amortizes: months < MAX_MONTHS };
  }
  function updateChart(minimum, extra) {
    const ctx = document.getElementById("minPaymentChart");
    if (!ctx || typeof Chart === "undefined") return;
    if (chart) chart.destroy();
    chart = new Chart(ctx, {
      type: "bar",
      data: { labels: ["Minimum only", "Minimum + extra"], datasets: [
        { label: "Total interest ($)", data: [Math.round(minimum.interestPaid), Math.round(extra.interestPaid)], backgroundColor: "#1f6fff", yAxisID: "y" },
        { label: "Months to payoff", data: [minimum.months, extra.months], backgroundColor: "#e65100", yAxisID: "y1" }
      ]},
      options: {
        responsive: true,
        plugins: { tooltip: { callbacks: { label: (c) => c.dataset.label.includes("interest") ? `${c.dataset.label}: ${fmtMoney(c.parsed.y)}` : `${c.dataset.label}: ${c.parsed.y}` } } },
        scales: { y: { type: "linear", position: "left", ticks: { callback: (v) => fmtMoney(v) } }, y1: { type: "linear", position: "right", grid: { drawOnChartArea: false } } }
      }
    });
  }
  function calculate() {
    const balance = Math.max(0, parseFloat(fields.ccBalance.value) || 0);
    const apr = Math.max(0, parseFloat(fields.ccApr.value) || 0);
    const minPct = Math.max(0.1, parseFloat(fields.minPct.value) || 2);
    const minFloor = Math.max(0, parseFloat(fields.minFloor.value) || 25);
    const extraPayment = Math.max(0, parseFloat(fields.extraPayment.value) || 0);
    document.getElementById("extraLabel").textContent = fmtMoney(extraPayment);
    const warning = document.getElementById("minWarning");
    warning.hidden = true;
    if (balance <= 0) return;
    const minimum = simulate(balance, apr, minPct, minFloor, 0);
    const extra = simulate(balance, apr, minPct, minFloor, extraPayment);
    if (!minimum.amortizes) {
      warning.hidden = false;
      warning.textContent = "The entered minimum-payment settings may not pay off this balance within 60 years. Increase the payment, raise the floor, or contact a nonprofit credit counselor.";
    }
    const interestSavings = minimum.interestPaid - extra.interestPaid;
    const monthSavings = minimum.months - extra.months;
    document.getElementById("minHeadline").textContent = minimum.amortizes ? fmtYearsMonths(minimum.months) : "60+ years";
    document.getElementById("minInterest").textContent = `${fmtMoney(minimum.interestPaid)} estimated interest`;
    document.getElementById("extraHeadline").textContent = extra.amortizes ? fmtYearsMonths(extra.months) : "60+ years";
    document.getElementById("extraInterest").textContent = `${fmtMoney(extra.interestPaid)} estimated interest`;
    document.getElementById("savingsHeadline").textContent = fmtMoney(Math.max(0, interestSavings));
    const ms = Math.max(0, monthSavings);
    document.getElementById("timeSavings").textContent = `${ms} month${ms === 1 ? "" : "s"} faster`;
    document.getElementById("minMonths").textContent = minimum.amortizes ? minimum.months : "720+";
    document.getElementById("extraMonths").textContent = extra.amortizes ? extra.months : "720+";
    document.getElementById("minTotalInterest").textContent = fmtMoney(minimum.interestPaid);
    document.getElementById("extraTotalInterest").textContent = fmtMoney(extra.interestPaid);
    document.getElementById("minRatio").textContent = balance > 0 ? `${((minimum.interestPaid / balance) * 100).toFixed(1)}%` : "\u2014";
    document.getElementById("extraRatio").textContent = balance > 0 ? `${((extra.interestPaid / balance) * 100).toFixed(1)}%` : "\u2014";
    updateChart(minimum, extra);
  }
  Object.values(fields).forEach(f => f.addEventListener("input", calculate));
  calculate();
})();
