const site = {
  name: "CreditCostGuide",
  domain: "https://creditcostguide.com",
  logo: "https://creditcostguide.com/assets/icons/logo.svg",
  social: "https://creditcostguide.com/assets/images/social-preview.svg"
};

function parseJSON(value, fallback) {
  try { return JSON.parse(value || ""); } catch { return fallback; }
}

function money(value) {
  const number = Number.isFinite(value) ? value : 0;
  return new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 }).format(number);
}

function rootPrefix() {
  if (location.protocol !== "file:") return "";
  const path = location.pathname;
  const marker = "/creditcostguide/";
  const idx = path.indexOf(marker);
  if (idx === -1) return "";
  return path.slice(0, idx + marker.length);
}

function localPathFromAbsolute(url) {
  try {
    const parsed = new URL(url);
    if (parsed.origin !== site.domain) return null;
    let pathname = parsed.pathname;
    if (pathname === "/") pathname = "/index.html";
    return `${rootPrefix()}${pathname.replace(/^\//, "")}`;
  } catch {
    return null;
  }
}

function wireLocalPreviewLinks() {
  if (location.protocol !== "file:") return;
  document.addEventListener("click", (event) => {
    const anchor = event.target.closest("a[href]");
    if (!anchor) return;
    const localTarget = localPathFromAbsolute(anchor.getAttribute("href"));
    if (!localTarget) return;
    event.preventDefault();
    location.href = localTarget;
  });
}

function wireMenu() {
  const button = document.querySelector(".ccg-menu-toggle");
  const nav = document.querySelector(".ccg-mobile-nav");
  if (!button || !nav) return;
  button.addEventListener("click", () => {
    const open = nav.classList.toggle("is-open");
    button.setAttribute("aria-expanded", String(open));
  });
}

function wireCookieBanner() {
  const banner = document.querySelector(".ccg-cookie-banner");
  if (!banner) return;
  const choice = localStorage.getItem("ccg-cookie-choice");
  if (!choice) banner.hidden = false;
  banner.querySelectorAll("[data-cookie-action]").forEach((button) => {
    button.addEventListener("click", () => {
      localStorage.setItem("ccg-cookie-choice", button.dataset.cookieAction);
      banner.hidden = true;
    });
  });
}

function drawCharts() {
  document.querySelectorAll("[data-chart]").forEach((node) => {
    const values = (node.dataset.chart || "").split(",").map(Number).filter((n) => Number.isFinite(n));
    if (values.length < 2) return;
    const width = 280;
    const height = 120;
    const min = Math.min(...values);
    const max = Math.max(...values);
    const range = max - min || 1;
    const step = width / (values.length - 1);
    const points = values.map((value, index) => {
      const x = index * step;
      const y = height - ((value - min) / range) * 82 - 18;
      return `${x},${y}`;
    }).join(" ");
    node.innerHTML = `
      <svg viewBox="0 0 ${width} ${height}" role="img" aria-label="${node.dataset.label || "financial chart"}">
        <defs>
          <linearGradient id="lineGrad" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#80b8ff" />
            <stop offset="100%" stop-color="#1f6fff" />
          </linearGradient>
        </defs>
        <path d="M0 ${height - 10} H${width}" stroke="rgba(16,34,62,0.12)" stroke-width="1" fill="none"></path>
        <polyline points="${points}" fill="none" stroke="url(#lineGrad)" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"></polyline>
      </svg>`;
  });
}

function loanPayment(amount, apr, months) {
  const rate = apr / 100 / 12;
  if (!rate) return amount / months;
  return amount * rate / (1 - Math.pow(1 + rate, -months));
}

function payoffMonths(balance, apr, payment, newCharges = 0) {
  let months = 0;
  let interest = 0;
  let current = balance;
  const rate = apr / 100 / 12;
  while (current > 0.5 && months < 1200) {
    const monthlyInterest = current * rate;
    interest += monthlyInterest;
    current = current + monthlyInterest + newCharges - payment;
    months += 1;
    if (payment <= monthlyInterest + newCharges) return { months: Infinity, interest: Infinity };
  }
  return { months, interest };
}

function updateCalculator(card) {
  const type = card.dataset.calculator;
  const form = card.querySelector("form");
  const result = {
    primary: card.querySelector('[data-result="primary"]'),
    interest: card.querySelector('[data-result="interest"]'),
    term: card.querySelector('[data-result="term"]'),
    note: card.querySelector('[data-result="note"]')
  };
  const data = Object.fromEntries(new FormData(form).entries());
  const num = (key) => Number(data[key] || 0);
  let primary = 0;
  let interest = 0;
  let term = "";
  let note = "";

  if (type === "loan") {
    const amount = num("amount");
    const apr = num("apr");
    const months = num("term");
    primary = loanPayment(amount, apr, months);
    interest = primary * months - amount;
    term = `${months} months`;
    note = "Fixed-rate loan estimate based on standard amortization.";
  }

  if (type === "card") {
    const balance = num("balance");
    const apr = num("apr");
    const payment = num("payment");
    const charges = num("charges");
    const payoff = payoffMonths(balance, apr, payment, charges);
    primary = payment;
    interest = payoff.interest;
    term = Number.isFinite(payoff.months) ? `${payoff.months} months` : "No payoff";
    note = Number.isFinite(payoff.months) ? "Assumes the APR remains steady." : "Payment is too low to cover interest and new charges.";
  }

  if (type === "mortgage") {
    const price = num("price");
    const down = num("down");
    const amount = Math.max(price - down, 0);
    const rate = num("rate");
    const years = num("years");
    const tax = num("tax") / 12;
    const ins = num("ins") / 12;
    const pmi = num("pmi");
    primary = loanPayment(amount, rate, years * 12) + tax + ins + pmi;
    interest = loanPayment(amount, rate, years * 12) * years * 12 - amount;
    term = `${years} years`;
    note = "Includes principal, interest, taxes, insurance, and PMI.";
  }

  if (type === "debt") {
    const balance = num("balance");
    const apr = num("apr");
    const minimum = num("minimum");
    const planned = num("planned");
    const minPayoff = payoffMonths(balance, apr, minimum);
    const fastPayoff = payoffMonths(balance, apr, planned);
    primary = planned;
    interest = (minPayoff.interest || 0) - (fastPayoff.interest || 0);
    term = Number.isFinite(fastPayoff.months) ? `${fastPayoff.months} months` : "No payoff";
    note = Number.isFinite(fastPayoff.months) ? `Estimated interest saved versus minimum payment: ${money(Math.max(interest, 0))}.` : "Planned payment is too low to create payoff progress.";
  }

  if (type === "utilization") {
    const balances = [num("balance1"), num("balance2"), num("balance3")];
    const limits = [num("limit1"), num("limit2"), num("limit3")];
    const totalBalance = balances.reduce((a, b) => a + b, 0);
    const totalLimit = limits.reduce((a, b) => a + b, 0);
    primary = totalLimit ? (totalBalance / totalLimit) * 100 : 0;
    interest = totalBalance;
    term = `${primary.toFixed(1)}% overall`;
    note = `Card-level utilization: ${balances.map((b, i) => limits[i] ? `${((b / limits[i]) * 100).toFixed(1)}%` : "0%").join(", ")}.`;
  }

  result.primary.textContent = type === "utilization" ? `${primary.toFixed(1)}%` : money(primary);
  result.interest.textContent = type === "utilization" ? money(interest) : money(Math.max(interest, 0));
  result.term.textContent = term;
  result.note.textContent = note;
}

function wireCalculators() {
  document.querySelectorAll("[data-calculator]").forEach((card) => {
    const form = card.querySelector("form");
    if (!form) return;
    form.addEventListener("submit", (event) => {
      event.preventDefault();
      updateCalculator(card);
    });
    updateCalculator(card);
  });
}

function injectSchema() {
  const body = document.body;
  const breadcrumbs = parseJSON(body.dataset.breadcrumbs, []);
  const faqs = parseJSON(body.dataset.faqs, []);
  const canonical = document.querySelector('link[rel="canonical"]')?.href || location.href;
  const description = document.querySelector('meta[name="description"]')?.content || "";
  const title = document.title;
  const pageType = body.dataset.pageType || "article";
  const graph = [];

  graph.push({
    "@type": pageType === "home" ? "WebSite" : "WebPage",
    "@id": `${canonical}#page`,
    name: title,
    url: canonical,
    description,
    isPartOf: { "@id": `${site.domain}/#website` }
  });

  graph.push({
    "@type": "Organization",
    "@id": `${site.domain}/#organization`,
    name: site.name,
    url: site.domain,
    logo: { "@type": "ImageObject", url: site.logo }
  });

  graph.push({
    "@type": "WebSite",
    "@id": `${site.domain}/#website`,
    name: site.name,
    url: site.domain,
    publisher: { "@id": `${site.domain}/#organization` }
  });

  if (breadcrumbs.length > 1) {
    graph.push({
      "@type": "BreadcrumbList",
      "@id": `${canonical}#breadcrumbs`,
      itemListElement: breadcrumbs.map((item, index) => ({
        "@type": "ListItem",
        position: index + 1,
        name: item.name,
        item: item.url
      }))
    });
  }

  if (pageType === "calculator") {
    graph.push({
      "@type": "SoftwareApplication",
      "@id": `${canonical}#calculator`,
      name: title,
      applicationCategory: "FinanceApplication",
      operatingSystem: "Web",
      url: canonical,
      description
    });
  } else if (pageType !== "home") {
    graph.push({
      "@type": "Article",
      "@id": `${canonical}#article`,
      headline: title,
      description,
      author: { "@type": "Person", name: "Maya Ellison" },
      publisher: { "@id": `${site.domain}/#organization` },
      mainEntityOfPage: canonical
    });
  }

  if (faqs.length) {
    graph.push({
      "@type": "FAQPage",
      "@id": `${canonical}#faq`,
      mainEntity: faqs.map((item) => ({
        "@type": "Question",
        name: item.q,
        acceptedAnswer: { "@type": "Answer", text: item.a }
      }))
    });
  }

  const script = document.createElement("script");
  script.type = "application/ld+json";
  script.textContent = JSON.stringify({ "@context": "https://schema.org", "@graph": graph });
  document.head.appendChild(script);
}

function wireContactForm() {
  const form = document.querySelector("[data-contact-form]");
  if (!form) return;
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    const status = form.querySelector("[data-contact-status]");
    if (status) status.textContent = "Thanks for your message. This static demo records nothing and is intended for layout preview only.";
    form.reset();
  });
}

wireLocalPreviewLinks();
wireMenu();
wireCookieBanner();
drawCharts();
wireCalculators();
injectSchema();
wireContactForm();
