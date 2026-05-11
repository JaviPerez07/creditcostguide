from __future__ import annotations

import html
import json
import math
import os
import re
import textwrap
from pathlib import Path
from typing import Dict, List, Optional, Tuple


SITE_NAME = "CreditCostGuide"
DOMAIN = "https://creditcostguide.com"
TARGET = Path("/Users/javiperezz7/Documents/creditcostguide")
ADSENSE_SCRIPT = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3733223915347669" crossorigin="anonymous"></script>'

# Editorial identity — single human editor, no fictional credentials.
EDITOR_NAME = "Javi Pérez"
EDITOR_ROLE = "Founder and Editor"
EDITOR_LINKEDIN = "https://www.linkedin.com/in/javi-perez-guides"
EDITOR_LOCATION = "Almería, Spain"
EDITOR_PHOTO = f"{DOMAIN}/assets/images/javi-perez-guides.jpg"
EDITOR_PHOTO_FALLBACK = f"{DOMAIN}/assets/images/social-preview.svg"
LAST_REVIEWED = "May 2026"
LAST_REVIEWED_ISO = "2026-05-06"
SITEMAP_LASTMOD = "2026-05-06"

# Standard non-advice disclaimer reused everywhere.
NON_ADVICE_DISCLAIMER = (
    "Javi Pérez is not a licensed financial advisor, CPA, CFP, loan officer, "
    "tax professional, or attorney. This content is educational only and "
    "does not replace advice from a qualified professional."
)

# AI-assisted disclosure reused on every indexable page.
AI_DISCLOSURE = (
    "This guide was created with AI-assisted drafting and human editorial review by "
    f"{EDITOR_NAME}. Figures, examples, and explanations are checked against public "
    "sources including CFPB, the Federal Reserve, FDIC, BLS, FTC, and SEC where applicable. "
    "Content is reviewed quarterly."
)

# Curated indexable set. Only URLs here get index,follow and a sitemap entry.
# Everything else is noindex,follow and never enters the sitemap. This keeps
# the indexable surface small, original, and defensible for AdSense review.
INDEXABLE_PAGES: set[str] = {
    # Root trust + legal pages.
    "index.html",
    "about.html",
    "contact.html",
    "how-we-research.html",
    "privacy-policy.html",
    "terms.html",
    "disclaimer.html",
    # Author page.
    "authors/javi-perez/index.html",
    # Pillar guides — kept because they have unique short content.
    "pages/personal-loans-guide.html",
    "pages/credit-cards-guide.html",
    "pages/mortgage-guide.html",
    "pages/credit-score-guide.html",
    "pages/banking-fees-guide.html",
    "pages/debt-payoff-guide.html",
    "pages/refinancing-guide.html",
    "pages/student-loans-guide.html",
    # Supporting articles with unique PAGE_CONTENT entries.
    "pages/how-credit-scores-work.html",
    "pages/best-credit-cards-for-bad-credit.html",
    "pages/how-to-lower-credit-card-interest.html",
    # Calculators (functional tools count as original value).
    "pages/loan-payment-calculator.html",
    "pages/credit-card-interest-calculator.html",
    "pages/mortgage-calculator.html",
    "pages/debt-payoff-calculator.html",
    "pages/credit-utilization-calculator.html",
    # New Chart.js calculators (Phase 2 — May 2026 launch).
    "pages/debt-avalanche-vs-snowball-calculator.html",
    "pages/credit-card-minimum-payment-true-cost-calculator.html",
    "pages/mortgage-refinance-break-even-calculator.html",
}


def is_indexable(path: str) -> bool:
    return path in INDEXABLE_PAGES

# SmartCredit (CJ) affiliate — offer IDs per link type
SC_TRIAL_URL = "https://www.tkqlhce.com/click-101736471-17138841"
SC_EVERGREEN_URL = "https://www.dpbolvw.net/click-101736471-16983231"
SC_BOOST_URL = "https://www.kqzyfj.com/click-101736471-16982685"
SC_PIXEL = '<img src="https://www.ftjcfx.com/image-101736471-17138841" width="1" height="1" border="0"/>'
SMARTCREDIT_PAGES = {
    "pages/credit-score-guide.html",
    "pages/how-credit-scores-work.html",
    "pages/best-credit-cards-for-bad-credit.html",
    "pages/debt-payoff-guide.html",
    "pages/credit-utilization-calculator.html",
    "pages/how-to-lower-credit-card-interest.html",
}


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
    # Charted calculators (Chart.js, per-page JS) — see calc_js_*() and html_doc(extra_scripts=...).
    ("pages/debt-avalanche-vs-snowball-calculator.html", "Debt Avalanche vs Snowball Calculator: Compare Payoff Methods", "Compare avalanche and snowball debt payoff strategies side by side using up to five debts and a single monthly payoff budget.", "avalanche-snowball"),
    ("pages/credit-card-minimum-payment-true-cost-calculator.html", "Minimum Payment Calculator: The True Cost of Paying the Minimum", "Estimate credit card payoff time and total interest when paying only the minimum, then see how an extra monthly payment changes the picture.", "min-payment"),
    ("pages/mortgage-refinance-break-even-calculator.html", "Mortgage Refinance Break-Even Calculator: Compare Old and New Payments", "Estimate refinance break-even months by comparing your current mortgage payment to a new offer with closing costs included.", "refinance"),
]

# Calculators that require Chart.js + a dedicated per-page JS file written to
# /assets/scripts/. Used by html_doc() to inject the right script tags.
CHARTED_CALCS: Dict[str, str] = {
    "avalanche-snowball": "debt-avalanche-snowball.js",
    "min-payment": "minimum-payment-true-cost.js",
    "refinance": "refinance-break-even.js",
}


ROOT_PAGES = [
    ("index.html", "CreditCostGuide: Credit, Loans, APRs, Fees, Refinancing, and Cost Calculators", "Explore U.S.-focused guides and calculators for credit cards, personal loans, mortgages, debt payoff, banking fees, refinancing, and credit scores.", "home"),
    ("about.html", "About CreditCostGuide", "Learn how CreditCostGuide approaches educational financial content, editorial standards, and reader-first explanations.", "article"),
    ("contact.html", "Contact CreditCostGuide", "Use the contact page to send editorial questions, corrections, partnership inquiries, and general feedback to CreditCostGuide.", "article"),
    ("how-we-research.html", "How We Research Financial Costs and Product Pricing", "See the research framework behind CreditCostGuide content, including source review, pricing comparisons, and update practices.", "article"),
    ("privacy-policy.html", "Privacy Policy | CreditCostGuide", "Review how CreditCostGuide handles analytics, cookies, contact submissions, and reader privacy preferences.", "legal"),
    ("terms.html", "Terms of Use | CreditCostGuide", "Read the terms that govern use of CreditCostGuide content, calculators, and site features.", "legal"),
    ("disclaimer.html", "Disclaimer | CreditCostGuide", "Understand the informational-only nature of CreditCostGuide content and the limits of calculators, examples, and editorial material.", "legal"),
]

# ---------------------------------------------------------------------------
# PAGE_CONTENT — real, unique content for the 6 SmartCredit-affiliated pages.
# Each section "body" is a raw HTML string inserted verbatim (not escaped).
# kicker / h2 / intro_h2 are plain text and ARE html.escape()'d at render time.
# FAQs are [[question, answer], ...] plain text pairs.
# ---------------------------------------------------------------------------
PAGE_CONTENT: Dict[str, dict] = {
    # -----------------------------------------------------------------------
    "pages/credit-score-guide.html": {
        "intro_h2": "What Your Credit Score Actually Measures",
        "intro_body": (
            "<p>Your credit score is a three-digit number between 300 and 850 that lenders, "
            "landlords, and some employers use to estimate financial risk. According to "
            "<a href=\"https://www.experian.com/blogs/ask-experian/consumer-credit-review/\" target=\"_blank\" rel=\"noopener nofollow\">Experian's most recent annual consumer credit review</a>, "
            "the average U.S. FICO score is 715 — solidly in the Good range (source: Experian 2025). "
            "But averages mask a wide spread: roughly 21% of Americans carry scores below 600, making "
            "them subprime in most lender frameworks, while about 23% have scores above 800.</p>"
            "<p>The practical cost of a lower score is large. A borrower at 760 applying for "
            "a 30-year fixed mortgage might receive a rate near 6.5%. The same loan to a "
            "borrower at 620 can come in at 8.0% or higher — a 1.5 percentage-point difference "
            "that adds over $100,000 in total interest on a $400,000 home. For credit cards, "
            "the gap between a prime APR and a subprime APR can exceed 12 percentage points. "
            "Understanding what drives your score is the first step toward lowering your "
            "borrowing costs across every product you use.</p>"
        ),
        "sections": [
            {
                "kicker": "Score Factors",
                "h2": "How FICO Scores Are Calculated",
                "body": (
                    "<p>The FICO scoring model, used in over 90% of U.S. lending decisions, "
                    "breaks your financial behavior into five weighted categories. "
                    "Payment history accounts for 35% — the largest single factor. Every "
                    "on-time payment incrementally builds your score; every missed payment "
                    "damages it. A single payment 30 days late can drop a 750-range score by "
                    "60–100 points. The impact is heavier for borrowers with shorter histories "
                    "and lighter for those with long, clean records.</p>"
                    "<p>Credit utilization accounts for 30% and measures the ratio of your "
                    "revolving balances to your credit limits, calculated both overall and "
                    "per card. If you carry $3,000 across cards with a $10,000 combined limit, "
                    "your utilization is 30%. Scores improve most noticeably when utilization "
                    "drops below 10%, and a large paydown can lift your score within a single "
                    "billing cycle because the model recalculates from the latest reported "
                    "statement balance each month.</p>"
                    "<p>The remaining three factors each carry less weight but still matter. "
                    "Length of credit history (15%) rewards older accounts and a longer average "
                    "account age — which is why keeping old cards open, even unused ones, "
                    "protects your score. Credit mix (10%) recognizes that managing both "
                    "revolving accounts (credit cards) and installment loans (auto, mortgage, "
                    "personal) signals broader financial capability. New credit (10%) covers "
                    "hard inquiries from applications, which typically reduce your score by "
                    "5–10 points and recover within 12 months.</p>"
                ),
            },
            {
                "kicker": "Score Ranges",
                "h2": "What the FICO Tiers Mean for Your Borrowing Costs",
                "body": (
                    "<p>FICO divides scores into five bands, and crossing a tier boundary "
                    "can materially change the rates and products available to you. Poor "
                    "(300–579) borrowers face the highest APRs and frequent denials. "
                    "Unsecured personal loans, when available at all, often carry APRs of "
                    "25–36%. Auto loan rates in this range regularly exceed 20%.</p>"
                    "<p>Fair (580–669) is the subprime zone. Some unsecured cards become "
                    "accessible, though APRs run 20–29% and limits are low. Mortgage access "
                    "is limited to FHA loans at elevated rates. Good (670–739) is where most "
                    "Americans sit. Prime credit card products become available, personal "
                    "loan rates drop toward 10–18%, and mortgage rates become competitive. "
                    "A jump from 668 to 672 — just four points — can open meaningfully "
                    "different product tiers.</p>"
                    "<p>Very Good (740–799) qualifies borrowers for most prime products and "
                    "the lower end of lender rate ranges. Exceptional (800–850) unlocks the "
                    "best available rates, most favorable transfer offers, and streamlined "
                    "approvals. In practice, the rate gap between 760 and 800+ is often small "
                    "— most lenders' best rates kick in around 740–760. The most impactful "
                    "score improvements are usually the ones that move you from one tier "
                    "boundary to the next, not marginal gains within the same band.</p>"
                ),
            },
            {
                "kicker": "Utilization",
                "h2": "How Credit Utilization Affects Your Score — And How to Fix It Fast",
                "body": (
                    "<p>Utilization is the most immediately actionable credit score factor "
                    "because it responds to changes in your current balances, not your "
                    "multi-year payment history. The calculation is simple: total revolving "
                    "balances divided by total revolving limits, times 100. The widely cited "
                    "30% guideline is a floor, not a target. Borrowers with Exceptional "
                    "scores typically carry utilization under 7–8%. Utilization above 50% "
                    "causes significantly more harm than utilization at 35%, and above 75% "
                    "on even a single card can suppress a score by 50–100 points on an "
                    "otherwise clean profile.</p>"
                    "<p>Both overall utilization and per-card utilization matter. You can "
                    "have low aggregate utilization but one nearly maxed card and still see "
                    "score suppression — the model treats individual card ratios as signals "
                    "of credit stress on specific accounts. A card at 85% utilization is a "
                    "higher-priority paydown target than two cards at 25%, even if the "
                    "dollar amounts involved are identical.</p>"
                    "<p>Two levers work quickly. First, pay down balances before your "
                    "statement closing date, not just before the due date. Most issuers "
                    "report the statement balance to the bureaus, so what's on your "
                    "statement is what determines your reported utilization — not what "
                    "you paid after the fact. Second, request a credit limit increase on "
                    "cards you're keeping open; a higher limit reduces your ratio without "
                    "requiring a paydown. Confirm with your issuer whether limit increases "
                    "trigger a soft or hard pull before requesting.</p>"
                ),
            },
            {
                "kicker": "New Credit",
                "h2": "Hard Inquiries, Rate Shopping, and Opening New Accounts",
                "body": (
                    "<p>When you apply for new credit, the lender pulls your credit report "
                    "in what's called a hard inquiry. This is recorded on your file and "
                    "typically reduces your score by 5–10 points. The impact is usually "
                    "minor and temporary — most hard inquiries stop affecting your score "
                    "meaningfully after 12 months and fall off your report after two years. "
                    "Soft inquiries — used for pre-qualification checks, employer background "
                    "reviews, and checking your own score — never affect your score at all.</p>"
                    "<p>Rate shopping is handled differently. FICO recognizes that "
                    "responsible borrowers compare loan offers before committing. Multiple "
                    "hard inquiries of the same type — mortgage, auto, or student loan — "
                    "within a 45-day window are treated as a single inquiry under FICO 8, "
                    "the most widely used version. Credit card applications do not receive "
                    "this treatment; each card application is its own inquiry.</p>"
                    "<p>Opening new accounts also lowers the average age of your accounts, "
                    "affecting the 15% length-of-credit-history component. A borrower with "
                    "three accounts averaging eight years who opens two new accounts "
                    "instantly drops their average to about 4.8 years. This drag is real "
                    "but temporary — accounts age quickly in their first year, and the "
                    "credit availability from a new account often outweighs the short-term "
                    "dip for borrowers with established histories.</p>"
                ),
            },
            {
                "kicker": "Credit Building",
                "h2": "How to Rebuild a Low Credit Score",
                "body": (
                    "<p>Rebuilding credit after missed payments, collections, or bankruptcy "
                    "follows a predictable sequence. The recovery timeline depends on what's "
                    "on your report and how aggressively you add positive history, but the "
                    "mechanics are the same regardless of your starting point.</p>"
                    "<p>The foundation is consistent on-time payments going forward. Because "
                    "payment history is 35% of your score, 12–24 months of clean history has "
                    "a measurable and growing effect. Secured credit cards — where you "
                    "provide a deposit (typically $200–$500) that becomes your credit limit "
                    "— are the most accessible tool. Capital One Secured Mastercard and "
                    "Discover it Secured both report to all three bureaus and offer upgrade "
                    "paths to unsecured cards after 6–12 months of responsible use. "
                    "Either card should be used for one small recurring purchase per month "
                    "and paid in full every statement — this generates positive payment "
                    "history at zero interest cost.</p>"
                    "<p>Becoming an authorized user on a trusted person's account can add a "
                    "significant boost quickly. If a parent or partner with a long, "
                    "low-utilization account adds you, that account's history can appear on "
                    "your report and raise your score 10–30 points within one or two billing "
                    "cycles. Derogatory marks — late payments, collections, charge-offs — "
                    "stay on your report for seven years (bankruptcies ten), but their "
                    "scoring impact diminishes significantly after two to three years, "
                    "especially when newer positive information accumulates alongside them.</p>"
                ),
            },
            {
                "kicker": "Monitoring",
                "h2": "Monitoring Your Credit and Disputing Errors",
                "body": (
                    "<p>Errors on credit reports are more common than most people realize. "
                    "A 2021 Consumer Reports study found that 34% of consumers who checked "
                    "their reports found at least one error. Common problems include accounts "
                    "that don't belong to you, incorrect late payment dates, balances that "
                    "haven't updated after payoff, duplicate collection entries for the same "
                    "debt, and accounts showing open that were closed years ago. Any of these "
                    "can suppress your score without you being aware.</p>"
                    "<p>Under the Fair Credit Reporting Act (FCRA), you can dispute any "
                    "inaccurate information, and the bureau must investigate within 30 days "
                    "(45 days in some circumstances). File disputes directly with the bureau "
                    "reporting the error — Experian, Equifax, or TransUnion — online, by "
                    "mail, or by phone. Include copies of documentation: a payoff letter, "
                    "bank statement showing a payment, or a letter from the original "
                    "creditor. Vague disputes without documentation are slower to resolve.</p>"
                    "<p>Free access to all three reports is available at "
                    "AnnualCreditReport.com — currently weekly under post-pandemic access "
                    "rules. Checking your own report is always a soft inquiry with zero "
                    "score impact. Real-time credit monitoring services alert you when "
                    "changes appear on any of your three bureau reports, making it easier "
                    "to catch errors and signs of identity theft quickly rather than "
                    "discovering them only when a loan application is declined.</p>"
                ),
            },
        ],
        "faqs": [
            ["What is a good credit score?",
             "670 or above is considered Good on the FICO scale. Most prime credit card "
             "products, competitive mortgage rates, and standard personal loan terms become "
             "accessible at 670. The practical sweet spot is 740+, where most lenders' "
             "best advertised rates begin. Crossing any tier boundary — for example moving "
             "from Fair to Good — typically has a larger real-world impact than marginal "
             "gains within the same band."],
            ["How quickly can I improve my credit score?",
             "The fastest improvement usually comes from paying down revolving balances "
             "before your statement closing date. Some borrowers see 20–40 point gains "
             "within a single billing cycle by reducing high utilization. Rebuilding "
             "payment history takes longer: 12 months of on-time payments creates a "
             "measurable positive pattern, but recovering from a recent late payment "
             "typically takes 12–24 months of clean history to offset significantly."],
            ["Does checking my own credit score lower it?",
             "No. Checking your own report or score is a soft inquiry and has no effect "
             "on your score. Only hard inquiries — when a lender pulls your report after "
             "you apply for credit — can temporarily lower your score. Most major card "
             "issuers now provide free FICO score monitoring through their mobile apps, "
             "so you can track your score without any risk."],
            ["How long do negative items stay on my report?",
             "Most negative information remains for seven years from the date of first "
             "delinquency: late payments, collections, charge-offs, and repossessions. "
             "Chapter 7 bankruptcies stay for ten years; Chapter 13 for seven. However, "
             "the scoring impact of old negatives diminishes over time, especially when "
             "newer positive history accumulates alongside them."],
            ["Can paying off a loan hurt my credit score?",
             "Paying off a loan can cause a small temporary dip because the active account "
             "closes, which may reduce credit mix and lower average account age. However, "
             "the benefit of eliminated debt and the positive payment history the account "
             "leaves behind far outweigh any short-term score movement in almost all cases. "
             "The dip is usually 5–15 points and recovers within a few months."],
            ["What is the difference between FICO and VantageScore?",
             "Both models use a 300–850 scale and evaluate similar factors, but FICO is "
             "used in over 90% of U.S. lending decisions. VantageScore 4.0 can generate a "
             "score with as little as one month of credit history, making it useful for "
             "thin-file consumers. Many free monitoring services show VantageScore; most "
             "lenders use FICO. Knowing which model a specific lender uses before applying "
             "helps you interpret your score correctly."],
        ],
    },

    # -----------------------------------------------------------------------
    "pages/how-credit-scores-work.html": {
        "intro_h2": "The Mathematics Behind Credit Scoring",
        "intro_body": (
            "<p>Credit scores are produced by applying a mathematical model to the data "
            "in your credit report. The model translates your borrowing behavior — how "
            "often you pay on time, how much of your available credit you use, how long "
            "your accounts have been open — into a three-digit number between 300 and "
            "850. FICO, developed by the Fair Isaac Corporation, is the dominant model: "
            "it's used in over 90% of U.S. lending decisions. VantageScore, created "
            "jointly by the three major credit bureaus, is a competing model with the "
            "same numerical range.</p>"
            "<p>Understanding exactly how each scoring factor works is more useful than "
            "chasing a target number. When you know that utilization has the second-largest "
            "weight and resets with every billing cycle, you can make tactical decisions "
            "about when to pay down balances and when to apply for new credit. When you "
            "know that authorized user accounts are reported to your file, you can explore "
            "that strategy deliberately. The mechanics are not secret — they're documented "
            "by FICO and the bureaus — but most borrowers never learn them systematically.</p>"
        ),
        "sections": [
            {
                "kicker": "Scoring Models",
                "h2": "FICO vs VantageScore: Two Models, One Range",
                "body": (
                    "<p>FICO 8, the most widely deployed version, requires at least one "
                    "account that has been open for six months and at least one account "
                    "reported to the bureau within the past six months. Borrowers with very "
                    "thin credit files may not have a FICO score at all — a limitation that "
                    "affects roughly 26 million Americans according to the CFPB.</p>"
                    "<p>VantageScore 3.0 and 4.0 can generate a score with as little as one "
                    "month of history and one account reported in the past two years, which "
                    "is why many free credit monitoring services default to VantageScore — it "
                    "produces a score for more people. VantageScore 4.0 also incorporates "
                    "trended data, meaning it considers whether your balances have been "
                    "rising or falling over the past 24 months, not just their current "
                    "snapshot. A borrower who has been steadily paying down debt may score "
                    "higher under VantageScore 4.0 than FICO even with identical current "
                    "balances.</p>"
                    "<p>In practice: confirm which model your lender uses before applying. "
                    "Mortgage lenders typically use FICO 2, 4, or 5 — older versions that "
                    "weight mortgage-specific factors somewhat differently than FICO 8. "
                    "Auto lenders often use FICO Auto Score 8. Credit card issuers typically "
                    "use FICO 8 or VantageScore 3.0. The score you see in a free monitoring "
                    "app may be 20–40 points different from what a mortgage lender pulls.</p>"
                ),
            },
            {
                "kicker": "Five Factors",
                "h2": "The Five Factors Behind Your FICO Score",
                "body": (
                    "<p>Payment history (35%): Every payment is recorded as on-time or late. "
                    "Payments that are 30, 60, 90, and 120+ days late are tracked separately "
                    "and treated as progressively more serious. A single 30-day late payment "
                    "on an otherwise clean account can drop a 750-range score by 60–110 "
                    "points. The damage is heavier when credit history is short and lighter "
                    "when years of clean history exist behind it.</p>"
                    "<p>Amounts owed (30%): Primarily your revolving utilization ratio — "
                    "how much you owe on credit cards and other revolving accounts relative "
                    "to their limits. Installment loan balances (mortgage, auto, personal) "
                    "also factor in here, but utilization on revolving accounts drives most "
                    "of the scoring action. Length of credit history (15%) covers the age "
                    "of your oldest account, newest account, and average age of all accounts. "
                    "Keeping older accounts open — even rarely used ones — protects this "
                    "factor, which is why closing an old card can cause a temporary score dip.</p>"
                    "<p>Credit mix (10%) rewards managing both installment and revolving "
                    "accounts, demonstrating you can handle different credit structures. "
                    "This factor matters more when the rest of your profile is thin — you "
                    "shouldn't open accounts you don't need just to improve it. New credit "
                    "(10%) covers hard inquiries from applications, each of which reduces "
                    "your score by roughly 5–10 points. Multiple same-type inquiries within "
                    "45 days are treated as a single inquiry under FICO 8 when shopping for "
                    "a mortgage, auto loan, or student loan.</p>"
                ),
            },
            {
                "kicker": "Inquiries",
                "h2": "Soft vs Hard Inquiries: Which Affects Your Score",
                "body": (
                    "<p>Hard inquiries occur when you apply for credit — a credit card, "
                    "personal loan, auto loan, mortgage, or most other credit products. You "
                    "authorize this when you submit an application. Hard inquiries reduce "
                    "your FICO score by roughly 5–10 points for most borrowers and remain "
                    "on your credit report for two years. Their scoring impact fades "
                    "significantly after 12 months.</p>"
                    "<p>Soft inquiries occur in situations that don't involve a credit "
                    "application: checking your own score, a lender running a pre-approval "
                    "check, an employer doing a background review, or an existing creditor "
                    "doing routine account monitoring. Soft inquiries are visible on your "
                    "own report if you request it, but lenders cannot see them and they have "
                    "zero effect on your score — ever, under any circumstances.</p>"
                    "<p>The common confusion: when a card company mails you a pre-approved "
                    "offer, that pre-check used a soft pull against bureau marketing data. "
                    "You're not actually approved yet — the hard pull happens when you "
                    "formally apply. Most major card issuers offer pre-qualification tools "
                    "on their websites that use soft inquiries to estimate your approval "
                    "odds without affecting your score. Using these before applying formally "
                    "helps target applications toward cards you're likely to receive.</p>"
                ),
            },
            {
                "kicker": "Negative Marks",
                "h2": "How Derogatory Marks Work and How Long They Last",
                "body": (
                    "<p>Derogatory marks are negative items that reflect serious credit "
                    "problems. Late payments stay on your report for seven years from the "
                    "date of first delinquency. A payment 90 days late can drop a score of "
                    "700 by 100 points or more. The later the payment — 60, 90, 120+ days "
                    "— the more severe the initial damage, and the longer it takes to "
                    "rebuild positive history around it.</p>"
                    "<p>Collections appear when a debt is sold to a collection agency. "
                    "Under FICO 9 and VantageScore 4.0, paid collections have no scoring "
                    "impact. Under FICO 8 (still the most widely used model), paid "
                    "collections may still suppress your score — which is why paying a "
                    "collection doesn't always produce an immediate score improvement. "
                    "Charge-offs occur when a lender writes off a debt as uncollectible "
                    "(typically after 180 days of non-payment) and stay on your report "
                    "for seven years even after the underlying debt is settled.</p>"
                    "<p>Chapter 7 bankruptcy stays for ten years from the filing date. "
                    "Chapter 13 stays for seven years. The immediate impact is severe — "
                    "typically 100–200 points — but the trajectory improves significantly "
                    "if you rebuild actively. Many borrowers reach the 600s by year three "
                    "of a Chapter 7 discharge when they use credit responsibly afterward. "
                    "The scoring impact of derogatory marks diminishes over time; a "
                    "three-year-old collection hurts less than one from last month on an "
                    "otherwise identical credit profile.</p>"
                ),
            },
            {
                "kicker": "Credit Building",
                "h2": "Authorized User Strategy: How Being Added to a Card Helps",
                "body": (
                    "<p>Being added as an authorized user on someone else's credit card "
                    "account is one of the fastest legal credit-building strategies "
                    "available. When an issuer adds you as an authorized user, the "
                    "account — including its age, credit limit, utilization history, "
                    "and payment record — typically appears on your credit report. You "
                    "don't need to use the card or even possess it to benefit from the "
                    "reporting history.</p>"
                    "<p>The impact depends heavily on the primary account's quality. The "
                    "ideal account to be added to is old (10+ years), low utilization "
                    "(under 10%), and clean payment history. Being added to a maxed-out "
                    "card with missed payments will hurt your score rather than help it. "
                    "Not all issuers report authorized user accounts to all three bureaus "
                    "— American Express, Chase, Citibank, and Capital One generally do. "
                    "Confirm this before asking someone to add you.</p>"
                    "<p>The realistic score improvement from being added to a well-maintained "
                    "account varies by profile. Borrowers with thin files or short histories "
                    "often see improvements of 10–30 points within one to two billing cycles. "
                    "The strategy works best as a supplement to building your own credit, "
                    "not a replacement. Using a secured card simultaneously while leveraging "
                    "authorized user status creates two parallel credit-building tracks and "
                    "accelerates the timeline toward a standard credit profile.</p>"
                ),
            },
            {
                "kicker": "Disputes",
                "h2": "Disputing Errors on Your Credit Report Under the FCRA",
                "body": (
                    "<p>Under the Fair Credit Reporting Act, you have the right to dispute "
                    "any information in your credit report you believe is inaccurate or "
                    "incomplete. The bureau receiving the dispute must investigate within "
                    "30 days (45 days in some circumstances) and correct or remove "
                    "information that cannot be verified by the original furnisher.</p>"
                    "<p>The three major bureaus — Experian, Equifax, and TransUnion — "
                    "maintain independent databases. An error on one report doesn't "
                    "automatically mean the same error appears on the others. Common errors "
                    "include accounts that don't belong to you (possible identity theft or "
                    "name confusion), duplicate collection entries for the same debt, "
                    "balances not updated after payoff, and accounts showing open that were "
                    "closed years ago. Any of these can suppress your score without your "
                    "knowledge.</p>"
                    "<p>To dispute effectively: file directly with the bureau reporting the "
                    "error online, by certified mail, or by phone. Be specific about the "
                    "account name, number, and nature of the error. Attach documentation "
                    "when available — a payoff letter, a bank statement, or a letter from "
                    "the original creditor. Vague disputes without documentation are slower "
                    "to resolve. If the bureau's investigation removes the item, monitor "
                    "your report over the next 30–60 days to confirm it stays removed; some "
                    "furnishers re-report corrected information, requiring a second dispute "
                    "or escalation to the CFPB.</p>"
                ),
            },
        ],
        "faqs": [
            ["What's the minimum credit history needed for a FICO score?",
             "FICO 8 requires at least one account open for six months and at least one "
             "account reported to the bureau within the past six months. VantageScore can "
             "score borrowers with as little as one month of history and one account "
             "reported in the past two years, which is why many free monitoring services "
             "use it — it produces a score for more people."],
            ["Does my income affect my credit score?",
             "No. Credit scores are based entirely on information in your credit report: "
             "payment history, account balances, credit age, mix, and inquiry activity. "
             "Income, employment status, savings balances, and net worth are not scoring "
             "factors at all. Lenders check income separately when evaluating an "
             "application, but it has no bearing on the three-digit score itself."],
            ["If I pay off a collection, will it disappear from my report?",
             "No. Paying a collection changes its status from unpaid to paid but does not "
             "remove it from your report. Under FICO 8 (still the most widely used model), "
             "paid collections can still affect your score. Under FICO 9 and VantageScore "
             "4.0, paid collections are ignored in scoring entirely. The collection remains "
             "visible on your report for seven years from the date of first delinquency "
             "regardless of payment status."],
            ["How often do credit scores update?",
             "Credit scores are recalculated every time a lender requests them, based on "
             "the most current data in your file. Lenders typically report new account "
             "information — balances, payment status — to the bureaus monthly. So your "
             "score effectively refreshes monthly as new data flows in. Some monitoring "
             "services update your displayed score weekly or daily as their data refreshes, "
             "even though lender-reported data still cycles monthly."],
            ["Does closing a credit card hurt my score?",
             "It can. Closing a card reduces your total available credit (raising "
             "utilization on remaining cards) and, if it's an old account, lowers the "
             "average age of your accounts. The effect is usually small for people with "
             "multiple other accounts but can be meaningful for thin-file borrowers. "
             "Keeping zero-balance cards open, especially old ones, is generally the "
             "right default — the utilization and age protection outweighs any marginal "
             "reason to close them."],
            ["Can a landlord check my credit?",
             "Yes. Landlords typically request your permission to pull your credit report "
             "as part of a rental application. This generates a hard inquiry and does "
             "affect your score, though the impact is small and temporary (5–10 points). "
             "Some landlords use screening services that pull soft inquiries instead — "
             "ask which type before consenting to avoid unnecessary hard inquiries during "
             "a period when you're also applying for other credit."],
        ],
    },

    # -----------------------------------------------------------------------
    "pages/best-credit-cards-for-bad-credit.html": {
        "intro_h2": "How to Choose a Card That Actually Rebuilds Credit",
        "intro_body": (
            "<p>A credit score below 580 doesn't disqualify you from credit entirely — "
            "it redirects you toward products designed for the rebuilding phase. The right "
            "card at this stage isn't about rewards or perks. It's a tool for adding "
            "consistent positive payment history to your credit report month by month until "
            "you qualify for standard products. Every month of on-time payments is a "
            "building block; every missed payment is a setback that extends your timeline "
            "significantly.</p>"
            "<p>The primary options are secured credit cards, which require an upfront "
            "deposit that typically becomes your credit limit, and a smaller number of "
            "unsecured starter cards designed for subprime borrowers. Both types report to "
            "the major credit bureaus — that's the fundamental requirement. A card that "
            "doesn't report your payments to all three bureaus doesn't help your score, "
            "regardless of how responsibly you use it. This guide covers the mechanics, "
            "what to expect in fees and APRs, how to actually move your score with a "
            "secured card, and what to look for in the top options available in 2026.</p>"
        ),
        "sections": [
            {
                "kicker": "Card Types",
                "h2": "Secured vs Unsecured Cards: Which Makes More Sense for Rebuilding",
                "body": (
                    "<p>A secured credit card requires you to deposit money with the issuer "
                    "as collateral. That deposit — usually $200–$500 — becomes your credit "
                    "limit. From the issuer's perspective the risk is minimal: if you don't "
                    "pay, they keep your deposit. This lower risk is why secured cards are "
                    "accessible to borrowers with scores in the 500s or even no credit "
                    "history at all. The card operates identically to a regular credit card "
                    "for purchases and reporting purposes.</p>"
                    "<p>Unsecured starter cards for bad credit don't require a deposit but "
                    "compensate for higher lender risk with APRs of 25–29.99%, annual fees "
                    "of $75–$99, and initial limits of $300–$500. When you have a $300 "
                    "limit and a $75 annual fee charged to the account on day one, your "
                    "utilization is immediately 25% before you've made a single purchase. "
                    "Some also charge monthly maintenance fees on top of the annual fee. "
                    "The fee burden on these cards is disproportionate to the credit limit "
                    "they provide.</p>"
                    "<p>The practical comparison: if you can afford to tie up $200–$500 in "
                    "a deposit, a secured card from a reputable issuer is almost always the "
                    "better rebuilding tool. Your deposit comes back to you — either when "
                    "you upgrade to an unsecured card or when you close the account in good "
                    "standing. One critical detail: confirm the card reports to all three "
                    "bureaus (Experian, Equifax, and TransUnion). Some prepaid and "
                    "credit-builder cards only report to one or two.</p>"
                ),
            },
            {
                "kicker": "Costs",
                "h2": "What to Expect in APRs, Fees, and Credit Limits",
                "body": (
                    "<p>Secured and subprime unsecured cards carry higher costs across the "
                    "board. APRs typically range from 24.99% to 29.99%. Capital One Secured "
                    "currently carries a variable APR of 29.99%. Discover it Secured runs "
                    "at 28.24% variable. These rates are high, but they don't matter if you "
                    "pay your full statement balance every month — which should be your "
                    "default operating mode during the rebuilding phase. Carrying a balance "
                    "at these APRs compounds debt rapidly and undercuts the financial "
                    "improvement you're trying to build.</p>"
                    "<p>Annual fees vary significantly across products. The best secured "
                    "cards — Capital One Secured Mastercard and Discover it Secured — charge "
                    "no annual fee. Others charge $35–$99. A $99 annual fee on a $300 "
                    "secured card represents a 33% annualized cost on the credit available "
                    "to you, which is a poor value regardless of how it's structured. "
                    "Always calculate the annual fee as a percentage of your credit limit "
                    "before selecting a card.</p>"
                    "<p>Initial credit limits are typically equal to your deposit for "
                    "secured cards. Some issuers allow higher deposits for higher limits — "
                    "useful if you want a limit high enough to put meaningful purchases on "
                    "it without spiking your utilization. Capital One allows secured "
                    "deposits of $49, $99, or $200 for an initial $200 limit, then "
                    "automatically evaluates cardholders for limit increases after five "
                    "months of on-time payments.</p>"
                ),
            },
            {
                "kicker": "Usage Strategy",
                "h2": "How to Use a Secured Card to Actually Move Your Score",
                "body": (
                    "<p>Having a secured card doesn't automatically improve your credit "
                    "score — using it in a specific way does. Make one small purchase per "
                    "month. A $10–$20 recurring charge — a streaming subscription, a small "
                    "utility payment, anything you'd pay anyway — keeps the account active "
                    "and generates a monthly payment event to report. Accounts with no "
                    "activity can be closed by the issuer, and complete inactivity signals "
                    "that the card isn't functioning as a real credit account.</p>"
                    "<p>Pay the full statement balance before the due date every month "
                    "without exception. This builds a streak of on-time payment history — "
                    "the most important scoring factor — and keeps your interest charges at "
                    "exactly zero. Set up autopay for the full statement balance to "
                    "eliminate the risk of accidentally missing a payment due to a busy "
                    "month. Keep your utilization below 30% (ideally below 10%) by not "
                    "letting charges approach your limit before the statement closes.</p>"
                    "<p>Typical improvement trajectory: borrowers starting with a 580–600 "
                    "score who use a secured card responsibly for 12 months often reach "
                    "640–680. Those who also keep utilization under 10% and add a "
                    "credit-builder loan frequently break into the 700s by month 18–24. "
                    "Monitor your credit report at least quarterly to confirm the card is "
                    "reporting to all three bureaus and that payments are being recorded "
                    "correctly. Many issuers — including Discover and Capital One — provide "
                    "free FICO score tracking in their apps.</p>"
                ),
            },
            {
                "kicker": "Top Options",
                "h2": "Best Secured Cards for Rebuilding in 2026",
                "body": (
                    "<p>Capital One Secured Mastercard charges no annual fee, reports to "
                    "all three bureaus, and offers a $200 initial credit limit with deposit "
                    "options of $49, $99, or $200 depending on your creditworthiness at "
                    "application. Capital One runs automatic credit line reviews after five "
                    "months of on-time payments, and when eligible, the card can be upgraded "
                    "to a standard unsecured card without closing the account — preserving "
                    "the account age you've built.</p>"
                    "<p>Discover it Secured charges no annual fee, reports to all three "
                    "bureaus, and requires a minimum $200 deposit. It earns 2% cash back at "
                    "gas stations and restaurants (up to $1,000 per quarter) and 1% "
                    "everywhere else — unusual for a secured card. Discover begins automatic "
                    "upgrade reviews at 7 months, and after your first year, matches all "
                    "cash back earned in the first 12 months. For borrowers who plan to pay "
                    "in full monthly anyway, the rewards are a bonus on top of the "
                    "credit-building function.</p>"
                    "<p>What to avoid: cards with monthly maintenance fees, program fees "
                    "charged before account opening, annual fees above $35 on a $200–$500 "
                    "limit, or cards that only report to one bureau. Store-branded secured "
                    "cards (retail co-brand secured products) typically report to fewer "
                    "bureaus and offer limited credit limit growth paths. General-purpose "
                    "secured cards from major issuers are consistently better rebuilding "
                    "vehicles than store-specific alternatives.</p>"
                ),
            },
            {
                "kicker": "Graduation",
                "h2": "When and How to Transition to an Unsecured Card",
                "body": (
                    "<p>Graduation from secured to unsecured happens in one of two ways: "
                    "the issuer upgrades you proactively, or you apply for a new unsecured "
                    "card once your score has improved. For automatic upgrades, issuers "
                    "like Capital One and Discover review secured cardholders periodically "
                    "for eligibility. The minimum window is typically 6–12 months of "
                    "on-time payments with consistent low utilization. When approved, your "
                    "deposit is returned, your limit often increases, and the account "
                    "history carries over — you don't lose the positive months you built.</p>"
                    "<p>For applying independently: once your score reaches 640–660, you "
                    "may qualify for the lower tier of standard unsecured products. At 670+ "
                    "more options open. Apply for one new card at a time to limit hard "
                    "inquiries. After getting an unsecured card, closing the secured card "
                    "is optional — keeping it open maintains your credit limit (good for "
                    "utilization) and preserves account age. If it charges a high annual "
                    "fee, the calculus changes.</p>"
                    "<p>Timeline benchmarks: 12 months of responsible secured card use "
                    "from a starting score of 580–600 typically lands you at 630–660. "
                    "18–24 months with consistent behavior, low utilization, and no new "
                    "derogatory marks commonly produces scores in the 670–700+ range. The "
                    "credit-building phase is finite — every month of clean history, every "
                    "billing cycle with low utilization, and every avoided unnecessary "
                    "application moves the score in the right direction.</p>"
                ),
            },
        ],
        "faqs": [
            ["Do I get my deposit back from a secured credit card?",
             "Yes, in two situations: when the issuer upgrades you to an unsecured card "
             "(your deposit is returned and the account continues with the same history), "
             "or when you close the account in good standing. Most issuers return deposits "
             "within 1–2 billing cycles of closure or upgrade. Make sure your balance is "
             "fully paid before requesting account closure."],
            ["What credit score do I need for a secured card?",
             "Most secured cards don't set a minimum score — they're specifically designed "
             "for people with poor credit or no credit history. Some issuers will decline "
             "applicants with very recent charge-offs or bankruptcies, but a score of "
             "500–580 is generally sufficient for approval at most major issuers. If you're "
             "unsure, use the issuer's pre-qualification tool before formally applying to "
             "avoid an unnecessary hard inquiry."],
            ["Can I build credit with a $200 secured card?",
             "Yes, but use it precisely. One purchase per month, paid in full before the "
             "due date, with utilization kept under 30% (ideally under 10%). At those "
             "settings, a $200 secured card generates exactly as much positive payment "
             "history as a $5,000 card — the credit limit matters far less than the "
             "consistency of your payment behavior."],
            ["Is a secured card better than a credit-builder loan?",
             "They serve different purposes and work well in combination. A secured card "
             "builds revolving credit history and helps you practice utilization management. "
             "A credit-builder loan (offered by many credit unions) adds installment loan "
             "history, improving your credit mix. Using both simultaneously builds two "
             "parallel credit tracks and typically accelerates the path to a standard "
             "credit profile more than either tool alone."],
            ["How long does it take to go from poor to good credit?",
             "Starting from 550–580 with no ongoing derogatory activity — no new late "
             "payments — most borrowers who use credit responsibly reach Good (670) in "
             "18–30 months. The exact timeline depends on the severity and age of past "
             "negatives, and how actively you add positive history through secured cards "
             "or other credit-building products. There are no shortcuts that compress this "
             "timeline safely."],
        ],
    },

    # -----------------------------------------------------------------------
    "pages/debt-payoff-guide.html": {
        "intro_h2": "Why Most Debt Payoff Plans Fail — and How to Fix Them",
        "intro_body": (
            "<p>U.S. household credit card debt has remained near record highs in recent years, "
            "with average balances among households carrying debt running into the thousands of "
            "dollars (source: <a href=\"https://www.federalreserve.gov/releases/g19/current/\" target=\"_blank\" rel=\"noopener nofollow\">Federal Reserve G.19 Consumer Credit release</a>). "
            "Average credit card APRs have stayed well above 20% — the highest sustained level since "
            "the Federal Reserve began tracking the series. At those rates, even partially-paid "
            "balances generate substantial interest each year. The minimum payment trap makes it "
            "worse: a $5,000 balance at 20% APR paying the standard minimum takes approximately "
            "17 years to retire and costs over $4,300 in interest — more than 85 cents in interest "
            "for every dollar originally borrowed.</p>"
            "<p>Use the <a href=\"/pages/debt-avalanche-vs-snowball-calculator\">avalanche vs snowball calculator</a> to compare both methods on your specific balances and APRs.</p>"
            "<p>The problem is almost never a lack of desire to eliminate debt. It's choosing "
            "the wrong strategy, applying extra payments to the wrong accounts, or "
            "abandoning a plan when motivation drops. This guide covers the two primary "
            "repayment methods, the emergency fund tradeoff most plans get wrong, when "
            "consolidation actually helps, and how to build a timeline that survives real "
            "life without requiring perfect execution every month.</p>"
        ),
        "sections": [
            {
                "kicker": "Avalanche Method",
                "h2": "Paying the Highest APR First: How the Avalanche Method Works",
                "body": (
                    "<p>The debt avalanche is the mathematically optimal repayment strategy. "
                    "List your debts by interest rate, highest first, and direct all extra "
                    "payments toward the highest-rate balance while making minimum payments "
                    "on all others. When the top debt is eliminated, roll its freed payment "
                    "amount into the next-highest-rate balance. This creates a compounding "
                    "acceleration — each paid-off debt increases the payment available for "
                    "the next one.</p>"
                    "<p>Here's why it minimizes total cost: interest accrues daily on "
                    "revolving debt. The higher the rate, the faster the balance grows "
                    "between payments. Concentrating your extra dollars on the highest-rate "
                    "debt reduces the amount generating the most expensive interest as "
                    "quickly as possible. Example: three debts — a credit card at 26.99% "
                    "with $3,200, a store card at 29.99% with $850, and a personal loan at "
                    "14.5% with $6,000. The avalanche sequence starts with the 29.99% "
                    "store card (smallest but highest rate), then the 26.99% card, then "
                    "the loan. Compared to paying in reverse order, this saves hundreds "
                    "in total interest.</p>"
                    "<p>The primary drawback is motivational: if the highest-rate debt also "
                    "happens to be the largest balance, it can take months before any "
                    "account is fully paid off. For people who need early wins to stay "
                    "disciplined, the long wait can cause them to abandon the plan. "
                    "A practical variant: if two debts are within 2–3 percentage points of "
                    "each other, tackle the smaller one first for a quick closure, then "
                    "pivot fully to the higher-rate balance. The math is nearly identical "
                    "but the psychological win is real.</p>"
                ),
            },
            {
                "kicker": "Snowball Method",
                "h2": "Smallest Balance First: The Psychology Behind the Snowball",
                "body": (
                    "<p>The debt snowball prioritizes paying off the smallest balance first, "
                    "regardless of interest rate. Once the smallest debt is gone, the freed "
                    "payment amount rolls into the next-smallest balance, and so on. "
                    "The snowball doesn't minimize interest paid — but behavioral research "
                    "consistently shows that people are significantly more likely to stick "
                    "with a repayment plan when they get early account closures. Eliminating "
                    "an account entirely triggers a sense of completion that a partial "
                    "paydown doesn't replicate.</p>"
                    "<p>The practical tradeoff: the snowball costs more in total interest "
                    "than the avalanche, but only when you actually complete both. A "
                    "repayment method you finish is always superior to the theoretically "
                    "optimal method you abandon six months in. If you know from experience "
                    "that you need visible progress markers to maintain discipline, the "
                    "snowball's interest premium may be worth paying. The real cost "
                    "difference between the two methods is typically hundreds, not "
                    "thousands, on average debt loads — meaningful but not ruinous.</p>"
                    "<p>Hybrid approach: start with the snowball to build momentum through "
                    "the first two or three payoffs, then shift to the avalanche for the "
                    "remaining larger, higher-rate balances. This is not mathematically "
                    "perfect but is behaviorally practical for many households. Some "
                    "financial planners recommend it explicitly for clients who have "
                    "abandoned structured plans in the past. The goal is not the optimal "
                    "strategy on paper — it's completing a strategy that works in practice.</p>"
                ),
            },
            {
                "kicker": "Minimum Payment Trap",
                "h2": "The Real Cost of Paying Only the Minimum",
                "body": (
                    "<p>Minimum payments are structured to keep you in debt as long as "
                    "possible while maintaining account standing. Most card issuers set "
                    "minimums at 1–2% of the balance plus interest charges, or $25–$35, "
                    "whichever is greater. This produces the maximum interest income for "
                    "the lender while keeping the payment low enough to feel manageable.</p>"
                    "<p>The actual math: a $5,000 balance at 20% APR on minimum payments "
                    "(approximately $100 on the first statement, declining as the balance "
                    "drops) takes roughly 17 years to pay off and generates $4,300+ in "
                    "interest — the equivalent of paying for the original purchase twice. "
                    "The same $5,000 with a fixed $200/month payment is paid off in "
                    "approximately 32 months with roughly $1,300 in interest. Fixed "
                    "$300/month: 20 months and $800 in interest. Even an extra $50 above "
                    "the minimum meaningfully shortens the payoff timeline.</p>"
                    "<p>The second trap: many people aggressively pay down a balance, feel "
                    "relief, and gradually rebuild it. Debt payoff strategy must pair with "
                    "behavior change in the category that created the balance. If the debt "
                    "came from routine overspending on dining and entertainment, freeing "
                    "cash flow through paydown without addressing that pattern recreates "
                    "the debt within 12–18 months. The payoff plan and the spending plan "
                    "have to be built together.</p>"
                ),
            },
            {
                "kicker": "Emergency Fund",
                "h2": "Emergency Fund vs Debt Payoff: Finding the Right Balance",
                "body": (
                    "<p>Whether to build an emergency fund before aggressively paying down "
                    "debt is one of the most common questions in personal finance. The "
                    "answer depends on the APR of your debt and your risk of an unexpected "
                    "expense. Without any buffer, a single $800 car repair or $500 medical "
                    "bill goes straight onto the credit card you just paid down — wiping "
                    "out weeks of progress and potentially adding to the debt load.</p>"
                    "<p>A practical framework: maintain a starter emergency fund of "
                    "$1,000–$2,000 before shifting to aggressive debt paydown. This isn't "
                    "enough for a major emergency, but it covers most routine unexpected "
                    "expenses that would otherwise derail a repayment plan. The carrying "
                    "cost of that $1,000 reserve against 24% APR debt is about $240/year "
                    "in foregone interest savings — a reasonable price for the insurance "
                    "against restarting your payoff process after an unavoidable expense.</p>"
                    "<p>After the starter fund is in place and high-rate debt is under "
                    "control: build toward 3–6 months of essential expenses. Retirement "
                    "contributions complicate this — if your employer matches 401(k) "
                    "contributions, capturing the full match (often 50–100% on 3–6% of "
                    "salary) is generally worth continuing even while paying down credit "
                    "card debt, since the employer match is an immediate guaranteed return "
                    "that typically exceeds even high-rate card APRs.</p>"
                ),
            },
            {
                "kicker": "Consolidation",
                "h2": "When Debt Consolidation Actually Saves Money",
                "body": (
                    "<p>Debt consolidation — rolling multiple balances into a single lower-rate "
                    "loan — works when used correctly and backfires when used carelessly. "
                    "The right scenario: you have multiple credit card balances at 22–27% "
                    "APR, you qualify for a personal consolidation loan at 11–14% APR, and "
                    "you can complete the payoff within the loan term. Federal Reserve data "
                    "shows average personal loan APRs of approximately 11–12% for "
                    "well-qualified borrowers — roughly half the average card rate.</p>"
                    "<p>Example: $12,000 consolidated from 24% card APR to 11% personal "
                    "loan over 36 months requires a $393/month payment and totals about "
                    "$1,148 in interest. The same $12,000 on credit cards paying $393/month "
                    "at 24% takes about 41 months and costs $4,100+ in interest. That's a "
                    "savings of nearly $3,000. Balance transfer cards — 0% APR for 12–21 "
                    "months with a 3–5% transfer fee — offer an even lower-cost option "
                    "for balances you can realistically pay off within the promotional "
                    "window.</p>"
                    "<p>The trap: consolidation restructures debt rather than reducing it. "
                    "Borrowers who consolidate and then run the cards back up now have both "
                    "the consolidation loan and new card balances. This outcome is more "
                    "common than most people expect. Before consolidating, answer honestly: "
                    "can you stop using the cards you're consolidating? A practical "
                    "safeguard: keep zero-balance cards open for credit score purposes but "
                    "remove them from your wallet and unlink them from online payment "
                    "profiles to create friction against impulsive use.</p>"
                ),
            },
            {
                "kicker": "Timeline Planning",
                "h2": "Building a Payoff Timeline That Survives Real Life",
                "body": (
                    "<p>The gap between a debt payoff plan and actual debt payoff is usually "
                    "a realistic monthly budget. Plans fail when they assume a level of "
                    "surplus that doesn't exist after rent, groceries, transportation, and "
                    "other fixed costs. Build the timeline backward: start with your "
                    "take-home pay, subtract all fixed expenses, identify the maximum you "
                    "can realistically direct toward debt each month, then calculate how "
                    "long each sequence takes with that payment amount.</p>"
                    "<p>The most critical variable: irregular expenses. Payoff calculators "
                    "don't account for the routine irregular costs that appear in real "
                    "budgets — car registration, home repairs, medical copays, seasonal "
                    "spending. These are predictable in aggregate even when unpredictable "
                    "in timing. A plan that builds in a $100–$200/month cushion for "
                    "irregular expenses survives real life better than one that commits "
                    "your entire theoretical surplus to debt paydown.</p>"
                    "<p>The behavioral architecture matters too. Automating extra debt "
                    "payments on the day you're paid — before discretionary spending "
                    "absorbs the surplus — is one of the highest-leverage habits available. "
                    "Weekly or bi-monthly payments aligned with your paycheck schedule "
                    "work better than end-of-month scrambles to find extra funds. "
                    "Tracking the target balance on a simple chart creates the visual "
                    "reinforcement that sustains a 12–24 month commitment, especially "
                    "through the slower initial months when the balance seems to move "
                    "very little.</p>"
                ),
            },
        ],
        "faqs": [
            ["Is the debt avalanche always the best method?",
             "Mathematically yes — it minimizes total interest paid. But the best method "
             "is the one you actually complete. If you have a history of abandoning "
             "structured financial plans, the snowball's early wins may produce a better "
             "real-world outcome than the theoretically optimal avalanche. Some people "
             "successfully use the snowball for the first few payoffs to build momentum, "
             "then switch to avalanche for the remaining larger balances."],
            ["Should I pay off debt or invest?",
             "If your debt carries an APR above 7–8%, paying it down produces a guaranteed "
             "tax-equivalent return equal to that rate. Stock market long-term average "
             "returns are approximately 7–10% before inflation and are not guaranteed. "
             "Eliminating 24% APR credit card debt is a risk-free 24% return — far "
             "better than any standard investment option. The one exception is employer "
             "401(k) matching, which represents an immediate 50–100% return and is "
             "generally worth capturing even while paying down high-rate debt."],
            ["How long does debt payoff actually take?",
             "A $15,000 balance at 22% APR with $500/month payments takes approximately "
             "44 months and costs $6,500 in interest. The same balance with $750/month "
             "takes 25 months and costs $4,000 in interest. Every additional $100/month "
             "makes a larger difference than most people expect — often cutting months "
             "off the timeline rather than weeks. Use a fixed-payment calculator rather "
             "than minimum-payment math to see realistic timelines."],
            ["Does consolidating debt hurt my credit score?",
             "Applying for a consolidation loan triggers a hard inquiry (5–10 point "
             "temporary impact) and opens a new account. However, paying off the credit "
             "card balances dramatically reduces your utilization ratio, which typically "
             "produces a net score improvement within 1–3 months. The long-term effect "
             "of consistent installment loan payments on a consolidation loan is positive. "
             "Most borrowers see a net score increase within 60–90 days of consolidating."],
            ["What if I can only afford minimum payments right now?",
             "Continue making minimum payments on all accounts to avoid late marks, which "
             "would make the situation significantly worse. Focus on stabilizing income or "
             "reducing fixed expenses before adding extra payments. Contact issuers about "
             "hardship programs — many reduce APRs to 9.9% for 12–18 months for customers "
             "experiencing financial difficulty. Nonprofit credit counseling agencies "
             "(NFCC members) can also negotiate rate reductions across multiple cards "
             "simultaneously as part of a structured Debt Management Plan."],
        ],
    },

    # -----------------------------------------------------------------------
    "pages/credit-utilization-calculator.html": {
        "intro_h2": "How to Use This Calculator",
        "intro_body": (
            "<p>Credit utilization is the ratio of your revolving credit card balances to "
            "your total credit limits — and it accounts for 30% of your FICO score, making "
            "it the second most important scoring factor after payment history. Unlike "
            "payment history, which builds slowly over months and years, utilization "
            "responds to changes in your current balances. A large paydown can improve your "
            "score within a single billing period.</p>"
            "<p>Enter your balance and credit limit for each card below. The calculator "
            "shows your per-card utilization, your overall utilization across all cards, "
            "and your current position relative to the thresholds that affect scoring. "
            "Use the results to identify which card is the highest-priority paydown target "
            "and how much you'd need to pay to cross key utilization thresholds.</p>"
        ),
        "sections": [
            {
                "kicker": "Utilization Basics",
                "h2": "What Credit Utilization Is — and Why 30% Is a Floor, Not a Target",
                "body": (
                    "<p>Credit utilization is calculated by dividing your total revolving "
                    "balance by your total revolving credit limit, then multiplying by 100. "
                    "If you carry $3,000 in balances across cards with a combined $12,000 "
                    "limit, your overall utilization is 25%. This percentage is recalculated "
                    "monthly based on the balance your issuer reports to the credit bureaus "
                    "— typically your statement closing balance, not your current balance.</p>"
                    "<p>The 30% guideline you'll see everywhere is a floor — staying below "
                    "30% avoids significant damage, but it's not an optimization target. "
                    "Borrowers with Exceptional scores (800+) typically carry utilization "
                    "under 7–8%. The improvement in scores from 30% to 10% utilization is "
                    "often 20–40 points. From 10% to under 5% may add another 5–15 points. "
                    "Scoring models don't apply binary penalties at specific thresholds: "
                    "35% is somewhat damaging, 50% is more so, and 75%+ can suppress a "
                    "score by 50–100 points on an otherwise clean profile.</p>"
                    "<p>Both overall utilization and per-card utilization matter. FICO "
                    "considers each card individually. You can have a healthy 20% aggregate "
                    "utilization with one card nearly maxed and still see score suppression "
                    "from that card's per-card signal. A single card at 85% utilization "
                    "is typically a higher-priority paydown target than two cards at 25%, "
                    "even if the dollar amounts are the same — because the per-card signal "
                    "is driving more of the damage.</p>"
                ),
            },
            {
                "kicker": "Quick Wins",
                "h2": "How to Lower Your Utilization Quickly",
                "body": (
                    "<p>Timing is the key lever most borrowers miss. Most issuers report "
                    "your account balance to the credit bureaus on your statement closing "
                    "date — not your payment due date. This means: if you want a lower "
                    "balance on your credit report, pay it down before the statement "
                    "closes, not just before the bill is due. The two dates are typically "
                    "3–4 weeks apart, and what's on your statement at closing is what "
                    "appears on your credit report.</p>"
                    "<p>Practical implication: if your statement closes on the 15th and "
                    "your payment is due on the 11th of the following month, and you pay "
                    "your balance down to $200 on the 13th, your credit report will show "
                    "a $200 balance — regardless of what you charge between the 16th and "
                    "the 11th due date. This gives you substantial control over your "
                    "reported utilization with smart timing alone, even on the same income "
                    "and spending level.</p>"
                    "<p>The second lever: request a credit limit increase. If your issuer "
                    "approves a higher limit, your utilization ratio drops without requiring "
                    "any paydown. Going from a $3,000 limit to a $5,000 limit on a card "
                    "with a $1,000 balance drops per-card utilization from 33% to 20%. "
                    "Confirm whether the issuer uses a soft or hard pull for limit increase "
                    "requests — most allow you to check in your online account settings "
                    "or by calling before requesting, so you don't trigger an unnecessary "
                    "hard inquiry.</p>"
                ),
            },
            {
                "kicker": "Per-Card vs Overall",
                "h2": "Why One Maxed Card Can Hurt Even With Low Overall Utilization",
                "body": (
                    "<p>FICO scoring models evaluate utilization at two levels: aggregate "
                    "utilization across all revolving accounts, and utilization on each "
                    "individual card. Both signals feed into your score. A single maxed-out "
                    "card is a scoring problem even when your other cards have zero balances "
                    "and your overall ratio looks healthy.</p>"
                    "<p>Example: three cards — a $5,000 limit card at $4,500 balance (90% "
                    "utilization), a $3,000 limit card at $0 balance, and a $2,000 limit "
                    "card at $500 balance (25% utilization). Overall utilization: "
                    "($4,500 + $500) ÷ $10,000 = 50%. But the per-card signal on the "
                    "first card — 90% — is generating significant score suppression on its "
                    "own. If you have $1,000 to allocate toward paydown, applying all of "
                    "it to Card A drops it from 90% to 72.5% and generates more score "
                    "benefit than spreading $1,000 evenly, even though the aggregate "
                    "math changes similarly.</p>"
                    "<p>This also explains why closing a zero-balance card is often a "
                    "mistake. Closing a card removes its credit limit from your total "
                    "available credit, instantly raising your overall utilization ratio. "
                    "The common instinct to close cards you don't use to simplify your "
                    "profile — especially old cards with high limits — typically backfires "
                    "by raising utilization and lowering average account age simultaneously. "
                    "Keep zero-balance cards open unless there's a compelling fee-related "
                    "reason to close them.</p>"
                ),
            },
            {
                "kicker": "Score Impact",
                "h2": "Utilization as a Snapshot Metric: What This Means Tactically",
                "body": (
                    "<p>Unlike payment history, which accumulates and leaves permanent marks "
                    "for missed payments, utilization has no memory. It is a snapshot metric "
                    "recalculated fresh each month from the most recently reported balances. "
                    "A month of high utilization followed by a large paydown is treated the "
                    "same as a month of consistently low utilization — the score responds "
                    "to current position, not trajectory.</p>"
                    "<p>This has a direct practical implication: if you need your score "
                    "as high as possible for a near-term credit application — a mortgage "
                    "pre-approval, auto loan, or new card — you can optimize your reported "
                    "utilization in the 30–45 days before applying by paying down balances "
                    "before your statement closing dates. The improvement can be "
                    "substantial: borrowers with high utilization who pay down before "
                    "their closing date sometimes see 30–60 point score improvements "
                    "before the lender pulls their report.</p>"
                    "<p>The common mistake in reverse: charging a large expense to a card "
                    "and planning to pay it off next month without realizing that the "
                    "statement will close with the high balance before the payoff happens. "
                    "If a credit application falls in that window, the score a lender "
                    "pulls will reflect the high balance — not the payoff you made two "
                    "weeks later. Know your statement closing dates for any card you use "
                    "heavily, especially in the months before planned credit applications.</p>"
                ),
            },
        ],
        "faqs": [
            ["Does paying my balance in full each month mean zero utilization?",
             "Not necessarily. Even if you pay in full monthly, your statement balance is "
             "reported to the bureaus on the closing date — before you pay. If your "
             "statement shows a $1,500 balance, that's what gets reported as your "
             "utilization, even though you pay it off completely by the due date. To "
             "report a lower utilization, make a payment before your statement closing "
             "date rather than only before the due date."],
            ["What's the fastest way to improve my credit score?",
             "Paying down revolving credit card balances before your statement closing "
             "date is typically the fastest lever available. Some borrowers see 20–50 "
             "point improvements within a single billing cycle by reducing high "
             "utilization. The improvement appears on your report the month the new "
             "lower balance gets reported, which may be 2–4 weeks after you make the "
             "payment."],
            ["Can I have too low a utilization?",
             "No. Utilization of 0% — carrying no revolving balance — is fine for your "
             "score. Some older advice suggested keeping utilization at 1–5% rather than "
             "zero to demonstrate card usage, but current scoring research shows that "
             "near-zero utilization scores as well as or better than very low utilization. "
             "Using your card and paying in full each month (which reports some "
             "statement balance) is the normal pattern and works well."],
            ["If I close a credit card, does it affect utilization?",
             "Yes. Closing a card removes its limit from your total available credit, "
             "immediately raising your overall utilization ratio on any remaining balances. "
             "Closing a card with a $3,000 limit and zero balance when you have $2,000 in "
             "balances on other cards moves your overall utilization from, say, 20% to "
             "25%+, depending on your other limits. This is typically a score-lowering "
             "move unless there's a strong fee-related reason to close it."],
            ["Does utilization on installment loans work the same way?",
             "No. Installment loans (mortgage, auto, personal) contribute to the "
             "amounts-owed factor in a different way. The remaining loan balance as a "
             "percentage of the original loan amount does affect your score, but it "
             "doesn't drive the quick responses that revolving utilization does. Paying "
             "down a car loan improves your score over time but doesn't produce the "
             "single-billing-cycle jumps you can get from paying down credit card "
             "balances."],
        ],
    },

    # -----------------------------------------------------------------------
    "pages/how-to-lower-credit-card-interest.html": {
        "intro_h2": "Four Practical Ways to Reduce Your Credit Card Interest Costs",
        "intro_body": (
            "<p>The average credit card APR in the United States has stayed above 20% — the "
            "highest sustained level since the Federal Reserve began tracking the series "
            "(source: <a href=\"https://www.federalreserve.gov/releases/g19/current/\" target=\"_blank\" rel=\"noopener nofollow\">Federal Reserve G.19 Consumer Credit release</a>). "
            "At that rate, a balance of a few thousand dollars that's only partially paid "
            "down each month generates well over a thousand dollars in annual interest. "
            "Unlike a mortgage or auto loan where the rate is fixed at origination, credit "
            "card rates are actually movable — through negotiation with your issuer, balance "
            "transfers, debt consolidation loans, and hardship programs.</p>"
            "<p>This guide covers four approaches to reducing what you pay. Each has "
            "different costs, timelines, and eligibility requirements. The right option "
            "depends on your current balance size, your credit score, how quickly you can "
            "realistically pay down the balance, and whether you're optimizing or managing "
            "financial difficulty. Many people can use more than one approach in sequence.</p>"
        ),
        "sections": [
            {
                "kicker": "Negotiate",
                "h2": "Calling Your Issuer: The Underused Rate Reduction Request",
                "body": (
                    "<p>This approach is underused relative to how often it works. Multiple "
                    "surveys have found that roughly 70% of cardholders who call and request "
                    "a rate reduction on an account with good payment history receive at "
                    "least a partial reduction. Card issuers value retention: acquiring a "
                    "new customer costs significantly more than keeping an existing one, "
                    "especially one who carries a balance and pays regularly. A 2-percentage-"
                    "point rate cut on a $5,000 balance costs the issuer about $100/year in "
                    "foregone interest income — less than a month's worth of new customer "
                    "acquisition cost.</p>"
                    "<p>How to do it effectively: call the number on the back of your card "
                    "and ask specifically to speak with the retention department rather than "
                    "general customer service. Have your account information ready: how long "
                    "you've held the card, your payment history, your current APR, and "
                    "what competing transfer offers look like. Be direct: 'I've been a "
                    "customer for four years with no late payments. My current rate is "
                    "26.99% and I'm seeing balance transfer offers in the 15–18% range. "
                    "Is there anything you can do to reduce my rate?'</p>"
                    "<p>If the first agent declines, politely ask to speak with a "
                    "supervisor. The outcome is often different at that level. If rejected "
                    "entirely, note the call and try again in 3–6 months — issuer pricing "
                    "policies change with market conditions, and your account standing "
                    "may also improve. Rate reductions from this approach are typically "
                    "2–4 percentage points for good-standing customers. On a $7,000 "
                    "balance, 3 points is $210/year — permanent as long as you maintain "
                    "good standing.</p>"
                ),
            },
            {
                "kicker": "Balance Transfers",
                "h2": "Balance Transfer Cards: 0% Windows, Fees, and the Payoff Rule",
                "body": (
                    "<p>A balance transfer moves debt from high-APR cards to a new card "
                    "with a 0% introductory APR for a fixed period — typically 12 to 21 "
                    "months. During that window, every dollar you pay reduces principal "
                    "directly with no interest accruing. The math is compelling: $6,000 "
                    "at 24% APR accrues $1,440 in interest over 12 months if the balance "
                    "doesn't decrease. The same balance transferred to a 0% card costs "
                    "nothing in interest during that period — provided you stay within "
                    "the promotional window.</p>"
                    "<p>The cost of the transfer: most balance transfer cards charge a "
                    "fee of 3–5% of the transferred amount, applied upfront. A $6,000 "
                    "transfer at 3% costs $180. Compared to $1,440 in annual interest, "
                    "that's a favorable trade — as long as you have a specific payoff "
                    "plan. Current options to consider include the Citi Simplicity Card "
                    "(21 months at 0%, 5% fee), the Wells Fargo Reflect Card (up to 21 "
                    "months at 0%, 5% fee), and the Discover it Balance Transfer (18 "
                    "months at 0%, 3% fee in the first 14 months). Terms change — "
                    "verify directly with issuers before applying.</p>"
                    "<p>Critical rules: don't use the transfer card for new purchases "
                    "during the promotional period — those typically accrue interest at "
                    "the standard APR from the purchase date. Always make at least the "
                    "minimum payment every month — a single missed payment on most "
                    "transfer cards immediately terminates the 0% promotional rate and "
                    "reverts to the standard APR on the remaining balance. Calculate your "
                    "required monthly payment as (balance + fee) ÷ number of promotional "
                    "months, and set up autopay to ensure you hit it every cycle.</p>"
                ),
            },
            {
                "kicker": "Personal Loan Consolidation",
                "h2": "Replacing High-Rate Card Debt with a Fixed Personal Loan",
                "body": (
                    "<p>A personal loan consolidation replaces multiple high-rate credit "
                    "card balances with a single fixed-rate, fixed-term installment loan. "
                    "The advantage over a balance transfer: you get a defined payoff date "
                    "and a rate that doesn't expire after a promotional window. Federal "
                    "Reserve data shows average personal loan APRs of approximately 11–12% "
                    "for well-qualified borrowers — compared to the average card APR of "
                    "24.59%, the interest savings are substantial.</p>"
                    "<p>The math: $10,000 consolidated at 11% APR for 36 months requires "
                    "a $327/month payment and totals $1,772 in interest over the life of "
                    "the loan. The same $10,000 on credit cards at 24.59% minimum payments "
                    "takes years longer and costs several thousand dollars more. Personal "
                    "loan rates are heavily influenced by credit score — a borrower at 660 "
                    "might receive 16% where a 720 borrower gets 10%. If your score is "
                    "below 640, spending 6–12 months improving it before consolidating "
                    "can unlock significantly better rates and produce substantially "
                    "higher savings.</p>"
                    "<p>Online lenders to compare: LightStream (competitive rates for "
                    "excellent-credit borrowers), Marcus by Goldman Sachs (no fees, "
                    "transparent pricing), SoFi, and Discover Personal Loans are "
                    "frequently cited for straightforward consolidation products. Most "
                    "fund within 1–5 business days. The behavioral warning applies here "
                    "too: consolidating doesn't reduce debt — it restructures it. "
                    "Cardholders who consolidate and then rebuild card balances often "
                    "end up with more total debt within 18 months. Remove the consolidated "
                    "cards from your wallet and online payment profiles to create friction "
                    "against rebuilding them.</p>"
                ),
            },
            {
                "kicker": "Hardship Programs",
                "h2": "Hardship Programs and Rate Reduction Plans for Financial Difficulty",
                "body": (
                    "<p>If you're struggling to make payments rather than optimizing an "
                    "existing situation, hardship programs are a legitimate and underused "
                    "tool. Most major card issuers maintain formal hardship programs for "
                    "customers experiencing financial difficulty — these typically reduce "
                    "the APR to 9.9% or lower and may waive late fees for 12–18 months. "
                    "The tradeoff: your card is usually frozen during enrollment, meaning "
                    "no new purchases, but you continue making reduced-rate payments on "
                    "the existing balance.</p>"
                    "<p>How to access them: call the number on the back of your card and "
                    "ask specifically for the hardship or financial assistance department, "
                    "not general customer service. Be straightforward about what's "
                    "happening — job loss, medical bills, reduced income — without "
                    "oversharing unnecessary detail. What issuers are evaluating is whether "
                    "the difficulty is temporary and whether the customer intends to repay. "
                    "Most major issuers — Chase, Citibank, Bank of America, American "
                    "Express — have these programs; accessing them requires asking "
                    "explicitly.</p>"
                    "<p>Nonprofit credit counseling through NFCC (National Foundation for "
                    "Credit Counseling) member agencies is a more structured option. A "
                    "certified credit counselor can negotiate rate reductions with multiple "
                    "issuers simultaneously as part of a Debt Management Plan (DMP). "
                    "Monthly fees for DMPs are typically $25–$75, and programs usually "
                    "run 3–5 years. A hardship program or DMP may be noted on your "
                    "credit report, but the long-term impact is far less damaging than "
                    "late payments, collections, or charge-offs — the likely alternative "
                    "if payments become unmanageable.</p>"
                ),
            },
            {
                "kicker": "Long-Term Habits",
                "h2": "Habits That Keep Interest Costs Low Permanently",
                "body": (
                    "<p>The most durable way to eliminate credit card interest is paying "
                    "the full statement balance every month. If you carry no revolving "
                    "balance, you pay no interest regardless of the APR — the rate becomes "
                    "irrelevant. For the significant share of Americans who do carry "
                    "balances routinely, several habits meaningfully reduce ongoing costs.</p>"
                    "<p>Know your statement closing date and due date for every card. "
                    "These are the two critical calendar points: charges made after closing "
                    "go into the next billing cycle; paying down before closing reduces "
                    "your statement balance and your reported utilization simultaneously. "
                    "Set up autopay for the full statement balance — or at minimum for the "
                    "minimum payment as a backstop. A single missed payment triggers a "
                    "late fee, penalty APR on many cards, and a credit score hit that can "
                    "persist for two years.</p>"
                    "<p>Call for rate reviews annually. Card issuers adjust rates "
                    "periodically — both upward through variable-rate increases and "
                    "downward for customers with strong payment histories. A five-minute "
                    "annual call asking about your current APR and whether a rate "
                    "reduction is available is consistently one of the highest-return "
                    "actions in personal finance. Combined with paying in full when "
                    "possible and using balance transfers strategically when carrying a "
                    "balance, this annual check compounds the interest savings over time.</p>"
                ),
            },
        ],
        "faqs": [
            ["Can I actually negotiate a lower interest rate with my credit card issuer?",
             "Yes — and it works more often than most people expect. About 70% of "
             "cardholders with good payment histories who request a rate reduction receive "
             "at least a partial one. The key is calling the retention department, not "
             "general customer service, and framing the request around your loyalty and "
             "specific competing transfer offers you've received. The call takes about "
             "five minutes and costs nothing to try."],
            ["Is a 0% balance transfer worth it?",
             "Usually yes, if you can realistically pay off the transferred balance within "
             "the promotional window and the transfer fee is less than the interest you'd "
             "pay otherwise. A $5,000 balance at 24% would cost $1,200 in interest over "
             "12 months — a $150–$250 transfer fee is a significant savings even if you "
             "don't fully pay it off during the promo period, as long as you reduce the "
             "balance substantially."],
            ["What credit score do I need for a balance transfer card?",
             "Most 0% balance transfer cards require a good to excellent credit score — "
             "generally 670+. The best transfer offers (longest promotional windows, "
             "lowest fees) typically require 700+ or 720+. If your score is below 670, "
             "calling your current issuer to negotiate a rate reduction is a better "
             "first move, since new card applications at that score level are likely "
             "to result in denial or very short promotional windows."],
            ["How does a personal loan for consolidation affect my credit score?",
             "Applying triggers a hard inquiry (temporary 5–10 point impact). Opening "
             "the loan adds to your credit mix and creates a new installment account. "
             "Paying off the credit card balances dramatically reduces your utilization "
             "ratio — which typically produces a net score improvement within 1–3 months "
             "that more than offsets the inquiry impact. The long-term effect of "
             "consistent installment loan payments is positive."],
            ["What happens if I miss a payment during a 0% balance transfer period?",
             "Missing a payment — or being even one day late — typically terminates the "
             "0% promotional rate immediately on most transfer cards. The remaining "
             "balance begins accruing interest at the card's standard purchase APR, often "
             "24–29.99%. Always set up autopay for at least the minimum payment when "
             "doing a balance transfer. The small risk of forgetting a payment can cost "
             "you the entire benefit of the transfer."],
            ["Are hardship programs for credit cards legitimate?",
             "Yes. Most major issuers — including Chase, Citibank, Bank of America, and "
             "American Express — have formal hardship programs that reduce APRs to 9.9% "
             "or lower for qualifying borrowers experiencing financial difficulty. They're "
             "accessed by calling the issuer's hardship or retention department directly "
             "and explaining your situation. Nonprofit NFCC credit counselors can also "
             "negotiate rate reductions with multiple issuers simultaneously through a "
             "Debt Management Plan."],
        ],
    },

    # ------------------------------------------------------------------
    "pages/personal-loans-guide.html": {
        "intro_h2": "What a personal loan really costs once fees are in the picture",
        "intro_body": (
            "<p>Most personal loan shoppers compare a single number — the advertised APR — and stop there. That's the most expensive mistake in the category. The APR moves with credit profile, debt-to-income ratio, and lender risk appetite, and two lenders offering the same APR can quote very different total costs once an origination fee, prepayment rule, or term length difference enters the math. The <a href=\"https://www.consumerfinance.gov/consumer-tools/\" target=\"_blank\" rel=\"noopener noreferrer\">CFPB&rsquo;s consumer explainer</a> covers the mechanics in plain English.</p>"
            "<p>This guide walks through how to read a personal loan offer the way an underwriter reads it. The goal is to put the borrower in a position where the monthly payment shown in the offer is one of five numbers being compared, not the only one.</p>"
        ),
        "sections": [
            {
                "kicker": "Pricing",
                "h2": "APR vs. interest rate vs. fee-adjusted proceeds",
                "body": (
                    "<p>The advertised <em>interest rate</em> is what the lender charges on the outstanding principal. The <em>APR</em> bundles that interest with any required fees (most commonly the origination fee) and expresses the total cost as an annualized percentage. By federal Truth-in-Lending rules, the APR is the comparison number — but only if the same fees are included on both sides.</p>"
                    "<p><strong>Fee-adjusted proceeds</strong> is the missing third number. If you ask for $15,000 and the lender deducts a 6% origination fee at funding, you receive $14,100 but you make payments as if you borrowed $15,000. The effective cost to you is higher than the headline APR suggests. To compare two offers fairly, divide each lender&rsquo;s total interest paid (over the same term and on the same requested amount) by the actual cash you receive at funding.</p>"
                )
            },
            {
                "kicker": "Term length",
                "h2": "Why a longer term often costs more, not less",
                "body": (
                    "<p>Personal loans typically run 24 to 84 months. A longer term shrinks the monthly payment but extends the time interest compounds, and lenders often charge a slightly higher rate on longer terms because their capital is locked up. The general rule: pick the shortest term whose monthly payment still leaves a comfortable cushion in your monthly cash flow.</p>"
                    "<p>Comfortable means it survives a 10% income shock or a one-month emergency expense. If the payment only works in a perfect month, the term is too short.</p>"
                )
            },
            {
                "kicker": "Prepayment",
                "h2": "Prepayment penalties and how to spot them",
                "body": (
                    "<p>Federal law does not ban personal-loan prepayment penalties. Some lenders include them; many do not. The penalty (when present) is usually a flat fee or a percentage of the remaining balance and applies if you pay the loan off in the first 12&ndash;36 months. Before signing, ask explicitly: &ldquo;Is there any cost to paying this loan off early?&rdquo; and confirm the answer is reflected in the contract. The CFPB&rsquo;s <a href=\"https://www.consumerfinance.gov/ask-cfpb/what-is-a-prepayment-penalty-en-1957/\" target=\"_blank\" rel=\"noopener noreferrer\">consumer Q&amp;A on prepayment penalties</a> is a useful reference.</p>"
                )
            },
            {
                "kicker": "Use case",
                "h2": "Debt consolidation only works if behavior changes",
                "body": (
                    "<p>The most common use case for a personal loan is consolidating revolving credit-card debt into a fixed-rate installment loan. The math is usually attractive because credit-card APRs sit well above prime personal-loan APRs. But the math only works if the credit cards are not used to re-accumulate balances during the loan&rsquo;s payoff period. Treat the consolidation as one event in a plan that also includes a written rule for the credit cards (zero new balances, or strictly paid-in-full each month).</p>"
                    "<p>See <a href=\"/pages/debt-payoff-guide\">our debt payoff guide</a> for the fuller framework.</p>"
                )
            },
        ],
        "faqs": [
            ["What APR is realistic for a good personal-loan offer?",
             "It depends on credit profile and lender; the Federal Reserve&rsquo;s G.19 release tracks the average across reporting institutions. The right benchmark is not a number you saw online but three or four firm offers obtained on the same day for the same amount and term."],
            ["Is a credit-union personal loan always cheaper?",
             "Often, but not always. Credit unions have lower marketing costs and can pass that on, but the federal APR cap (18% for federal credit unions) is a ceiling, not a floor. Compare offers, do not assume."],
            ["What is the safest amount to borrow?",
             "The amount whose required monthly payment fits comfortably within your post-tax income after housing, food, utilities, and a small emergency buffer. If the payment requires perfection in your budget, the amount is too high."],
        ],
    },

    # ------------------------------------------------------------------
    "pages/credit-cards-guide.html": {
        "intro_h2": "Credit cards: where the real cost lives, and how to keep it low",
        "intro_body": (
            "<p>Credit cards are the most flexible borrowing product in U.S. consumer finance and the most expensive when used carelessly. The <a href=\"https://www.federalreserve.gov/releases/g19/current/\" target=\"_blank\" rel=\"noopener noreferrer\">Federal Reserve&rsquo;s G.19 release</a> tracks the average rate on accounts assessed interest; that number is the single most useful benchmark for whether you are paying more than the typical revolving borrower.</p>"
            "<p>This guide is not a list of &ldquo;best cards&rdquo;. It is a walkthrough of the mechanics that decide how much a credit card costs the person who carries one: the grace period, the way interest accrues, the role of utilization, and the fees that hide in fine print. If you are already carrying a balance and want to see the cost of paying only the minimum, jump to the <a href=\"/pages/credit-card-minimum-payment-true-cost-calculator\">minimum payment true cost calculator</a>.</p>"
        ),
        "sections": [
            {
                "kicker": "Grace period",
                "h2": "Why paying the statement balance in full changes everything",
                "body": (
                    "<p>If you pay the <em>statement balance</em> in full by the due date, most U.S. credit cards charge no interest on new purchases. That is the grace period — a regulator-required disclosure under the CARD Act. The instant you carry a balance into the next cycle, the grace period typically disappears and new purchases begin accruing interest from the date of purchase.</p>"
                    "<p>The practical implication: a credit card is either a free 30&ndash;55-day loan (paid in full each month) or one of the most expensive borrowing products on the market (revolving a balance). There is almost no in-between.</p>"
                )
            },
            {
                "kicker": "APR mechanics",
                "h2": "How daily interest accrual quietly increases your balance",
                "body": (
                    "<p>Most U.S. issuers use the &ldquo;average daily balance&rdquo; method. The annual rate is divided by 365 to get a daily rate; that daily rate is applied to each day&rsquo;s balance; the resulting interest is added to the balance at cycle close. The compounding is small per day and material over a year.</p>"
                    "<p>A worked example: a $4,000 balance at 24% APR with no new charges costs roughly $80 in the first month of pure revolving and rises slowly thereafter as the balance grows from compounded interest. Multiply across 12 months and the borrower pays close to a quarter of the balance in interest annually if no payment exceeds the interest charge.</p>"
                )
            },
            {
                "kicker": "Utilization",
                "h2": "Credit utilization and what credit-scoring models really do with it",
                "body": (
                    "<p>Utilization is the ratio of reported balances to credit limits. It is the second-largest factor in most credit scoring models (after payment history). Two practical points worth knowing: (1) issuers usually report the <em>statement</em> balance to the bureaus, not the current balance, so paying down before the statement closes is the most effective lever; (2) per-card utilization matters in addition to aggregate, so one maxed-out card can hurt the score even if the total ratio is moderate.</p>"
                    "<p>The CFPB&rsquo;s page on <a href=\"https://www.myfico.com/credit-education/credit-scores/amount-of-debt\" target=\"_blank\" rel=\"noopener noreferrer\">credit utilization rate</a> is a useful plain-language reference.</p>"
                )
            },
            {
                "kicker": "Fees",
                "h2": "Annual fee, balance transfer fee, late fee — the three to model first",
                "body": (
                    "<p>Annual fee: only worth paying if the year&rsquo;s expected rewards or benefits exceed the fee in real cash equivalent, not in inflated &ldquo;value&rdquo; estimates.</p>"
                    "<p>Balance transfer fee: typically 3&ndash;5% of the amount moved, paid up front. A 0% promo APR only saves money if the interest avoided exceeds the transfer fee over the promo period. Calculate the break-even before transferring.</p>"
                    "<p>Late fee: capped by federal rule (the cap is updated by the CFPB periodically — see their <a href=\"https://www.consumerfinance.gov/consumer-tools/credit-cards/\" target=\"_blank\" rel=\"noopener noreferrer\">credit card resources</a>). The bigger cost of paying late is usually not the fee itself but the loss of the grace period and the potential APR repricing.</p>"
                )
            },
        ],
        "faqs": [
            ["What credit card APR should I aim for?",
             "Rather than chasing a specific number, aim for a card whose APR you will never pay because you always pay the statement balance in full. If you must carry a balance, prioritize the lowest available APR over rewards."],
            ["Are credit-card rewards a net benefit?",
             "Only for borrowers who pay in full every month. For revolving borrowers, the interest paid almost always exceeds the value of rewards earned."],
            ["When is a balance transfer worth doing?",
             "When the transfer fee plus any new-purchase interest avoided is less than the interest that would have accrued on the original card during the same period. Always calculate the specific break-even before transferring."],
        ],
    },

    # ------------------------------------------------------------------
    "pages/mortgage-guide.html": {
        "intro_h2": "A mortgage costs more than the monthly payment shown on the marketing page",
        "intro_body": (
            "<p>A mortgage&rsquo;s sticker rate is what most shoppers compare. The actual all-in monthly cost is the sticker rate plus property taxes, homeowners insurance, mortgage insurance when applicable, and HOA dues when applicable — together called <strong>PITI(A)</strong>. The CFPB&rsquo;s <a href=\"https://www.consumerfinance.gov/owning-a-home/loan-estimate/\" target=\"_blank\" rel=\"noopener noreferrer\">Loan Estimate</a> is the federally standardized document that puts all of this on one page; every lender must deliver it within three business days of application.</p>"
            "<p>This guide explains how to read a Loan Estimate, how to compare two of them, and where money quietly leaks during the process. If you already have a mortgage and want to test whether refinancing makes sense, jump to the <a href=\"/pages/mortgage-refinance-break-even-calculator\">refinance break-even calculator</a> for the math.</p>"
        ),
        "sections": [
            {
                "kicker": "Rate vs APR",
                "h2": "APR captures fees the interest rate hides",
                "body": (
                    "<p>The interest rate determines the principal-and-interest portion of the monthly payment. The APR includes the interest rate plus most loan-related fees expressed as an annualized cost. Two lenders quoting the same interest rate can have very different APRs if one charges higher origination, underwriting, or rate-lock fees. APR is the right shopping number when comparing the same loan type and term.</p>"
                    "<p>The Loan Estimate&rsquo;s page 3 shows the &ldquo;In 5 Years&rdquo; total — total paid in principal, interest, mortgage insurance, and fees over the first five years. That is often a better real-world comparison than APR alone because it incorporates the actual amortization schedule.</p>"
                )
            },
            {
                "kicker": "Discount points",
                "h2": "When buying down the rate actually pays off",
                "body": (
                    "<p>One discount point typically costs 1% of the loan amount and reduces the rate by a fraction of a percent (often around 0.25%, but it varies). The break-even is monthly-savings ÷ point-cost. If the break-even is 6 years and you plan to keep the loan for 10, points are likely worth it; if you plan to sell or refinance in 3, they are not.</p>"
                )
            },
            {
                "kicker": "PMI and MIP",
                "h2": "Private mortgage insurance is removable; FHA MIP usually is not",
                "body": (
                    "<p>On conventional loans, private mortgage insurance (PMI) is required when the down payment is under 20% and is removable once the loan balance reaches 80% loan-to-value (LTV) — automatically at 78% by federal Homeowners Protection Act rules. On FHA loans, the mortgage insurance premium (MIP) is structured differently and, for most current FHA loans, is not removable for the life of the loan unless you refinance into a conventional product. That difference can outweigh the FHA loan&rsquo;s easier underwriting over the long run.</p>"
                )
            },
            {
                "kicker": "Closing costs",
                "h2": "Where closing-day cash actually goes",
                "body": (
                    "<p>Closing costs typically total 2&ndash;5% of the loan amount and are split into three buckets on the Loan Estimate: (A) services you can shop for (title, settlement, pest), (B) services you can&rsquo;t shop for (appraisal, credit report, lender-required), and (C) taxes and prepaid items (transfer taxes, prepaid interest, escrow deposits). Bucket A is where price comparison pays off. Bucket C is usually unavoidable but should still be verified for accuracy.</p>"
                    "<p>For the line-by-line math comparing two specific offers, open the <a href=\"/pages/mortgage-refinance-break-even-calculator\">refinance break-even calculator</a> and enter the figures from each Loan Estimate side by side.</p>"
                )
            },
        ],
        "faqs": [
            ["How much should I shop around for a mortgage?",
             "The CFPB&rsquo;s research suggests that shoppers who collect quotes from at least three lenders pay measurably less. Multiple credit pulls within a 14&ndash;45 day window are typically treated by scoring models as a single inquiry for shopping purposes."],
            ["What is the difference between pre-qualified and pre-approved?",
             "Pre-qualification is informal; pre-approval involves a credit check and documentation. Pre-approval letters carry weight in offers but are not loan commitments."],
            ["Is 20% down required to buy?",
             "No. Conventional loans allow as little as 3% down with PMI; FHA loans 3.5%; VA and USDA can be 0% for qualified borrowers. The cost calculation differs across programs and should be compared on the Loan Estimate, not on advertised rates."],
        ],
    },

    # ------------------------------------------------------------------
    "pages/banking-fees-guide.html": {
        "intro_h2": "The bank fees Americans pay most, and the ones easiest to avoid",
        "intro_body": (
            "<p>U.S. consumer bank fees fall into a small number of categories — overdraft, monthly maintenance, ATM, wire, paper statement, and minimum-balance penalties — and most are avoidable with a deliberate account choice. The <a href=\"https://www.consumerfinance.gov/about-us/blog/\" target=\"_blank\" rel=\"noopener noreferrer\">CFPB&rsquo;s overdraft resources</a> and the <a href=\"https://www.fdic.gov/national-rates-and-rate-caps\" target=\"_blank\" rel=\"noopener noreferrer\">FDIC National Rates</a> data are the right starting points for figuring out which fees you are actually paying.</p>"
            "<p>This guide describes how each fee works, when it is reasonable, and the account-level changes that remove it.</p>"
        ),
        "sections": [
            {
                "kicker": "Overdraft",
                "h2": "How overdraft and NSF fees work",
                "body": (
                    "<p>An overdraft fee is charged when the bank pays a transaction that exceeds the account balance. A non-sufficient-funds (NSF) fee is charged when the bank declines the transaction. After significant CFPB attention, many large banks have reduced or eliminated NSF fees and capped daily overdraft fee counts; smaller institutions vary. The single most effective lever is opting out of overdraft <em>coverage</em> for one-time debit and ATM transactions — Regulation E gives every account holder the right to do this.</p>"
                )
            },
            {
                "kicker": "Monthly fee",
                "h2": "Monthly maintenance fees and how to waive them",
                "body": (
                    "<p>Many checking accounts charge a monthly maintenance fee that can be waived by meeting at least one condition: a minimum balance, a recurring direct deposit, a number of debit transactions per month, or enrollment in a relationship pricing tier. Read the waiver conditions on the disclosure (the &ldquo;Schedule of Fees&rdquo;) before opening the account.</p>"
                    "<p>The simplest way to avoid the fee permanently is to open a checking account that does not charge one. Several large national banks, regional online banks, and most credit unions offer no-monthly-fee checking with no balance requirement.</p>"
                )
            },
            {
                "kicker": "ATM",
                "h2": "Out-of-network ATM fees: two charges, one transaction",
                "body": (
                    "<p>Using an out-of-network ATM typically triggers two fees: one from the ATM operator (the &ldquo;surcharge&rdquo;) and one from your own bank (the &ldquo;foreign ATM fee&rdquo;). Combined, they often total $5&ndash;$8 per withdrawal. Online-only banks frequently reimburse some or all of these monthly; some networks (Allpoint, MoneyPass, CO-OP) provide surcharge-free access at tens of thousands of locations.</p>"
                )
            },
            {
                "kicker": "Other",
                "h2": "Wire, paper-statement, and minimum-balance fees",
                "body": (
                    "<p><strong>Wires.</strong> Domestic outgoing wires typically cost $20&ndash;$35; international outgoing wires more. ACH transfers are free at most institutions and clear in 1&ndash;3 business days for most uses.</p>"
                    "<p><strong>Paper statement.</strong> Increasingly charged as a small monthly fee unless you opt into e-statements. A one-click change in online banking eliminates it.</p>"
                    "<p><strong>Minimum balance.</strong> If your account requires a minimum to avoid a fee, either keep that minimum reliably or switch to an account without one. Paying a $12 fee to keep money in checking is a bad trade if a competing free checking account is available.</p>"
                )
            },
        ],
        "faqs": [
            ["Are credit unions always cheaper than banks?",
             "Often, but not always. Federal credit unions have an 18% APR ceiling and tend to charge fewer fees on basic accounts. The right comparison is your specific account&rsquo;s disclosure schedule against a competing institution&rsquo;s, not bank-vs-credit-union as a category."],
            ["What is the simplest way to avoid overdraft fees?",
             "Opt out of overdraft coverage for debit and ATM transactions (your right under Regulation E), then maintain a small buffer in checking. If a debit exceeds the balance, the bank will decline it rather than approving and charging an overdraft fee."],
            ["Why are some banks fee-free?",
             "Online-only and challenger banks typically have lower overhead than branch-based banks and earn revenue from interchange (the small fee merchants pay on each debit swipe) rather than account fees."],
        ],
    },

    # ------------------------------------------------------------------
    "pages/refinancing-guide.html": {
        "intro_h2": "Refinancing: the math that actually decides whether to do it",
        "intro_body": (
            "<p>Refinancing replaces an existing loan with a new one that has different terms. Done well, it lowers total cost; done poorly, it resets a clock and adds fees for negligible improvement. The CFPB&rsquo;s <a href=\"https://www.consumerfinance.gov/owning-a-home/\" target=\"_blank\" rel=\"noopener noreferrer\">refinance overview</a> is the clearest starting point for mortgages; the same principles apply, with smaller fee scales, to auto loans, personal loans, and student loans.</p>"
            "<p>This guide focuses on the decision math: when refinancing saves money, when it does not, and how to compare a new loan against the one you already have.</p>"
        ),
        "sections": [
            {
                "kicker": "Break-even",
                "h2": "How long until refinancing pays for itself",
                "body": (
                    "<p>Refinancing has up-front costs: closing costs on a mortgage refinance (often 2&ndash;5% of the new loan), title and escrow fees, and (where applicable) prepayment penalties on the old loan. The right way to evaluate the trade is: <em>break-even months</em> = total refinance costs ÷ monthly savings. If you expect to keep the loan past that break-even, the refinance is worth doing; if you might sell, move, or refinance again before then, it usually is not.</p>"
                    "<p>Always run the break-even on the actual numbers from the Loan Estimate (mortgages) or the lender&rsquo;s itemized fee disclosure (other products), not on advertised &ldquo;average&rdquo; savings.</p>"
                )
            },
            {
                "kicker": "Term reset",
                "h2": "Watch the reset of the amortization clock",
                "body": (
                    "<p>Refinancing a 30-year mortgage into a new 30-year mortgage after eight years of payments resets the schedule. Even at a lower rate, you may pay more total interest because you stretched the timeline by eight years. If reducing total cost is the goal, ask the lender to quote a shorter term (e.g., refinance the remaining 22 years into a new 20-year loan).</p>"
                )
            },
            {
                "kicker": "Student loans",
                "h2": "Federal student-loan refinancing trades benefits for rate",
                "body": (
                    "<p>Refinancing a federal student loan into a private loan converts the loan permanently — you lose access to income-driven repayment, public service loan forgiveness, and federal forbearance programs. For borrowers in stable income with no expected use of those federal benefits, the lower rate may still be the right trade. For everyone else, it generally is not. The CFPB&rsquo;s <a href=\"https://www.consumerfinance.gov/consumer-tools/student-loans/\" target=\"_blank\" rel=\"noopener noreferrer\">student loan tools</a> walk through the trade-offs.</p>"
                )
            },
            {
                "kicker": "Cash-out",
                "h2": "Cash-out refinances increase total cost — always",
                "body": (
                    "<p>A cash-out refinance is a refinance plus a new loan against the equity you already have. The new loan amount is higher, so total interest paid will be higher even if the rate is the same. Treat the cash-out portion as a separate borrowing decision evaluated against alternatives: HELOC, home equity loan, personal loan, or simply not borrowing.</p>"
                )
            },
        ],
        "faqs": [
            ["How much should rates drop before refinancing a mortgage?",
             "There is no universal threshold. The right test is whether the break-even months are shorter than the time you plan to keep the loan. A 0.5-percentage-point drop can be worth it for borrowers who will hold the loan many years; a 1.5-point drop can be wrong for someone planning to move in two years."],
            ["Does refinancing hurt my credit?",
             "There is a temporary small dip from the hard inquiry and the closing of the old account. Both effects fade within months and are typically far smaller than the long-term cost of holding a more expensive loan than necessary."],
            ["What if I cannot afford the refinance closing costs?",
             "Most mortgage refinances allow rolling costs into the loan amount. That changes the math — you are now financing the costs at the new rate, so they should be included on the cost side of the break-even calculation, not treated as zero."],
        ],
    },

    # ------------------------------------------------------------------
    "pages/student-loans-guide.html": {
        "intro_h2": "Federal vs. private student loans: the trade you cannot undo",
        "intro_body": (
            "<p>The most consequential decision in student-loan borrowing is whether the loan is federal or private. Federal loans (Direct Subsidized, Direct Unsubsidized, PLUS) come with standardized rates set by Congress, income-driven repayment plans, deferment and forbearance options, and (for some borrowers) Public Service Loan Forgiveness eligibility. Private loans, originated by banks and credit unions, are priced individually based on credit, can have lower rates for high-credit borrowers, but lack all of the federal protections. The authoritative source for federal loans is <a href=\"https://studentaid.gov/\" target=\"_blank\" rel=\"noopener noreferrer\">StudentAid.gov</a>, run by the U.S. Department of Education.</p>"
            "<p>This guide explains the major decision points before borrowing and the repayment options after.</p>"
        ),
        "sections": [
            {
                "kicker": "Federal first",
                "h2": "Why federal loans are almost always the right starting point",
                "body": (
                    "<p>Federal Direct Subsidized loans do not accrue interest while the borrower is enrolled at least half-time. Federal Direct Unsubsidized loans accrue interest but do not require payments during enrollment. Both qualify for income-driven repayment, which caps payments as a percentage of discretionary income after graduation. Those are large protections that no private lender matches. Exhaust federal eligibility (file the FAFSA) before considering private debt.</p>"
                )
            },
            {
                "kicker": "Capitalized interest",
                "h2": "How unpaid interest becomes principal",
                "body": (
                    "<p>Interest that accrues during deferment, forbearance, or grace periods is often <em>capitalized</em> — added to the principal — at the end of those periods. Future interest then accrues on the larger balance. The practical effect on a loan held many years can be material. Paying even small amounts of interest during enrollment, where possible, prevents this.</p>"
                )
            },
            {
                "kicker": "Repayment plans",
                "h2": "Income-driven repayment in plain English",
                "body": (
                    "<p>Income-driven repayment (IDR) plans cap monthly payments at a percentage of discretionary income and forgive remaining balances after 20&ndash;25 years (10 years for borrowers in qualifying public-service employment via PSLF). The newer SAVE plan replaced REPAYE; older plans (PAYE, IBR, ICR) remain available for some borrowers. The Department of Education&rsquo;s <a href=\"https://studentaid.gov/manage-loans/repayment/plans/income-driven\" target=\"_blank\" rel=\"noopener noreferrer\">IDR overview</a> shows current plan rules and a loan simulator.</p>"
                )
            },
            {
                "kicker": "Private",
                "h2": "When private loans make sense — and when they do not",
                "body": (
                    "<p>Private loans can offer lower rates than federal Direct PLUS loans for high-credit parent borrowers, and can fill funding gaps after federal limits. Before signing, confirm: (1) the rate is fixed (variable rates have shown sharp moves historically), (2) the repayment options if you lose income, (3) whether a cosigner can be released and on what schedule, and (4) the full cost over the expected repayment period, not just the monthly payment.</p>"
                    "<p>Refinancing federal loans into private loans is rarely the right move for most borrowers — see <a href=\"/pages/refinancing-guide\">our refinancing guide</a> for that decision.</p>"
                )
            },
        ],
        "faqs": [
            ["Should I use a private loan to avoid federal loan limits?",
             "Only after running the math on Parent PLUS and other federal options. Federal protections (IDR, forbearance, PSLF) have significant real value that should be priced into the comparison."],
            ["Does loan forgiveness create a tax bill?",
             "Historically yes for many IDR forgiveness paths, though recent federal legislation has temporarily excluded student-loan forgiveness from federal tax through specific dates. State tax treatment varies. Confirm current rules at StudentAid.gov and IRS.gov before relying on forgiveness as a plan."],
            ["What is the safest way to pay down student debt fast?",
             "Stay on the standard or income-driven plan, make extra payments to the principal of the highest-rate loan first, and only refinance if you no longer need federal benefits and a meaningfully lower rate is available."],
        ],
    },

    # ------------------------------------------------------------------
    # Calculators with unique short content.
    # ------------------------------------------------------------------
    "pages/loan-payment-calculator.html": {
        "intro_h2": "Loan payment calculator: estimate a monthly payment in seconds",
        "intro_body": (
            "<p>This calculator estimates a fixed-rate installment-loan monthly payment using the standard amortization formula. It is useful for personal loans, auto loans, and any other fully-amortizing fixed-rate product where the term is expressed in months.</p>"
        ),
        "sections": [
            {
                "kicker": "Formula",
                "h2": "The math behind the calculator",
                "body": (
                    "<p>The monthly payment <em>P</em> on a loan of amount <em>A</em>, monthly rate <em>r</em> (annual APR ÷ 12), and term <em>n</em> months is:</p>"
                    "<p><code>P = A · r ÷ (1 − (1 + r)<sup>−n</sup>)</code></p>"
                    "<p>This is the same closed-form amortization formula used by every standard lender quoting tool. It assumes a fixed rate over the full term and no fees added to the monthly payment. Fees that come out of the loan&rsquo;s proceeds at funding (origination fees) reduce the cash you receive but do not change the calculated monthly payment for the requested amount.</p>"
                )
            },
            {
                "kicker": "Example",
                "h2": "Worked example",
                "body": (
                    "<p>A $20,000 personal loan at 9.0% APR over 48 months produces a monthly payment near $498. Total interest over the life of the loan is roughly $3,894. Move the rate to 12% and the payment rises to about $527 with total interest near $5,275 — a single rate change adds more than a thousand dollars in total cost on the same loan amount.</p>"
                )
            },
            {
                "kicker": "Limits",
                "h2": "What this calculator cannot tell you",
                "body": (
                    "<p>The calculator does not estimate approval odds, does not account for variable rates, does not include lender fees in the APR, and does not adjust for credit profile. Use it for &ldquo;is this payment realistic?&rdquo; planning, then verify the final terms on a lender&rsquo;s firm offer or Loan Estimate.</p>"
                )
            },
        ],
        "faqs": [
            ["Does the calculator account for origination fees?",
             "Not directly. To capture fees, calculate the payment for the full loan amount the lender quotes, then divide total interest by the cash you actually receive at funding (loan amount minus origination fee) to compare offers fairly."],
            ["Can I use this for an auto loan?",
             "Yes. Use the loan amount net of down payment and trade-in. For an apples-to-apples lender comparison, include any dealer-financed fees in the loan amount or in your manual cost calculation."],
            ["Why does my actual quote differ?",
             "Lenders may round, apply different day-count conventions, or include fees in different places. The calculator&rsquo;s result is a planning estimate that should match within a few dollars of a fee-free quote."],
        ],
    },

    # ------------------------------------------------------------------
    "pages/credit-card-interest-calculator.html": {
        "intro_h2": "Credit card interest calculator: see how long a payoff really takes",
        "intro_body": (
            "<p>This calculator simulates month-by-month payoff of a credit-card balance at a given APR with a chosen monthly payment, optionally adding new monthly charges. It is built to expose how slowly minimum payments retire a balance and how quickly a moderate payment increase changes the timeline.</p>"
        ),
        "sections": [
            {
                "kicker": "How it works",
                "h2": "The simulation, in plain English",
                "body": (
                    "<p>Each simulated month: monthly interest = balance × (APR ÷ 12). New balance = balance + interest + new charges − payment. The simulation continues until the balance reaches zero or the payment fails to cover monthly interest (in which case the balance grows forever).</p>"
                )
            },
            {
                "kicker": "Example",
                "h2": "Worked example",
                "body": (
                    "<p>A $6,000 balance at 24% APR with a $150 monthly payment and zero new charges retires in roughly 73 months and costs about $4,950 in interest. Increase the payment to $250 and the timeline drops to roughly 32 months with interest near $1,950 — saving about three years and three thousand dollars on the same balance.</p>"
                )
            },
            {
                "kicker": "Limits",
                "h2": "What the calculator cannot model",
                "body": (
                    "<p>Real credit-card statements use slightly different daily-balance methods, may reprice on missed payments, and impose minimum payment formulas (often the larger of 1% of balance + interest or a flat dollar minimum). The simulator&rsquo;s assumption of a constant payment is a simplification. For a debt that you carry close to its limit, real APR repricing risk is the biggest unmodeled factor.</p>"
                )
            },
        ],
        "faqs": [
            ["Should I always pay more than the minimum?",
             "Yes when cash flow allows. Minimum payments are designed to extend revenue to the issuer; even small increases significantly shorten the payoff and reduce total interest."],
            ["What if I keep adding new charges?",
             "Use the &ldquo;new monthly charges&rdquo; input. If your payment is less than the interest charge plus the new charges, the balance will grow rather than shrink. The simulator will flag this case."],
            ["Should I do a balance transfer?",
             "Run the math first. Add the transfer fee to the new card&rsquo;s starting balance, simulate payoff at the promo APR over the promo period, then assume the regular APR after. Compare total cost to staying on the current card."],
        ],
    },

    # ------------------------------------------------------------------
    "pages/mortgage-calculator.html": {
        "intro_h2": "Mortgage calculator: principal, interest, taxes, insurance, PMI",
        "intro_body": (
            "<p>This calculator estimates the full monthly housing payment (PITI plus PMI) for a fixed-rate mortgage. It is meant for early affordability planning, not as a substitute for a lender&rsquo;s Loan Estimate.</p>"
        ),
        "sections": [
            {
                "kicker": "Inputs",
                "h2": "What each field represents",
                "body": (
                    "<p><strong>Home price</strong>: the contract or expected purchase price. <strong>Down payment</strong>: cash to closing applied to principal. <strong>Rate</strong>: annual interest rate; APR if you want to include lender fees. <strong>Term</strong>: typically 30 or 15 years. <strong>Annual taxes</strong> and <strong>insurance</strong>: divided by 12 and added to the monthly payment. <strong>Monthly PMI</strong>: required on conventional loans with under 20% down (and on FHA loans as MIP, with different removal rules).</p>"
                )
            },
            {
                "kicker": "Formula",
                "h2": "The amortization math",
                "body": (
                    "<p>The principal-and-interest portion uses the standard amortization formula <code>P = A · r ÷ (1 − (1 + r)<sup>−n</sup>)</code> with <em>r</em> as the monthly rate and <em>n</em> as the number of monthly payments. Taxes, insurance, and PMI are added directly to the monthly figure to produce a planning estimate of the full payment.</p>"
                )
            },
            {
                "kicker": "Limits",
                "h2": "What the calculator does not include",
                "body": (
                    "<p>HOA dues, condo special assessments, supplemental property tax assessments in some states, flood insurance where required, and any state or municipal tax credits are not included. For a true line-item picture, request a Loan Estimate from at least three lenders; see the <a href=\"https://www.consumerfinance.gov/owning-a-home/loan-estimate/\" target=\"_blank\" rel=\"noopener noreferrer\">CFPB&rsquo;s Loan Estimate guide</a>.</p>"
                )
            },
        ],
        "faqs": [
            ["Should I include taxes and insurance even if they are paid separately?",
             "Yes. Whether your lender escrows or not, those costs come out of your household budget every month. The most honest affordability test treats them as part of the housing payment."],
            ["Does the calculator account for interest-only or ARM loans?",
             "No. It assumes a fixed-rate fully-amortizing loan. Interest-only and adjustable-rate mortgages have different payment dynamics that this tool does not model."],
            ["How conservative should I be on rate and taxes?",
             "Conservative. Pick a rate that gives you cushion if pricing moves before lock, and use the highest plausible local property-tax rate. Underestimating either is a common reason buyers feel stretched after closing."],
        ],
    },

    # ------------------------------------------------------------------
    "pages/debt-payoff-calculator.html": {
        "intro_h2": "Debt payoff calculator: compare minimum vs. accelerated payments",
        "intro_body": (
            "<p>This calculator simulates two payoff scenarios on the same starting balance: paying the minimum monthly amount versus paying a higher planned amount. It is built to show, in months and dollars, what the extra payment buys.</p>"
        ),
        "sections": [
            {
                "kicker": "What it does",
                "h2": "Two simulations, one output",
                "body": (
                    "<p>For each scenario the calculator runs the same month-by-month payoff loop: interest accrues at APR ÷ 12; payment is applied; remaining balance carries to the next month. The output is months to payoff and total interest paid for both the minimum-payment and planned-payment paths.</p>"
                )
            },
            {
                "kicker": "Worked example",
                "h2": "Why $100 extra per month matters",
                "body": (
                    "<p>A $12,000 balance at 19.99% APR with a $320 minimum payment retires in roughly 67 months and costs about $5,470 in interest. The same balance with a $475 planned payment retires in roughly 32 months and costs about $2,490 in interest — a difference of nearly $3,000 in total cost and more than two years off the timeline.</p>"
                )
            },
            {
                "kicker": "Two methods",
                "h2": "Avalanche vs. snowball",
                "body": (
                    "<p>This tool simulates a single balance. When you have multiple debts, two well-known strategies exist: <em>avalanche</em> (pay highest APR first, mathematically optimal) and <em>snowball</em> (pay smallest balance first, behaviorally easier for some). The CFPB does not endorse either; both work if followed. Run the math on your specific balances with the <a href=\"/pages/debt-avalanche-vs-snowball-calculator\">avalanche vs snowball calculator</a>.</p>"
                )
            },
        ],
        "faqs": [
            ["Should I tackle one debt at a time or split extra payments?",
             "Mathematically, concentrating extra payments on the highest-APR debt minimizes total interest. Behaviorally, some borrowers stick with payoff better when they see quick wins on small balances. The CFPB does not pick one over the other; both work if maintained."],
            ["Does this account for cards still being used?",
             "The single-balance simulator assumes no new charges. If you are still actively charging on the same card, the &ldquo;new monthly charges&rdquo; field on the credit card interest calculator gives a more realistic picture."],
            ["What APR should I use if I do not know mine?",
             "Check your most recent statement; the APR is disclosed in plain language. For multiple cards, use the weighted average by balance for a single-balance estimate or run each card separately."],
        ],
    },

    # ------------------------------------------------------------------
    "pages/debt-avalanche-vs-snowball-calculator.html": {
        "intro_h2": "Avalanche vs. snowball: which one actually saves more?",
        "sources_topic": "debt-payoff",
        "intro_body": (
            "<p>The two named approaches to multi-debt payoff are the <strong>avalanche</strong> (extra dollars to the highest-APR balance first) and the <strong>snowball</strong> (extra dollars to the smallest balance first). The CFPB does not endorse either method &mdash; both work if the borrower stays the course. The right one for you depends on the math of your specific debts and on what keeps you paying consistently month after month.</p>"
            "<p>This calculator runs both simulations on your real balances and APRs at the same monthly payoff budget, then shows months to debt-free, total interest paid, balance curves over time, and a verdict that tells you exactly how much each method costs or saves versus the other. No login, no tracking, no localStorage &mdash; the math runs entirely in your browser.</p>"
        ),
        "sections": [
            {
                "kicker": "How avalanche works",
                "h2": "Highest APR first &mdash; the mathematical winner most of the time",
                "body": (
                    "<p>The avalanche method directs all extra payment dollars to the debt with the highest APR until that balance reaches zero, then rolls the entire freed-up payment down to the next highest APR. Minimum-interest discipline kicks in immediately because the most expensive dollar of debt is the one being attacked first.</p>"
                    "<p>For most borrowers with mixed credit-card and installment debt, avalanche minimizes total interest paid &mdash; sometimes by hundreds, sometimes by thousands of dollars compared with snowball, depending on the spread between the highest and lowest APR. The trade-off: if the highest-APR debt also happens to be the biggest balance, it can take many months before the borrower sees any account fully retired. Visible progress is slower.</p>"
                )
            },
            {
                "kicker": "How snowball works",
                "h2": "Smallest balance first &mdash; the behavioral winner for some",
                "body": (
                    "<p>The snowball method directs extra dollars to the debt with the smallest balance first, regardless of APR. The first account is typically retired within a few months, which creates a visible win, builds momentum, and freed-up minimum payments roll into the next account.</p>"
                    "<p>The research on snowball vs. avalanche is mixed. A frequently cited Harvard Business Review study found that consumers were more likely to complete debt payoff when they focused on closing smaller balances first. If past attempts at debt payoff have stalled out, snowball can be the right answer even when avalanche would technically cost less in interest. The calculator quantifies the trade-off so you can decide.</p>"
                )
            },
            {
                "kicker": "Inside the simulation",
                "h2": "What the model does each simulated month",
                "body": (
                    "<p>Each month the calculator: (1) adds monthly interest = balance &times; (APR &divide; 12) to every account that still has a balance, (2) sorts active accounts by avalanche or snowball priority, (3) applies the full monthly payoff budget starting from the top of the priority list and cascading down once a balance hits zero, (4) records the new total balance for the chart, (5) repeats until every balance is zero or 600 months pass.</p>"
                    "<p>If the monthly budget cannot cover total monthly interest across all active debts, the calculator triggers a warning &mdash; this is the &ldquo;negative amortization&rdquo; case where the balance grows even with payments applied. The fix is almost always a higher monthly budget; if that isn&rsquo;t possible, the next step is usually a hardship plan from the lender or a CFPB-listed nonprofit credit counselor.</p>"
                )
            },
            {
                "kicker": "Worked example",
                "h2": "Three real-looking debts and a $600 monthly budget",
                "body": (
                    "<p>The default inputs in the calculator load three illustrative debts: a $4,200 credit card at 24.99% APR, an $8,000 personal loan at 12.5%, and a $1,200 store card at 28.99%. At a $600 monthly payoff budget, avalanche attacks the 28.99% store card first, then the 24.99% credit card, then the personal loan. Snowball attacks the $1,200 store card first (smallest balance), then the $4,200 credit card, then the personal loan.</p>"
                    "<p>In this specific scenario both methods reach the same first target because the smallest-balance debt also happens to carry the highest APR. The order diverges on debts two and three: avalanche pays the 24.99% credit card next, snowball pays the $4,200 credit card next. Change one input &mdash; for example, raise the personal-loan APR above the credit-card APR &mdash; and the verdict changes immediately. Try it.</p>"
                )
            },
            {
                "kicker": "Method choice",
                "h2": "When the two methods produce nearly the same result",
                "body": (
                    "<p>If your highest-APR debt is also the smallest balance, avalanche and snowball converge. If your highest-APR debt is much larger than the others, avalanche saves materially more. If all your APRs are similar (e.g., a portfolio of three credit cards all between 22% and 26%), the two methods produce nearly identical interest costs and the &ldquo;right&rdquo; one is whichever you will actually stick with.</p>"
                    "<p>For most borrowers we recommend running both simulations once a year and re-checking after a big change &mdash; a balance transfer, a personal loan to consolidate, a missed payment that bumped an APR to a penalty rate. The right method is rarely a permanent decision; it&rsquo;s a recurring one.</p>"
                )
            },
        ],
        "faqs": [
            ["Which method usually saves more interest?",
             "Avalanche, because it pays the highest-APR balance first. The size of the savings depends on the APR spread between your debts and how long you carry the highest-rate balance."],
            ["Why would I ever choose snowball?",
             "Snowball gives visible wins faster. Behavioral research has shown that some borrowers finish payoff plans more reliably when they see balances retired quickly, even when avalanche would cost less in interest."],
            ["Does this calculator include minimum payments?",
             "No. It assumes a single monthly payoff budget that you allocate across your debts. If your lender requires specific minimum payments on each account, treat this calculator as a planning aid and confirm the math against your statements."],
            ["What if my payoff budget is too low?",
             "If your budget cannot cover monthly interest on all active balances, the calculator warns you that negative amortization may occur. The realistic options are increasing the budget, negotiating with the lender, or contacting a nonprofit credit counselor listed by the CFPB."],
            ["Can I include both loans and credit cards?",
             "Yes. The model treats every entered debt with a simple monthly-APR interest calculation. Real credit-card billing uses average-daily-balance accounting, and some installment loans amortize differently, so results are planning estimates, not exact lender reconciliations."],
            ["Is this financial advice?",
             NON_ADVICE_DISCLAIMER],
        ],
    },

    # ------------------------------------------------------------------
    "pages/credit-card-minimum-payment-true-cost-calculator.html": {
        "intro_h2": "What paying only the minimum actually costs",
        "sources_topic": "credit-cards",
        "intro_body": (
            "<p>Minimum payments are designed to be affordable, not to retire a balance. They are typically calculated as the greater of a small percentage of the balance (often 1&ndash;3%) or a flat dollar floor (often $25&ndash;$35). On a high-APR balance, the early minimum payment can barely beat the monthly interest, which is why a credit-card balance can survive for a decade even when payments never miss.</p>"
            "<p>This calculator simulates payoff month by month under two scenarios &mdash; minimum only, and minimum plus an extra payment you choose with a slider &mdash; and reports payoff time, total interest paid, the interest-to-principal ratio, and how much you save by adding the extra payment. Move the slider; the numbers update instantly.</p>"
        ),
        "sections": [
            {
                "kicker": "Why minimums stretch payoff",
                "h2": "The arithmetic that keeps balances alive",
                "body": (
                    "<p>A 24.99% APR is about 2.08% per month. On a $5,000 balance, the first month&rsquo;s interest is roughly $104. If the minimum payment is 2% of the balance ($100) or a $25 floor &mdash; whichever is larger &mdash; then the borrower pays $100, of which $104 was interest. Principal actually grew that month. The next month, the borrower pays 2% of a slightly larger balance and so on, in a slow grind that can run more than 25 years on a $5,000 starting balance.</p>"
                    "<p>The CARD Act of 2009 required issuers to include a Minimum Payment Warning Box on every statement, showing the years and total interest implied by paying only the minimum. Look for it on your statement &mdash; the numbers tend to be eye-opening.</p>"
                )
            },
            {
                "kicker": "How issuers calculate minimums",
                "h2": "Three common formulas",
                "body": (
                    "<p><strong>Percentage of balance:</strong> typically 1&ndash;3% of the statement balance. Common for general-purpose credit cards.</p>"
                    "<p><strong>Percentage plus interest:</strong> 1% of balance plus any interest and fees from the current cycle. This is the Regulation Z &ldquo;safe harbor&rdquo; formula and is required for some subprime cards. It pays interest faster than a flat percentage formula but leaves principal moving slowly.</p>"
                    "<p><strong>Flat dollar floor:</strong> a minimum dollar amount (e.g., $25, $35, or $40) regardless of balance, as long as the balance is above that floor. When a flat floor kicks in on a small balance, the implied payoff timeline shortens dramatically.</p>"
                    "<p>The calculator lets you set both the percentage and the floor so you can model your specific cardholder agreement.</p>"
                )
            },
            {
                "kicker": "Extra payment impact",
                "h2": "Why a small extra payment moves the needle so much",
                "body": (
                    "<p>Adding $50 or $100 a month to the minimum is rarely transformative for a single month&rsquo;s cash flow, but the compound effect over many months is large. Every extra dollar paid early reduces the principal that all future months&rsquo; interest accrues on. The calculator shows this directly: with a $5,000 balance at 24.99% APR, moving from minimum-only to a minimum plus $50 typically cuts payoff time roughly in half and saves several thousand dollars in interest.</p>"
                    "<p>The slider lets you find the lowest extra-payment amount that still produces a tolerable payoff timeline. For most borrowers, the right answer is whatever amount keeps the monthly budget sustainable but pays the balance off in under 24 months.</p>"
                )
            },
            {
                "kicker": "Limits of the model",
                "h2": "What this calculator does not include",
                "body": (
                    "<p>It does not model: new purchases during payoff (which reset the grace period and add to the balance immediately), promotional APRs that revert, late fees, penalty APRs triggered by a missed payment, deferred-interest store-card structures (where if you don&rsquo;t pay the full balance by the promo end date, all accrued interest is charged retroactively), balance-transfer fees, or hardship-plan repricing.</p>"
                    "<p>Each of those can move the actual cost significantly. Treat the result as a planning floor: your real-world cost is at least this much and probably more if any of the above apply.</p>"
                )
            },
        ],
        "faqs": [
            ["Why do minimum payments take so long?",
             "Because the minimum payment is calculated as a small percentage of the balance and the high APR consumes most of each payment as interest in the early months. Principal moves slowly."],
            ["Does this calculator include new purchases?",
             "No. It assumes the starting balance is closed to new charges. If you continue to use the card, payoff takes longer."],
            ["What minimum-payment percentage should I use?",
             "Use the percentage from your cardholder agreement if you know it. Otherwise, 2% to 3% is a common planning range. The floor (e.g., $25 minimum) often dominates when balances are small."],
            ["Can a small extra payment really save thousands?",
             "On high-APR balances, yes. Extra payments reduce principal earlier in the schedule, which reduces every future month&rsquo;s interest charge. Compounding works in both directions."],
            ["What if the calculator says my balance never pays off?",
             "That means the minimum payment is not exceeding monthly interest under your inputs. Increase the payment, raise the floor, or contact your lender or a nonprofit credit counselor."],
            ["Is this financial advice?",
             NON_ADVICE_DISCLAIMER],
        ],
    },

    # ------------------------------------------------------------------
    "pages/mortgage-refinance-break-even-calculator.html": {
        "intro_h2": "Should you refinance? The break-even math, in one screen.",
        "sources_topic": "refinancing",
        "intro_body": (
            "<p>A mortgage refinance lowers (or raises) your monthly payment in exchange for closing costs paid up front. The decision turns on a single arithmetic question: <strong>how many months of payment savings does it take to recover those closing costs?</strong> If you plan to keep the loan longer than that break-even, refinancing usually saves money. If you might sell, move, or refinance again before then, it usually doesn&rsquo;t.</p>"
            "<p>This calculator compares your current loan with a new offer, shows the monthly payment difference, divides closing costs by monthly savings, and warns you if your planned sale or next refinance comes before the break-even point. The chart visualizes cumulative savings net of closing costs over time.</p>"
        ),
        "sections": [
            {
                "kicker": "The break-even formula",
                "h2": "Closing costs &divide; monthly savings = break-even months",
                "body": (
                    "<p>The standard break-even calculation is straightforward: total refinance closing costs divided by the monthly principal-and-interest savings between the old and new loans. If your new loan saves $250 a month and the refinance costs $6,500 to close, the simple break-even is 26 months. After month 26 every additional payment saved is a net gain.</p>"
                    "<p>This calculator uses that simple model on purpose. Some online calculators add tax-deduction adjustments, opportunity-cost discount rates, or amortization-aware accounting for the larger principal balance early in the new loan. Those refinements matter at the margin, but they don&rsquo;t change the basic question of whether your timeline beats the simple break-even.</p>"
                )
            },
            {
                "kicker": "Read your Loan Estimate first",
                "h2": "The federal Loan Estimate is the right closing-costs number",
                "body": (
                    "<p>Federal Truth-in-Lending rules require every lender to deliver a Loan Estimate within three business days of an application. The CFPB&rsquo;s page on the <a href=\"https://www.consumerfinance.gov/owning-a-home/loan-estimate/\" target=\"_blank\" rel=\"noopener noreferrer\">Loan Estimate</a> shows the exact form. Pull closing-cost totals from there &mdash; not from advertised &ldquo;average&rdquo; numbers &mdash; for the most accurate break-even calculation.</p>"
                    "<p>Closing costs typically run 2&ndash;5% of the new loan amount. They include lender origination, appraisal, title and settlement, recording, prepaid interest, and the funding of the new escrow account. Some of these are negotiable (or shoppable), and some are not. The Loan Estimate splits them into three buckets so you can see which is which.</p>"
                )
            },
            {
                "kicker": "Term-reset risk",
                "h2": "Why a lower payment can still cost more total",
                "body": (
                    "<p>The most common silent mistake in refinancing is rolling 22 years remaining on a 30-year loan into a brand-new 30-year loan. The new monthly payment is lower &mdash; but the timeline extended by 8 years, and total interest paid often goes up even at a lower rate.</p>"
                    "<p>If your goal is total-cost reduction, ask the lender to quote the refinance at a term that doesn&rsquo;t extend your existing schedule (e.g., a new 20-year loan to replace 22 years remaining on the original 30-year). The monthly payment may not drop as much, but the total interest savings can be much larger.</p>"
                )
            },
            {
                "kicker": "Planned-sale warning",
                "h2": "If you might sell before break-even, refinance carefully",
                "body": (
                    "<p>The calculator asks for your planned timeline in years for a sale, payoff, or next refinance. If that number is shorter than the calculated break-even months, the calculator surfaces a warning. The economic interpretation is simple: you would pay the closing costs once and only partially recover them through monthly savings before the loan goes away.</p>"
                    "<p>Job moves, marriage and divorce, deaths and births, and unforeseen relocations all shorten loan timelines. A conservative rule for borrowers who aren&rsquo;t certain of their five-year plan is to refinance only when the break-even comes inside 36 months &mdash; that leaves a buffer for life happening.</p>"
                )
            },
        ],
        "faqs": [
            ["What is a refinance break-even point?",
             "It is the number of months your monthly payment savings need to add up before they equal your refinance closing costs. After break-even, you are net ahead."],
            ["Does this include taxes and insurance?",
             "No. It estimates principal-and-interest payments only. Taxes, homeowners insurance, mortgage insurance, and HOA dues are unchanged by a typical refinance and are excluded from the break-even calculation."],
            ["What if the new payment is higher?",
             "Then there is no payment-based break-even. Some borrowers refinance to a higher payment intentionally (e.g., 30-year to 15-year) to cut total interest; this calculator focuses specifically on the payment-savings case."],
            ["Should I include closing costs?",
             "Yes. Closing costs drive the break-even calculation. Use the figure from your Loan Estimate for accuracy; advertised &ldquo;average&rdquo; numbers are not specific to your loan."],
            ["What if I plan to sell soon?",
             "If your planned timeline is shorter than the calculated break-even months, the calculator surfaces a warning. In that case, refinancing may not recover closing costs through monthly savings."],
            ["Is this mortgage advice?",
             NON_ADVICE_DISCLAIMER],
        ],
    },
}


CONTACT_EMAIL = "javiperezguides@gmail.com"


NAV_ITEMS = [
    ("/", "Home"),
    ("/pages/personal-loans-guide", "Personal Loans"),
    ("/pages/credit-cards-guide", "Credit Cards"),
    ("/pages/mortgage-guide", "Mortgages"),
    ("/pages/debt-payoff-guide", "Debt Payoff"),
    ("/pages/loan-payment-calculator", "Calculators"),
]


DISCLAIM = "This content is for informational purposes only and does not constitute financial advice."


def title_from_path(path: str) -> str:
    slug = Path(path).stem.replace("-", " ")
    return " ".join(word.capitalize() for word in slug.split())


def public_path(path: str) -> str:
    if path == "index.html":
        return "/"
    # A directory index file like authors/javi-perez/index.html should map to
    # the directory URL (/authors/javi-perez), not /authors/javi-perez/index.
    if path.endswith("/index.html"):
        return "/" + path[:-len("/index.html")]
    return f"/{path.removesuffix('.html')}"


def url_for(path: str) -> str:
    return f"{DOMAIN}{public_path(path)}"


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
        items.append({"name": "Guides", "url": url_for("pages/personal-loans-guide.html")})
    elif path not in {"index.html"}:
        items.append({"name": "Company", "url": url_for("about.html")})
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
    """Deprecated. The previous implementation chose from five hardcoded
    scenarios/figures/compliance strings and pasted the same paragraph shape
    into every page that lacked unique PAGE_CONTENT, producing scaled-content
    abuse. Returns empty string so any residual call site renders nothing
    rather than templated copy."""
    return ""


# Topic -> list of (label, href, role) tuples for the Sources & methodology block.
# Only official .gov / regulator URLs and a small set of high-trust supplemental
# sources are linked. Every link opens in a new tab with rel="noopener".
SOURCES_BY_TOPIC: Dict[str, List[Tuple[str, str, str]]] = {
    "personal-loans": [
        ("CFPB · Personal loans explained", "https://www.consumerfinance.gov/consumer-tools/", "Plain-language CFPB explainer on how personal loans work, what fees to expect, and consumer protections."),
        ("Federal Reserve · G.19 Consumer Credit release", "https://www.federalreserve.gov/releases/g19/current/", "Official monthly consumer credit data used for APR and balance context."),
        ("FTC · Personal loan scams", "https://consumer.ftc.gov/articles/what-know-about-personal-loans", "Plain-English FTC guidance on what to watch for when shopping for a personal loan."),
    ],
    "credit-cards": [
        ("CFPB · Credit cards", "https://www.consumerfinance.gov/consumer-tools/credit-cards/", "CFPB resources on APR, fees, billing, and disputes."),
        ("Federal Reserve · Report to Congress on the Profitability of Credit Card Operations", "https://www.federalreserve.gov/publications/credit-card-profitability.htm", "Official Federal Reserve reporting on credit card pricing and profitability."),
        ("CFPB · Credit card complaint database", "https://www.consumerfinance.gov/data-research/consumer-complaints/", "Searchable public complaint database used to spot recurring issuer issues."),
    ],
    "mortgage": [
        ("CFPB · Loan Estimate form", "https://www.consumerfinance.gov/owning-a-home/loan-estimate/", "The standardized federal disclosure every lender must give within three business days."),
        ("Federal Reserve · Mortgage rates (FRED)", "https://fred.stlouisfed.org/series/MORTGAGE30US", "30-year fixed mortgage average, updated weekly by the Federal Reserve via Freddie Mac PMMS."),
        ("HUD · FHA loan limits", "https://www.hud.gov/buying/loans", "FHA program rules, limits, and counseling resources."),
    ],
    "credit-score": [
        ("CFPB · Credit reports and scores", "https://www.consumerfinance.gov/consumer-tools/credit-reports-and-scores/", "CFPB-curated resources on how scores are built, how to dispute errors, and how to get free reports."),
        ("FTC · Free credit reports", "https://consumer.ftc.gov/articles/free-credit-reports", "How to use AnnualCreditReport.com — the only federally authorized source for free reports."),
        ("AnnualCreditReport.com", "https://www.annualcreditreport.com/index.action", "Federally authorized source for free credit reports from Equifax, Experian, and TransUnion."),
    ],
    "banking-fees": [
        ("FDIC · National rates and rate caps", "https://www.fdic.gov/national-rates-and-rate-caps", "Weekly FDIC national average rates for deposit products."),
        ("CFPB · Bank account fees", "https://www.consumerfinance.gov/about-us/blog/", "CFPB consumer resources on overdraft, NSF, and account fees."),
        ("Federal Reserve · Consumers and mobile financial services", "https://www.federalreserve.gov/data.htm", "Federal Reserve research on consumer banking behavior."),
    ],
    "debt-payoff": [
        ("CFPB · Debt repayment strategies", "https://www.consumerfinance.gov/ask-cfpb/what-is-a-debt-relief-program-and-how-do-i-know-if-i-should-use-one-en-1457/", "CFPB explainer on debt management plans and repayment approaches."),
        ("FTC · Coping with debt", "https://consumer.ftc.gov/articles/coping-with-debt", "FTC guidance on negotiating with creditors and avoiding scams."),
        ("Federal Reserve · Household Debt and Credit Report", "https://www.newyorkfed.org/microeconomics/hhdc.html", "Quarterly New York Fed Center for Microeconomic Data report."),
    ],
    "refinancing": [
        ("CFPB · Refinancing your mortgage", "https://www.consumerfinance.gov/owning-a-home/", "CFPB checklist and explainer for mortgage refinancing decisions."),
        ("CFPB · Auto loan refinancing", "https://www.consumerfinance.gov/consumer-tools/auto-loans/", "CFPB short answer on when refinancing an auto loan makes sense."),
        ("Federal Reserve · Mortgage rates (FRED)", "https://fred.stlouisfed.org/series/MORTGAGE30US", "Weekly 30-year fixed mortgage rate average used to gauge refinance timing."),
    ],
    "student-loans": [
        ("Federal Student Aid · StudentAid.gov", "https://studentaid.gov/", "Official U.S. Department of Education portal for federal student aid."),
        ("CFPB · Student loans", "https://www.consumerfinance.gov/consumer-tools/student-loans/", "CFPB consumer resources on federal vs. private loans, servicing, and repayment."),
        ("Federal Student Aid · Income-driven repayment", "https://studentaid.gov/manage-loans/repayment/plans/income-driven", "Plain-English explainer on IDR plans including SAVE, PAYE, IBR."),
    ],
    "default": [
        ("CFPB · Consumer tools", "https://www.consumerfinance.gov/consumer-tools/", "Plain-language explainers and disclosure forms from the Consumer Financial Protection Bureau."),
        ("Federal Reserve · Consumer credit data", "https://www.federalreserve.gov/releases/g19/current/", "Monthly G.19 release on consumer credit outstanding and revolving APRs."),
        ("FTC · Money and credit", "https://consumer.ftc.gov/money-and-credit", "FTC consumer protection guidance on money and credit."),
    ],
}


def sources_block(topic_key: str) -> str:
    """Render a 'Sources and methodology' section pointing at primary regulators
    plus a short methodology note. The topic_key picks the link set; unknown
    keys fall back to a sensible default."""
    key = (topic_key or "").strip().lower()
    aliases = {
        "personal loans": "personal-loans",
        "credit cards": "credit-cards",
        "mortgage": "mortgage",
        "credit score": "credit-score",
        "banking fees": "banking-fees",
        "debt payoff": "debt-payoff",
        "refinancing": "refinancing",
        "student loans": "student-loans",
    }
    key = aliases.get(key, key)
    sources = SOURCES_BY_TOPIC.get(key) or SOURCES_BY_TOPIC["default"]
    items = "".join(
        f'<li><a href="{html.escape(href)}" target="_blank" rel="noopener noreferrer">{html.escape(label)}</a> — {html.escape(role)}</li>'
        for label, href, role in sources
    )
    return trim(
        f"""
        <section class="ccg-section ccg-section--sources" aria-label="Sources and methodology">
          <div class="ccg-section-head">
            <p class="ccg-kicker">Sources & Methodology</p>
            <h2>Where we pulled the numbers</h2>
          </div>
          <ul class="ccg-list ccg-list--sources">{items}</ul>
          <p class="ccg-sources-note">{html.escape(AI_DISCLOSURE)} {html.escape(NON_ADVICE_DISCLAIMER)}</p>
        </section>
        """
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
        <section class="ccg-author-box editorial-byline" aria-label="Editor information">
          <img class="editorial-byline__photo" src="{EDITOR_PHOTO}" alt="{EDITOR_NAME}" width="56" height="56" loading="lazy" onerror="this.onerror=null;this.src='{EDITOR_PHOTO_FALLBACK}';">
          <div class="editorial-byline__body">
            <p class="editorial-byline__name"><strong>Edited by <a href="{DOMAIN}/authors/javi-perez">{EDITOR_NAME}</a></strong> · {EDITOR_ROLE}</p>
            <p class="editorial-byline__meta">
              <a href="{EDITOR_LINKEDIN}" target="_blank" rel="noopener noreferrer">LinkedIn</a>
              · Last reviewed: {LAST_REVIEWED}
            </p>
            <p class="editorial-byline__note">{AI_DISCLOSURE} {NON_ADVICE_DISCLAIMER}</p>
          </div>
        </section>
        """
    )


def editorial_trust_block() -> str:
    return trim(
        f"""
        <section class="ccg-section editorial-trust" aria-label="About the editor">
          <img class="editorial-trust__photo" src="{EDITOR_PHOTO}" alt="{EDITOR_NAME}" width="80" height="80" loading="lazy" onerror="this.onerror=null;this.src='{EDITOR_PHOTO_FALLBACK}';">
          <div class="editorial-trust__body">
            <p class="ccg-kicker">Editorial Standards</p>
            <h2>Built by <a href="{DOMAIN}/authors/javi-perez">{EDITOR_NAME}</a> with public data you can verify.</h2>
            <p>Every indexable guide cites primary sources — CFPB, Federal Reserve / FRED, FDIC, BLS, FTC, and SEC. {AI_DISCLOSURE}</p>
            <p><strong>{NON_ADVICE_DISCLAIMER}</strong></p>
            <p><a class="editorial-trust__link" href="{DOMAIN}/how-we-research">Read our research methodology →</a></p>
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


def sc_disclosure() -> str:
    return (
        '<div class="affiliate-disclosure">\n'
        '  <p><strong>Advertiser Disclosure:</strong> This page contains affiliate links. '
        'We may earn a commission at no extra cost to you if you click through and '
        'make a purchase. This does not influence our editorial content.</p>\n'
        '</div>'
    )


def sc_cta_primary() -> str:
    """Bloque 1 — Blue trial CTA. Placed after the first </section>."""
    return (
        '<div class="smartcredit-cta-box" style="background:#e8f4fd;border:2px solid #0066cc;'
        'border-radius:10px;padding:28px 24px;margin:32px 0;text-align:center;">\n'
        '  <p style="font-size:0.85em;font-weight:700;letter-spacing:0.08em;color:#0066cc;'
        'text-transform:uppercase;margin:0 0 10px 0;">Recommended Tool</p>\n'
        '  <p style="font-size:1.25em;font-weight:800;margin:0 0 12px 0;color:#002a6e;">\n'
        '    Monitor Your Credit \u2014 Try SmartCredit for $1\n'
        '  </p>\n'
        '  <p style="margin:0 0 20px 0;color:#444;max-width:520px;margin-left:auto;margin-right:auto;">\n'
        '    Get your full credit report, daily score updates, real-time alerts, and\n'
        '    identity-theft protection all in one place. 7-day trial for just $1.\n'
        '  </p>\n'
        f'  <a href="{SC_TRIAL_URL}"\n'
        '     rel="nofollow sponsored" target="_blank"\n'
        '     style="background:#0066cc;color:#fff;padding:14px 36px;border-radius:6px;'
        'text-decoration:none;font-weight:700;font-size:1.05em;display:inline-block;">\n'
        '    Start 7-Day Trial for $1 \u2192\n'
        '  </a>\n'
        '  <p style="font-size:0.78em;color:#666;margin:10px 0 0 0;">'
        'Sponsored \u00b7 Cancel anytime</p>\n'
        '</div>'
    )


def sc_cta_boost() -> str:
    """Bloque 2 — Orange boost CTA. Placed after the second </section>."""
    return (
        '<div class="smartcredit-cta-boost" style="background:#fff3e0;border:2px solid #e65100;'
        'border-radius:10px;padding:28px 24px;margin:32px 0;text-align:center;">\n'
        '  <p style="font-size:0.85em;font-weight:700;letter-spacing:0.08em;color:#e65100;'
        'text-transform:uppercase;margin:0 0 10px 0;">Score Builder</p>\n'
        '  <p style="font-size:1.25em;font-weight:800;margin:0 0 12px 0;color:#7a2800;">\n'
        '    Boost Your Score an Average of 34 Points\n'
        '  </p>\n'
        '  <p style="margin:0 0 20px 0;color:#444;max-width:520px;margin-left:auto;margin-right:auto;">\n'
        '    SmartCredit\u2019s ScoreBuilder\u2122 shows you exactly which accounts to pay down\n'
        '    and by how much to maximise your credit score gains.\n'
        '  </p>\n'
        f'  <a href="{SC_BOOST_URL}"\n'
        '     rel="nofollow sponsored" target="_blank"\n'
        '     style="background:#e65100;color:#fff;padding:14px 36px;border-radius:6px;'
        'text-decoration:none;font-weight:700;font-size:1.05em;display:inline-block;">\n'
        '    See How ScoreBuilder Works \u2192\n'
        '  </a>\n'
        '  <p style="font-size:0.78em;color:#666;margin:10px 0 0 0;">Sponsored</p>\n'
        '</div>'
    )


def sc_cta_secondary() -> str:
    """Bloque 3 — Purple evergreen CTA. Placed before the FAQ section."""
    return (
        '<div class="smartcredit-cta-secondary" style="background:#f3e5f5;border:2px solid #7b1fa2;'
        'border-radius:10px;padding:28px 24px;margin:32px 0;text-align:center;">\n'
        '  <p style="font-size:0.85em;font-weight:700;letter-spacing:0.08em;color:#7b1fa2;'
        'text-transform:uppercase;margin:0 0 10px 0;">Credit Monitoring</p>\n'
        '  <p style="font-size:1.25em;font-weight:800;margin:0 0 12px 0;color:#38006b;">\n'
        '    Stay on Top of Your Credit 24\u202f/\u202f7\n'
        '  </p>\n'
        '  <p style="margin:0 0 20px 0;color:#444;max-width:520px;margin-left:auto;margin-right:auto;">\n'
        '    SmartCredit monitors all three credit bureaus and alerts you the moment\n'
        '    anything changes \u2014 so you can act fast before damage is done.\n'
        '  </p>\n'
        f'  <a href="{SC_EVERGREEN_URL}"\n'
        '     rel="nofollow sponsored" target="_blank"\n'
        '     style="background:#7b1fa2;color:#fff;padding:14px 36px;border-radius:6px;'
        'text-decoration:none;font-weight:700;font-size:1.05em;display:inline-block;">\n'
        '    Start Monitoring Now \u2192\n'
        '  </a>\n'
        '  <p style="font-size:0.78em;color:#666;margin:10px 0 0 0;">Sponsored</p>\n'
        '</div>'
    )


def _in_tag(s: str, pos: int) -> bool:
    """Return True if pos is inside an HTML tag (between < and >)."""
    last_open = s.rfind('<', 0, pos)
    last_close = s.rfind('>', 0, pos)
    return last_open > last_close


def smartcredit_inject(content: str) -> str:
    """Post-process page body HTML to insert SmartCredit affiliate content.

    Insertion order per page:
      A) Disclosure before the first <section class="ccg-section">
      B) Bloque 1 (blue trial) after the first </section>
      C) Bloque 2 (orange boost) after the second </section>
      D) Bloque 3 (purple evergreen) before the FAQ section
      E) Tracking pixel at the very end
    """
    sec_marker = '<section class="ccg-section">'

    # A) Disclosure before first <section class="ccg-section">
    idx = content.find(sec_marker)
    if idx != -1:
        content = content[:idx] + sc_disclosure() + '\n' + content[idx:]

    # B) Bloque 1 after the first </section>
    end_tag = '</section>'
    end_idx = content.find(end_tag)
    if end_idx != -1:
        insert_at = end_idx + len(end_tag)
        content = content[:insert_at] + '\n' + sc_cta_primary() + content[insert_at:]

    # C) Bloque 2 after the second </section>
    second_end_idx = content.find(end_tag, end_idx + len(end_tag) + 1 if end_idx != -1 else 0)
    if second_end_idx != -1:
        insert_at2 = second_end_idx + len(end_tag)
        content = content[:insert_at2] + '\n' + sc_cta_boost() + content[insert_at2:]

    # D) Bloque 3 before FAQ section
    faq_kicker = '<p class="ccg-kicker">FAQ</p>'
    faq_pos = content.find(faq_kicker)
    if faq_pos != -1:
        faq_sec_start = content.rfind(sec_marker, 0, faq_pos)
        if faq_sec_start != -1:
            content = content[:faq_sec_start] + sc_cta_secondary() + '\n' + content[faq_sec_start:]

    # E) Tracking pixel at end of content
    content = content + '\n' + SC_PIXEL

    return content


def section_block(topic: str, page_title: str, index: int) -> str:
    """Deprecated. The previous implementation produced templated 'Deep Dive'
    paragraphs that recycled five hardcoded example figures across many pages,
    triggering AdSense scaled-content heuristics. Kept as a stub so any
    leftover call sites get a tiny placeholder instead of repeating content.
    Do not use in new code paths."""
    return ""


def article_body(config: Dict[str, object], min_words: int, related_paths: List[str]) -> str:
    """Short, non-templated body for pillar/supporting pages that do NOT have a
    custom PAGE_CONTENT entry. These pages render only their unique hero text,
    one comparison table, one FAQ block, the editor byline, and related links.
    The legacy 'Deep Dive' loop was removed to eliminate scaled-content patterns.
    Pages that need long-form depth must opt in via PAGE_CONTENT.
    """
    intro = trim(
        f"""
        <section class="ccg-section">
          <div class="ccg-section-head">
            <p class="ccg-kicker">Overview</p>
            <h2>{html.escape(str(config["hero"]))}</h2>
          </div>
          <p>{html.escape(str(config.get("summary") or config.get("description") or ""))}</p>
        </section>
        """
    )
    content = (
        intro
        + comparison_table(str(config["hero"]))
        + faq_html(config["faqs"])
        + sources_block(str(config.get("sources_topic") or config["hero"]))
        + author_box()
        + related_html(related_paths)
    )
    return content


def support_body(path: str, title: str, desc: str, related_paths: List[str]) -> Tuple[str, List[List[str]]]:
    """Minimal body for supporting articles that do NOT have unique PAGE_CONTENT.
    These pages are intentionally short and rendered as noindex,follow during
    AdSense review — they remain available via internal links but stay out of
    the indexable surface until they get unique long-form content of their own."""
    faqs = [
        [f"Is this page financial advice?", NON_ADVICE_DISCLAIMER],
        [f"Where do the examples come from?", "Examples are hypothetical scenarios used to illustrate how a cost mechanic works. Real product pricing changes; always verify the latest rates and fees directly with the lender or bank before deciding."],
        [f"How can I reach the editor?", f"Email {CONTACT_EMAIL} for editorial questions, corrections, or partnership inquiries."],
    ]
    intro = trim(
        f"""
        <section class="ccg-section">
          <div class="ccg-section-head">
            <p class="ccg-kicker">Overview</p>
            <h2>{html.escape(title)}</h2>
          </div>
          <p>{html.escape(desc)}</p>
          <p>This article is part of a wider set of guides on CreditCostGuide. It is short on purpose: it explains the core mechanic and links to the relevant pillar guide for the longer treatment. For the worked examples, calculators, and primary-source citations, follow the links to the pillar guide and any related calculator below.</p>
        </section>
        """
    )
    body = (
        intro
        + faq_html(faqs)
        + author_box()
        + related_html(related_paths)
    )
    return body, faqs


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
    # Charted calculators have their own DOM contracts (multi-row debt table,
    # range slider, before/after grid, cumulative chart). Their per-page JS
    # binds to these specific IDs.
    if calc_type == "avalanche-snowball":
        return _calc_module_avalanche_snowball()
    if calc_type == "min-payment":
        return _calc_module_min_payment()
    if calc_type == "refinance":
        return _calc_module_refinance()
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


def _calc_module_avalanche_snowball() -> str:
    """Multi-debt input table + result cards + comparison table + chart canvas.
    Per-page JS at /assets/scripts/debt-avalanche-snowball.js binds to these IDs.
    No localStorage, no analytics, no input tracking — all math is browser-local."""
    return trim(
        """
        <section class="ccg-section">
          <div class="ccg-calc-card ccg-calc-card--charted" data-charted-calc="avalanche-snowball">
            <h3 class="ccg-calc-title">Compare your debt payoff strategies</h3>
            <div class="ccg-calc-row">
              <label><span>Monthly payoff budget</span>
                <input id="totalPayment" type="number" inputmode="decimal" min="1" step="10" value="600">
              </label>
            </div>
            <div class="ccg-debt-table-wrap">
              <table class="ccg-debt-input-table">
                <thead>
                  <tr><th>Debt name</th><th>Balance</th><th>APR (%)</th><th aria-label="Actions"></th></tr>
                </thead>
                <tbody id="debtRows"></tbody>
              </table>
            </div>
            <button type="button" class="ccg-button ccg-button--ghost" id="addDebtBtn">+ Add another debt</button>
            <p class="ccg-calc-help">You can compare up to 5 debts. The calculator assumes the full monthly payoff budget is available every month and that no new charges are added.</p>
            <div id="debtWarning" class="ccg-calc-warning" hidden></div>
            <div class="ccg-result-grid ccg-result-grid--three">
              <div class="ccg-result-card"><span>Avalanche payoff</span><strong id="avalancheMonths">&mdash;</strong><span id="avalancheInterest">&mdash;</span></div>
              <div class="ccg-result-card"><span>Snowball payoff</span><strong id="snowballMonths">&mdash;</strong><span id="snowballInterest">&mdash;</span></div>
              <div class="ccg-result-card ccg-result-card--highlight"><span>Verdict</span><strong id="methodVerdict">&mdash;</strong><span id="methodVerdictSub">&mdash;</span></div>
            </div>
            <div class="ccg-calc-subsection">
              <h4>Side-by-side comparison</h4>
              <div class="ccg-table-wrap">
                <table class="ccg-table">
                  <thead><tr><th>Method</th><th>Months</th><th>Debt-free date</th><th>Total interest</th></tr></thead>
                  <tbody>
                    <tr><td>Avalanche</td><td id="avalancheTableMonths">&mdash;</td><td id="avalancheDate">&mdash;</td><td id="avalancheTableInterest">&mdash;</td></tr>
                    <tr><td>Snowball</td><td id="snowballTableMonths">&mdash;</td><td id="snowballDate">&mdash;</td><td id="snowballTableInterest">&mdash;</td></tr>
                  </tbody>
                </table>
              </div>
            </div>
            <div class="ccg-calc-subsection">
              <h4>Balance over time</h4>
              <div class="ccg-chart-wrap"><canvas id="debtChart" height="160" role="img" aria-label="Balance over time for avalanche vs snowball"></canvas></div>
            </div>
          </div>
        </section>
        """
    )


def _calc_module_min_payment() -> str:
    return trim(
        """
        <section class="ccg-section">
          <div class="ccg-calc-card ccg-calc-card--charted" data-charted-calc="min-payment">
            <h3 class="ccg-calc-title">Estimate the true cost of paying the minimum</h3>
            <div class="ccg-calc-row">
              <label><span>Credit card balance</span><input id="ccBalance" type="number" inputmode="decimal" min="0" step="50" value="5000"></label>
              <label><span>APR (%)</span><input id="ccApr" type="number" inputmode="decimal" min="0" max="99" step="0.01" value="24.99"></label>
              <label><span>Minimum payment %</span><input id="minPct" type="number" inputmode="decimal" min="0.1" max="10" step="0.1" value="2"></label>
              <label><span>Minimum payment floor ($)</span><input id="minFloor" type="number" inputmode="decimal" min="0" step="5" value="25"></label>
              <label class="ccg-calc-row__wide"><span>Extra monthly payment: <strong id="extraLabel">$50</strong></span>
                <input id="extraPayment" type="range" min="0" max="500" step="10" value="50">
              </label>
            </div>
            <div id="minWarning" class="ccg-calc-warning" hidden></div>
            <div class="ccg-result-grid ccg-result-grid--three">
              <div class="ccg-result-card ccg-result-card--highlight"><span>Minimum only</span><strong id="minHeadline">&mdash;</strong><span id="minInterest">&mdash;</span></div>
              <div class="ccg-result-card"><span>With extra payment</span><strong id="extraHeadline">&mdash;</strong><span id="extraInterest">&mdash;</span></div>
              <div class="ccg-result-card"><span>Estimated savings</span><strong id="savingsHeadline">&mdash;</strong><span id="timeSavings">&mdash;</span></div>
            </div>
            <div class="ccg-calc-subsection">
              <h4>Minimum vs extra payment</h4>
              <div class="ccg-table-wrap">
                <table class="ccg-table">
                  <thead><tr><th>Scenario</th><th>Months</th><th>Total interest</th><th>Interest / principal</th></tr></thead>
                  <tbody>
                    <tr><td>Minimum only</td><td id="minMonths">&mdash;</td><td id="minTotalInterest">&mdash;</td><td id="minRatio">&mdash;</td></tr>
                    <tr><td>Minimum + extra</td><td id="extraMonths">&mdash;</td><td id="extraTotalInterest">&mdash;</td><td id="extraRatio">&mdash;</td></tr>
                  </tbody>
                </table>
              </div>
            </div>
            <div class="ccg-calc-subsection">
              <h4>Cost comparison</h4>
              <div class="ccg-chart-wrap"><canvas id="minPaymentChart" height="160" role="img" aria-label="Total interest and payoff months bar chart"></canvas></div>
            </div>
          </div>
        </section>
        """
    )


def _calc_module_refinance() -> str:
    return trim(
        """
        <section class="ccg-section">
          <div class="ccg-calc-card ccg-calc-card--charted" data-charted-calc="refinance">
            <h3 class="ccg-calc-title">Estimate your refinance break-even point</h3>
            <div class="ccg-calc-row">
              <label><span>Current loan balance</span><input id="loanBalance" type="number" inputmode="decimal" min="0" step="1000" value="275000"></label>
              <label><span>Current interest rate (%)</span><input id="currentRate" type="number" inputmode="decimal" min="0" max="30" step="0.01" value="7.25"></label>
              <label><span>Remaining term (years)</span><input id="remainingYears" type="number" inputmode="numeric" min="1" max="40" step="1" value="25"></label>
              <label><span>New interest rate (%)</span><input id="newRate" type="number" inputmode="decimal" min="0" max="30" step="0.01" value="6.25"></label>
              <label><span>New loan term (years)</span><input id="newYears" type="number" inputmode="numeric" min="1" max="40" step="1" value="30"></label>
              <label><span>Closing costs ($)</span><input id="closingCosts" type="number" inputmode="decimal" min="0" step="100" value="6500"></label>
              <label><span>Planned sale or refi (years)</span><input id="plannedYears" type="number" inputmode="numeric" min="0" max="40" step="1" value="5"></label>
            </div>
            <div id="refiWarning" class="ccg-calc-warning" hidden></div>
            <div class="ccg-result-grid ccg-result-grid--three">
              <div class="ccg-result-card"><span>Current payment</span><strong id="oldPayment">&mdash;</strong><span>Principal &amp; interest estimate</span></div>
              <div class="ccg-result-card"><span>New payment</span><strong id="newPayment">&mdash;</strong><span>Principal &amp; interest estimate</span></div>
              <div class="ccg-result-card ccg-result-card--highlight"><span>Break-even point</span><strong id="breakEven">&mdash;</strong><span id="breakEvenSub">&mdash;</span></div>
            </div>
            <div class="ccg-calc-subsection">
              <h4>Before / after refinance</h4>
              <div class="ccg-table-wrap">
                <table class="ccg-table">
                  <thead><tr><th>Metric</th><th>Current loan</th><th>New refinance</th></tr></thead>
                  <tbody>
                    <tr><td>Monthly payment</td><td id="tableOldPayment">&mdash;</td><td id="tableNewPayment">&mdash;</td></tr>
                    <tr><td>Remaining interest estimate</td><td id="oldInterest">&mdash;</td><td id="newInterest">&mdash;</td></tr>
                    <tr><td>Closing costs</td><td>&mdash;</td><td id="tableClosingCosts">&mdash;</td></tr>
                  </tbody>
                </table>
              </div>
            </div>
            <div class="ccg-calc-subsection">
              <h4>Cumulative savings after closing costs</h4>
              <div class="ccg-chart-wrap"><canvas id="refiChart" height="160" role="img" aria-label="Cumulative refinance savings over time"></canvas></div>
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


def rich_article_body(
    path: str,
    related_paths: List[str],
    calc_type: Optional[str] = None,
) -> Tuple[str, List[List[str]]]:
    """Render a page from PAGE_CONTENT — real, unique content per page.

    For calculator pages pass calc_type to inject the calculator widget
    between the intro section and the content sections.
    """
    cfg = PAGE_CONTENT[path]

    # Intro section (body is raw HTML)
    intro_section = trim(
        f"""
        <section class="ccg-section">
          <div class="ccg-section-head">
            <p class="ccg-kicker">Overview</p>
            <h2>{html.escape(cfg["intro_h2"])}</h2>
          </div>
          {cfg["intro_body"]}
        </section>
        """
    )

    # Calculator widget (only for calculator pages)
    calc_widget = calculator_module(calc_type) if calc_type else ""

    # Content sections (body is raw HTML — do NOT escape)
    section_blocks = []
    for sec in cfg["sections"]:
        section_blocks.append(trim(
            f"""
            <section class="ccg-section">
              <div class="ccg-section-head">
                <p class="ccg-kicker">{html.escape(sec["kicker"])}</p>
                <h2>{html.escape(sec["h2"])}</h2>
              </div>
              {sec["body"]}
            </section>
            """
        ))

    faqs_list: List[List[str]] = cfg["faqs"]
    faq_section = faq_html(faqs_list)

    # Sources block keyed by the page's pillar topic. Custom keys can be
    # specified via cfg["sources_topic"]; otherwise we infer from the slug.
    topic_key = cfg.get("sources_topic") or _infer_sources_topic(path)
    sources_section = sources_block(topic_key)

    content = (
        intro_section
        + calc_widget
        + "".join(section_blocks)
        + faq_section
        + sources_section
        + author_box()
        + related_html(related_paths)
    )
    return content, faqs_list


def _infer_sources_topic(path: str) -> str:
    """Map a page path to a key in SOURCES_BY_TOPIC."""
    slug = Path(path).stem
    rules = [
        ("personal-loan", "personal-loans"),
        ("credit-card", "credit-cards"),
        ("mortgage", "mortgage"),
        ("credit-score", "credit-score"),
        ("banking-fees", "banking-fees"),
        ("debt-payoff", "debt-payoff"),
        ("debt-snowball", "debt-payoff"),
        ("debt-consolidation", "debt-payoff"),
        ("refinanc", "refinancing"),
        ("student-loan", "student-loans"),
        ("loan-payment", "personal-loans"),
        ("balance-transfer", "credit-cards"),
        ("utilization", "credit-cards"),
        ("savings-account", "banking-fees"),
        ("checking", "banking-fees"),
        ("best-banks", "banking-fees"),
    ]
    for needle, key in rules:
        if needle in slug:
            return key
    return "default"


def simple_page_body(title: str, desc: str, related_paths: List[str], legal: bool = False) -> Tuple[str, List[List[str]]]:
    """Generic short body for root-level pages that do NOT have a custom
    body builder. The 'legal' flag is preserved for backwards compatibility
    but actual legal pages (privacy, terms, disclaimer) now use legal_body()
    so they get proper, non-templated copy."""
    faqs = [
        ["Is this page financial advice?", NON_ADVICE_DISCLAIMER],
        ["How can I reach the editor?", f"Email {CONTACT_EMAIL} for editorial questions, corrections, or partnership inquiries."],
        ["When was this page last reviewed?", f"{LAST_REVIEWED}. Editorial and policy pages are revisited when site practices, contact information, or legal language change."],
    ]
    intro = trim(
        f"""
        <section class="ccg-section">
          <div class="ccg-section-head">
            <p class="ccg-kicker">{'Policy' if legal else 'Institutional'}</p>
            <h2>{html.escape(title)}</h2>
          </div>
          <p>{html.escape(desc)}</p>
        </section>
        """
    )
    body = intro + faq_html(faqs) + author_box() + related_html(related_paths)
    return body, faqs


def contact_page_body(related_paths: List[str]) -> Tuple[str, List[List[str]]]:
    """Slim, focused contact page. No templated finance paragraphs, no form
    that pretends to do anything. Just clear contact info and the limits of
    what we can help with."""
    faqs = [
        ["Can the editor recommend a specific lender or product?", "No. CreditCostGuide is an educational resource. We do not match readers with lenders and do not recommend specific products to individuals."],
        ["Can the editor review my credit file or loan offer?", "No. We cannot review personal credit files or specific loan offers. For that kind of review, contact a HUD-certified housing counselor or a CFPB-listed nonprofit credit counselor."],
        ["What is a reasonable response time?", "We aim to acknowledge editorial questions and corrections within five business days. Partnership inquiries may take longer."],
    ]
    body = trim(
        f"""
        <section class="ccg-section">
          <div class="ccg-section-head">
            <p class="ccg-kicker">Contact</p>
            <h2>Contact CreditCostGuide</h2>
          </div>
          <p>For corrections, source updates, editorial questions, or partnership inquiries, email <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a>.</p>
        </section>
        <section class="ccg-section ccg-section--soft">
          <div class="ccg-section-head">
            <p class="ccg-kicker">What we cannot do</p>
            <h2>Limits of this site</h2>
          </div>
          <ul>
            <li>We cannot provide personal financial advice.</li>
            <li>We cannot review personal credit files, loan offers, or tax situations.</li>
            <li>We cannot recommend specific lenders, banks, or financial products to individual readers.</li>
            <li>For urgent financial, legal, or tax decisions, contact a qualified licensed professional.</li>
          </ul>
          <p><strong>{NON_ADVICE_DISCLAIMER}</strong></p>
        </section>
        {faq_html(faqs)}
        {author_box()}
        {related_html(related_paths)}
        """
    )
    return body, faqs


def author_page_body(related_paths: List[str]) -> Tuple[str, List[List[str]]]:
    """Dedicated author profile at /authors/javi-perez/. Honest bio, no fake
    credentials, links to LinkedIn, and a Person schema is added in
    build_jsonld() via the editor node already used site-wide."""
    faqs = [
        ["What does Javi do at CreditCostGuide?",
         f"{EDITOR_NAME} is the founder and sole editor of CreditCostGuide. He plans the editorial calendar, writes and revises every guide, builds the calculators, and is the single contact for corrections at {CONTACT_EMAIL}."],
        ["Is Javi a licensed financial professional?",
         NON_ADVICE_DISCLAIMER],
        ["How is this content produced?",
         AI_DISCLOSURE + " The final wording, examples, sources, and figures shown on the site are reviewed by Javi before publication."],
    ]
    body = trim(
        f"""
        <section class="ccg-section">
          <div class="ccg-section-head">
            <p class="ccg-kicker">Author Profile</p>
            <h2>About {EDITOR_NAME}</h2>
          </div>
          <p>{EDITOR_NAME} is the founder and sole editor of CreditCostGuide. He is an independent publisher based in {EDITOR_LOCATION} who builds long-form educational resources for U.S. consumers on credit, loans, mortgages, banking fees, refinancing, and debt payoff.</p>
          <p>His background is technical — operating digital products and editorial sites — not regulated financial services. <strong>{NON_ADVICE_DISCLAIMER}</strong></p>
          <p>Find Javi on LinkedIn: <a href="{EDITOR_LINKEDIN}" target="_blank" rel="noopener noreferrer">{EDITOR_LINKEDIN}</a>. For corrections, source updates, or partnership inquiries, email <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a>.</p>
        </section>
        <section class="ccg-section ccg-section--soft">
          <div class="ccg-section-head">
            <p class="ccg-kicker">Editorial Approach</p>
            <h2>How Javi works</h2>
          </div>
          <ul>
            <li><strong>Primary-source first.</strong> Every page links to at least three regulator or government sources (CFPB, Federal Reserve, FDIC, BLS, FTC, SEC, studentaid.gov).</li>
            <li><strong>AI-assisted drafting, human review.</strong> Drafts are produced with large-language-model help, then revised, fact-checked, and signed off by Javi before publishing.</li>
            <li><strong>Quarterly review.</strong> Every indexable guide is revisited at least every 90 days; rate-sensitive numbers are checked monthly against the original federal data series.</li>
            <li><strong>No personalized advice.</strong> CreditCostGuide does not collect reader data, does not match readers with lenders, and is not a registered investment adviser.</li>
          </ul>
        </section>
        {faq_html(faqs)}
        {author_box()}
        {related_html(related_paths)}
        """
    )
    return body, faqs


def legal_body(kind: str, related_paths: List[str]) -> Tuple[str, List[List[str]]]:
    """Proper original copy for the three legal pages. Each is concise,
    accurate for a small static publisher running display ads and a couple of
    affiliate links, and free of placeholder text."""
    if kind == "privacy":
        faqs = [
            ["Does this site collect personal data?", "CreditCostGuide does not run analytics on its own infrastructure. Third-party services (Google AdSense for advertising) may set cookies and process limited data; details are below."],
            ["Can readers opt out of advertising cookies?", "Yes. Google offers ad personalization controls at adssettings.google.com, and EU/UK readers see a consent prompt at first visit."],
            ["How can a reader request data deletion?", f"Email {CONTACT_EMAIL}. Because the site does not have user accounts, deletion requests typically concern any prior email correspondence."],
        ]
        body = trim(
            f"""
            <section class="ccg-section">
              <div class="ccg-section-head">
                <p class="ccg-kicker">Policy</p>
                <h2>Privacy Policy</h2>
              </div>
              <p>This policy explains what information CreditCostGuide (the &ldquo;Site&rdquo;) collects, how it is used, and the choices readers have. It applies to the website at <a href="{DOMAIN}/">creditcostguide.com</a>. Last reviewed: {LAST_REVIEWED}.</p>
            </section>
            <section class="ccg-section">
              <div class="ccg-section-head"><p class="ccg-kicker">1</p><h2>Information we do not collect</h2></div>
              <p>The Site does not have user accounts, newsletters, or login features. It does not run first-party analytics. We do not collect names, addresses, payment information, credit reports, or any other personal financial data through ordinary browsing.</p>
            </section>
            <section class="ccg-section">
              <div class="ccg-section-head"><p class="ccg-kicker">2</p><h2>Third-party services</h2></div>
              <p><strong>Advertising.</strong> The Site displays ads through Google AdSense. Google may use cookies (including the DoubleClick DART cookie) and similar technologies to serve ads based on visit history and to measure performance. See Google&rsquo;s <a href="https://policies.google.com/technologies/ads" target="_blank" rel="noopener noreferrer">Advertising policies</a> and <a href="https://policies.google.com/privacy" target="_blank" rel="noopener noreferrer">Privacy Policy</a>.</p>
              <p><strong>Affiliate links.</strong> Some pages contain affiliate links, including SmartCredit (via CJ Affiliate). When a reader clicks an affiliate link, the affiliate network may set a cookie used to attribute a later sign-up or purchase to CreditCostGuide. CreditCostGuide does not see the reader&rsquo;s identity through this process; only aggregate conversion reporting is provided to us.</p>
              <p><strong>Hosting.</strong> The Site is hosted on Cloudflare Pages. Cloudflare may process IP addresses and basic request metadata as part of normal CDN and security operations. See <a href="https://www.cloudflare.com/privacypolicy/" target="_blank" rel="noopener noreferrer">Cloudflare&rsquo;s Privacy Policy</a>.</p>
            </section>
            <section class="ccg-section">
              <div class="ccg-section-head"><p class="ccg-kicker">3</p><h2>Cookies and consent</h2></div>
              <p>A small cookie banner offers an Accept / Reject choice for non-essential cookies. The reader&rsquo;s choice is stored in browser localStorage under <code>ccg-cookie-choice</code>. Rejecting non-essential cookies signals to advertising scripts that personalized advertising should not be used in regions where that signal is honored.</p>
              <p>Readers can also clear advertising cookies through their browser settings or Google&rsquo;s <a href="https://adssettings.google.com/" target="_blank" rel="noopener noreferrer">Ad Settings</a> page.</p>
            </section>
            <section class="ccg-section">
              <div class="ccg-section-head"><p class="ccg-kicker">4</p><h2>Email correspondence</h2></div>
              <p>If a reader emails <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a>, the address and message are visible to the editor and stored in the email provider&rsquo;s standard inbox infrastructure. Correspondence is used only to respond and is not sold, rented, or shared with third parties.</p>
            </section>
            <section class="ccg-section">
              <div class="ccg-section-head"><p class="ccg-kicker">5</p><h2>Children</h2></div>
              <p>The Site is not directed to children under 13. We do not knowingly collect information from children.</p>
            </section>
            <section class="ccg-section">
              <div class="ccg-section-head"><p class="ccg-kicker">6</p><h2>Changes to this policy</h2></div>
              <p>Material changes will be reflected by updating the Last reviewed date and, where appropriate, a brief change note in the editor byline.</p>
            </section>
            {faq_html(faqs)}
            {author_box()}
            {related_html(related_paths)}
            """
        )
    elif kind == "terms":
        faqs = [
            ["Can I republish content from CreditCostGuide?", "Short quotes with a link back are welcome. For full reuse, email " + CONTACT_EMAIL + " for permission."],
            ["Are the calculators warranted to be accurate?", "Calculators use standard amortization formulas and are accurate for the inputs given, but real-world quotes depend on lender pricing, taxes, insurance, and credit. Always confirm with the lender or bank."],
            ["What happens if I rely on this content?", NON_ADVICE_DISCLAIMER],
        ]
        body = trim(
            f"""
            <section class="ccg-section">
              <div class="ccg-section-head"><p class="ccg-kicker">Policy</p><h2>Terms of Use</h2></div>
              <p>These terms govern use of CreditCostGuide. By using the Site, the reader agrees to the terms below. Last reviewed: {LAST_REVIEWED}.</p>
            </section>
            <section class="ccg-section">
              <div class="ccg-section-head"><p class="ccg-kicker">1</p><h2>Educational purpose</h2></div>
              <p>All content is published for general educational purposes. {NON_ADVICE_DISCLAIMER}</p>
            </section>
            <section class="ccg-section">
              <div class="ccg-section-head"><p class="ccg-kicker">2</p><h2>Accuracy and freshness</h2></div>
              <p>Rates, fees, and product details change. CreditCostGuide reviews every indexable page at least quarterly and updates rate-sensitive numbers when the underlying federal data series publishes new figures, but the Site cannot guarantee that any specific number is current at the moment of reading. Always confirm pricing and terms directly with the lender or bank.</p>
            </section>
            <section class="ccg-section">
              <div class="ccg-section-head"><p class="ccg-kicker">3</p><h2>Calculators</h2></div>
              <p>Calculators use standard, publicly documented formulas (loan amortization, month-by-month payoff simulation, utilization ratio). They are tools for testing scenarios, not lending or banking applications. They do not transmit input data to any server; calculation runs entirely in the reader&rsquo;s browser.</p>
            </section>
            <section class="ccg-section">
              <div class="ccg-section-head"><p class="ccg-kicker">4</p><h2>Affiliate links and advertising</h2></div>
              <p>Some pages contain affiliate links (currently SmartCredit via CJ Affiliate), marked <code>rel=&quot;nofollow sponsored&quot;</code> and disclosed where they appear. CreditCostGuide may earn a commission when a reader signs up through an affiliate link, at no additional cost to the reader. Affiliate partnerships do not influence editorial recommendations. The Site also displays ads through Google AdSense.</p>
            </section>
            <section class="ccg-section">
              <div class="ccg-section-head"><p class="ccg-kicker">5</p><h2>Limitation of liability</h2></div>
              <p>To the maximum extent permitted by law, CreditCostGuide and its editor are not liable for any loss, damages, or claim arising from use of the Site or reliance on its content. The Site is provided &ldquo;as is&rdquo;.</p>
            </section>
            <section class="ccg-section">
              <div class="ccg-section-head"><p class="ccg-kicker">6</p><h2>Contact</h2></div>
              <p>For corrections, source updates, or permission requests, email <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a>.</p>
            </section>
            {faq_html(faqs)}
            {author_box()}
            {related_html(related_paths)}
            """
        )
    else:  # disclaimer
        faqs = [
            ["Does CreditCostGuide give financial advice?", NON_ADVICE_DISCLAIMER],
            ["Are the examples real customer data?", "No. Numeric examples on this site are hypothetical scenarios used to illustrate how a cost mechanic works. They are not based on individual reader data, lender quotes, or any real consumer&rsquo;s file."],
            ["Where should I go for personalized advice?", "Consult a licensed professional: a financial advisor (registered with the SEC or a state regulator), a CPA, an attorney, a HUD-certified housing counselor, or a CFPB-listed nonprofit credit counselor."],
        ]
        body = trim(
            f"""
            <section class="ccg-section">
              <div class="ccg-section-head"><p class="ccg-kicker">Policy</p><h2>Disclaimer</h2></div>
              <p>Last reviewed: {LAST_REVIEWED}.</p>
            </section>
            <section class="ccg-section">
              <div class="ccg-section-head"><p class="ccg-kicker">Educational only</p><h2>This site does not provide financial advice</h2></div>
              <p>{NON_ADVICE_DISCLAIMER} Use the content as a starting point for your own research, then verify pricing and product terms directly with the lender, bank, or licensed professional relevant to your situation.</p>
            </section>
            <section class="ccg-section">
              <div class="ccg-section-head"><p class="ccg-kicker">Examples</p><h2>Hypothetical scenarios, not real customer data</h2></div>
              <p>The numeric examples used in calculators and guides — APRs, balances, monthly payments — are hypothetical illustrations chosen to make a cost mechanic easy to follow. They are not lender quotes and not based on any individual reader&rsquo;s credit profile. Real product pricing depends on your credit, income, debt-to-income ratio, collateral (if any), and the lender&rsquo;s underwriting at the moment you apply.</p>
            </section>
            <section class="ccg-section">
              <div class="ccg-section-head"><p class="ccg-kicker">Sources</p><h2>Reliance on public data</h2></div>
              <p>CreditCostGuide relies on public sources including CFPB (consumerfinance.gov), the Federal Reserve (federalreserve.gov, FRED), FDIC (fdic.gov), BLS (bls.gov), FTC (consumer.ftc.gov), the SEC (sec.gov), and the U.S. Department of Education (studentaid.gov). Sources are linked on each page where they are used.</p>
            </section>
            <section class="ccg-section">
              <div class="ccg-section-head"><p class="ccg-kicker">Advertising and affiliates</p><h2>How the site is funded</h2></div>
              <p>The Site is funded by display advertising (Google AdSense) and a small number of affiliate partnerships (currently SmartCredit via CJ Affiliate). Affiliate links are marked <code>rel=&quot;nofollow sponsored&quot;</code> and disclosed on the pages where they appear. Funding does not influence which products are mentioned, the order in which they appear, or the editorial conclusions reached.</p>
            </section>
            <section class="ccg-section">
              <div class="ccg-section-head"><p class="ccg-kicker">Where to get personalized help</p><h2>Licensed professionals and free resources</h2></div>
              <p>For decisions specific to your situation, consult a licensed professional. Free or low-cost options include <a href="https://www.consumerfinance.gov/find-a-housing-counselor/" target="_blank" rel="noopener noreferrer">HUD-certified housing counselors</a>, CFPB-listed <a href="https://www.consumerfinance.gov/ask-cfpb/what-is-credit-counseling-en-1451/" target="_blank" rel="noopener noreferrer">nonprofit credit counselors</a>, and your state&rsquo;s attorney general consumer protection unit.</p>
            </section>
            {faq_html(faqs)}
            {author_box()}
            {related_html(related_paths)}
            """
        )
    return body, faqs


def about_body(related_paths: List[str]) -> Tuple[str, List[List[str]]]:
    faqs = [
        ["Who runs CreditCostGuide?",
         f"{EDITOR_NAME}, a technology professional and editorial site builder based in {EDITOR_LOCATION}, runs the site as an independent education project. Javi is not a licensed financial advisor, CPA, CFP, or loan officer."],
        ["Does CreditCostGuide give financial advice?",
         "No. The content is educational. It explains how borrowing costs, fees, and credit scoring work, using public data from CFPB, the Federal Reserve, FDIC, BLS, and SEC. Always consult a licensed professional for decisions about your situation."],
        ["How can I reach the editor?",
         f"Email {CONTACT_EMAIL} for editorial questions, corrections, or partnership inquiries. The site does not collect reader data through the contact form in this static demo build."],
    ]
    body = trim(
        f"""
        <section class="ccg-section">
          <div class="ccg-section-head">
            <p class="ccg-kicker">About</p>
            <h2>Who runs this site</h2>
          </div>
          <p>CreditCostGuide was created by <strong>{EDITOR_NAME}</strong>, a technology professional and editorial site builder based in {EDITOR_LOCATION}. Javi builds independent financial-education sites that help U.S. consumers compare borrowing costs using verified public data — not affiliate-driven product recommendations.</p>
          <p><strong>Important disclaimer:</strong> {EDITOR_NAME} is <em>not</em> a licensed financial advisor, CPA, CFP, or loan officer. Nothing on this site constitutes financial, legal, or tax advice. Consult a licensed professional for guidance specific to your situation.</p>
          <p>Connect with the editor: <a href="{EDITOR_LINKEDIN}" target="_blank" rel="noopener noreferrer">{EDITOR_LINKEDIN}</a></p>
        </section>
        <section class="ccg-section ccg-section--soft">
          <div class="ccg-section-head">
            <p class="ccg-kicker">Coverage</p>
            <h2>What this site covers</h2>
          </div>
          <p>CreditCostGuide is organized around the major U.S. consumer-finance cost categories, each anchored by a long-form pillar guide and supported by calculators and explainer articles:</p>
          <ul>
            <li><strong>Personal loans</strong> — APRs, origination fees, prepayment, debt consolidation.</li>
            <li><strong>Credit cards</strong> — interest charges, annual fees, rewards math, balance transfers.</li>
            <li><strong>Mortgages</strong> — rates, points, PMI, escrow, closing costs, affordability rules.</li>
            <li><strong>Credit scores</strong> — how scores are calculated, how they translate to rates.</li>
            <li><strong>Banking fees</strong> — overdrafts, ATM, wires, minimums, no-fee alternatives.</li>
            <li><strong>Debt payoff</strong> — avalanche vs. snowball, cash-flow planning, consolidation.</li>
            <li><strong>Refinancing</strong> — break-even math for mortgages, autos, personal, and student loans.</li>
            <li><strong>Student loans</strong> — federal vs. private, refinancing, repayment plans.</li>
          </ul>
          <p>Five interactive calculators (loan payment, credit-card interest, mortgage, debt payoff, credit utilization) sit alongside the guides for quick scenario testing. All calculator math is implemented in plain JavaScript using standard amortization formulas readers can verify against any public source.</p>
        </section>
        <section class="ccg-section">
          <div class="ccg-section-head">
            <p class="ccg-kicker">Method</p>
            <h2>How we research</h2>
          </div>
          <p>The sourcing hierarchy on this site is deliberate, in order of precedence:</p>
          <ol>
            <li><strong>CFPB</strong> (Consumer Financial Protection Bureau) — complaint data, consumer protections, regulatory disclosures.</li>
            <li><strong>Federal Reserve</strong> — interest rates, consumer surveys, household debt and credit reports.</li>
            <li><strong>FDIC</strong> — national bank rate tables, deposit data, insurance limits.</li>
            <li><strong>BLS</strong> (Bureau of Labor Statistics) — inflation, CPI, wage data context.</li>
            <li><strong>SEC</strong> — investment-product disclosures and filings where relevant.</li>
            <li>Industry reports cited explicitly when used (e.g., Experian, FICO, NerdWallet rate tables) and never as primary sources for regulated products.</li>
          </ol>
          <p>Pages are reviewed quarterly. The "Last reviewed" date in each editor byline reflects the most recent verification pass. When a reader emails a correction, the page is updated and the dateModified field in its Article schema is bumped immediately. See <a href="{DOMAIN}/how-we-research">our editorial methodology</a> for the full process.</p>
        </section>
        <section class="ccg-section ccg-section--soft">
          <div class="ccg-section-head">
            <p class="ccg-kicker">AI Disclosure</p>
            <h2>How content is produced</h2>
          </div>
          <p><strong>{AI_DISCLOSURE}</strong> Specifically: drafts are produced with large-language-model assistance using publicly documented prompts, then revised, fact-checked against the linked sources, and edited by Javi before publishing. AI is not used to generate fake statistics, fake quotes, or fake personal experiences. Every numeric example is either calculated from a public formula or attributed to a regulator or industry publication.</p>
        </section>
        <section class="ccg-section">
          <div class="ccg-section-head">
            <p class="ccg-kicker">Independence</p>
            <h2>Editorial independence and disclosure</h2>
          </div>
          <p>CreditCostGuide is reader-supported via display advertising (Google AdSense) and a small number of affiliate partnerships, including SmartCredit (CJ Affiliate), which is disclosed on every page where it appears. Affiliate links are marked <code>rel="nofollow sponsored"</code> and never override editorial recommendations. We do not accept payment for placement in core guides, and we publish corrections promptly.</p>
        </section>
        <section class="ccg-section ccg-section--soft">
          <div class="ccg-section-head">
            <p class="ccg-kicker">Contact</p>
            <h2>Contact the editor</h2>
          </div>
          <p>For editorial questions, corrections, or partnership inquiries, email <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a>.</p>
        </section>
        {faq_html(faqs)}
        {author_box()}
        {related_html(related_paths)}
        """
    )
    return body, faqs


def how_we_research_body(related_paths: List[str]) -> Tuple[str, List[List[str]]]:
    faqs = [
        ["What primary sources does CreditCostGuide use?",
         "CFPB for consumer protections and complaint data, the Federal Reserve for rates and consumer surveys, FDIC for bank rate tables, BLS for inflation context, and SEC for investment-related disclosures. Industry reports are cited when used and never substituted for primary public data."],
        ["How often is content updated?",
         "Pages are reviewed at least quarterly. Pages with rate-sensitive numbers (mortgage averages, credit card APR averages, savings APYs) are reviewed when the underlying data sources publish updates — usually monthly for Fed series and quarterly for FDIC."],
        ["What is the correction policy?",
         f"Email {CONTACT_EMAIL} with the URL, the specific paragraph, and the issue. Verified corrections are applied within five business days, the editor byline is updated, and the page's dateModified field is refreshed."],
    ]
    body = trim(
        f"""
        <section class="ccg-section">
          <div class="ccg-section-head">
            <p class="ccg-kicker">Methodology</p>
            <h2>How CreditCostGuide researches financial costs</h2>
          </div>
          <p>This page documents the editorial process behind every guide and calculator. The goal is reproducibility: a reader who follows our citations should be able to land on the same primary data we used and see exactly where any numeric claim originated.</p>
        </section>
        <section class="ccg-section ccg-section--soft">
          <div class="ccg-section-head">
            <p class="ccg-kicker">Sourcing Hierarchy</p>
            <h2>Public-data sources, in order of precedence</h2>
          </div>
          <ol>
            <li><strong>Consumer Financial Protection Bureau (CFPB)</strong> — primary source for consumer protection rules, complaint data, and regulated-product disclosure standards. Used for credit cards, mortgages, debt collection, overdraft practices, and student-loan servicing.</li>
            <li><strong>Federal Reserve (Board and FRED)</strong> — primary source for interest-rate context (effective federal funds rate, prime rate), the Survey of Consumer Finances, and the Quarterly Report on Household Debt and Credit. Series IDs are cited inline where used.</li>
            <li><strong>FDIC</strong> — bank-rate tables (national rate caps, weekly average APYs), deposit data, insurance limits. Used for checking, savings, MMA, and CD comparisons.</li>
            <li><strong>Bureau of Labor Statistics (BLS)</strong> — Consumer Price Index for All Urban Consumers (CPI-U) and household expenditure data. Used for real-rate context and affordability framing.</li>
            <li><strong>Securities and Exchange Commission (SEC)</strong> — investment-product disclosures and registered offerings, where they intersect with consumer borrowing decisions.</li>
            <li><strong>Industry data</strong> (Experian, FICO, NerdWallet rate trackers, LendingTree surveys) — cited explicitly when used and treated as supplemental, never as substitutes for the regulators above.</li>
          </ol>
        </section>
        <section class="ccg-section">
          <div class="ccg-section-head">
            <p class="ccg-kicker">Update Cycle</p>
            <h2>Review and update frequency</h2>
          </div>
          <p>Every guide receives a full editorial review at least every 90 days. Pages with rate-sensitive numbers are revisited when the source publishes new data:</p>
          <ul>
            <li><strong>Federal Reserve series</strong> (effective federal funds rate, mortgage rate averages) — checked monthly.</li>
            <li><strong>FDIC national rates</strong> — checked when FDIC publishes the weekly update relevant to a deposit-product page.</li>
            <li><strong>BLS CPI</strong> — referenced on inflation-context pages monthly when the new release lands.</li>
            <li><strong>Regulatory changes</strong> (CFPB rulemakings, Fed policy actions) — applied within five business days of publication when material to a page.</li>
          </ul>
          <p>The "Last reviewed" date in each page's editor byline is the date of the most recent verification pass, not the original publication date.</p>
        </section>
        <section class="ccg-section">
          <div class="ccg-section-head">
            <p class="ccg-kicker">AI Disclosure</p>
            <h2>AI-assisted drafting and human review</h2>
          </div>
          <p>{AI_DISCLOSURE}</p>
          <p>What that means concretely: long-form sections are drafted with large-language-model assistance, then edited by {EDITOR_NAME}. Specific numeric claims — interest rates, fee ranges, regulatory limits — are checked against the primary source linked in the page&rsquo;s Sources block before publishing. AI is not used to invent statistics, attribute quotes to people, or describe personal experiences the editor does not have. Calculators use closed-form mathematical formulas (amortization, balance simulation) and do not depend on AI at runtime.</p>
          <p><strong>{NON_ADVICE_DISCLAIMER}</strong></p>
        </section>
        <section class="ccg-section ccg-section--soft">
          <div class="ccg-section-head">
            <p class="ccg-kicker">Calculators</p>
            <h2>Calculator methodology</h2>
          </div>
          <p>All calculators on the site use standard, publicly documented formulas:</p>
          <ul>
            <li><strong>Loan payment</strong> — fixed-rate amortization formula <code>P · r / (1 − (1+r)<sup>−n</sup>)</code>, where r is the periodic rate and n the number of periods.</li>
            <li><strong>Credit card payoff</strong> — month-by-month simulation: monthly interest = balance × (APR / 12); balance reduces by (payment − interest + new charges) each month until paid.</li>
            <li><strong>Mortgage</strong> — same amortization formula plus a monthly add-on for property tax, homeowners insurance, and PMI.</li>
            <li><strong>Debt payoff</strong> — compares months and total interest at the minimum payment versus a planned payment, both via month-by-month simulation.</li>
            <li><strong>Credit utilization</strong> — total balances ÷ total limits, plus per-card utilization for context.</li>
          </ul>
          <p>The implementation lives in <code>main.js</code> on the public site and uses no external libraries. Readers can verify the math against any public amortization reference.</p>
        </section>
        <section class="ccg-section">
          <div class="ccg-section-head">
            <p class="ccg-kicker">Corrections</p>
            <h2>Correction and feedback policy</h2>
          </div>
          <p>If you spot an error — a stale rate, a misquoted statistic, an outdated regulation — email <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a> with the page URL and the paragraph in question. Verified corrections are applied within five business days. We update the page's dateModified field and the editor byline so readers can see the change history at a glance.</p>
          <p>We do not silently rewrite published numbers. When a number changes for a real-world reason (e.g., a Fed rate change), the page reflects the new value and the dateModified bumps; when a number changes because it was wrong, the correction is noted in the editor byline note for that update cycle.</p>
        </section>
        <section class="ccg-section ccg-section--soft">
          <div class="ccg-section-head">
            <p class="ccg-kicker">Independence</p>
            <h2>Editorial independence disclosure</h2>
          </div>
          <p>CreditCostGuide earns revenue from display advertising (Google AdSense) and from a limited set of affiliate partnerships (currently SmartCredit via CJ Affiliate). Affiliate links are marked <code>rel="nofollow sponsored"</code>, opened in a new tab, and disclosed on every page where they appear. We do not allow advertisers or affiliates to influence the recommendations, ordering, or editorial language inside our pillar guides. If a partnership ever conflicts with editorial neutrality, the partnership is dropped, not the editorial position.</p>
          <p>The site is not a registered investment adviser. Nothing here is a recommendation to buy or sell any specific financial product. Readers should consult a licensed professional before acting on educational material.</p>
        </section>
        {faq_html(faqs)}
        {author_box()}
        {related_html(related_paths)}
        """
    )
    return body, faqs


def home_body() -> str:
    # Pillars: every pillar is in INDEXABLE_PAGES by design, so we can link to all.
    pillar_cards = "".join(
        f'<a class="ccg-topic-card" href="{local_href(item["path"])}"><span>{html.escape(item["hero"])}</span><strong>{html.escape(title_from_path(item["path"]))}</strong><p>{html.escape(item["description"])}</p></a>'
        for item in PILLARS
    )
    # Calculators: every calculator is in INDEXABLE_PAGES.
    calc_cards = "".join(
        f'<a class="ccg-topic-card ccg-topic-card--small" href="{local_href(path)}"><span>Calculator</span><strong>{html.escape(title_from_path(path))}</strong><p>{html.escape(desc)}</p></a>'
        for path, _, desc, _ in CALCULATORS
    )
    # "Popular reads" must only spotlight indexable supporting articles; we do
    # not want the home page to surface noindex URLs as featured content.
    indexable_supporting = [
        (path, title, desc)
        for path, title, desc in SUPPORTING
        if is_indexable(path)
    ]
    spotlight = "".join(
        f'<a class="ccg-spotlight-item" href="{local_href(path)}">{html.escape(title)}</a>'
        for path, title, _ in indexable_supporting[:6]
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
        {editorial_trust_block()}
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
            <p class="ccg-kicker">Featured Reads</p>
            <h2>Specific guides on APR, payoff methods, and credit scoring</h2>
          </div>
          <div class="ccg-spotlight-list">{spotlight}</div>
          <p style="margin-top:1rem;"><a href="{DOMAIN}/authors/javi-perez">Meet the editor →</a></p>
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
    active_public = public_path(active_path)
    nav = "".join(
        f'<a class="{"is-active" if item[0] == active_public else ""}" href="{html.escape(f"{DOMAIN}{item[0]}" if item[0] != "/" else f"{DOMAIN}/")}">{html.escape(item[1])}</a>'
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


def contact_email_html() -> str:
    if CONTACT_EMAIL:
        return trim(
            f"""
            <section class="ccg-section">
              <div class="ccg-section-head">
                <p class="ccg-kicker">Contact Details</p>
                <h2>Contact information</h2>
              </div>
              <p>For editorial questions, corrections, or general feedback, email us at <a href="mailto:{html.escape(CONTACT_EMAIL)}">{html.escape(CONTACT_EMAIL)}</a>.</p>
            </section>
            """
        )
    return trim(
        """
        <section class="ccg-section">
          <div class="ccg-section-head">
            <p class="ccg-kicker">Contact Details</p>
            <h2>Contact information</h2>
          </div>
          <p>We are updating our contact information. Please check back soon.</p>
        </section>
        """
    )


def build_jsonld(
    path: str,
    title: str,
    description: str,
    page_type: str,
    breadcrumbs: List[Dict[str, str]],
    faqs: List[List[str]] | None,
) -> str:
    canonical = url_for(path)
    graph: List[Dict[str, object]] = []

    publisher = {
        "@type": "Organization",
        "@id": f"{DOMAIN}/#organization",
        "name": SITE_NAME,
        "url": DOMAIN,
        "logo": {"@type": "ImageObject", "url": f"{DOMAIN}/assets/icons/logo.svg"},
        "email": CONTACT_EMAIL,
        "sameAs": [EDITOR_LINKEDIN],
    }
    graph.append(publisher)

    graph.append({
        "@type": "WebSite",
        "@id": f"{DOMAIN}/#website",
        "name": SITE_NAME,
        "url": DOMAIN,
        "publisher": {"@id": f"{DOMAIN}/#organization"},
        "inLanguage": "en-US",
    })

    editor = {
        "@type": "Person",
        "@id": f"{DOMAIN}/#editor",
        "name": EDITOR_NAME,
        "jobTitle": EDITOR_ROLE,
        "url": EDITOR_LINKEDIN,
        "sameAs": [EDITOR_LINKEDIN],
    }
    graph.append(editor)

    graph.append({
        "@type": "WebPage" if page_type != "home" else "WebSite",
        "@id": f"{canonical}#page",
        "name": title,
        "url": canonical,
        "description": description,
        "isPartOf": {"@id": f"{DOMAIN}/#website"},
        "dateModified": f"{LAST_REVIEWED_ISO}T00:00:00+00:00",
    })

    if breadcrumbs and len(breadcrumbs) > 1:
        graph.append({
            "@type": "BreadcrumbList",
            "@id": f"{canonical}#breadcrumbs",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": idx + 1,
                    "name": item["name"],
                    "item": item["url"],
                }
                for idx, item in enumerate(breadcrumbs)
            ],
        })

    if page_type == "calculator":
        graph.append({
            "@type": "SoftwareApplication",
            "@id": f"{canonical}#calculator",
            "name": title,
            "applicationCategory": "FinanceApplication",
            "operatingSystem": "Web",
            "url": canonical,
            "description": description,
            "publisher": {"@id": f"{DOMAIN}/#organization"},
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
        })
    elif page_type != "home":
        graph.append({
            "@type": "Article",
            "@id": f"{canonical}#article",
            "headline": title,
            "description": description,
            "url": canonical,
            "mainEntityOfPage": canonical,
            "publisher": {"@id": f"{DOMAIN}/#organization"},
            "editor": {"@id": f"{DOMAIN}/#editor"},
            "dateModified": f"{LAST_REVIEWED_ISO}T00:00:00+00:00",
            "image": f"{DOMAIN}/assets/images/social-preview.svg",
            "inLanguage": "en-US",
        })

    if faqs:
        graph.append({
            "@type": "FAQPage",
            "@id": f"{canonical}#faq",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": q,
                    "acceptedAnswer": {"@type": "Answer", "text": a},
                }
                for q, a in faqs
            ],
        })

    payload = {"@context": "https://schema.org", "@graph": graph}
    return json.dumps(payload, ensure_ascii=False)


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
    is_404: bool = False,
    extra_scripts: List[str] | None = None,
) -> str:
    canonical = url_for(path)
    indexable = is_indexable(path) and not is_404
    if is_404:
        robots = "noindex,nofollow"
    elif not indexable:
        # Non-indexable pages stay reachable for users but are hidden from Google
        # during AdSense review. Internal links still pass link equity (follow).
        robots = "noindex,follow"
    else:
        robots = "index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1"
    hero_title = hero_title or title
    hero_summary = hero_summary or description
    breadcrumb_nav = "" if path == "index.html" or is_404 else breadcrumb_html(breadcrumbs)
    adsense = "" if is_404 else ADSENSE_SCRIPT
    # Only indexable pages get schema. Non-indexable pages skip JSON-LD so Google
    # has nothing to lift from them when scaling content review heuristics fire.
    jsonld_block = "" if (is_404 or not indexable) else f'<script type="application/ld+json">{build_jsonld(path, title, description, page_type, breadcrumbs, faqs)}</script>'
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
          <meta property="og:locale" content="en_US">
          <meta name="twitter:card" content="summary_large_image">
          <meta name="twitter:title" content="{html.escape(title)}">
          <meta name="twitter:description" content="{html.escape(description)}">
          <meta name="twitter:image" content="{DOMAIN}/assets/images/social-preview.svg">
          {adsense}
          <link rel="icon" href="{DOMAIN}/assets/icons/favicon.svg" type="image/svg+xml">
          <link rel="stylesheet" href="{DOMAIN}/styles.css">
          {jsonld_block}
        </head>
        <body data-page-type="{html.escape(page_type)}" data-page-path="{html.escape(public_path(path))}">
          {header(path)}
          <main class="ccg-shell">
            {breadcrumb_nav}
            {hero}
            {main_content}
          </main>
          {footer()}
          <div class="ccg-cookie-banner" style="display:none">
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
          {''.join(extra_scripts or [])}
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

        .editorial-block {
          margin-top: 1.4rem;
          padding: 1.3rem;
          border: 1px solid var(--ccg-line);
          border-radius: 22px;
          background: #fbfdff;
          box-shadow: var(--ccg-shadow);
        }
        .editorial-block strong {
          display: block;
          margin-bottom: 0.65rem;
          font-size: 1.05rem;
        }
        .editorial-block p { margin: 0.4rem 0 0; }

        .editorial-byline {
          display: flex;
          gap: 1rem;
          align-items: flex-start;
          margin-top: 2rem;
          padding: 1.25rem 1.4rem;
          border: 1px solid var(--ccg-line);
          border-radius: 22px;
          background: #fbfdff;
          box-shadow: var(--ccg-shadow);
        }
        .editorial-byline__photo {
          width: 56px;
          height: 56px;
          border-radius: 50%;
          object-fit: cover;
          flex-shrink: 0;
          border: 2px solid var(--ccg-blue-soft);
        }
        .editorial-byline__body { flex: 1; }
        .editorial-byline__name { margin: 0 0 0.25rem; font-size: 1.05rem; }
        .editorial-byline__meta {
          margin: 0 0 0.5rem;
          font-size: 0.92rem;
          color: var(--ccg-slate);
        }
        .editorial-byline__meta a { color: var(--ccg-blue); font-weight: 700; }
        .editorial-byline__note {
          margin: 0;
          font-size: 0.92rem;
          color: var(--ccg-slate);
          line-height: 1.55;
        }

        .editorial-trust {
          display: grid;
          grid-template-columns: 96px 1fr;
          gap: 1.5rem;
          align-items: center;
          padding: 1.6rem;
          border: 1px solid var(--ccg-line);
          border-radius: 28px;
          background: linear-gradient(135deg, #f3f8ff 0%, #ffffff 100%);
          box-shadow: var(--ccg-shadow);
        }
        .editorial-trust__photo {
          width: 96px;
          height: 96px;
          border-radius: 50%;
          object-fit: cover;
          border: 3px solid var(--ccg-blue);
        }
        .editorial-trust__body h2 { margin: 0.4rem 0 0.7rem; font-size: clamp(1.4rem, 3vw, 1.8rem); }
        .editorial-trust__body p { margin: 0 0 0.5rem; }
        .editorial-trust__link { color: var(--ccg-blue); font-weight: 800; }
        @media (max-width: 600px) {
          .editorial-trust { grid-template-columns: 1fr; text-align: left; }
          .editorial-trust__photo { width: 80px; height: 80px; }
        }

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

        /* Charted calculators (avalanche-snowball, min-payment, refinance).
           Custom widget layouts that don't fit the generic .ccg-calc-form grid. */
        .ccg-calc-card--charted { padding: 1.4rem; display: grid; gap: 1.1rem; }
        .ccg-calc-title { margin: 0 0 0.4rem; font-size: 1.25rem; }
        .ccg-calc-row {
          display: grid;
          gap: 0.85rem;
          grid-template-columns: 1fr;
        }
        @media (min-width: 640px) {
          .ccg-calc-row { grid-template-columns: repeat(2, minmax(0, 1fr)); }
        }
        @media (min-width: 960px) {
          .ccg-calc-row { grid-template-columns: repeat(3, minmax(0, 1fr)); }
        }
        .ccg-calc-row__wide { grid-column: 1 / -1; }
        .ccg-calc-row label { display: grid; gap: 0.35rem; font-weight: 700; }
        .ccg-calc-row label span { color: var(--ccg-slate); font-weight: 600; font-size: 0.92rem; }
        .ccg-calc-row input[type="number"],
        .ccg-calc-row input[type="text"] {
          min-height: 44px;
          padding: 0.65rem 0.85rem;
          border: 1px solid var(--ccg-line);
          border-radius: 12px;
          background: #fbfdff;
          color: var(--ccg-ink);
          font: inherit;
        }
        .ccg-calc-row input[type="range"] {
          accent-color: var(--ccg-blue);
          width: 100%;
          padding: 0;
          min-height: 32px;
        }
        .ccg-calc-row input:focus { outline: 2px solid var(--ccg-blue); outline-offset: 2px; }
        .ccg-calc-help { color: var(--ccg-slate); font-size: 0.92rem; margin: 0; }
        .ccg-calc-warning {
          padding: 0.85rem 1rem;
          border-radius: 12px;
          border: 1px solid #b91c1c;
          background: #fef2f2;
          color: #b91c1c;
          font-size: 0.95rem;
        }
        .ccg-calc-subsection { display: grid; gap: 0.7rem; }
        .ccg-calc-subsection h4 { margin: 0; font-size: 1.05rem; }
        .ccg-chart-wrap {
          padding: 0.8rem;
          background: #fbfdff;
          border: 1px solid var(--ccg-line);
          border-radius: 16px;
        }
        /* Multi-debt table for avalanche-snowball */
        .ccg-debt-table-wrap { overflow-x: auto; }
        .ccg-debt-input-table {
          width: 100%;
          min-width: 520px;
          border-collapse: collapse;
        }
        .ccg-debt-input-table th,
        .ccg-debt-input-table td {
          padding: 0.6rem 0.55rem;
          text-align: left;
          border-bottom: 1px solid var(--ccg-line);
          vertical-align: middle;
        }
        .ccg-debt-input-table input[type="text"],
        .ccg-debt-input-table input[type="number"] {
          width: 100%;
          min-height: 40px;
          padding: 0.45rem 0.6rem;
          border: 1px solid var(--ccg-line);
          border-radius: 10px;
          background: #fbfdff;
          color: var(--ccg-ink);
          font: inherit;
        }
        .ccg-button--small { padding: 0.5rem 0.85rem; min-height: 38px; font-size: 0.88rem; }
        /* Result cards */
        .ccg-result-grid--three {
          display: grid;
          gap: 0.85rem;
          grid-template-columns: 1fr;
        }
        @media (min-width: 720px) {
          .ccg-result-grid--three { grid-template-columns: repeat(3, minmax(0, 1fr)); }
        }
        .ccg-result-card {
          padding: 1rem 1.1rem;
          border-radius: 16px;
          border: 1px solid var(--ccg-line);
          background: #fbfdff;
          display: grid;
          gap: 0.3rem;
        }
        .ccg-result-card span { color: var(--ccg-slate); font-size: 0.88rem; }
        .ccg-result-card strong { font-size: 1.3rem; line-height: 1.2; }
        .ccg-result-card--highlight {
          background: linear-gradient(135deg, #eaf2ff 0%, #ffffff 100%);
          border-color: var(--ccg-blue);
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
          if (!choice) banner.style.display = "flex";
          banner.querySelectorAll("[data-cookie-action]").forEach((button) => {
            button.addEventListener("click", () => {
              localStorage.setItem("ccg-cookie-choice", button.dataset.cookieAction);
              banner.style.display = "none";
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
        Disallow: /*?q=*
        Disallow: /*?s=*

        Sitemap: {DOMAIN}/sitemap.xml
        """
    )


def calc_js_avalanche_snowball() -> str:
    """Browser-local JavaScript for the avalanche-vs-snowball calculator.
    No localStorage. No analytics. All math runs in the user's browser.
    Binds to the DOM IDs emitted by _calc_module_avalanche_snowball()."""
    return (
        "(() => {\n"
        "  const MAX_DEBTS = 5;\n"
        "  const MAX_MONTHS = 600;\n"
        "  let debtChart = null;\n"
        "  const debtRows = document.getElementById(\"debtRows\");\n"
        "  if (!debtRows) return;\n"
        "  const addDebtBtn = document.getElementById(\"addDebtBtn\");\n"
        "  const totalPaymentInput = document.getElementById(\"totalPayment\");\n"
        "  const warning = document.getElementById(\"debtWarning\");\n"
        "  const fmtMoney = (n) => new Intl.NumberFormat(\"en-US\", { style: \"currency\", currency: \"USD\", maximumFractionDigits: 0 }).format(Number.isFinite(n) ? n : 0);\n"
        "  const fmtMonths = (m) => `${m} month${m === 1 ? \"\" : \"s\"}`;\n"
        "  const defaultDebts = [\n"
        "    { name: \"Credit card\", balance: 4200, apr: 24.99 },\n"
        "    { name: \"Personal loan\", balance: 8000, apr: 12.5 },\n"
        "    { name: \"Store card\", balance: 1200, apr: 28.99 }\n"
        "  ];\n"
        "  function addDebtRow(debt = { name: \"Debt\", balance: 1000, apr: 18 }) {\n"
        "    if (debtRows.children.length >= MAX_DEBTS) return;\n"
        "    const tr = document.createElement(\"tr\");\n"
        "    tr.innerHTML = `\n"
        "      <td><input class=\"debt-name\" type=\"text\" value=\"${debt.name}\" aria-label=\"Debt name\"></td>\n"
        "      <td><input class=\"debt-balance\" type=\"number\" inputmode=\"decimal\" min=\"0\" step=\"50\" value=\"${debt.balance}\" aria-label=\"Debt balance\"></td>\n"
        "      <td><input class=\"debt-apr\" type=\"number\" inputmode=\"decimal\" min=\"0\" max=\"99\" step=\"0.01\" value=\"${debt.apr}\" aria-label=\"Debt APR\"></td>\n"
        "      <td><button type=\"button\" class=\"ccg-button ccg-button--ghost ccg-button--small remove-button\">Remove</button></td>\n"
        "    `;\n"
        "    debtRows.appendChild(tr);\n"
        "    tr.querySelectorAll(\"input\").forEach(input => input.addEventListener(\"input\", calculate));\n"
        "    tr.querySelector(\".remove-button\").addEventListener(\"click\", () => { tr.remove(); calculate(); });\n"
        "    calculate();\n"
        "  }\n"
        "  function getDebts() {\n"
        "    return Array.from(debtRows.querySelectorAll(\"tr\"))\n"
        "      .map(row => ({\n"
        "        name: row.querySelector(\".debt-name\").value.trim() || \"Debt\",\n"
        "        balance: Math.max(0, parseFloat(row.querySelector(\".debt-balance\").value) || 0),\n"
        "        apr: Math.max(0, parseFloat(row.querySelector(\".debt-apr\").value) || 0)\n"
        "      }))\n"
        "      .filter(d => d.balance > 0);\n"
        "  }\n"
        "  function simulate(strategy, debts, totalPayment) {\n"
        "    let balances = debts.map(d => ({ ...d }));\n"
        "    let totalInterest = 0;\n"
        "    let months = 0;\n"
        "    const timeline = [balances.reduce((s, d) => s + d.balance, 0)];\n"
        "    while (balances.some(d => d.balance > 0.01) && months < MAX_MONTHS) {\n"
        "      months += 1;\n"
        "      let monthlyInterest = 0;\n"
        "      balances.forEach(d => {\n"
        "        if (d.balance <= 0) return;\n"
        "        const interest = d.balance * (d.apr / 100 / 12);\n"
        "        d.balance += interest;\n"
        "        monthlyInterest += interest;\n"
        "      });\n"
        "      totalInterest += monthlyInterest;\n"
        "      let paymentLeft = totalPayment;\n"
        "      const active = balances.filter(d => d.balance > 0.01);\n"
        "      active.sort((a, b) => strategy === \"avalanche\" ? (b.apr - a.apr || a.balance - b.balance) : (a.balance - b.balance || b.apr - a.apr));\n"
        "      for (const debt of active) {\n"
        "        if (paymentLeft <= 0) break;\n"
        "        const payment = Math.min(paymentLeft, debt.balance);\n"
        "        debt.balance -= payment;\n"
        "        paymentLeft -= payment;\n"
        "      }\n"
        "      timeline.push(balances.reduce((s, d) => s + Math.max(0, d.balance), 0));\n"
        "    }\n"
        "    return { months, totalInterest, timeline, amortizes: months < MAX_MONTHS };\n"
        "  }\n"
        "  function debtFreeDate(months) {\n"
        "    const d = new Date();\n"
        "    d.setMonth(d.getMonth() + months);\n"
        "    return d.toLocaleDateString(\"en-US\", { month: \"short\", year: \"numeric\" });\n"
        "  }\n"
        "  function updateChart(avalanche, snowball) {\n"
        "    const ctx = document.getElementById(\"debtChart\");\n"
        "    if (!ctx || typeof Chart === \"undefined\") return;\n"
        "    const len = Math.max(avalanche.timeline.length, snowball.timeline.length);\n"
        "    const labels = Array.from({ length: len }, (_, i) => i);\n"
        "    if (debtChart) debtChart.destroy();\n"
        "    debtChart = new Chart(ctx, {\n"
        "      type: \"line\",\n"
        "      data: { labels, datasets: [\n"
        "        { label: \"Avalanche balance\", data: avalanche.timeline, borderColor: \"#1f6fff\", backgroundColor: \"rgba(31,111,255,0.12)\", tension: 0.25 },\n"
        "        { label: \"Snowball balance\", data: snowball.timeline, borderColor: \"#e65100\", backgroundColor: \"rgba(230,81,0,0.12)\", tension: 0.25 }\n"
        "      ]},\n"
        "      options: {\n"
        "        responsive: true,\n"
        "        interaction: { mode: \"index\", intersect: false },\n"
        "        plugins: { tooltip: { callbacks: { label: (c) => `${c.dataset.label}: ${fmtMoney(c.parsed.y)}` } } },\n"
        "        scales: { y: { ticks: { callback: (v) => fmtMoney(v) } }, x: { title: { display: true, text: \"Months\" } } }\n"
        "      }\n"
        "    });\n"
        "  }\n"
        "  function calculate() {\n"
        "    const debts = getDebts();\n"
        "    const totalPayment = Math.max(0, parseFloat(totalPaymentInput.value) || 0);\n"
        "    const monthlyInterest = debts.reduce((s, d) => s + d.balance * (d.apr / 100 / 12), 0);\n"
        "    warning.hidden = true;\n"
        "    warning.textContent = \"\";\n"
        "    if (!debts.length || totalPayment <= 0) return;\n"
        "    if (totalPayment <= monthlyInterest) {\n"
        "      warning.hidden = false;\n"
        "      warning.textContent = \"Your monthly payment may not cover estimated monthly interest across all debts. The balance can grow under these assumptions. Try a larger monthly payment.\";\n"
        "    }\n"
        "    const avalanche = simulate(\"avalanche\", debts, totalPayment);\n"
        "    const snowball = simulate(\"snowball\", debts, totalPayment);\n"
        "    const interestSaved = snowball.totalInterest - avalanche.totalInterest;\n"
        "    const monthDiff = snowball.months - avalanche.months;\n"
        "    document.getElementById(\"avalancheMonths\").textContent = avalanche.amortizes ? fmtMonths(avalanche.months) : \"600+ months\";\n"
        "    document.getElementById(\"avalancheInterest\").textContent = `${fmtMoney(avalanche.totalInterest)} interest`;\n"
        "    document.getElementById(\"snowballMonths\").textContent = snowball.amortizes ? fmtMonths(snowball.months) : \"600+ months\";\n"
        "    document.getElementById(\"snowballInterest\").textContent = `${fmtMoney(snowball.totalInterest)} interest`;\n"
        "    document.getElementById(\"avalancheTableMonths\").textContent = avalanche.amortizes ? avalanche.months : \"600+\";\n"
        "    document.getElementById(\"snowballTableMonths\").textContent = snowball.amortizes ? snowball.months : \"600+\";\n"
        "    document.getElementById(\"avalancheDate\").textContent = avalanche.amortizes ? debtFreeDate(avalanche.months) : \"Not estimated\";\n"
        "    document.getElementById(\"snowballDate\").textContent = snowball.amortizes ? debtFreeDate(snowball.months) : \"Not estimated\";\n"
        "    document.getElementById(\"avalancheTableInterest\").textContent = fmtMoney(avalanche.totalInterest);\n"
        "    document.getElementById(\"snowballTableInterest\").textContent = fmtMoney(snowball.totalInterest);\n"
        "    if (interestSaved > 0) document.getElementById(\"methodVerdict\").textContent = `Avalanche saves ${fmtMoney(interestSaved)}`;\n"
        "    else if (interestSaved < 0) document.getElementById(\"methodVerdict\").textContent = `Snowball saves ${fmtMoney(Math.abs(interestSaved))}`;\n"
        "    else document.getElementById(\"methodVerdict\").textContent = \"Both methods cost the same\";\n"
        "    document.getElementById(\"methodVerdictSub\").textContent = monthDiff > 0 ? `Avalanche is ${monthDiff} month${monthDiff === 1 ? \"\" : \"s\"} faster.` : monthDiff < 0 ? `Snowball is ${Math.abs(monthDiff)} month${Math.abs(monthDiff) === 1 ? \"\" : \"s\"} faster.` : \"Same payoff time.\";\n"
        "    updateChart(avalanche, snowball);\n"
        "  }\n"
        "  addDebtBtn.addEventListener(\"click\", () => addDebtRow());\n"
        "  totalPaymentInput.addEventListener(\"input\", calculate);\n"
        "  defaultDebts.forEach(addDebtRow);\n"
        "})();\n"
    )


def calc_js_min_payment() -> str:
    return (
        "(() => {\n"
        "  const MAX_MONTHS = 720;\n"
        "  let chart = null;\n"
        "  const fields = [\"ccBalance\", \"ccApr\", \"minPct\", \"minFloor\", \"extraPayment\"].reduce((acc, id) => { acc[id] = document.getElementById(id); return acc; }, {});\n"
        "  if (!fields.ccBalance) return;\n"
        "  const fmtMoney = (n) => new Intl.NumberFormat(\"en-US\", { style: \"currency\", currency: \"USD\", maximumFractionDigits: 0 }).format(Number.isFinite(n) ? n : 0);\n"
        "  const fmtYearsMonths = (months) => {\n"
        "    const y = Math.floor(months / 12);\n"
        "    const m = months % 12;\n"
        "    if (y <= 0) return `${m} month${m === 1 ? \"\" : \"s\"}`;\n"
        "    return `${y} year${y === 1 ? \"\" : \"s\"}${m ? `, ${m} month${m === 1 ? \"\" : \"s\"}` : \"\"}`;\n"
        "  };\n"
        "  function simulate(balance, apr, minPct, minFloor, extra) {\n"
        "    let current = balance;\n"
        "    let months = 0;\n"
        "    let interestPaid = 0;\n"
        "    const monthlyRate = apr / 100 / 12;\n"
        "    while (current > 0.01 && months < MAX_MONTHS) {\n"
        "      months += 1;\n"
        "      const interest = current * monthlyRate;\n"
        "      current += interest;\n"
        "      interestPaid += interest;\n"
        "      const minPayment = Math.max(current * (minPct / 100), minFloor);\n"
        "      const payment = Math.min(current, minPayment + extra);\n"
        "      if (payment <= interest && monthlyRate > 0) return { months: MAX_MONTHS, interestPaid, amortizes: false };\n"
        "      current -= payment;\n"
        "    }\n"
        "    return { months, interestPaid, amortizes: months < MAX_MONTHS };\n"
        "  }\n"
        "  function updateChart(minimum, extra) {\n"
        "    const ctx = document.getElementById(\"minPaymentChart\");\n"
        "    if (!ctx || typeof Chart === \"undefined\") return;\n"
        "    if (chart) chart.destroy();\n"
        "    chart = new Chart(ctx, {\n"
        "      type: \"bar\",\n"
        "      data: { labels: [\"Minimum only\", \"Minimum + extra\"], datasets: [\n"
        "        { label: \"Total interest ($)\", data: [Math.round(minimum.interestPaid), Math.round(extra.interestPaid)], backgroundColor: \"#1f6fff\", yAxisID: \"y\" },\n"
        "        { label: \"Months to payoff\", data: [minimum.months, extra.months], backgroundColor: \"#e65100\", yAxisID: \"y1\" }\n"
        "      ]},\n"
        "      options: {\n"
        "        responsive: true,\n"
        "        plugins: { tooltip: { callbacks: { label: (c) => c.dataset.label.includes(\"interest\") ? `${c.dataset.label}: ${fmtMoney(c.parsed.y)}` : `${c.dataset.label}: ${c.parsed.y}` } } },\n"
        "        scales: { y: { type: \"linear\", position: \"left\", ticks: { callback: (v) => fmtMoney(v) } }, y1: { type: \"linear\", position: \"right\", grid: { drawOnChartArea: false } } }\n"
        "      }\n"
        "    });\n"
        "  }\n"
        "  function calculate() {\n"
        "    const balance = Math.max(0, parseFloat(fields.ccBalance.value) || 0);\n"
        "    const apr = Math.max(0, parseFloat(fields.ccApr.value) || 0);\n"
        "    const minPct = Math.max(0.1, parseFloat(fields.minPct.value) || 2);\n"
        "    const minFloor = Math.max(0, parseFloat(fields.minFloor.value) || 25);\n"
        "    const extraPayment = Math.max(0, parseFloat(fields.extraPayment.value) || 0);\n"
        "    document.getElementById(\"extraLabel\").textContent = fmtMoney(extraPayment);\n"
        "    const warning = document.getElementById(\"minWarning\");\n"
        "    warning.hidden = true;\n"
        "    if (balance <= 0) return;\n"
        "    const minimum = simulate(balance, apr, minPct, minFloor, 0);\n"
        "    const extra = simulate(balance, apr, minPct, minFloor, extraPayment);\n"
        "    if (!minimum.amortizes) {\n"
        "      warning.hidden = false;\n"
        "      warning.textContent = \"The entered minimum-payment settings may not pay off this balance within 60 years. Increase the payment, raise the floor, or contact a nonprofit credit counselor.\";\n"
        "    }\n"
        "    const interestSavings = minimum.interestPaid - extra.interestPaid;\n"
        "    const monthSavings = minimum.months - extra.months;\n"
        "    document.getElementById(\"minHeadline\").textContent = minimum.amortizes ? fmtYearsMonths(minimum.months) : \"60+ years\";\n"
        "    document.getElementById(\"minInterest\").textContent = `${fmtMoney(minimum.interestPaid)} estimated interest`;\n"
        "    document.getElementById(\"extraHeadline\").textContent = extra.amortizes ? fmtYearsMonths(extra.months) : \"60+ years\";\n"
        "    document.getElementById(\"extraInterest\").textContent = `${fmtMoney(extra.interestPaid)} estimated interest`;\n"
        "    document.getElementById(\"savingsHeadline\").textContent = fmtMoney(Math.max(0, interestSavings));\n"
        "    const ms = Math.max(0, monthSavings);\n"
        "    document.getElementById(\"timeSavings\").textContent = `${ms} month${ms === 1 ? \"\" : \"s\"} faster`;\n"
        "    document.getElementById(\"minMonths\").textContent = minimum.amortizes ? minimum.months : \"720+\";\n"
        "    document.getElementById(\"extraMonths\").textContent = extra.amortizes ? extra.months : \"720+\";\n"
        "    document.getElementById(\"minTotalInterest\").textContent = fmtMoney(minimum.interestPaid);\n"
        "    document.getElementById(\"extraTotalInterest\").textContent = fmtMoney(extra.interestPaid);\n"
        "    document.getElementById(\"minRatio\").textContent = balance > 0 ? `${((minimum.interestPaid / balance) * 100).toFixed(1)}%` : \"\\u2014\";\n"
        "    document.getElementById(\"extraRatio\").textContent = balance > 0 ? `${((extra.interestPaid / balance) * 100).toFixed(1)}%` : \"\\u2014\";\n"
        "    updateChart(minimum, extra);\n"
        "  }\n"
        "  Object.values(fields).forEach(f => f.addEventListener(\"input\", calculate));\n"
        "  calculate();\n"
        "})();\n"
    )


def calc_js_refinance() -> str:
    return (
        "(() => {\n"
        "  let chart = null;\n"
        "  const ids = [\"loanBalance\", \"currentRate\", \"remainingYears\", \"newRate\", \"newYears\", \"closingCosts\", \"plannedYears\"];\n"
        "  const el = ids.reduce((acc, id) => { acc[id] = document.getElementById(id); return acc; }, {});\n"
        "  if (!el.loanBalance) return;\n"
        "  const fmtMoney = (n) => new Intl.NumberFormat(\"en-US\", { style: \"currency\", currency: \"USD\", maximumFractionDigits: 0 }).format(Number.isFinite(n) ? n : 0);\n"
        "  const fmtMonths = (m) => `${m} month${m === 1 ? \"\" : \"s\"}`;\n"
        "  function payment(principal, annualRate, years) {\n"
        "    const n = years * 12;\n"
        "    const r = annualRate / 100 / 12;\n"
        "    if (principal <= 0 || n <= 0) return 0;\n"
        "    if (r === 0) return principal / n;\n"
        "    return principal * r / (1 - Math.pow(1 + r, -n));\n"
        "  }\n"
        "  function updateChart(monthlySavings, closingCosts, horizonMonths) {\n"
        "    const ctx = document.getElementById(\"refiChart\");\n"
        "    if (!ctx || typeof Chart === \"undefined\") return;\n"
        "    const months = Math.min(Math.max(horizonMonths, 12), 360);\n"
        "    const labels = [];\n"
        "    const values = [];\n"
        "    const step = Math.max(1, Math.round(months / 24));\n"
        "    for (let i = 0; i <= months; i += step) {\n"
        "      labels.push(i);\n"
        "      values.push((monthlySavings * i) - closingCosts);\n"
        "    }\n"
        "    if (chart) chart.destroy();\n"
        "    chart = new Chart(ctx, {\n"
        "      type: \"line\",\n"
        "      data: { labels, datasets: [{ label: \"Cumulative savings after closing costs\", data: values, borderColor: \"#1f6fff\", backgroundColor: \"rgba(31,111,255,0.12)\", tension: 0.2, fill: true }]},\n"
        "      options: {\n"
        "        responsive: true,\n"
        "        plugins: { tooltip: { callbacks: { label: (c) => `${c.dataset.label}: ${fmtMoney(c.parsed.y)}` } } },\n"
        "        scales: { y: { ticks: { callback: (v) => fmtMoney(v) } }, x: { title: { display: true, text: \"Months\" } } }\n"
        "      }\n"
        "    });\n"
        "  }\n"
        "  function calculate() {\n"
        "    const balance = Math.max(0, parseFloat(el.loanBalance.value) || 0);\n"
        "    const currentRate = Math.max(0, parseFloat(el.currentRate.value) || 0);\n"
        "    const remainingYears = Math.max(1, parseFloat(el.remainingYears.value) || 1);\n"
        "    const newRate = Math.max(0, parseFloat(el.newRate.value) || 0);\n"
        "    const newYears = Math.max(1, parseFloat(el.newYears.value) || 1);\n"
        "    const closingCosts = Math.max(0, parseFloat(el.closingCosts.value) || 0);\n"
        "    const plannedYears = Math.max(0, parseFloat(el.plannedYears.value) || 0);\n"
        "    const oldPmt = payment(balance, currentRate, remainingYears);\n"
        "    const newPmt = payment(balance, newRate, newYears);\n"
        "    const monthlySavings = oldPmt - newPmt;\n"
        "    const breakEvenMonths = monthlySavings > 0 ? Math.ceil(closingCosts / monthlySavings) : Infinity;\n"
        "    const oldInterest = (oldPmt * remainingYears * 12) - balance;\n"
        "    const newInterest = (newPmt * newYears * 12) - balance;\n"
        "    document.getElementById(\"oldPayment\").textContent = fmtMoney(oldPmt);\n"
        "    document.getElementById(\"newPayment\").textContent = fmtMoney(newPmt);\n"
        "    document.getElementById(\"tableOldPayment\").textContent = fmtMoney(oldPmt);\n"
        "    document.getElementById(\"tableNewPayment\").textContent = fmtMoney(newPmt);\n"
        "    document.getElementById(\"oldInterest\").textContent = fmtMoney(oldInterest);\n"
        "    document.getElementById(\"newInterest\").textContent = fmtMoney(newInterest);\n"
        "    document.getElementById(\"tableClosingCosts\").textContent = fmtMoney(closingCosts);\n"
        "    const warning = document.getElementById(\"refiWarning\");\n"
        "    warning.hidden = true;\n"
        "    if (!Number.isFinite(breakEvenMonths)) {\n"
        "      document.getElementById(\"breakEven\").textContent = \"No monthly break-even\";\n"
        "      document.getElementById(\"breakEvenSub\").textContent = \"The new payment is not lower than the current payment.\";\n"
        "      warning.hidden = false;\n"
        "      warning.textContent = \"This refinance does not lower the estimated principal-and-interest payment. Review the offer carefully and confirm the Loan Estimate.\";\n"
        "      updateChart(monthlySavings, closingCosts, plannedYears * 12 || 120);\n"
        "      return;\n"
        "    }\n"
        "    document.getElementById(\"breakEven\").textContent = fmtMonths(breakEvenMonths);\n"
        "    document.getElementById(\"breakEvenSub\").textContent = `After that, estimated savings are ${fmtMoney(monthlySavings)}/month.`;\n"
        "    const plannedMonths = plannedYears * 12;\n"
        "    if (plannedMonths > 0 && plannedMonths < breakEvenMonths) {\n"
        "      warning.hidden = false;\n"
        "      warning.textContent = `Warning: your planned sale or next refinance is in ${plannedMonths} months \\u2014 before the estimated break-even point of ${breakEvenMonths} months. This refinance may not recover closing costs through monthly savings.`;\n"
        "    }\n"
        "    updateChart(monthlySavings, closingCosts, plannedMonths || newYears * 12);\n"
        "  }\n"
        "  Object.values(el).forEach(input => input.addEventListener(\"input\", calculate));\n"
        "  calculate();\n"
        "})();\n"
    )


def sitemap_xml(paths: List[str]) -> str:
    # Sitemap contains ONLY indexable URLs. Noindex pages are deliberately excluded
    # so Search Console / AdSense do not see them as eligible-for-index candidates.
    items = []
    for path in paths:
        if not is_indexable(path):
            continue
        items.append(
            f"<url><loc>{html.escape(url_for(path))}</loc><lastmod>{SITEMAP_LASTMOD}</lastmod><changefreq>weekly</changefreq><priority>{'1.0' if path == 'index.html' else '0.8'}</priority></url>"
        )
    return trim(
        f"""
        <?xml version="1.0" encoding="UTF-8"?>
        <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
          {''.join(items)}
        </urlset>
        """
    )


def redirects_txt(paths: List[str]) -> str:
    # Per project rules: NEVER 200 rules; never www rules in this file
    # (www and http→https handled in Cloudflare dashboard).
    lines: List[str] = []

    # 1. Hide internal artifacts from the public deploy. Anything inside scripts/,
    #    every .md report at root, every .py file, and every .mjs helper returns
    #    404 to crawlers and direct visitors.
    lines += [
        "/scripts/* /404 404",
        "/*.md /404 404",
        "/*.py /404 404",
        "/*.mjs /404 404",
    ]

    # 2. Canonicalize legacy .html routes to clean URLs.
    lines += ["/index.html / 301!", "/index / 301!"]
    for path in paths:
        if path == "index.html" or path == "404.html":
            continue
        if path.endswith("/index.html"):
            continue
        lines.append(f"/{path} /{path.removesuffix('.html')} 301!")
    return "\n".join(lines) + "\n"


def headers_txt() -> str:
    return trim(
        """
        /*
          X-Frame-Options: DENY
          X-Content-Type-Options: nosniff
          Referrer-Policy: strict-origin-when-cross-origin
          Permissions-Policy: geolocation=(), microphone=(), camera=()
          Strict-Transport-Security: max-age=31536000; includeSubDomains; preload

        /*.md
          X-Robots-Tag: noindex, nofollow

        /*.py
          X-Robots-Tag: noindex, nofollow

        /scripts/*
          X-Robots-Tag: noindex, nofollow
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

        def public_path(path: str) -> str:
            if path == "index.html":
                return "/"
            return f"/{{path.removesuffix('.html')}}"

        def local_file_for_public_url(url: str) -> Path:
            path = url.replace(DOMAIN, "", 1) or "/"
            if path == "/":
                return ROOT / "index.html"
            clean = path.lstrip("/")
            if clean.endswith("/"):
                clean = clean[:-1]
            return ROOT / f"{{clean}}.html"

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
                if rel == "404.html":
                    continue
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
                    assert_true(local_file_for_public_url(link).exists(), f"Broken internal link in {{rel}} -> {{link}}", problems)

            robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
            assert_true("Sitemap: https://creditcostguide.com/sitemap.xml" in robots, "robots.txt missing sitemap directive", problems)

            sitemap = ET.parse(ROOT / "sitemap.xml").getroot()
            ns = {{"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}}
            urls = [loc.text for loc in sitemap.findall("sm:url/sm:loc", ns)]
            assert_true(len(urls) == len(expected_paths), "sitemap.xml URL count does not match HTML file count", problems)
            for path in expected_paths:
                loc = f"{{DOMAIN}}{{public_path(path)}}"
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
                "## Monetization Checklist",
                "- Clear navigation is present across the site.",
                "- Legal pages exist: privacy policy, terms, and disclaimer.",
                "- Content is educational, original, and themed around U.S. consumer finance costs.",
                "- No placeholder ad blocks were included.",
                "- Cookie preference controls are present.",
                "",
                "## Indexing Checklist",
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
    # Static review pages not generated by this script but committed alongside output
    all_paths += ["pages/smartcredit-review.html"]

    related_pool = [item["path"] for item in PILLARS] + [path for path, _, _ in SUPPORTING] + [path for path, _, _, _ in CALCULATORS]

    for cfg in PILLARS:
        path = cfg["path"]
        related = [p for p in related_pool if p != path][:6]
        if path in PAGE_CONTENT:
            body, page_faqs = rich_article_body(path, related)
        else:
            body = article_body(cfg, 3000, related)
            page_faqs = cfg["faqs"]
        if path in SMARTCREDIT_PAGES:
            body = smartcredit_inject(body)
        doc = html_doc(
            path=path,
            title=cfg["title"],
            description=cfg["description"],
            page_type="guide",
            main_content=body,
            breadcrumbs=breadcrumb_items(path, cfg["title"]),
            faqs=page_faqs,
            hero_title=cfg["hero"],
            hero_summary=cfg["summary"],
        )
        write(TARGET / path, doc)

    for path, title, desc in SUPPORTING:
        related = [p for p in related_pool if p != path][:6]
        if path in PAGE_CONTENT:
            body, faqs = rich_article_body(path, related)
        else:
            body, faqs = support_body(path, title, desc, related)
        if path in SMARTCREDIT_PAGES:
            body = smartcredit_inject(body)
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
        if path in PAGE_CONTENT:
            body, faqs = rich_article_body(path, related, calc_type=calc_type)
        else:
            body, faqs = calculator_body(path, title, desc, calc_type, related)
        if path in SMARTCREDIT_PAGES:
            body = smartcredit_inject(body)
        # Charted calculators load Chart.js (defer) and their dedicated per-page
        # JS bundle. Other calculators rely on main.js wireCalculators().
        extra_scripts: List[str] = []
        if calc_type in CHARTED_CALCS:
            extra_scripts.append(
                '<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.6/dist/chart.umd.min.js" defer></script>'
            )
            extra_scripts.append(
                f'<script src="{DOMAIN}/assets/scripts/{CHARTED_CALCS[calc_type]}" defer></script>'
            )
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
            extra_scripts=extra_scripts,
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
            body, faqs = contact_page_body(generic_related)
        elif path == "about.html":
            generic_related = [p for p in related_pool if p != path][:6]
            body, faqs = about_body(generic_related)
        elif path == "how-we-research.html":
            generic_related = [p for p in related_pool if p != path][:6]
            body, faqs = how_we_research_body(generic_related)
        elif path == "privacy-policy.html":
            generic_related = [p for p in related_pool if p != path][:6]
            body, faqs = legal_body("privacy", generic_related)
        elif path == "terms.html":
            generic_related = [p for p in related_pool if p != path][:6]
            body, faqs = legal_body("terms", generic_related)
        elif path == "disclaimer.html":
            generic_related = [p for p in related_pool if p != path][:6]
            body, faqs = legal_body("disclaimer", generic_related)
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

    # Author page at /authors/javi-perez/
    author_path = "authors/javi-perez/index.html"
    all_paths.append(author_path)
    author_related = [p for p in related_pool][:6]
    author_body, author_faqs = author_page_body(author_related)
    write(
        TARGET / author_path,
        html_doc(
            path=author_path,
            title=f"{EDITOR_NAME} — Editor of CreditCostGuide",
            description=f"{EDITOR_NAME} is the founder and sole editor of CreditCostGuide, an independent U.S. consumer-finance education site. Honest bio, no fictional credentials.",
            page_type="article",
            main_content=author_body,
            breadcrumbs=[
                # Two-level breadcrumb only — there is no /authors index page,
                # so we go straight from Home to the author profile to avoid a
                # broken intermediate link.
                {"name": "Home", "url": f"{DOMAIN}/"},
                {"name": EDITOR_NAME, "url": f"{DOMAIN}/authors/javi-perez"},
            ],
            faqs=author_faqs,
            hero_title=f"{EDITOR_NAME}",
            hero_summary=f"Founder and editor of CreditCostGuide, based in {EDITOR_LOCATION}.",
        ),
    )

    not_found_body = trim(
        f"""
        <section class="ccg-section">
          <div class="ccg-section-head">
            <p class="ccg-kicker">Missing Page</p>
            <h2>The page you requested could not be found</h2>
          </div>
          <p>The address may be outdated, the page may have moved, or the link may have been entered incorrectly. Use the links below to continue exploring CreditCostGuide.</p>
          <div class="ccg-related-grid">
            <a class="ccg-related-card" href="{url_for('index.html')}"><span>Home</span><strong>Return to the homepage</strong></a>
            <a class="ccg-related-card" href="{url_for('pages/personal-loans-guide.html')}"><span>Guide</span><strong>Read the personal loans guide</strong></a>
            <a class="ccg-related-card" href="{url_for('pages/loan-payment-calculator.html')}"><span>Calculator</span><strong>Open the loan payment calculator</strong></a>
            <a class="ccg-related-card" href="{url_for('contact.html')}"><span>Support</span><strong>Visit the contact page</strong></a>
          </div>
        </section>
        """
    )
    write(
        TARGET / "404.html",
        html_doc(
            path="404.html",
            title="Page Not Found | CreditCostGuide",
            description="The requested CreditCostGuide page could not be found. Browse guides, calculators, and key finance topics from the main site sections.",
            page_type="article",
            main_content=not_found_body,
            breadcrumbs=breadcrumb_items("404.html", "Page Not Found"),
            faqs=[],
            hero_title="Page not found",
            hero_summary="Use the navigation below to return to credit, loan, mortgage, and debt payoff resources.",
            is_404=True,
        ),
    )

    write(TARGET / "styles.css", styles_css())
    write(TARGET / "main.js", main_js())
    # Per-page JS bundles for charted calculators.
    write(TARGET / "assets" / "scripts" / "debt-avalanche-snowball.js", calc_js_avalanche_snowball())
    write(TARGET / "assets" / "scripts" / "minimum-payment-true-cost.js", calc_js_min_payment())
    write(TARGET / "assets" / "scripts" / "refinance-break-even.js", calc_js_refinance())
    write(TARGET / "robots.txt", robots_txt())
    write(TARGET / "sitemap.xml", sitemap_xml(all_paths))
    write(TARGET / "_redirects", redirects_txt(all_paths))
    write(TARGET / "_headers", headers_txt())
    write(TARGET / "assets" / "icons" / "logo.svg", logo_svg())
    write(TARGET / "assets" / "icons" / "favicon.svg", favicon_svg())
    write(TARGET / "assets" / "images" / "social-preview.svg", social_svg())
    write(TARGET / "scripts" / "verify_site.py", verification_script())
    write(TARGET / "scripts" / "build_site.py", Path(__file__).read_text(encoding="utf-8"))
    if not (TARGET / "walkthrough.md").exists():
        write(TARGET / "walkthrough.md", "# CreditCostGuide Launch Walkthrough\n\nRun `python3 scripts/verify_site.py` to populate the audit report.\n")


if __name__ == "__main__":
    build()
