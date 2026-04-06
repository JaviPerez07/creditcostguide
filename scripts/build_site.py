from __future__ import annotations

import html
import json
import math
import os
import re
import textwrap
from pathlib import Path
from typing import Dict, List, Tuple


SITE_NAME = "CreditCostGuide"
DOMAIN = "https://creditcostguide.com"
TARGET = Path("/Users/javiperezz7/Documents/creditcostguide")


PILLARS = [
    {
        "path": "pages/personal-loans-guide.html",
        "title": "Personal Loans Guide: APRs, Fees, Monthly Costs, and Smart Borrowing Strategies",
        "description": "Understand how U.S. personal loans are priced, what drives APRs, how origination fees affect payoff, and when a fixed monthly payment makes sense.",
        "hero": "Price personal loans with more confidence",
        "summary": "This guide explains how lenders set rates, how fees change your total cost, and how to compare loan offers with realistic monthly payment examples.",
        "topics": ["APR pricing", "Origination fees", "Prepayment rules", "Debt consolidation", "Affordable payment sizing", "Approval factors"],
        "faqs": [
            ["What is a good APR for a personal loan?", "A good APR depends on credit score, income stability, and debt-to-income ratio, but well-qualified borrowers often see lower single-digit or low double-digit offers while riskier profiles can cost much more."],
            ["Does an origination fee matter if the monthly payment looks affordable?", "Yes. An origination fee can reduce the amount you actually receive while leaving the scheduled payment nearly unchanged, which raises the true borrowing cost."],
            ["Are personal loans better than credit cards for debt payoff?", "They can be if the APR is lower, the term is short enough to avoid excess interest, and you do not run balances back up after consolidating."],
        ],
    },
    {
        "path": "pages/credit-cards-guide.html",
        "title": "Credit Cards Guide: Interest Charges, Annual Fees, Rewards Math, and Balance Strategies",
        "description": "Learn how U.S. credit card costs work, from APR and grace periods to annual fees, utilization, balance transfers, and reward break-even calculations.",
        "hero": "Know what your credit card really costs",
        "summary": "This page breaks down revolving interest, annual fees, penalty pricing, utilization impacts, and how to compare rewards with real household spending examples.",
        "topics": ["APR and grace periods", "Annual fee tradeoffs", "Rewards valuation", "Balance transfers", "Late fees", "Utilization management"],
        "faqs": [
            ["Why does carrying a balance erase the value of rewards?", "Because interest charges can exceed cashback or points value very quickly, especially when balances revolve for several billing cycles."],
            ["When is a balance transfer worth it?", "A transfer can help when the intro offer lasts long enough, the transfer fee is reasonable, and the repayment plan fits inside the promotional window."],
            ["How much of my credit limit should I use?", "Staying well below your limit usually helps your profile, and many borrowers aim for low utilization both overall and on each card."],
        ],
    },
    {
        "path": "pages/mortgage-guide.html",
        "title": "Mortgage Guide: Rates, Closing Costs, Escrows, and the True Cost of Home Financing",
        "description": "Compare U.S. mortgage costs with a full breakdown of interest rates, points, PMI, escrow, taxes, insurance, and affordability planning.",
        "hero": "Decode the full cost of a mortgage",
        "summary": "Mortgage costs go far beyond principal and interest. This guide covers rate shopping, closing costs, escrow, PMI, and the tradeoffs behind term and down payment choices.",
        "topics": ["Rate shopping", "Discount points", "PMI and MIP", "Escrow costs", "Affordability rules", "Refinance readiness"],
        "faqs": [
            ["How much house can I afford?", "Affordability depends on your income, taxes, insurance, debt obligations, savings, and the payment level you can sustain without crowding out other priorities."],
            ["What are mortgage points?", "Points are optional upfront fees paid to reduce the interest rate. They can make sense if you expect to keep the loan long enough to break even."],
            ["Why is my housing payment higher than the quoted principal and interest?", "Taxes, homeowners insurance, mortgage insurance, and HOA dues often push the all-in monthly payment significantly higher."],
        ],
    },
    {
        "path": "pages/credit-score-guide.html",
        "title": "Credit Score Guide: How Scores Are Calculated and How Better Credit Lowers Borrowing Costs",
        "description": "See how payment history, utilization, account age, mix, and new credit affect U.S. credit scores and the rates lenders may offer.",
        "hero": "Understand how credit scores change borrowing costs",
        "summary": "This guide connects credit behavior to loan pricing, insurance-adjacent banking decisions, and practical strategies for improving approval odds without gimmicks.",
        "topics": ["Score factors", "Utilization timing", "Hard inquiries", "Credit mix", "Rebuilding credit", "Rate impact"],
        "faqs": [
            ["How fast can a credit score improve?", "Some changes like lower reported balances can help quickly, while rebuilding payment history and account age usually takes longer."],
            ["Do checking accounts affect credit scores?", "Standard checking and savings accounts typically do not report to the major credit bureaus unless an account goes unpaid and is sent to collections."],
            ["Can paying off a loan hurt my score?", "A score can dip temporarily because the account closes and your mix changes, but lower debt and stronger finances usually matter more over time."],
        ],
    },
    {
        "path": "pages/banking-fees-guide.html",
        "title": "Banking Fees Guide: Monthly Charges, Overdrafts, ATM Costs, and How to Avoid Paying More",
        "description": "Review common U.S. bank account fees, including maintenance charges, overdrafts, wire fees, ATM surcharges, and account minimum requirements.",
        "hero": "Cut avoidable banking fees",
        "summary": "From overdraft rules to account minimums, this guide shows where routine banking costs hide and how consumers can choose lower-friction account structures.",
        "topics": ["Monthly fees", "Overdraft pricing", "ATM charges", "Wire and transfer costs", "Minimum balance rules", "No-fee alternatives"],
        "faqs": [
            ["Are overdraft fees still common?", "Yes, although many banks have reduced or removed them, overdraft practices still vary widely and should be reviewed before opening an account."],
            ["What is the cheapest checking account setup?", "A practical low-cost setup often combines a no-monthly-fee checking account, in-network ATM access, and overdraft controls turned on."],
            ["Do credit unions usually charge fewer fees?", "Many credit unions offer competitive fee structures, but the best choice still depends on branch access, ATM reach, and account features."],
        ],
    },
    {
        "path": "pages/debt-payoff-guide.html",
        "title": "Debt Payoff Guide: Interest Priorities, Cash Flow Planning, and Faster Repayment Strategies",
        "description": "Build a U.S.-focused debt payoff plan with avalanche and snowball methods, cash flow sequencing, refinancing considerations, and payoff timelines.",
        "hero": "Build a debt payoff plan that fits real cash flow",
        "summary": "This guide compares payoff methods, emergency fund tradeoffs, refinancing triggers, and budgeting decisions that matter when interest costs keep growing.",
        "topics": ["Avalanche vs snowball", "Cash flow strategy", "Emergency fund balance", "Consolidation analysis", "Late payment avoidance", "Timeline planning"],
        "faqs": [
            ["Is the debt avalanche always best?", "It usually minimizes total interest, but some households stick with repayment better when they also get motivation from quick wins."],
            ["Should I save or pay off debt first?", "Most people benefit from a small emergency buffer before aggressively paying down debt so surprise expenses do not force new borrowing."],
            ["Does debt consolidation solve the problem by itself?", "No. It only helps when the new terms are better and spending habits do not recreate the old balances."],
        ],
    },
    {
        "path": "pages/refinancing-guide.html",
        "title": "Refinancing Guide: When Lower Rates, New Terms, and Fee Tradeoffs Actually Save Money",
        "description": "See how refinancing works for mortgages, auto loans, personal loans, and student loans, including break-even math, fees, and repayment timing.",
        "hero": "Refinance when the math actually works",
        "summary": "Refinancing can reduce monthly costs or total interest, but fees, reset terms, and lost borrower protections can offset the benefit. This guide shows how to weigh it all.",
        "topics": ["Rate reduction math", "Term reset risks", "Closing and transfer fees", "Cash-out caution", "Borrower protections", "Break-even timing"],
        "faqs": [
            ["How much lower should the new rate be before refinancing?", "There is no universal threshold. The better test is whether projected savings exceed fees before you expect to sell, repay, or refinance again."],
            ["Can refinancing increase total cost even with a lower payment?", "Yes. Extending the repayment term can lower the monthly bill while increasing total interest paid."],
            ["What documents are usually needed?", "Income verification, recent statements, property or payoff information, and identity documents are commonly requested."],
        ],
    },
    {
        "path": "pages/student-loans-guide.html",
        "title": "Student Loans Guide: Federal vs Private Costs, Repayment Plans, and Refinancing Tradeoffs",
        "description": "Understand federal and private student loan costs, capitalization, repayment options, refinancing tradeoffs, and long-term budget planning.",
        "hero": "Compare student loan costs with fewer surprises",
        "summary": "This guide explains how federal and private student loans are priced, what repayment plans change the timeline, and where refinancing can help or hurt.",
        "topics": ["Federal vs private", "Capitalized interest", "Income-driven repayment", "Refinancing pros and cons", "Grace periods", "Borrower protections"],
        "faqs": [
            ["Why are federal and private student loans so different?", "Federal loans come with standardized benefits and protections while private lenders price risk individually and may offer fewer relief options."],
            ["What is capitalized interest?", "It is unpaid interest that gets added to the principal balance, causing future interest charges to grow from a higher starting amount."],
            ["Should I refinance federal student loans?", "Only after carefully weighing the loss of federal protections, repayment flexibility, and any forgiveness-related options."],
        ],
    },
]


SUPPORTING = [
    ("pages/best-credit-cards-for-bad-credit.html", "Best Credit Cards for Bad Credit: Features, Fees, Deposits, and Rebuilding Tactics", "Compare secured and starter cards for borrowers rebuilding credit, with attention to annual fees, deposit size, utilization, and reporting practices."),
    ("pages/how-credit-scores-work.html", "How Credit Scores Work: The Factors Behind Pricing, Approval, and Risk", "Learn the main scoring components, why lenders care, and how changes in balances, payment history, and account age can affect borrowing costs."),
    ("pages/how-to-lower-credit-card-interest.html", "How to Lower Credit Card Interest: Negotiation, Transfers, and Repayment Moves", "See practical ways to reduce credit card APR costs, including issuer calls, balance transfers, hardship programs, and disciplined repayment steps."),
    ("pages/personal-loan-vs-credit-card.html", "Personal Loan vs Credit Card: Which Costs Less for Planned and Emergency Spending?", "Compare installment loans and revolving credit for emergency bills, projects, and debt payoff with examples using APR, fees, and repayment speed."),
    ("pages/how-much-house-can-i-afford.html", "How Much House Can I Afford? Budget Ratios, Closing Costs, and Payment Buffers", "Estimate safe home affordability by looking beyond lender maximums to taxes, insurance, repairs, reserves, and debt obligations."),
    ("pages/fixed-vs-variable-rate-loans.html", "Fixed vs Variable Rate Loans: Stability, Risk, and Total Cost Tradeoffs", "Review how fixed and variable rates behave across credit products and when payment certainty matters more than a lower starting rate."),
    ("pages/how-to-refinance-a-loan.html", "How to Refinance a Loan: Step-by-Step Cost Review and Approval Prep", "Follow the refinance process from rate shopping to document prep, break-even checks, and lender comparison."),
    ("pages/best-banks-with-no-fees.html", "Best Banks With No Fees: What to Look For in Checking and Savings Accounts", "Compare the features behind low-fee banking, including ATM access, overdraft policy, transfer tools, and minimum balance rules."),
    ("pages/average-credit-card-interest-rate.html", "Average Credit Card Interest Rate: What Consumers Pay and What Changes the Number", "Understand average card APR ranges, why pricing differs by credit profile, and how issuers evaluate risk."),
    ("pages/what-is-apr.html", "What Is APR? How Annual Percentage Rate Measures Loan and Credit Costs", "APR combines interest and certain fees into a borrowing cost metric that helps compare credit products more fairly."),
    ("pages/how-to-improve-credit-score-fast.html", "How to Improve Credit Score Fast: The Changes Most Likely to Help Soonest", "Focus on utilization, reporting timing, and error correction strategies that can move a score faster than long-horizon tactics."),
    ("pages/what-happens-if-you-miss-a-loan-payment.html", "What Happens If You Miss a Loan Payment? Fees, Reporting, and Recovery Steps", "Review the financial and credit consequences of missed payments and the smartest steps to take before and after one happens."),
    ("pages/how-to-pay-off-debt-faster.html", "How to Pay Off Debt Faster: Extra Payment Tactics, Budget Moves, and Motivation Systems", "Learn how small payment increases, interest prioritization, and cash flow systems can shorten debt payoff meaningfully."),
    ("pages/student-loan-refinancing-guide.html", "Student Loan Refinancing Guide: Rates, Cosigners, and Federal Benefit Tradeoffs", "Compare refinance savings against borrower protections, term choices, and qualification requirements for student debt."),
    ("pages/debt-snowball-vs-avalanche.html", "Debt Snowball vs Avalanche: Cost Savings, Momentum, and When Each Method Fits", "See how the two major payoff strategies affect total interest, behavior, and household budgeting."),
    ("pages/mortgage-closing-costs-guide.html", "Mortgage Closing Costs Guide: Lender Fees, Third-Party Charges, and Cash-to-Close Planning", "Break down origination charges, title costs, prepaid items, and negotiation areas so closing-day cash needs are less surprising."),
    ("pages/balance-transfer-credit-cards-guide.html", "Balance Transfer Credit Cards Guide: Promo Windows, Fees, and Payoff Deadlines", "Use balance transfer offers more safely by understanding transfer fees, deferred timelines, and payoff pacing."),
    ("pages/secured-vs-unsecured-loans.html", "Secured vs Unsecured Loans: Collateral Risk, APR Differences, and Approval Factors", "Compare collateral-backed and unsecured borrowing with practical examples on pricing, access, and downside risk."),
    ("pages/checking-vs-savings-account.html", "Checking vs Savings Account: Liquidity, Yield, Fees, and Best Use Cases", "Review when to keep money accessible in checking, when savings yields matter, and how to avoid common account costs."),
    ("pages/how-much-does-a-personal-loan-cost.html", "How Much Does a Personal Loan Cost? APR, Fees, and Amortization Explained", "Calculate the true cost of a personal loan by combining payment schedules, fees, and payoff timing."),
]


CALCULATORS = [
    ("pages/loan-payment-calculator.html", "Loan Payment Calculator: Estimate Monthly Cost and Total Interest", "Estimate installment loan payments using principal, APR, and term length with quick side-by-side comparisons.", "loan"),
    ("pages/credit-card-interest-calculator.html", "Credit Card Interest Calculator: Project Carrying Costs and Payoff Paths", "Model how revolving balances grow based on APR, payment size, and new spending assumptions.", "card"),
    ("pages/mortgage-calculator.html", "Mortgage Calculator: Principal, Interest, Taxes, Insurance, and PMI", "Estimate housing payments with mortgage principal, rate, term, taxes, insurance, and down payment assumptions.", "mortgage"),
    ("pages/debt-payoff-calculator.html", "Debt Payoff Calculator: Compare Repayment Speed and Interest Saved", "Compare minimum-payment debt payoff against a faster monthly budget to see time and interest differences.", "debt"),
    ("pages/credit-utilization-calculator.html", "Credit Utilization Calculator: Measure Balance-to-Limit Ratios", "Check utilization by card and overall to see how revolving balances may affect credit health.", "utilization"),
]


ROOT_PAGES = [
    ("index.html", "CreditCostGuide: Credit, Loans, APRs, Fees, Refinancing, and Cost Calculators", "Explore U.S.-focused guides and calculators for credit cards, personal loans, mortgages, debt payoff, banking fees, refinancing, and credit scores.", "home"),
    ("about.html", "About CreditCostGuide", "Learn how CreditCostGuide approaches educational financial content, editorial standards, and reader-first explanations.", "article"),
    ("contact.html", "Contact CreditCostGuide", "Use the contact page to send editorial questions, corrections, partnership inquiries, and general feedback to CreditCostGuide.", "article"),
    ("how-we-research.html", "How We Research Financial Costs and Product Pricing", "See the research framework behind CreditCostGuide content, including source review, pricing comparisons, and update practices.", "article"),
    ("privacy-policy.html", "Privacy Policy | CreditCostGuide", "Review how CreditCostGuide handles analytics, cookies, contact submissions, and reader privacy preferences.", "legal"),
    ("terms.html", "Terms of Use | CreditCostGuide", "Read the terms that govern use of CreditCostGuide content, calculators, and site features.", "legal"),
    ("disclaimer.html", "Disclaimer | CreditCostGuide", "Understand the informational-only nature of CreditCostGuide content and the limits of calculators, examples, and editorial material.", "legal"),
]


AUTHOR = {
    "name": "Maya Ellison",
    "role": "Senior Personal Finance Editor",
    "bio": "Maya covers borrowing costs, banking fees, mortgage pricing, and payoff strategy with a focus on plain-English explanations and realistic household budgeting.",
}


NAV_ITEMS = [
    ("/", "Home"),
    ("/pages/personal-loans-guide.html", "Personal Loans"),
    ("/pages/credit-cards-guide.html", "Credit Cards"),
    ("/pages/mortgage-guide.html", "Mortgages"),
    ("/pages/debt-payoff-guide.html", "Debt Payoff"),
    ("/pages/loan-payment-calculator.html", "Calculators"),
]


DISCLAIM = "This content is for informational purposes only and does not constitute financial advice."


def title_from_path(path: str) -> str:
    slug = Path(path).stem.replace("-", " ")
    return " ".join(word.capitalize() for word in slug.split())


def url_for(path: str) -> str:
    if path == "index.html":
        return f"{DOMAIN}/"
    return f"{DOMAIN}/{path}"


def local_href(path: str) -> str:
    return url_for(path)


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def write(path: Path, content: str) -> None:
    ensure_dir(path.parent)
    path.write_text(content, encoding="utf-8")


def trim(s: str) -> str:
    return textwrap.dedent(s).strip() + "\n"


def words(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", re.sub(r"<[^>]+>", " ", text)))


def breadcrumb_items(path: str, page_title: str) -> List[Dict[str, str]]:
    items = [{"name": "Home", "url": f"{DOMAIN}/"}]
    if path.startswith("pages/"):
        items.append({"name": "Guides", "url": f"{DOMAIN}/pages/personal-loans-guide.html"})
    elif path not in {"index.html"}:
        items.append({"name": "Company", "url": f"{DOMAIN}/about.html"})
    if path != "index.html":
        items.append({"name": page_title, "url": url_for(path)})
    return items


def breadcrumb_html(items: List[Dict[str, str]]) -> str:
    links = []
    for idx, item in enumerate(items):
        current = ' aria-current="page"' if idx == len(items) - 1 else ""
        links.append(f'<a href="{html.escape(item["url"])}"{current}>{html.escape(item["name"])}</a>')
    return f'<nav class="ccg-breadcrumbs" aria-label="Breadcrumb">{"<span>/</span>".join(links)}</nav>'


def slug_value(path: str) -> str:
    return Path(path).stem


def generate_paragraph(topic: str, section: str, page_title: str, index: int) -> str:
    scenarios = [
        "a borrower comparing two lenders with the same monthly payment but different upfront fees",
        "a household balancing emergency savings against a faster payoff plan",
        "a rate shopper evaluating whether a lower APR offsets transfer or closing costs",
        "a family reviewing how taxes, insurance, and debt obligations affect a realistic monthly budget",
        "a consumer deciding whether convenience features are worth ongoing account charges",
    ]
    figures = [
        "$8,000 at 11.9% APR over 36 months",
        "$15,000 at 9.4% APR with a 4% fee",
        "$275,000 financed over 30 years with taxes and insurance added",
        "$4,200 revolving at 24.99% with only minimum payments",
        "$18,500 refinanced into a shorter term with a lower rate",
    ]
    compliance = [
        "Federal disclosures can help, but shoppers still need to compare APR, fees, and timing side by side.",
        "A lower monthly payment does not automatically mean a lower total borrowing cost.",
        "Cash-flow resilience matters because tight budgets often turn one missed payment into several new problems.",
        "Looking at the total cost over the expected holding period usually produces a better decision than focusing on teaser pricing alone.",
        "Credit profile, income stability, and debt-to-income ratio often matter just as much as the headline rate.",
    ]
    return (
        f"<p>{html.escape(section)} matters in {html.escape(page_title.lower())} because lenders and consumers are usually solving for "
        f"more than one goal at once. In practice, this often looks like {scenarios[index % len(scenarios)]}. "
        f"A simple example is {figures[index % len(figures)]}, where the quote only becomes truly useful after you factor in fees, repayment speed, and what the borrower needs from the transaction. "
        f"{compliance[index % len(compliance)]} When reviewing {html.escape(topic.lower())}, it helps to compare best-case marketing language against a conservative budget that assumes rates can change, life expenses can surprise you, and the cheapest option on paper may not be the easiest plan to maintain.</p>"
    )


def comparison_table(topic: str) -> str:
    headers = ["Scenario", "Estimated APR", "Fee Range", "Key Watchout"]
    rows = [
        ["Prime-credit offer", "6% to 10%", "0% to 3%", "Promotional rate may not last on revolving credit"],
        ["Mid-tier profile", "10% to 18%", "1% to 6%", "Fees can erase a modest rate advantage"],
        ["High-risk profile", "18% to 30%+", "0% to 10%", "Payment stress increases quickly"],
        ["Refinance option", "Varies", "0% to 5%", "Break-even period matters most"],
    ]
    table_rows = "".join(
        f"<tr><td>{html.escape(r[0])}</td><td>{html.escape(r[1])}</td><td>{html.escape(r[2])}</td><td>{html.escape(r[3])}</td></tr>"
        for r in rows
    )
    return trim(
        f"""
        <section class="ccg-section">
          <div class="ccg-section-head">
            <p class="ccg-kicker">Comparison Table</p>
            <h2>How shoppers can benchmark {html.escape(topic.lower())}</h2>
          </div>
          <div class="ccg-table-wrap">
            <table class="ccg-table">
              <thead><tr>{''.join(f'<th>{html.escape(h)}</th>' for h in headers)}</tr></thead>
              <tbody>{table_rows}</tbody>
            </table>
          </div>
        </section>
        """
    )


def mini_chart(values: List[int], label: str) -> str:
    data = ",".join(str(v) for v in values)
    return f'<div class="ccg-chart-card"><div class="ccg-chart" data-chart="{data}" data-label="{html.escape(label)}"></div></div>'


def faq_html(faqs: List[List[str]]) -> str:
    items = []
    for q, a in faqs:
        items.append(
            f"<details class=\"ccg-faq-item\"><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>"
        )
    return trim(
        f"""
        <section class="ccg-section">
          <div class="ccg-section-head">
            <p class="ccg-kicker">FAQ</p>
            <h2>Common questions</h2>
          </div>
          <div class="ccg-faq-grid">
            {''.join(items)}
          </div>
        </section>
        """
    )


def author_box() -> str:
    return trim(
        f"""
        <section class="ccg-author-box" aria-label="Author information">
          <div class="ccg-author-mark">ME</div>
          <div>
            <p class="ccg-author-label">Written by</p>
            <h2>{html.escape(AUTHOR["name"])}</h2>
            <p class="ccg-author-role">{html.escape(AUTHOR["role"])}</p>
            <p>{html.escape(AUTHOR["bio"])}</p>
          </div>
        </section>
        """
    )


def related_html(paths: List[str]) -> str:
    items = []
    for path in paths[:4]:
        items.append(
            f'<a class="ccg-related-card" href="{html.escape(local_href(path))}"><span>Related Article</span><strong>{html.escape(title_from_path(path))}</strong></a>'
        )
    return trim(
        f"""
        <section class="ccg-section">
          <div class="ccg-section-head">
            <p class="ccg-kicker">Keep Exploring</p>
            <h2>Related articles and tools</h2>
          </div>
          <div class="ccg-related-grid">
            {''.join(items)}
          </div>
        </section>
        """
    )


def disclaimer_html() -> str:
    return f'<div class="ccg-disclaimer" role="note">{html.escape(DISCLAIM)}</div>'


def section_block(topic: str, page_title: str, index: int) -> str:
    subheads = [
        "Why this cost category matters",
        "How pricing changes by borrower profile",
        "Where comparison shopping often goes wrong",
        "Budget examples that keep costs realistic",
        "How to reduce downside risk",
    ]
    paragraphs = "".join(generate_paragraph(topic, f"{topic} {subheads[(index + i) % len(subheads)]}", page_title, index + i) for i in range(4))
    list_items = [
        "Compare the all-in cost, not just the monthly payment.",
        "Review fees, timing, and rate adjustment rules before signing.",
        "Use conservative household cash-flow assumptions in every example.",
        "Check whether a lower payment simply extends the repayment timeline.",
    ]
    bullets = "".join(f"<li>{html.escape(item)}</li>" for item in list_items)
    return trim(
        f"""
        <section class="ccg-section">
          <div class="ccg-section-head">
            <p class="ccg-kicker">Deep Dive {index + 1}</p>
            <h2>{html.escape(topic)}</h2>
          </div>
          {paragraphs}
          <ul class="ccg-list">{bullets}</ul>
          {mini_chart([42 + index * 2, 51 + index, 47 + index * 2, 58 + index, 64 + index], f"{topic} trend")}
        </section>
        """
    )


def article_body(config: Dict[str, object], min_words: int, related_paths: List[str]) -> str:
    sections = [section_block(str(topic), str(config["title"]), idx) for idx, topic in enumerate(config["topics"])]
    content = "".join(sections)
    content += comparison_table(str(config["hero"]))
    content += faq_html(config["faqs"])
    content += author_box()
    content += related_html(related_paths)
    while words(content) < min_words:
        idx = len(re.findall(r"<section class=\"ccg-section\">", content))
        extra_topic = f"{config['hero']} scenario planning {idx}"
        content += section_block(extra_topic, str(config["title"]), idx)
    return content


def support_body(path: str, title: str, desc: str, related_paths: List[str]) -> Tuple[str, List[List[str]]]:
    core = title.replace(":", "").split(" ")
    focus = " ".join(core[:4])
    faqs = [
        [f"What should readers compare first in {focus.lower()}?", "Start with the all-in cost, then test whether the monthly payment still works once fees, timing, and normal living expenses are included."],
        [f"How can someone use {focus.lower()} information responsibly?", "Use examples as planning guides, confirm lender or bank disclosures directly, and revisit the numbers if rates or income change."],
        [f"Which mistake raises costs most often in {focus.lower()} decisions?", "Many consumers focus on a teaser monthly payment and underestimate the impact of fees, longer repayment, or renewed borrowing afterward."],
    ]
    topics = [
        "Cost mechanics",
        "Rate comparison examples",
        "Budget planning",
        "Fee analysis",
        "Household scenarios",
    ]
    temp = {"hero": title, "title": title, "topics": topics, "faqs": faqs}
    content = article_body(temp, 1500, related_paths)
    intro = trim(
        f"""
        <section class="ccg-section">
          <div class="ccg-section-head">
            <p class="ccg-kicker">Overview</p>
            <h2>{html.escape(title)}</h2>
          </div>
          <p>{html.escape(desc)} This article is written for U.S. readers who want realistic examples, not marketing gloss. It highlights how fees, APR, term length, and everyday cash flow interact when you borrow, refinance, or choose between financial products.</p>
          <p>Because pricing changes with credit profile and lender policy, the most useful comparison usually starts with a worksheet: amount needed, expected repayment speed, likely fees, and the downside of a missed payment. That framework helps translate broad averages into a decision you can actually live with.</p>
        </section>
        """
    )
    return intro + content, faqs


def calculator_intro(title: str, desc: str) -> str:
    return trim(
        f"""
        <section class="ccg-section">
          <div class="ccg-section-head">
            <p class="ccg-kicker">Interactive Tool</p>
            <h2>{html.escape(title)}</h2>
          </div>
          <p>{html.escape(desc)} Use the inputs below to test a conservative scenario and then adjust assumptions. The most reliable estimate usually comes from pairing the calculator with lender disclosures and a realistic monthly budget.</p>
          <p>These examples are educational and U.S.-focused. Numbers may differ based on credit profile, state-specific taxes or fees, and the terms of the exact financial product you choose.</p>
        </section>
        """
    )


def calculator_module(calc_type: str) -> str:
    config = {
        "loan": {
            "fields": [
                ("Amount", "amount", "15000"),
                ("APR (%)", "apr", "10.5"),
                ("Term (months)", "term", "48"),
            ],
            "legend": "Loan payment results",
        },
        "card": {
            "fields": [
                ("Balance", "balance", "4200"),
                ("APR (%)", "apr", "24.99"),
                ("Monthly payment", "payment", "175"),
                ("New monthly charges", "charges", "0"),
            ],
            "legend": "Credit card payoff results",
        },
        "mortgage": {
            "fields": [
                ("Home price", "price", "425000"),
                ("Down payment", "down", "85000"),
                ("Rate (%)", "rate", "6.75"),
                ("Term (years)", "years", "30"),
                ("Annual taxes", "tax", "5400"),
                ("Annual insurance", "ins", "1800"),
                ("Monthly PMI", "pmi", "145"),
            ],
            "legend": "Mortgage estimate results",
        },
        "debt": {
            "fields": [
                ("Starting balance", "balance", "12000"),
                ("APR (%)", "apr", "19.99"),
                ("Minimum payment", "minimum", "320"),
                ("Planned payment", "planned", "475"),
            ],
            "legend": "Debt payoff comparison",
        },
        "utilization": {
            "fields": [
                ("Card 1 balance", "balance1", "800"),
                ("Card 1 limit", "limit1", "3000"),
                ("Card 2 balance", "balance2", "1200"),
                ("Card 2 limit", "limit2", "5000"),
                ("Card 3 balance", "balance3", "0"),
                ("Card 3 limit", "limit3", "2500"),
            ],
            "legend": "Utilization results",
        },
    }[calc_type]
    inputs = "".join(
        f'<label><span>{html.escape(label)}</span><input inputmode="decimal" name="{html.escape(name)}" value="{html.escape(value)}"></label>'
        for label, name, value in config["fields"]
    )
    return trim(
        f"""
        <section class="ccg-section">
          <div class="ccg-calc-card" data-calculator="{html.escape(calc_type)}">
            <form class="ccg-calc-form">
              {inputs}
              <button class="ccg-button" type="submit">Calculate</button>
            </form>
            <div class="ccg-calc-output" aria-live="polite">
              <h3>{html.escape(config["legend"])}</h3>
              <div class="ccg-result-grid">
                <div><span>Monthly result</span><strong data-result="primary">$0</strong></div>
                <div><span>Total interest</span><strong data-result="interest">$0</strong></div>
                <div><span>Payoff time</span><strong data-result="term">0 months</strong></div>
                <div><span>Notes</span><strong data-result="note">Enter values and calculate.</strong></div>
              </div>
            </div>
          </div>
        </section>
        """
    )


def calculator_body(path: str, title: str, desc: str, calc_type: str, related_paths: List[str]) -> Tuple[str, List[List[str]]]:
    faqs = [
        ["How accurate are calculator results?", "The calculators are directional planning tools. Actual rates, fees, taxes, and product rules can differ by lender and borrower profile."],
        ["Why should I test more than one scenario?", "Changing rates, fees, payment size, or term length can dramatically alter total cost, so conservative and best-case scenarios are both useful."],
        ["Should I rely on the monthly payment alone?", "No. A lower monthly payment can still be a worse deal if it adds fees or extends the timeline significantly."],
    ]
    topics = ["Interpret the output", "Compare realistic scenarios", "Use the calculator with lender quotes"]
    temp = {"hero": title, "title": title, "topics": topics, "faqs": faqs}
    content = calculator_intro(title, desc) + calculator_module(calc_type) + article_body(temp, 500, related_paths)
    return content, faqs


def simple_page_body(title: str, desc: str, related_paths: List[str], legal: bool = False) -> Tuple[str, List[List[str]]]:
    faqs = [
        [f"What should readers know about {title.lower()}?", "The goal is to explain how this page works in plain language, what readers can expect, and where content is informational rather than personalized advice."],
        [f"How often is {title.lower()} reviewed?", "Editorial and policy pages should be revisited when site practices, contact information, legal language, or measurement tools change."],
        [f"Can readers rely on {title.lower()} for personal recommendations?", "No. Site materials are educational and should be paired with direct professional or provider guidance for personal decisions."],
    ]
    topics = ["Purpose and scope", "What information readers can expect", "How the page supports informed decisions", "Important limits and disclosures"]
    temp = {"hero": title, "title": title, "topics": topics, "faqs": faqs}
    intro = trim(
        f"""
        <section class="ccg-section">
          <div class="ccg-section-head">
            <p class="ccg-kicker">{'Policy' if legal else 'Institutional'}</p>
            <h2>{html.escape(title)}</h2>
          </div>
          <p>{html.escape(desc)} CreditCostGuide is designed for U.S. readers who want clearer explanations of borrowing costs, banking fees, mortgage pricing, and payoff strategy. This page explains how the site handles its responsibilities in that context.</p>
          <p>{'Legal and policy language can feel dense, so this version aims for clarity without removing important limitations.' if legal else 'Transparency matters, especially in finance. We explain research methods, editorial goals, and communication channels so readers know how to interpret what they find here.'}</p>
        </section>
        """
    )
    content = intro + article_body(temp, 1000 if legal else 800, related_paths)
    return content, faqs


def home_body() -> str:
    pillar_cards = "".join(
        f'<a class="ccg-topic-card" href="{local_href(item["path"])}"><span>{html.escape(item["hero"])}</span><strong>{html.escape(title_from_path(item["path"]))}</strong><p>{html.escape(item["description"])}</p></a>'
        for item in PILLARS
    )
    calc_cards = "".join(
        f'<a class="ccg-topic-card ccg-topic-card--small" href="{local_href(path)}"><span>Calculator</span><strong>{html.escape(title_from_path(path))}</strong><p>{html.escape(desc)}</p></a>'
        for path, _, desc, _ in CALCULATORS
    )
    spotlight = "".join(
        f'<a class="ccg-spotlight-item" href="{local_href(path)}">{html.escape(title)}</a>'
        for path, title, _ in SUPPORTING[:6]
    )
    return trim(
        f"""
        <section class="ccg-hero-home">
          <div class="ccg-hero-copy">
            <p class="ccg-kicker">U.S. Personal Finance Costs</p>
            <h1>Compare borrowing costs, bank fees, and payoff timelines without the jargon.</h1>
            <p>CreditCostGuide helps readers understand APR, fees, refinancing tradeoffs, mortgage costs, credit card interest, and credit score dynamics with calculators and long-form explainers built for real budgets.</p>
            <div class="ccg-hero-actions">
              <a class="ccg-button" href="{local_href('pages/loan-payment-calculator.html')}">Open Calculators</a>
              <a class="ccg-button ccg-button--ghost" href="{local_href('pages/credit-cards-guide.html')}">Read Credit Card Guide</a>
            </div>
            <div class="ccg-metrics">
              <div><strong>40</strong><span>Standalone pages</span></div>
              <div><strong>5</strong><span>Working calculators</span></div>
              <div><strong>100%</strong><span>Educational focus</span></div>
            </div>
          </div>
          <div class="ccg-hero-visual">
            <div class="ccg-glass-card">
              <p>Estimated savings after refinance review</p>
              <strong>$238/mo</strong>
              {mini_chart([18, 22, 26, 24, 29, 34, 38], 'Savings trend')}
            </div>
            <div class="ccg-glass-card ccg-glass-card--alt">
              <p>Credit utilization snapshot</p>
              <strong>17%</strong>
              {mini_chart([31, 28, 26, 24, 20, 18, 17], 'Utilization trend')}
            </div>
          </div>
        </section>
        <section class="ccg-section ccg-section--soft">
          <div class="ccg-section-head">
            <p class="ccg-kicker">Pillar Guides</p>
            <h2>Start with the big cost categories</h2>
          </div>
          <div class="ccg-topic-grid">{pillar_cards}</div>
        </section>
        <section class="ccg-section">
          <div class="ccg-section-head">
            <p class="ccg-kicker">Calculators</p>
            <h2>Estimate payments, interest, and utilization</h2>
          </div>
          <div class="ccg-topic-grid ccg-topic-grid--small">{calc_cards}</div>
        </section>
        <section class="ccg-section ccg-section--soft">
          <div class="ccg-section-head">
            <p class="ccg-kicker">Popular Reads</p>
            <h2>Deep dives on APR, payoff methods, and loan decisions</h2>
          </div>
          <div class="ccg-spotlight-list">{spotlight}</div>
        </section>
        <section class="ccg-section">
          <div class="ccg-section-head">
            <p class="ccg-kicker">What You Will Find Here</p>
            <h2>Educational content designed for practical comparisons</h2>
          </div>
          <p>Readers often need more than a rate quote. A useful decision also depends on fees, credit profile, liquidity, term length, and the fallback plan if income or expenses shift. CreditCostGuide is organized around those real-world questions. Every guide is written to help compare options in context rather than chase the lowest advertised number.</p>
          <p>Whether you are exploring a personal loan, checking mortgage affordability, trying to lower credit card interest, or simply looking for a bank account with fewer fees, the site is structured to show the mechanics first and the marketing language second. That approach is especially important in consumer finance because a small change in APR or term length can have a much larger effect than it seems.</p>
          <div class="ccg-table-wrap">
            <table class="ccg-table">
              <thead><tr><th>Topic</th><th>Main Cost Drivers</th><th>Helpful Tool</th><th>Common Mistake</th></tr></thead>
              <tbody>
                <tr><td>Credit cards</td><td>APR, annual fee, utilization, transfer fees</td><td>Credit card interest calculator</td><td>Carrying rewards cards without a payoff plan</td></tr>
                <tr><td>Personal loans</td><td>APR, origination fee, term</td><td>Loan payment calculator</td><td>Ignoring fee-adjusted proceeds</td></tr>
                <tr><td>Mortgages</td><td>Rate, taxes, insurance, PMI, closing costs</td><td>Mortgage calculator</td><td>Underestimating all-in monthly housing cost</td></tr>
                <tr><td>Debt payoff</td><td>APR order, payment size, missed-payment risk</td><td>Debt payoff calculator</td><td>Choosing a strategy without cash-flow testing</td></tr>
              </tbody>
            </table>
          </div>
        </section>
        {faq_html([
          ["What does CreditCostGuide cover?", "The site focuses on U.S. credit, loans, banking fees, mortgages, debt payoff, refinancing, and financial calculators built for educational planning."],
          ["Is this site giving financial advice?", "No. The material is informational only and is meant to help readers ask better questions and compare options more clearly."],
          ["How should readers use the calculators?", "Use them to test conservative scenarios, then compare the outputs against official lender or bank disclosures before making a decision."],
        ])}
        {author_box()}
        {related_html([item["path"] for item in PILLARS[:4]] + [CALCULATORS[0][0], CALCULATORS[1][0]])}
        """
    )


def header(active_path: str) -> str:
    nav = "".join(
        f'<a class="{"is-active" if (item[0] == "/" and active_path == "index.html") or item[0].lstrip("/") == active_path else ""}" href="{html.escape(DOMAIN if item[0] == "/" else DOMAIN + item[0])}">{html.escape(item[1])}</a>'
        for item in NAV_ITEMS
    )
    return trim(
        f"""
        <header class="ccg-site-header">
          <div class="ccg-shell ccg-header-row">
            <a class="ccg-brand" href="{DOMAIN}/" aria-label="{SITE_NAME} home">
              <img src="{DOMAIN}/assets/icons/logo.svg" alt="{SITE_NAME} logo">
              <span>{SITE_NAME}</span>
            </a>
            <button class="ccg-menu-toggle" aria-expanded="false" aria-controls="mobile-nav">Menu</button>
            <nav class="ccg-main-nav" aria-label="Primary navigation">{nav}</nav>
          </div>
          <nav class="ccg-mobile-nav" id="mobile-nav" aria-label="Mobile navigation">{nav}</nav>
        </header>
        """
    )


def footer() -> str:
    primary = [
        "pages/personal-loans-guide.html",
        "pages/credit-cards-guide.html",
        "pages/mortgage-guide.html",
        "pages/credit-score-guide.html",
        "pages/banking-fees-guide.html",
        "pages/debt-payoff-guide.html",
        "pages/refinancing-guide.html",
        "pages/student-loans-guide.html",
    ]
    legal = ["about.html", "contact.html", "how-we-research.html", "privacy-policy.html", "terms.html", "disclaimer.html"]
    links1 = "".join(f'<a href="{local_href(p)}">{html.escape(title_from_path(p))}</a>' for p in primary)
    links2 = "".join(f'<a href="{local_href(p)}">{html.escape(title_from_path(p))}</a>' for p in legal)
    return trim(
        f"""
        <footer class="ccg-site-footer">
          <div class="ccg-shell ccg-footer-grid">
            <div>
              <a class="ccg-brand ccg-brand--footer" href="{DOMAIN}/">
                <img src="{DOMAIN}/assets/icons/logo.svg" alt="{SITE_NAME} logo">
                <span>{SITE_NAME}</span>
              </a>
              <p>U.S.-focused educational guides and calculators for borrowing costs, banking fees, credit health, mortgages, and debt payoff.</p>
            </div>
            <div class="ccg-footer-links">{links1}</div>
            <div class="ccg-footer-links">{links2}</div>
          </div>
        </footer>
        """
    )


def html_doc(
    path: str,
    title: str,
    description: str,
    page_type: str,
    main_content: str,
    breadcrumbs: List[Dict[str, str]],
    faqs: List[List[str]] | None = None,
    hero_title: str | None = None,
    hero_summary: str | None = None,
) -> str:
    canonical = url_for(path)
    robots = "index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1"
    breadcrumb_attr = html.escape(json.dumps(breadcrumbs))
    faq_attr = html.escape(json.dumps([{"q": q, "a": a} for q, a in (faqs or [])]))
    hero_title = hero_title or title
    hero_summary = hero_summary or description
    breadcrumb_nav = "" if path == "index.html" else breadcrumb_html(breadcrumbs)
    hero = trim(
        f"""
        <section class="ccg-page-hero">
          <p class="ccg-kicker">{'Calculator' if page_type == 'calculator' else 'Guide' if path.startswith('pages/') else 'CreditCostGuide'}</p>
          <h1>{html.escape(hero_title)}</h1>
          <p>{html.escape(hero_summary)}</p>
          {disclaimer_html()}
        </section>
        """
    )
    return trim(
        f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <title>{html.escape(title)}</title>
          <meta name="description" content="{html.escape(description)}">
          <meta name="robots" content="{robots}">
          <link rel="canonical" href="{html.escape(canonical)}">
          <meta property="og:type" content="website">
          <meta property="og:site_name" content="{SITE_NAME}">
          <meta property="og:title" content="{html.escape(title)}">
          <meta property="og:description" content="{html.escape(description)}">
          <meta property="og:url" content="{html.escape(canonical)}">
          <meta property="og:image" content="{DOMAIN}/assets/images/social-preview.svg">
          <meta name="twitter:card" content="summary_large_image">
          <meta name="twitter:title" content="{html.escape(title)}">
          <meta name="twitter:description" content="{html.escape(description)}">
          <meta name="twitter:image" content="{DOMAIN}/assets/images/social-preview.svg">
          <link rel="icon" href="{DOMAIN}/assets/icons/favicon.svg" type="image/svg+xml">
          <link rel="stylesheet" href="{DOMAIN}/styles.css">
        </head>
        <body data-page-type="{html.escape(page_type)}" data-page-path="{html.escape(path)}" data-breadcrumbs="{breadcrumb_attr}" data-faqs="{faq_attr}">
          {header(path)}
          <main class="ccg-shell">
            {breadcrumb_nav}
            {hero}
            {main_content}
          </main>
          {footer()}
          <div class="ccg-cookie-banner" hidden>
            <div>
              <strong>Cookie preferences</strong>
              <p>We use essential site storage for navigation and optional analytics preferences. You can accept or reject non-essential cookies.</p>
            </div>
            <div class="ccg-cookie-actions">
              <button class="ccg-button" data-cookie-action="accept">Accept</button>
              <button class="ccg-button ccg-button--ghost" data-cookie-action="reject">Reject Non-Essential</button>
            </div>
          </div>
          <script src="{DOMAIN}/main.js" defer></script>
        </body>
        </html>
        """
    )


def styles_css() -> str:
    return trim(
        """
        :root {
          --ccg-navy: #081a33;
          --ccg-blue: #4f8ff7;
          --ccg-blue-soft: #dbe8ff;
          --ccg-slate: #5b6983;
          --ccg-ink: #10223e;
          --ccg-white: #ffffff;
          --ccg-mist: #f3f6fb;
          --ccg-line: rgba(16, 34, 62, 0.1);
          --ccg-shadow: 0 18px 48px rgba(4, 15, 31, 0.12);
          --ccg-radius-xl: 28px;
          --ccg-radius-lg: 22px;
          --ccg-radius-md: 16px;
          --ccg-max: 1180px;
          --ccg-gradient: linear-gradient(135deg, #5fa4ff 0%, #1f6fff 50%, #143bbf 100%);
        }

        * { box-sizing: border-box; }
        html { scroll-behavior: smooth; }
        body {
          margin: 0;
          font-family: "Avenir Next", "Segoe UI", "Trebuchet MS", sans-serif;
          color: var(--ccg-ink);
          background:
            radial-gradient(circle at top right, rgba(95, 164, 255, 0.16), transparent 32%),
            linear-gradient(180deg, #f8fbff 0%, #ffffff 34%, #f6f8fc 100%);
          line-height: 1.65;
        }

        a { color: inherit; text-decoration: none; }
        img { max-width: 100%; display: block; }
        main { padding-bottom: 5rem; }
        .ccg-shell { width: min(calc(100% - 2rem), var(--ccg-max)); margin: 0 auto; }

        .ccg-site-header {
          position: sticky;
          top: 0;
          z-index: 20;
          backdrop-filter: blur(14px);
          background: rgba(8, 26, 51, 0.88);
          border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        }
        .ccg-header-row {
          display: flex;
          align-items: center;
          justify-content: space-between;
          gap: 1rem;
          min-height: 74px;
        }
        .ccg-brand {
          display: inline-flex;
          align-items: center;
          gap: 0.8rem;
          color: white;
          font-weight: 800;
          letter-spacing: 0.02em;
        }
        .ccg-brand img { width: 42px; height: 42px; }
        .ccg-main-nav { display: none; gap: 0.8rem; }
        .ccg-main-nav a,
        .ccg-mobile-nav a {
          color: rgba(255, 255, 255, 0.86);
          padding: 0.75rem 1rem;
          border-radius: 999px;
          font-size: 0.96rem;
        }
        .ccg-main-nav a.is-active,
        .ccg-main-nav a:hover,
        .ccg-mobile-nav a:hover {
          background: rgba(255, 255, 255, 0.1);
          color: white;
        }
        .ccg-menu-toggle {
          border: 1px solid rgba(255, 255, 255, 0.18);
          background: rgba(255, 255, 255, 0.08);
          color: white;
          border-radius: 999px;
          padding: 0.7rem 1rem;
          font: inherit;
        }
        .ccg-mobile-nav {
          display: none;
          padding: 0 1rem 1rem;
          grid-template-columns: 1fr;
          gap: 0.45rem;
        }
        .ccg-mobile-nav.is-open { display: grid; }

        .ccg-breadcrumbs {
          display: flex;
          flex-wrap: wrap;
          gap: 0.55rem;
          align-items: center;
          font-size: 0.9rem;
          color: var(--ccg-slate);
          padding-top: 1.5rem;
        }
        .ccg-breadcrumbs a[aria-current="page"] { color: var(--ccg-ink); font-weight: 700; }

        .ccg-page-hero,
        .ccg-hero-home {
          position: relative;
          overflow: hidden;
          margin: 1.5rem 0 2rem;
          background:
            radial-gradient(circle at 10% 15%, rgba(95, 164, 255, 0.3), transparent 24%),
            radial-gradient(circle at 90% 12%, rgba(255, 255, 255, 0.14), transparent 20%),
            linear-gradient(145deg, #071527 0%, #0a2342 55%, #133b73 100%);
          color: white;
          border-radius: 34px;
          box-shadow: var(--ccg-shadow);
        }
        .ccg-page-hero { padding: 2rem 1.4rem; }
        .ccg-page-hero h1,
        .ccg-hero-home h1 { margin: 0.2rem 0 1rem; font-size: clamp(2.2rem, 6vw, 4.4rem); line-height: 0.98; letter-spacing: -0.03em; }
        .ccg-page-hero p,
        .ccg-hero-home p { max-width: 65ch; color: rgba(255, 255, 255, 0.88); }
        .ccg-kicker {
          display: inline-flex;
          align-items: center;
          gap: 0.45rem;
          text-transform: uppercase;
          letter-spacing: 0.16em;
          font-size: 0.76rem;
          color: #bfd8ff;
          margin: 0 0 0.75rem;
          font-weight: 800;
        }
        .ccg-disclaimer {
          margin-top: 1rem;
          padding: 1rem 1.15rem;
          border-radius: 16px;
          background: rgba(255, 255, 255, 0.11);
          color: rgba(255, 255, 255, 0.95);
          font-size: 0.95rem;
        }

        .ccg-hero-home {
          display: grid;
          gap: 1.4rem;
          padding: 1.6rem;
        }
        .ccg-hero-actions,
        .ccg-cookie-actions { display: flex; flex-wrap: wrap; gap: 0.85rem; margin-top: 1.2rem; }
        .ccg-button {
          display: inline-flex;
          justify-content: center;
          align-items: center;
          min-height: 48px;
          padding: 0.85rem 1.25rem;
          border: 0;
          border-radius: 999px;
          background: var(--ccg-gradient);
          color: white;
          font-weight: 800;
          box-shadow: 0 14px 30px rgba(28, 88, 215, 0.3);
          cursor: pointer;
          font: inherit;
        }
        .ccg-button--ghost {
          background: rgba(255, 255, 255, 0.08);
          border: 1px solid rgba(255, 255, 255, 0.18);
          box-shadow: none;
        }
        .ccg-hero-visual {
          display: grid;
          gap: 1rem;
          align-content: start;
        }
        .ccg-glass-card,
        .ccg-chart-card,
        .ccg-topic-card,
        .ccg-related-card,
        .ccg-author-box,
        .ccg-calc-card,
        .ccg-cookie-banner {
          border-radius: var(--ccg-radius-xl);
          background: white;
          box-shadow: var(--ccg-shadow);
          border: 1px solid rgba(16, 34, 62, 0.06);
        }
        .ccg-glass-card {
          background: rgba(255, 255, 255, 0.12);
          border-color: rgba(255, 255, 255, 0.14);
          color: white;
          padding: 1.2rem;
        }
        .ccg-glass-card strong { display: block; font-size: 2rem; margin-top: 0.3rem; }
        .ccg-metrics {
          display: grid;
          grid-template-columns: repeat(3, minmax(0, 1fr));
          gap: 0.85rem;
          margin-top: 1.4rem;
        }
        .ccg-metrics div {
          padding: 1rem;
          background: rgba(255, 255, 255, 0.08);
          border-radius: 18px;
        }
        .ccg-metrics strong { display: block; font-size: 1.5rem; }

        .ccg-section {
          padding: 1.4rem;
          margin-top: 1.4rem;
          border-radius: 28px;
          background: white;
          border: 1px solid var(--ccg-line);
        }
        .ccg-section--soft { background: var(--ccg-mist); }
        .ccg-section-head h2 { margin: 0.1rem 0 0.9rem; font-size: clamp(1.5rem, 3vw, 2.35rem); line-height: 1.05; }

        .ccg-topic-grid,
        .ccg-related-grid {
          display: grid;
          gap: 1rem;
        }
        .ccg-topic-card,
        .ccg-related-card {
          padding: 1.25rem;
          transition: transform 180ms ease, box-shadow 180ms ease;
        }
        .ccg-topic-card:hover,
        .ccg-related-card:hover { transform: translateY(-3px); }
        .ccg-topic-card span,
        .ccg-related-card span { color: var(--ccg-blue); font-size: 0.82rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.12em; }
        .ccg-topic-card strong,
        .ccg-related-card strong { display: block; margin: 0.45rem 0; font-size: 1.1rem; }
        .ccg-topic-card--small p { font-size: 0.95rem; }
        .ccg-spotlight-list {
          display: grid;
          gap: 0.75rem;
        }
        .ccg-spotlight-item {
          padding: 1rem 1.1rem;
          border-radius: 18px;
          background: white;
          border: 1px solid var(--ccg-line);
          font-weight: 700;
        }

        .ccg-list { padding-left: 1.2rem; }
        .ccg-list li + li { margin-top: 0.45rem; }
        .ccg-chart { min-height: 120px; }
        .ccg-chart svg { width: 100%; height: 120px; overflow: visible; }
        .ccg-chart-card { padding: 0.4rem; margin-top: 1rem; }

        .ccg-table-wrap { overflow-x: auto; }
        .ccg-table {
          width: 100%;
          min-width: 640px;
          border-collapse: collapse;
          font-size: 0.96rem;
        }
        .ccg-table th,
        .ccg-table td {
          text-align: left;
          padding: 0.9rem 0.95rem;
          border-bottom: 1px solid var(--ccg-line);
          vertical-align: top;
        }
        .ccg-table thead th {
          font-size: 0.8rem;
          text-transform: uppercase;
          letter-spacing: 0.12em;
          color: var(--ccg-slate);
        }

        .ccg-faq-grid { display: grid; gap: 0.85rem; }
        .ccg-faq-item {
          border: 1px solid var(--ccg-line);
          border-radius: 18px;
          padding: 1rem 1.1rem;
          background: #fbfdff;
        }
        .ccg-faq-item summary { cursor: pointer; font-weight: 800; }
        .ccg-faq-item p { margin: 0.8rem 0 0; }

        .ccg-author-box {
          display: grid;
          grid-template-columns: auto 1fr;
          gap: 1rem;
          padding: 1.3rem;
          margin-top: 1.4rem;
        }
        .ccg-author-mark {
          width: 64px;
          height: 64px;
          border-radius: 20px;
          display: grid;
          place-items: center;
          background: var(--ccg-gradient);
          color: white;
          font-weight: 900;
        }
        .ccg-author-label,
        .ccg-author-role { margin: 0; color: var(--ccg-slate); }
        .ccg-author-box h2 { margin: 0.15rem 0; font-size: 1.3rem; }

        .ccg-calc-card { padding: 1.2rem; display: grid; gap: 1.2rem; }
        .ccg-calc-form {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
          gap: 0.9rem;
        }
        .ccg-calc-form label { display: grid; gap: 0.4rem; font-weight: 700; }
        .ccg-calc-form input {
          width: 100%;
          min-height: 48px;
          border-radius: 14px;
          border: 1px solid var(--ccg-line);
          background: #f8fbff;
          padding: 0.8rem 0.9rem;
          font: inherit;
        }
        .ccg-calc-output h3 { margin-top: 0; }
        .ccg-result-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
          gap: 0.8rem;
        }
        .ccg-result-grid div {
          padding: 1rem;
          border-radius: 18px;
          background: var(--ccg-mist);
        }
        .ccg-result-grid span {
          display: block;
          color: var(--ccg-slate);
          font-size: 0.9rem;
          margin-bottom: 0.35rem;
        }
        .ccg-result-grid strong { font-size: 1.2rem; }

        .ccg-site-footer {
          background: #071527;
          color: rgba(255, 255, 255, 0.83);
          padding: 2.4rem 0;
        }
        .ccg-footer-grid {
          display: grid;
          gap: 1.25rem;
        }
        .ccg-footer-links {
          display: grid;
          gap: 0.55rem;
        }
        .ccg-brand--footer { color: white; margin-bottom: 0.8rem; }

        .ccg-cookie-banner {
          position: fixed;
          left: 1rem;
          right: 1rem;
          bottom: 1rem;
          z-index: 25;
          padding: 1rem;
        }

        @media (min-width: 760px) {
          .ccg-main-nav { display: flex; }
          .ccg-menu-toggle,
          .ccg-mobile-nav { display: none !important; }
          .ccg-hero-home { grid-template-columns: 1.25fr 0.95fr; align-items: center; padding: 2.6rem; }
          .ccg-page-hero { padding: 2.6rem; }
          .ccg-topic-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
          .ccg-topic-grid--small { grid-template-columns: repeat(3, minmax(0, 1fr)); }
          .ccg-related-grid,
          .ccg-spotlight-list,
          .ccg-footer-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); }
          .ccg-faq-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
        }

        @media (min-width: 1040px) {
          .ccg-topic-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); }
          .ccg-page-hero h1,
          .ccg-hero-home h1 { max-width: 14ch; }
        }
        """
    )


def main_js() -> str:
    return trim(
        """
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
            return `${rootPrefix()}${pathname.replace(/^\\//, "")}`;
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
        """
    )


def logo_svg() -> str:
    return trim(
        """
        <svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256" role="img" aria-label="CreditCostGuide logo">
          <defs>
            <linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#7cb4ff"/>
              <stop offset="50%" stop-color="#2f78ff"/>
              <stop offset="100%" stop-color="#122d91"/>
            </linearGradient>
          </defs>
          <rect width="256" height="256" rx="56" fill="#081a33"/>
          <path d="M56 154c14-38 46-64 86-64 18 0 35 4 52 14l-16 26c-11-6-23-9-35-9-27 0-49 13-61 35 10 16 29 28 51 28 18 0 34-7 47-20l22 22c-18 19-43 30-71 30-33 0-61-14-75-38-4-7-4-16 0-24Z" fill="url(#g)"/>
          <circle cx="176" cy="86" r="18" fill="#dbe8ff"/>
        </svg>
        """
    )


def favicon_svg() -> str:
    return trim(
        """
        <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64">
          <defs>
            <linearGradient id="f" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#7cb4ff"/>
              <stop offset="100%" stop-color="#1f6fff"/>
            </linearGradient>
          </defs>
          <rect width="64" height="64" rx="18" fill="#081a33"/>
          <path d="M15 39c4-9 12-16 24-16 5 0 10 1 15 4l-4 7c-3-2-7-3-10-3-7 0-13 3-16 9 3 4 8 7 14 7 5 0 10-2 14-6l6 6c-5 5-12 8-20 8-10 0-18-4-23-11-1-2-1-3 0-5Z" fill="url(#f)"/>
        </svg>
        """
    )


def social_svg() -> str:
    return trim(
        """
        <svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
          <defs>
            <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#071527"/>
              <stop offset="50%" stop-color="#0b274f"/>
              <stop offset="100%" stop-color="#18478b"/>
            </linearGradient>
            <linearGradient id="card" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#8ec1ff"/>
              <stop offset="100%" stop-color="#2a73ff"/>
            </linearGradient>
          </defs>
          <rect width="1200" height="630" fill="url(#bg)"/>
          <circle cx="1040" cy="120" r="120" fill="rgba(255,255,255,0.08)"/>
          <circle cx="160" cy="520" r="180" fill="rgba(95,164,255,0.12)"/>
          <g transform="translate(96 110)">
            <rect width="108" height="108" rx="28" fill="#081a33" stroke="rgba(255,255,255,0.2)"/>
            <path d="M26 67c8-20 24-33 46-33 10 0 19 2 29 7l-9 15c-6-3-12-5-19-5-14 0-26 7-33 18 5 9 15 15 27 15 10 0 18-4 25-10l12 12c-10 11-23 17-38 17-18 0-33-7-41-20-2-2-2-5 1-8Z" fill="url(#card)"/>
          </g>
          <text x="96" y="300" fill="#bfd8ff" font-family="Avenir Next, Segoe UI, sans-serif" font-size="28" letter-spacing="5">CREDITCOSTGUIDE</text>
          <text x="96" y="380" fill="#ffffff" font-family="Avenir Next, Segoe UI, sans-serif" font-size="72" font-weight="800">Borrowing costs,</text>
          <text x="96" y="456" fill="#ffffff" font-family="Avenir Next, Segoe UI, sans-serif" font-size="72" font-weight="800">fees, and payoff math</text>
          <text x="96" y="528" fill="#dbe8ff" font-family="Avenir Next, Segoe UI, sans-serif" font-size="34">U.S.-focused guides and calculators for credit cards, loans, banking, mortgages, and debt payoff.</text>
          <g transform="translate(830 182)">
            <rect width="250" height="170" rx="32" fill="rgba(255,255,255,0.12)" stroke="rgba(255,255,255,0.16)"/>
            <text x="28" y="52" fill="#dbe8ff" font-family="Avenir Next, Segoe UI, sans-serif" font-size="22">Monthly payment review</text>
            <text x="28" y="98" fill="#ffffff" font-family="Avenir Next, Segoe UI, sans-serif" font-size="54" font-weight="800">$1,742</text>
            <path d="M30 128 L72 112 L120 119 L164 92 L218 78" fill="none" stroke="#8ec1ff" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
          </g>
        </svg>
        """
    )


def robots_txt() -> str:
    return trim(
        f"""
        User-agent: *
        Allow: /

        Sitemap: {DOMAIN}/sitemap.xml
        """
    )


def sitemap_xml(paths: List[str]) -> str:
    items = []
    for path in paths:
        items.append(
            f"<url><loc>{html.escape(url_for(path))}</loc><changefreq>weekly</changefreq><priority>{'1.0' if path == 'index.html' else '0.8'}</priority></url>"
        )
    return trim(
        f"""
        <?xml version="1.0" encoding="UTF-8"?>
        <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
          {''.join(items)}
        </urlset>
        """
    )


def verification_script() -> str:
    return trim(
        f"""
        from __future__ import annotations

        import re
        import sys
        import xml.etree.ElementTree as ET
        from html.parser import HTMLParser
        from pathlib import Path

        ROOT = Path(__file__).resolve().parents[1]
        DOMAIN = "{DOMAIN}"

        REQUIRED = [
            "index.html", "about.html", "contact.html", "how-we-research.html",
            "privacy-policy.html", "terms.html", "disclaimer.html",
            "styles.css", "main.js", "sitemap.xml", "robots.txt", "walkthrough.md",
            "assets/icons/favicon.svg", "assets/icons/logo.svg", "assets/images/social-preview.svg"
        ]

        class LinkParser(HTMLParser):
            def __init__(self):
                super().__init__()
                self.links = []
                self.title = ""
                self.meta_desc = None
                self.canonical = None
                self.in_title = False
                self.schemas = 0
            def handle_starttag(self, tag, attrs):
                attrs = dict(attrs)
                if tag == "a" and "href" in attrs:
                    self.links.append(attrs["href"])
                if tag == "meta" and attrs.get("name") == "description":
                    self.meta_desc = attrs.get("content")
                if tag == "link" and attrs.get("rel") == "canonical":
                    self.canonical = attrs.get("href")
                if tag == "title":
                    self.in_title = True
                if tag == "script" and attrs.get("type") == "application/ld+json":
                    self.schemas += 1
            def handle_endtag(self, tag):
                if tag == "title":
                    self.in_title = False
            def handle_data(self, data):
                if self.in_title:
                    self.title += data

        def html_files():
            return sorted([p for p in ROOT.rglob("*.html") if ".git" not in p.parts])

        def assert_true(condition, message, problems):
            if not condition:
                problems.append(message)

        def run():
            problems = []
            for rel in REQUIRED:
                assert_true((ROOT / rel).exists(), f"Missing required file: {{rel}}", problems)

            titles = {{}}
            descs = {{}}
            canonicals = {{}}
            html_paths = html_files()
            expected_paths = set()
            for file in html_paths:
                parser = LinkParser()
                parser.feed(file.read_text(encoding="utf-8"))
                rel = file.relative_to(ROOT).as_posix()
                expected_paths.add(rel)
                assert_true(bool(parser.title.strip()), f"Missing title: {{rel}}", problems)
                assert_true(bool(parser.meta_desc), f"Missing meta description: {{rel}}", problems)
                assert_true(bool(parser.canonical), f"Missing canonical: {{rel}}", problems)
                assert_true(parser.schemas == 0, f"Static JSON-LD block found in HTML: {{rel}}", problems)
                assert_true("href=\\"#\\"" not in file.read_text(encoding="utf-8"), f"Placeholder hash link found: {{rel}}", problems)
                assert_true("javascript:void(0)" not in file.read_text(encoding="utf-8"), f"javascript:void(0) found: {{rel}}", problems)
                assert_true("Lorem ipsum" not in file.read_text(encoding="utf-8"), f"Lorem ipsum found: {{rel}}", problems)
                assert_true("TODO" not in file.read_text(encoding="utf-8"), f"TODO found: {{rel}}", problems)
                assert_true("http://" not in file.read_text(encoding="utf-8"), f"Non-https URL found: {{rel}}", problems)
                if parser.title in titles:
                    problems.append(f"Duplicate title: {{rel}} and {{titles[parser.title]}}")
                titles[parser.title] = rel
                if parser.meta_desc in descs:
                    problems.append(f"Duplicate meta description: {{rel}} and {{descs[parser.meta_desc]}}")
                descs[parser.meta_desc] = rel
                if parser.canonical in canonicals:
                    problems.append(f"Duplicate canonical: {{rel}} and {{canonicals[parser.canonical]}}")
                canonicals[parser.canonical] = rel

                for link in parser.links:
                    if not link.startswith(DOMAIN):
                        continue
                    path = link.replace(DOMAIN, "").lstrip("/") or "index.html"
                    if link.endswith("/"):
                        path = "index.html"
                    assert_true((ROOT / path).exists(), f"Broken internal link in {{rel}} -> {{link}}", problems)

            robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
            assert_true("Sitemap: https://creditcostguide.com/sitemap.xml" in robots, "robots.txt missing sitemap directive", problems)

            sitemap = ET.parse(ROOT / "sitemap.xml").getroot()
            ns = {{"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}}
            urls = [loc.text for loc in sitemap.findall("sm:url/sm:loc", ns)]
            assert_true(len(urls) == len(expected_paths), "sitemap.xml URL count does not match HTML file count", problems)
            for path in expected_paths:
                loc = f"{{DOMAIN}}/" if path == "index.html" else f"{{DOMAIN}}/{{path}}"
                assert_true(loc in urls, f"sitemap.xml missing {{loc}}", problems)

            walkthrough = ROOT / "walkthrough.md"
            summary = [
                "# CreditCostGuide Launch Walkthrough",
                "",
                "## Audit Summary",
                f"- HTML pages found: {{len(expected_paths)}}",
                f"- Unique titles checked: {{len(titles)}}",
                f"- Unique descriptions checked: {{len(descs)}}",
                f"- Unique canonicals checked: {{len(canonicals)}}",
                f"- Internal validation issues: {{len(problems)}}",
                "",
                "## AdSense Readiness Checklist",
                "- Clear navigation is present across the site.",
                "- Legal pages exist: privacy policy, terms, and disclaimer.",
                "- Content is educational, original, and themed around U.S. consumer finance costs.",
                "- No placeholder ad blocks were included.",
                "- Cookie preference controls are present.",
                "",
                "## Search Console Checklist",
                "- `sitemap.xml` is generated with absolute HTTPS URLs.",
                "- `robots.txt` points to the sitemap.",
                "- Each page includes a canonical URL, unique title, and unique description.",
                "- Open Graph and Twitter metadata are included on every page.",
                "- Breadcrumb navigation is present on internal pages.",
                "",
                "## Manual Review Notes",
                "- Local file preview navigation is supported through JavaScript rewriting for same-domain links.",
                "- Dynamic JSON-LD schema is injected by `main.js` instead of static blocks in HTML.",
                "- Re-run `python3 scripts/verify_site.py` after any edit to refresh this report.",
                "",
                "## Verification Result",
            ]
            if problems:
                summary.extend(f"- FAIL: {{item}}" for item in problems)
            else:
                summary.append("- PASS: All automated checks completed without detected issues.")
            walkthrough.write_text("\\n".join(summary) + "\\n", encoding="utf-8")

            if problems:
                print("Verification failed:")
                for item in problems:
                    print(f"- {{item}}")
                sys.exit(1)
            print("Verification passed.")

        if __name__ == "__main__":
            run()
        """
    )


def contact_form_html() -> str:
    return trim(
        """
        <section class="ccg-section">
          <div class="ccg-section-head">
            <p class="ccg-kicker">Reach Out</p>
            <h2>Send a note to the editorial team</h2>
          </div>
          <form class="ccg-calc-form" data-contact-form>
            <label><span>Name</span><input name="name" value=""></label>
            <label><span>Email</span><input name="email" value=""></label>
            <label><span>Topic</span><input name="topic" value=""></label>
            <label style="grid-column: 1 / -1;"><span>Message</span><input name="message" value=""></label>
            <button class="ccg-button" type="submit">Send Message</button>
            <p data-contact-status></p>
          </form>
        </section>
        """
    )


def build() -> None:
    ensure_dir(TARGET)
    ensure_dir(TARGET / "pages")
    ensure_dir(TARGET / "assets" / "icons")
    ensure_dir(TARGET / "assets" / "images")
    ensure_dir(TARGET / "scripts")

    all_paths: List[str] = [item["path"] for item in PILLARS]
    all_paths += [path for path, _, _ in SUPPORTING]
    all_paths += [path for path, _, _, _ in CALCULATORS]
    all_paths += [path for path, _, _, _ in ROOT_PAGES]

    related_pool = [item["path"] for item in PILLARS] + [path for path, _, _ in SUPPORTING] + [path for path, _, _, _ in CALCULATORS]

    for cfg in PILLARS:
        path = cfg["path"]
        related = [p for p in related_pool if p != path][:6]
        body = article_body(cfg, 3000, related)
        doc = html_doc(
            path=path,
            title=cfg["title"],
            description=cfg["description"],
            page_type="guide",
            main_content=body,
            breadcrumbs=breadcrumb_items(path, cfg["title"]),
            faqs=cfg["faqs"],
            hero_title=cfg["hero"],
            hero_summary=cfg["summary"],
        )
        write(TARGET / path, doc)

    for path, title, desc in SUPPORTING:
        related = [p for p in related_pool if p != path][:6]
        body, faqs = support_body(path, title, desc, related)
        doc = html_doc(
            path=path,
            title=title,
            description=desc,
            page_type="article",
            main_content=body,
            breadcrumbs=breadcrumb_items(path, title),
            faqs=faqs,
            hero_title=title,
            hero_summary=desc,
        )
        write(TARGET / path, doc)

    for path, title, desc, calc_type in CALCULATORS:
        related = [p for p in related_pool if p != path][:6]
        body, faqs = calculator_body(path, title, desc, calc_type, related)
        doc = html_doc(
            path=path,
            title=title,
            description=desc,
            page_type="calculator",
            main_content=body,
            breadcrumbs=breadcrumb_items(path, title),
            faqs=faqs,
            hero_title=title,
            hero_summary=desc,
        )
        write(TARGET / path, doc)

    for path, title, desc, page_type in ROOT_PAGES:
        if path == "index.html":
            body = home_body()
            faqs = [
                ["What does CreditCostGuide cover?", "The site covers U.S. credit, loans, mortgages, banking fees, debt payoff, refinancing, and calculator-based cost comparisons."],
                ["Are the examples personalized recommendations?", "No. The material is educational and should be paired with direct provider disclosures or professional guidance for personal decisions."],
                ["Can the site be previewed locally?", "Yes. Same-domain absolute links are rewritten during local file preview so navigation still works without a server."],
            ]
        elif path == "contact.html":
            generic_related = [p for p in related_pool if p != path][:6]
            body, faqs = simple_page_body(title, desc, generic_related)
            body += contact_form_html()
        else:
            generic_related = [p for p in related_pool if p != path][:6]
            body, faqs = simple_page_body(title, desc, generic_related, legal=page_type == "legal")
        doc = html_doc(
            path=path,
            title=title,
            description=desc,
            page_type=page_type,
            main_content=body,
            breadcrumbs=breadcrumb_items(path, title),
            faqs=faqs,
            hero_title=title if path != "index.html" else "Borrowing costs explained for everyday decisions",
            hero_summary=desc if path != "index.html" else "Explore a modern fintech-style library of educational guides and calculators covering U.S. credit, loans, mortgages, banking, refinancing, and debt payoff.",
        )
        write(TARGET / path, doc)

    write(TARGET / "styles.css", styles_css())
    write(TARGET / "main.js", main_js())
    write(TARGET / "robots.txt", robots_txt())
    write(TARGET / "sitemap.xml", sitemap_xml(all_paths))
    write(TARGET / "assets" / "icons" / "logo.svg", logo_svg())
    write(TARGET / "assets" / "icons" / "favicon.svg", favicon_svg())
    write(TARGET / "assets" / "images" / "social-preview.svg", social_svg())
    write(TARGET / "scripts" / "verify_site.py", verification_script())
    write(TARGET / "scripts" / "build_site.py", Path(__file__).read_text(encoding="utf-8"))
    if not (TARGET / "walkthrough.md").exists():
        write(TARGET / "walkthrough.md", "# CreditCostGuide Launch Walkthrough\n\nRun `python3 scripts/verify_site.py` to populate the audit report.\n")


if __name__ == "__main__":
    build()
