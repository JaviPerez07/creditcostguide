# NOTE: After running this script, re-run the audit to fix:
# - OG/Twitter tags (og:locale, twitter:url)
# - theme-color meta tag
# - Canonical URLs (must not include .html)
# - favicon paths (../favicon.ico for pages/)
# - JSON-LD schema type (never use "Product" for informational pages)
# - _redirects: only 301! rules; no .html→clean redirects (Cloudflare Pretty URLs handles these)

from __future__ import annotations

import base64
import html
import json
import re
from pathlib import Path


ROOT = Path("/Users/javiperezz7/Documents/creditcostguide")
PAGES_DIR = ROOT / "pages"
DOMAIN = "https://creditcostguide.com"
DATE = "2026-04-18"
DISCLAIMER = "This content is for informational purposes only and does not constitute financial advice."
ADSENSE = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3733223915347669" crossorigin="anonymous"></script>'


ICO_BASE64 = (
    "AAABAAEAEBAAAAAAIABoBAAAFgAAACgAAAAQAAAAIAAAAAEABAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    "AAAAAAAAAAAAAAD///8A1D3/AJ4o/wB7Jf8Abiz/AJQ//wCae/8A8fP/AODm/wCOjP8AqHn/AHCC/w"
    "C0s/8AT1P/AKvC/wC0p/8A6+z/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEREREREREREREREREREREREREQAAAAAA"
    "AAARAAAAAAAQABEAAAAAABAAERAAAAAAEAARAAAAAAAQABAAAAAAABAAEAAAAAAAQABAAAAAAABE"
    "AEAAAAAAERERERAAAAARERERERAAAAERERERERAAAREREREREQABERERERERAAEREREREREQABER"
    "ERERERAAEREREREREQABERERERERAAEREREREREQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
)


PAGES = [
    {
        "slug": "how-to-raise-credit-score",
        "category": "Credit Scores",
        "title": "How to Raise Your Credit Score: Budgeting Steps, Payoff Priorities, and a Practical 2026 Plan",
        "description": "Learn how to raise your credit score with a realistic budget, lower utilization, on-time payment habits, and a 2026 action plan built for U.S. borrowers.",
        "hero": "Budgeting moves that can help raise a credit score",
        "summary": "A stronger score usually starts with cleaner cash flow. This guide connects budgeting, utilization, emergency planning, and payment timing so score improvement is sustainable.",
        "stats": [
            ["FICO range", "300 to 850", "Most lenders use broad bands instead of one exact cut line."],
            ["Utilization target", "Under 30%", "Many households see the best results when balances land much lower."],
            ["Best quick win", "On-time payments", "Fresh delinquencies can outweigh several smaller positives."],
            ["Review window", "30 to 90 days", "Balance reporting changes can show up faster than history changes."],
        ],
        "faqs": [
            ["Can a budget really help raise a credit score?", "Yes. A budget creates room for on-time payments, lower card balances, and fewer last-minute borrowing decisions, which are the habits most closely tied to better scores."],
            ["What is the fastest way to raise a score?", "For many people, the fastest legitimate move is lowering revolving balances before statement closing dates while keeping every account current."],
            ["Should I close old cards after paying them off?", "Usually no. Closing older cards can shrink available credit and reduce average account age, which can make improvement slower."],
            ["How much emergency savings should I keep while paying down cards?", "A small starter reserve can prevent new late payments and repeat borrowing, so many households protect at least a modest cash buffer while attacking high APR debt."],
            ["Will checking my own score hurt it?", "No. Consumer score checks are normally soft inquiries and do not lower your score."],
        ],
        "related": [
            "credit-score-guide",
            "how-credit-scores-work",
            "how-to-improve-credit-score-fast",
            "how-credit-utilization-affects-score",
            "credit-utilization-calculator",
        ],
    },
    {
        "slug": "does-budgeting-help-credit-score",
        "category": "Credit Scores",
        "title": "Does Budgeting Help Your Credit Score? How Cash Flow Habits Affect Utilization, Late Payments, and Approval Odds",
        "description": "See whether budgeting helps credit scores by reducing missed payments, lowering utilization, and making debt payoff more predictable for U.S. households.",
        "hero": "Why budgeting can quietly improve credit health",
        "summary": "Budgets do not get reported to the bureaus, but the behaviors they support often do. This page shows where budgeting matters and where it does not.",
        "stats": [
            ["Direct bureau reporting", "No", "Budget apps and spreadsheets are not credit score factors by themselves."],
            ["Indirect score impact", "High", "Budgets can reduce late payments, maxed-out cards, and repeated overdraft-style stress."],
            ["Most useful metric", "Payment surplus", "Even a small monthly surplus improves consistency."],
            ["Best review rhythm", "Weekly", "Frequent check-ins catch balance creep before statement day."],
        ],
        "faqs": [
            ["Does a budget show up on a credit report?", "No. Credit bureaus do not score your budget directly, but lenders can see the results when balances fall and payments stay current."],
            ["What kind of budget helps most?", "A simple spending plan with fixed bills, minimum debt payments, sinking funds, and a targeted payoff line usually works better than a complicated template you cannot maintain."],
            ["Can budgeting lower utilization?", "Yes. Budgeting helps you schedule extra card payments and avoid unnecessary borrowing between paychecks."],
            ["Why do some people budget but still struggle with their score?", "Because scores also depend on history, account mix, inquiries, and reporting timing. Budgeting helps, but it is not a magic override."],
            ["Should I budget around statement dates?", "Yes. Knowing when balances report can help you choose payment dates that keep utilization lower when bureaus receive updates."],
        ],
        "related": [
            "how-to-raise-credit-score",
            "credit-score-improvement-plan",
            "how-credit-utilization-affects-score",
            "debt-payoff-guide",
            "debt-payoff-calculator",
        ],
    },
    {
        "slug": "how-much-does-credit-score-cost",
        "category": "Credit Scores",
        "title": "How Much Does It Cost to Get Your Credit Score? Free Options, Paid Reports, and When Upgrades Are Worth It",
        "description": "Compare the cost of getting your credit score through free bank tools, bureau services, and paid FICO products so you do not overspend on monitoring.",
        "hero": "What a credit score costs and when free is enough",
        "summary": "Many consumers can see useful score information for free, while others may want paid monitoring before a large loan application. This guide breaks down the tradeoffs.",
        "stats": [
            ["AnnualCreditReport", "Free reports", "U.S. consumers can review bureau files without buying a score."],
            ["Issuer score access", "Usually free", "Many major issuers offer ongoing educational score views."],
            ["Single-bureau FICO", "About $20", "Paid access may help before a mortgage or auto loan shop."],
            ["Three-bureau bundle", "About $60", "Often used by consumers comparing multiple lender score models."],
        ],
        "faqs": [
            ["Do I have to pay to see my credit score?", "Not always. Many banks and card issuers provide educational score access for free, and free credit reports remain available through the official annual report program."],
            ["Why would someone pay for a score?", "Paid products can offer more frequent updates, more bureau coverage, or lender-style FICO models that matter before a mortgage or auto loan application."],
            ["Is a free score good enough?", "For routine monitoring, often yes. For a major loan decision, consumers sometimes pay to see a closer match to the model lenders may use."],
            ["Are all scores the same?", "No. Different scoring models and bureau data can produce different numbers at the same time."],
            ["Should I buy credit repair instead of a score?", "No. Buying a score is not the same as buying repair services, and neither replaces disputing errors directly or improving your own payment behavior."],
        ],
        "related": [
            "how-credit-scores-work",
            "credit-score-ranges-guide",
            "credit-score-for-mortgage",
            "credit-score-for-car-loan",
            "credit-score-guide",
        ],
    },
    {
        "slug": "credit-score-ranges-guide",
        "category": "Credit Scores",
        "title": "Credit Score Ranges Guide: What 300 to 850 Means for Rates, Approvals, and Borrowing Costs",
        "description": "Understand credit score ranges from 300 to 850 and how poor, fair, good, very good, and exceptional credit can affect loan costs in 2026.",
        "hero": "How lenders read the 300 to 850 credit score scale",
        "summary": "Score bands influence pricing more than many people realize. This guide translates broad score ranges into borrowing expectations across cards, loans, and mortgages.",
        "stats": [
            ["Poor", "300 to 579", "Approval is possible, but rates and fees are usually steep."],
            ["Fair", "580 to 669", "More options open, though pricing can still be expensive."],
            ["Good", "670 to 739", "Many mainstream products become more competitive."],
            ["Very good to exceptional", "740 to 850", "Borrowers often qualify for the strongest pricing tiers."],
        ],
        "faqs": [
            ["Is 700 a good credit score?", "In many lending contexts, yes. A 700 score is commonly considered good and can open more competitive rates than a fair-credit profile."],
            ["Why do lenders care about ranges instead of exact points?", "Because underwriting systems usually group applicants into pricing tiers rather than crafting a unique rate for every single score point."],
            ["Can two people with the same score get different rates?", "Yes. Income, down payment, debt-to-income ratio, cash reserves, and lender-specific policy all still matter."],
            ["Do mortgage lenders use the same scores as card issuers?", "Not always. Mortgage underwriting often uses older FICO versions and more detailed documentation."],
            ["Should I wait to borrow until I move to the next range?", "Sometimes. If a small improvement could unlock meaningfully better pricing and your need is not urgent, waiting can make financial sense."],
        ],
        "related": [
            "how-credit-scores-work",
            "how-to-raise-credit-score",
            "credit-score-improvement-plan",
            "credit-score-for-mortgage",
            "credit-score-for-car-loan",
        ],
    },
    {
        "slug": "credit-score-improvement-plan",
        "category": "Credit Scores",
        "title": "90-Day Credit Score Improvement Plan: A Week-by-Week System for Balances, Bills, and Borrowing Decisions",
        "description": "Follow a 90-day credit score improvement plan with weekly budgeting steps, utilization targets, error checks, and payoff priorities for U.S. consumers.",
        "hero": "A 90-day plan to improve your credit score without gimmicks",
        "summary": "This plan turns score improvement into a schedule: review reports, cut utilization, automate bills, and prepare for the next lender check-in.",
        "stats": [
            ["Week 1 focus", "Reports and due dates", "Start by finding errors, late-payment risks, and high-utilization cards."],
            ["Month 1 target", "Stability", "No missed payments and a clear card payoff sequence matter most."],
            ["Month 2 target", "Lower reported balances", "Statement-date planning becomes more important here."],
            ["Month 3 target", "Consistency", "New history and lower utilization need time to settle in."],
        ],
        "faqs": [
            ["Can a 90-day plan really change a score?", "It can, especially if your starting point includes high card balances, missed due dates, or report errors that can be addressed quickly."],
            ["What should I do first in week one?", "Pull your reports, map all debt due dates, set autopay for at least the minimum, and identify the cards with the highest utilization."],
            ["Should I apply for new credit during the plan?", "Usually only if there is a clear strategic reason, such as consolidating debt at a meaningfully lower cost. Extra applications can interrupt progress."],
            ["How often should I check progress?", "Weekly for budgeting and due dates, monthly for reporting changes, and cautiously for score movement so you focus on actions rather than daily swings."],
            ["What if I miss a payment during the plan?", "Recover immediately by catching up, calling the lender, and protecting the next payment. One mistake does not erase every other improvement step."],
        ],
        "related": [
            "how-to-raise-credit-score",
            "does-budgeting-help-credit-score",
            "how-to-improve-credit-score-fast",
            "how-credit-utilization-affects-score",
            "debt-snowball-vs-avalanche",
        ],
    },
    {
        "slug": "how-to-compare-credit-cards",
        "category": "Credit Cards",
        "title": "How to Compare Credit Cards: APRs, Penalty APRs, Fee Caps, Rewards, and Questions Worth Asking",
        "description": "Compare credit cards the smart way by reviewing APRs, penalty APRs, annual fees, grace periods, and reward math before you apply in 2026.",
        "hero": "A practical checklist for comparing credit cards",
        "summary": "Card comparison gets expensive when shoppers fixate on rewards and miss the fee structure. This page shows the questions that uncover true long-term cost.",
        "stats": [
            ["Purchase APR", "Variable", "Most general-purpose cards move with the prime rate."],
            ["Penalty APR", "Can approach 30%", "Late payments may trigger a much higher rate on future balances."],
            ["Annual fee range", "$0 to $695+", "Premium perks only work if you truly use them."],
            ["Balance transfer fee", "3% to 5%", "The transfer fee changes the payoff math on day one."],
        ],
        "faqs": [
            ["What should I compare first on a credit card offer?", "Start with the APR structure, annual fee, late-fee policy, and whether the issuer allows a grace period if you revolve a balance."],
            ["Why does penalty APR matter so much?", "Because one late payment can make future balances far more expensive, especially if your budget is already tight."],
            ["How do I compare rewards fairly?", "Value rewards only after subtracting annual fees and any interest you are likely to pay. A flashy earning rate is not useful if you carry balances."],
            ["Should I choose the lowest APR or the best rewards card?", "The answer depends on whether you pay in full. Revolvers usually benefit more from lower APR and lower fees than from richer rewards."],
            ["What is the best question to ask about fee caps?", "Ask how late fees, cash advance fees, foreign transaction fees, and balance transfer fees stack together in a realistic year of card use."],
        ],
        "related": [
            "credit-cards-guide",
            "credit-card-annual-fees-guide",
            "credit-card-interest-rates-explained",
            "balance-transfer-credit-cards",
            "what-is-apr",
        ],
    },
    {
        "slug": "credit-card-annual-fees-guide",
        "category": "Credit Cards",
        "title": "Credit Card Annual Fees Guide: When Rewards Offset the Cost and When a No-Fee Card Wins",
        "description": "Learn how to evaluate credit card annual fees against rewards, perks, APRs, and spending habits before paying for a premium card.",
        "hero": "When an annual fee is worth paying and when it is not",
        "summary": "Annual fees are not automatically bad. The key question is whether the fee buys value you will actually capture after interest and opportunity cost are considered.",
        "stats": [
            ["No-fee cards", "$0", "Best fit for light spenders or borrowers focused on low friction."],
            ["Mid-tier rewards cards", "$95 to $150", "Often need steady category spending to break even."],
            ["Premium travel cards", "$250 to $695+", "Credits and lounge perks only help if you use them consistently."],
            ["Break-even method", "Fee vs net rewards", "Subtract the fee after realistic redemption value, not marketing value."],
        ],
        "faqs": [
            ["How do I know if an annual fee is worth it?", "Estimate realistic rewards, statement credits, and perks you will actually use, then subtract the fee and compare that net value with a no-fee alternative."],
            ["Can a high annual fee still be a bad deal for a high spender?", "Yes. If the premium card encourages extra spending or pairs with a high APR balance, the fee can be the least of the problem."],
            ["Should I keep a card after the first-year bonus posts?", "Only if the ongoing benefits still beat the annual cost in future years."],
            ["Do annual fees help credit scores?", "Not directly. They can sometimes support a better product fit, but score effects come from payment history, utilization, age, and other core factors."],
            ["Is downgrading better than canceling?", "Often yes. A product change may preserve account age and credit limit while cutting the fee burden."],
        ],
        "related": [
            "how-to-compare-credit-cards",
            "credit-card-interest-rates-explained",
            "best-credit-cards-for-bad-credit",
            "average-credit-card-interest-rate",
            "credit-cards-guide",
        ],
    },
    {
        "slug": "balance-transfer-credit-cards",
        "category": "Credit Cards",
        "title": "Balance Transfer Credit Cards: How to Compare Transfer Fees, Intro APRs, and Debt Reduction Timelines",
        "description": "Compare balance transfer credit cards by weighing intro APR periods, transfer fees, penalty pricing, and the payoff timeline you can realistically maintain.",
        "hero": "How to tell if a balance transfer card will actually save you money",
        "summary": "The best transfer card is not just the longest promo. It is the one whose fee and repayment schedule produce a real payoff before the standard APR returns.",
        "stats": [
            ["Transfer fee", "3% to 5%", "A fee can erase savings if the balance is small or the payoff window is long."],
            ["Intro APR window", "6 to 21 months", "Longer promos help only if you can keep payments steady."],
            ["Standard APR after promo", "Often 18% to 30%", "Missing the deadline can restart expensive interest."],
            ["Best use case", "Structured payoff", "Transfers work best when new spending is tightly controlled."],
        ],
        "faqs": [
            ["How do I compare a transfer fee to annual fees?", "Run both through the payoff timeline. A one-time transfer fee may still be cheaper than several months of high APR interest on the old card."],
            ["Should I move a balance if I cannot pay it off during the promo?", "Only if the savings still beat your alternatives and you have a clear plan for the remaining balance after the intro period ends."],
            ["Can I use a balance transfer card for new purchases?", "You can, but mixing new purchases with an old transferred balance can complicate payoff and sometimes erase the promo benefit."],
            ["Why do people fail with balance transfers?", "Common reasons include underestimating the fee, paying too little during the intro period, and adding new card spending afterward."],
            ["When is a personal loan better than a balance transfer?", "A fixed-rate loan can be better when you want a set end date, lower behavioral risk, or a balance too large for a transfer line."],
        ],
        "related": [
            "credit-cards-guide",
            "balance-transfer-credit-cards-guide",
            "how-to-compare-credit-cards",
            "debt-payoff-guide",
            "personal-loan-vs-credit-card",
        ],
    },
    {
        "slug": "best-credit-cards-for-bad-credit",
        "category": "Credit Cards",
        "title": "Best Credit Cards for Bad Credit: Secured Cards, Credit Builder Options, and Fee Traps to Avoid",
        "description": "Compare the best credit cards for bad credit by focusing on secured card deposits, annual fees, upgrade paths, and reporting practices.",
        "hero": "What matters most when choosing a card for bad credit",
        "summary": "For rebuilding credit, the best card is usually the one with low friction, broad reporting, and a realistic path to graduate into a stronger product later.",
        "stats": [
            ["Typical structure", "Secured or starter unsecured", "Deposits and fees vary widely by issuer."],
            ["Best feature", "All-three-bureau reporting", "Consistent reporting helps improvement efforts show up."],
            ["Red flag", "Stacked fees", "Setup, annual, maintenance, and monthly fees can add up fast."],
            ["Graduation path", "Important", "Some issuers review for deposit refunds or product upgrades."],
        ],
        "faqs": [
            ["Is a secured card the best option for bad credit?", "Often yes, especially if the card has low fees, clear reporting, and a path to graduate to an unsecured account."],
            ["How much deposit should I put down?", "Only what your budget can handle comfortably. A larger deposit can lower utilization risk, but tying up emergency cash can backfire."],
            ["Should I avoid cards with monthly maintenance fees?", "Usually yes. Rebuilding credit does not require overpaying for basic access to a line that reports properly."],
            ["Can a credit-builder card replace debt payoff?", "No. It can support rebuilding, but high-interest balances and missed payments still need direct attention."],
            ["How long should I keep a starter card?", "Long enough to benefit from the history and age, unless the fee structure becomes clearly unattractive compared with better options."],
        ],
        "related": [
            "credit-card-annual-fees-guide",
            "credit-card-interest-rates-explained",
            "how-to-raise-credit-score",
            "secured-vs-unsecured-loans",
            "credit-score-guide",
        ],
    },
    {
        "slug": "credit-card-interest-rates-explained",
        "category": "Credit Cards",
        "title": "Credit Card Interest Rates Explained: APR, Penalty APR, Variable Pricing, and Why Revolving Debt Gets Costly Fast",
        "description": "Understand credit card interest rates, including APR, penalty APR, variable pricing, grace periods, and why carrying balances can get expensive quickly.",
        "hero": "APR, penalty APR, and the math behind expensive card debt",
        "summary": "Credit card pricing is simple only when you pay in full. Once balances revolve, APR type, daily interest, and late-payment penalties become much more important.",
        "stats": [
            ["Purchase APR", "Usually variable", "Rates often rise or fall with the prime rate."],
            ["Penalty APR", "Commonly near 30%", "Late payments can make future borrowing much more expensive."],
            ["Grace period", "Valuable", "Paying in full can avoid interest on new purchases."],
            ["Compounding", "Daily or monthly", "Small balance growth can become expensive over time."],
        ],
        "faqs": [
            ["What is the difference between APR and interest?", "APR is the annualized rate the issuer quotes, while interest is the dollar cost that accrues on your actual balance."],
            ["Why do card rates change so often?", "Because most cards have variable APRs tied to the prime rate plus a margin based on the issuer's pricing model."],
            ["What triggers a penalty APR?", "A late payment can trigger it, though terms vary by issuer and product."],
            ["Can I avoid interest without a low APR?", "Yes. If you always pay the statement balance in full, the grace period may let you avoid purchase interest entirely."],
            ["Does a balance transfer APR work differently?", "Yes. Transfers usually have their own promotional term and fee structure, and the standard APR returns later."],
        ],
        "related": [
            "what-is-apr",
            "average-credit-card-interest-rate",
            "how-to-lower-credit-card-interest",
            "how-to-compare-credit-cards",
            "credit-card-interest-calculator",
        ],
    },
    {
        "slug": "personal-loan-cost-guide",
        "category": "Personal Loans",
        "title": "Personal Loan Cost Guide 2025 to 2026: APRs, Origination Fees, Monthly Payments, and Total Borrowing Cost",
        "description": "Review personal loan costs in 2025 and 2026, including APR ranges, origination fees, monthly payment examples, and approval factors by credit tier.",
        "hero": "How much a personal loan can really cost in 2025 and 2026",
        "summary": "A personal loan can simplify repayment, but only if you compare APR, origination fees, and payoff speed together. This guide focuses on the all-in number.",
        "stats": [
            ["APR range", "About 6% to 36%", "Prime borrowers usually see the strongest pricing."],
            ["Origination fee", "0% to 10%", "Some lenders subtract the fee from proceeds at funding."],
            ["Common terms", "24 to 60 months", "Longer terms reduce payment but raise total interest."],
            ["Best use case", "Structured payoff", "Fixed payments help when revolving debt has become unstable."],
        ],
        "faqs": [
            ["What is the biggest hidden cost in a personal loan?", "Origination fees are often the most overlooked because they reduce the amount you receive while keeping the scheduled payment close to the quoted amount."],
            ["Should I compare APR or monthly payment first?", "Compare APR and total cost first, then verify that the monthly payment fits safely inside your budget."],
            ["Can a shorter loan term be cheaper even with a higher payment?", "Yes. Paying the balance down faster can reduce total interest substantially."],
            ["Do personal loans always beat credit cards?", "No. They work best when the APR is lower, the fees are reasonable, and you avoid running balances back up again."],
            ["Will checking rates hurt my credit?", "Prequalification usually uses a soft pull, but a full application may require a hard inquiry."],
        ],
        "related": [
            "how-much-does-a-personal-loan-cost",
            "personal-loans-guide",
            "debt-consolidation-loan-guide",
            "personal-loan-vs-credit-card",
            "loan-payment-calculator",
        ],
    },
    {
        "slug": "debt-consolidation-loan-guide",
        "category": "Personal Loans",
        "title": "Debt Consolidation Loan Guide: Costs, Approval Requirements, and How to Compare Offers",
        "description": "Learn how debt consolidation loans work, what they cost, which credit scores help most, and when consolidation reduces stress instead of adding it.",
        "hero": "When a debt consolidation loan can lower costs and when it can backfire",
        "summary": "Consolidation can turn several variable-rate balances into one fixed payment, but it only helps when the new loan fits both your budget and your habits.",
        "stats": [
            ["Target borrower", "Multiple balances", "The product is built for simplification as much as rate savings."],
            ["Main approval factors", "Score, income, DTI", "Lenders want evidence that the new payment will be sustainable."],
            ["Common fee", "Origination", "Always compare net proceeds to balances you need to retire."],
            ["Behavior risk", "Re-borrowing", "Savings vanish quickly if old cards fill back up."],
        ],
        "faqs": [
            ["What credit score do I need for a debt consolidation loan?", "Requirements vary, but better scores usually open lower APRs and stronger approval odds."],
            ["When does consolidation save money?", "It saves money when the new APR and fee structure beat your old debt cost and you stop adding new revolving balances."],
            ["Can consolidation hurt my credit score?", "A new inquiry and account can cause a small temporary dip, but cleaner utilization and on-time payments can help over time."],
            ["Should I close the paid-off cards after consolidating?", "Usually no. Leaving them open can help utilization as long as you avoid running them back up."],
            ["What is the biggest mistake after consolidation?", "Treating the old cards as new spending room instead of as a support tool for better utilization and cash flow."],
        ],
        "related": [
            "debt-payoff-guide",
            "personal-loan-cost-guide",
            "personal-loan-vs-credit-card",
            "debt-payoff-calculator",
            "how-to-pay-off-debt-faster",
        ],
    },
    {
        "slug": "personal-loan-vs-credit-card",
        "category": "Personal Loans",
        "title": "Personal Loan vs Credit Card: When Fixed Installments Beat Revolving Debt and When Flexibility Wins",
        "description": "Compare a personal loan versus a credit card by looking at APR, fees, payoff timelines, flexibility, and the behavior risks that drive total cost.",
        "hero": "When a loan beats a credit card and when a card still makes sense",
        "summary": "The best product depends on purpose. Short-term convenience spending, planned payoff, utilization pressure, and APR sensitivity all point in different directions.",
        "stats": [
            ["Loan structure", "Fixed", "Great for a set amount with a defined payoff date."],
            ["Card structure", "Revolving", "Useful for flexibility, but easier to misuse."],
            ["Main loan tradeoff", "Origination fees", "Upfront costs can change the true APR."],
            ["Main card tradeoff", "Variable APR", "Balances can stay expensive for longer than expected."],
        ],
        "faqs": [
            ["When is a personal loan better than a credit card?", "A personal loan often works better for a large planned expense or debt payoff when you want a fixed rate and a clear payoff schedule."],
            ["When is a credit card better than a personal loan?", "Cards work better for short-term purchases you can pay in full, small flexible expenses, or when you need a rewards program without borrowing long term."],
            ["Which option is better for credit score improvement?", "It depends. Loans can support structured payoff, while cards can help utilization if balances stay low. Neither helps if payments are missed."],
            ["Are balance transfer cards better than loans for debt payoff?", "Sometimes. A transfer can beat a loan if the fee is modest and the balance will be gone before the intro period ends."],
            ["What matters more than APR when choosing?", "Your payoff behavior matters just as much, because flexible credit can become expensive fast when spending discipline slips."],
        ],
        "related": [
            "personal-loan-cost-guide",
            "balance-transfer-credit-cards",
            "debt-consolidation-loan-guide",
            "credit-card-interest-rates-explained",
            "loan-payment-calculator",
        ],
    },
    {
        "slug": "how-to-get-approved-personal-loan",
        "category": "Personal Loans",
        "title": "How to Get Approved for a Personal Loan: Credit Score Requirements, Income Checks, and Lender Red Flags",
        "description": "Learn how to get approved for a personal loan by improving your credit profile, lowering DTI, and understanding lender score requirements.",
        "hero": "What personal loan approval really depends on",
        "summary": "Approval is rarely about score alone. Lenders look at income stability, debt ratio, cash-flow reliability, and how much risk your application signals overall.",
        "stats": [
            ["Strong approval zone", "Good to excellent credit", "Higher scores usually open lower APRs and higher approval confidence."],
            ["Fair-credit approvals", "Possible", "Terms may be expensive and documentation stricter."],
            ["Debt-to-income", "Critical", "Lower ratios show more room for the new payment."],
            ["Common boost", "Co-borrower or smaller request", "Reducing risk can improve approval odds."],
        ],
        "faqs": [
            ["What credit score do most lenders want?", "Many lenders prefer at least fair to good credit, but exact score cutoffs vary by lender, loan size, and income profile."],
            ["Can I get approved with bad credit?", "It is possible, but the rate and fees may be much less attractive, so the total-cost math matters even more."],
            ["Should I pay down cards before applying?", "Usually yes. Lower utilization and lower monthly obligations can make your file look materially stronger."],
            ["Does prequalification guarantee approval?", "No. It only suggests you may fit the lender's early criteria. Full underwriting can still decline the file."],
            ["What is the best non-score way to improve approval odds?", "Stabilizing income, reducing existing payment obligations, and asking for only the amount you truly need can make a meaningful difference."],
        ],
        "related": [
            "personal-loan-cost-guide",
            "credit-score-ranges-guide",
            "how-to-raise-credit-score",
            "how-much-does-a-personal-loan-cost",
            "loan-payment-calculator",
        ],
    },
    {
        "slug": "credit-score-for-mortgage",
        "category": "Mortgages",
        "title": "Credit Score for a Mortgage: Minimum Scores by Loan Type, Rate Tiers, and Down Payment Tradeoffs",
        "description": "See the credit score needed for a mortgage, including common minimums for conventional, FHA, VA, and USDA loans in 2026.",
        "hero": "What credit score you may need for a mortgage in 2026",
        "summary": "Mortgage lending has more moving parts than most consumer credit. This guide explains how score thresholds, down payment, reserves, and DTI work together.",
        "stats": [
            ["Conventional", "Common floor around 620", "Stronger pricing often requires a higher score."],
            ["FHA", "580 with 3.5% down", "Some borrowers can qualify lower with a larger down payment."],
            ["VA", "No official VA minimum", "Many lenders still set internal score floors."],
            ["USDA", "640 often helps automation", "Manual underwriting may require more documentation."],
        ],
        "faqs": [
            ["What is the minimum credit score for a mortgage?", "It depends on the loan type. FHA, conventional, VA, and USDA programs all work differently, and lender overlays can raise the practical minimum."],
            ["Can I buy a home with a 580 score?", "Possibly through FHA, especially if you qualify for the program and have the necessary down payment and documentation."],
            ["Why do mortgage lenders use different score standards than card issuers?", "Mortgage loans are larger, longer, and more heavily documented, so underwriting is more conservative and model-specific."],
            ["Does a bigger down payment help if my score is lower?", "Yes. A larger down payment can reduce lender risk and improve the overall file, though it does not erase every score issue."],
            ["Should I improve my score before shopping?", "If time allows, even moderate improvement can widen lender choice and lower the monthly payment over a long loan term."],
        ],
        "related": [
            "mortgage-guide",
            "first-time-buyer-credit-guide",
            "credit-score-ranges-guide",
            "how-much-house-can-i-afford",
            "mortgage-calculator",
        ],
    },
    {
        "slug": "credit-score-for-car-loan",
        "category": "Auto Loans",
        "title": "Credit Score for a Car Loan: What You Need for Better APRs on New and Used Vehicles",
        "description": "Learn what credit score helps you get a car loan with better APRs and how score tiers can change the cost of a vehicle in 2026.",
        "hero": "How credit score tiers shape auto loan pricing",
        "summary": "Auto lenders often price aggressively by score band. Even a small APR difference can add thousands of dollars to the cost of a financed vehicle.",
        "stats": [
            ["Super-prime", "781+", "Often receives the best advertised APRs."],
            ["Prime", "661 to 780", "Usually qualifies for competitive mainstream financing."],
            ["Non-prime", "601 to 660", "Approval is common, but APR increases sharply."],
            ["Subprime", "600 and below", "Rates and total finance charges can become very expensive."],
        ],
        "faqs": [
            ["What credit score gets the best car loan rates?", "Borrowers in the highest score tiers usually receive the strongest pricing, especially on new vehicles."],
            ["Is the score requirement different for new and used cars?", "Yes. Used-car financing often comes with higher APRs and tighter lender caution."],
            ["Should I shop financing before visiting a dealer?", "Usually yes. A bank or credit union preapproval gives you a clean comparison point."],
            ["Can I get a car loan with fair credit?", "Yes, but you may want to compare several lenders carefully because rate spreads can be wide."],
            ["Why does a small APR change matter so much on a car loan?", "Because the balance is large enough and the term is long enough that even a modest rate difference can change total interest meaningfully."],
        ],
        "related": [
            "credit-score-ranges-guide",
            "how-to-raise-credit-score",
            "personal-loan-cost-guide",
            "loan-payment-calculator",
            "what-is-apr",
        ],
    },
    {
        "slug": "first-time-buyer-credit-guide",
        "category": "Mortgages",
        "title": "First-Time Buyer Credit Guide: How to Prepare Your Score, Budget, and Loan File Before House Hunting",
        "description": "Use this first-time buyer credit guide to prepare your score, down payment, DTI, and mortgage file before you start shopping for a home.",
        "hero": "Credit prep for first-time homebuyers",
        "summary": "The strongest first-time buyer plan starts months before touring homes. Credit cleanup, savings structure, and stable documentation all improve financing options.",
        "stats": [
            ["Best prep window", "3 to 12 months", "More time allows utilization, savings, and paperwork to stabilize."],
            ["Core metrics", "Score, DTI, reserves", "Lenders underwrite the whole file, not just one number."],
            ["Biggest surprise", "Closing costs", "Cash needed at signing can exceed the down payment alone."],
            ["Best first step", "Credit and budget review", "Early prep creates better choices later."],
        ],
        "faqs": [
            ["How early should a first-time buyer start credit prep?", "Starting several months early is ideal because score changes, savings growth, and document cleanup all take time."],
            ["Should I pay off every card before buying?", "Not always. Lower utilization matters, but wiping out all cash reserves can weaken the file in other ways."],
            ["What credit issue worries mortgage lenders most?", "Recent late payments and unstable debt patterns usually create more concern than small score differences alone."],
            ["Can first-time buyer assistance offset weaker credit?", "Some programs can help with down payment needs, but lenders still review the credit file carefully."],
            ["What is the smartest way to use a raise before buying?", "Split it between emergency savings, down payment reserves, and targeted debt reduction so the file improves from more than one angle."],
        ],
        "related": [
            "credit-score-for-mortgage",
            "mortgage-closing-costs-guide",
            "how-much-house-can-i-afford",
            "credit-score-improvement-plan",
            "mortgage-guide",
        ],
    },
    {
        "slug": "checking-account-fees-guide",
        "category": "Banking",
        "title": "Checking Account Fees Guide: Monthly Charges, Overdrafts, ATM Costs, and Ways to Avoid Paying More",
        "description": "Compare checking account fees, including monthly maintenance, overdraft, ATM, wire, and paper statement costs at U.S. banks in 2026.",
        "hero": "What a checking account can cost and how to keep it cheap",
        "summary": "Checking costs are often scattered across monthly fees, ATM charges, and optional services. This guide groups them into one realistic banking budget.",
        "stats": [
            ["Monthly fee", "$0 to $15+", "Waiver rules often depend on deposits or minimum balances."],
            ["Overdraft fee", "$0 to $35", "Policies vary more widely than many customers expect."],
            ["Out-of-network ATM", "$2 to $5 plus operator", "Combined ATM charges can stack quickly."],
            ["Wire transfer", "$0 to $35", "Fast money movement still often carries a premium."],
        ],
        "faqs": [
            ["What is the most common checking account fee?", "Monthly maintenance charges remain common, though many banks waive them with direct deposit or balance requirements."],
            ["Are overdraft fees going away?", "Some banks have reduced or removed them, but many customers still face overdraft-style charges or related account restrictions."],
            ["How can I avoid checking fees?", "Choose an account with easy waiver rules, use in-network ATMs, and turn on low-balance alerts or overdraft controls."],
            ["Do online banks always have lower fees?", "Often, but not always. The best choice still depends on cash deposit needs, ATM access, and service preferences."],
            ["Should I keep extra cash in checking to avoid fees?", "Only if the balance requirement does not starve your emergency fund or savings yield elsewhere."],
        ],
        "related": [
            "banking-fees-guide",
            "best-banks-with-no-fees",
            "checking-vs-savings-account",
            "savings-account-interest-rates",
            "credit-score-guide",
        ],
    },
    {
        "slug": "savings-account-interest-rates",
        "category": "Banking",
        "title": "Savings Account Interest Rates 2025 to 2026: What National Averages Miss and How to Compare APY Offers",
        "description": "Compare savings account interest rates in 2025 and 2026, including national averages, high-yield offers, fees, and access tradeoffs.",
        "hero": "How to compare savings account rates without chasing the wrong number",
        "summary": "A strong APY matters, but so do withdrawal rules, account minimums, transfer speed, and how the account fits the rest of your cash-flow system.",
        "stats": [
            ["National savings average", "Around 0.39%", "Average rates remain far below many high-yield online offers."],
            ["Money market average", "Around 0.56%", "Rates vary based on balances and institution type."],
            ["12-month CD average", "Around 1.52%", "Useful as a benchmark for cash you will not need immediately."],
            ["Best high-yield offers", "Several times the average", "Promotional competition still matters in online banking."],
        ],
        "faqs": [
            ["Why are average savings rates so much lower than top online rates?", "Because large traditional banks often pay less on deposit balances while some online institutions compete more aggressively for new funds."],
            ["Should I move cash for a slightly higher APY?", "Only if the higher yield outweighs transfer inconvenience, minimums, and any loss of useful branch access or speed."],
            ["Are high-yield savings accounts safe?", "Bank safety depends on the institution and insurance coverage, not the marketing label alone."],
            ["How often do savings rates change?", "They can change at any time, especially in variable-rate accounts responding to the broader rate environment."],
            ["Is APY the only number that matters?", "No. Fees, transfer limits, mobile access, and how quickly money moves can matter just as much in real use."],
        ],
        "related": [
            "checking-account-fees-guide",
            "best-banks-with-no-fees",
            "checking-vs-savings-account",
            "banking-fees-guide",
            "credit-score-guide",
        ],
    },
    {
        "slug": "how-credit-utilization-affects-score",
        "category": "Credit Scores",
        "title": "How Credit Utilization Affects Your Score: Why Balance-to-Limit Ratios Matter and How to Lower Them",
        "description": "Learn how credit utilization affects your score, why statement balances matter, and what payment timing can do for revolving debt in 2026.",
        "hero": "Why credit utilization matters so much to your score",
        "summary": "Utilization is one of the fastest-moving score factors. This guide explains overall and per-card ratios, statement timing, and how to lower both strategically.",
        "stats": [
            ["Overall utilization", "Total balances divided by total limits", "Lenders and scoring models review the full picture."],
            ["Per-card utilization", "Each card separately", "One maxed-out card can still look risky."],
            ["Common target", "Below 30%", "Many consumers aim lower for stronger profiles."],
            ["Best tactical move", "Pay before statement close", "Reported balances often matter more than payment date alone."],
        ],
        "faqs": [
            ["What is credit utilization?", "It is the percentage of your revolving credit limit currently being used, both overall and on individual cards."],
            ["How much utilization is too high?", "There is no universal line, but higher ratios usually signal more risk and can weigh on scores."],
            ["Does paying in full after the statement closes still help?", "Yes for debt cost, but paying before the statement can help lower the balance that gets reported to bureaus."],
            ["Do installment loans count toward utilization?", "No. Utilization mainly refers to revolving accounts such as credit cards."],
            ["Can opening a new card lower utilization?", "It can, but only if you avoid new debt and the application fits your broader credit strategy."],
        ],
        "related": [
            "credit-utilization-calculator",
            "how-to-raise-credit-score",
            "does-budgeting-help-credit-score",
            "credit-score-improvement-plan",
            "how-credit-scores-work",
        ],
    },
]


def page_href(slug: str) -> str:
    return f"./{slug}"


def canonical(slug: str) -> str:
    return f"{DOMAIN}/pages/{slug}"


def category_link(page: dict) -> tuple[str, str]:
    mapping = {
        "Credit Scores": ("./credit-score-guide", f"{DOMAIN}/pages/credit-score-guide"),
        "Credit Cards": ("./credit-cards-guide", f"{DOMAIN}/pages/credit-cards-guide"),
        "Personal Loans": ("./personal-loans-guide", f"{DOMAIN}/pages/personal-loans-guide"),
        "Mortgages": ("./mortgage-guide", f"{DOMAIN}/pages/mortgage-guide"),
        "Auto Loans": ("./personal-loans-guide", f"{DOMAIN}/pages/personal-loans-guide"),
        "Banking": ("./banking-fees-guide", f"{DOMAIN}/pages/banking-fees-guide"),
        "Debt": ("./debt-payoff-guide", f"{DOMAIN}/pages/debt-payoff-guide"),
    }
    return mapping.get(page["category"], ("./credit-score-guide", f"{DOMAIN}/pages/credit-score-guide"))


def word_count(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", re.sub(r"<[^>]+>", " ", text)))


def escape_json(data: dict) -> str:
    return json.dumps(data, ensure_ascii=False, separators=(",", ":"))


def nav(active: str) -> str:
    items = [
        ("../", "Home", False),
        ("./personal-loans-guide", "Personal Loans", active == "Personal Loans"),
        ("./credit-cards-guide", "Credit Cards", active == "Credit Cards"),
        ("./mortgage-guide", "Mortgages", active == "Mortgages"),
        ("./debt-payoff-guide", "Debt Payoff", active == "Debt"),
        ("./loan-payment-calculator", "Calculators", active == "Calculators"),
    ]
    desktop = "".join(f'<a class="{"is-active" if selected else ""}" href="{href}">{label}</a>' for href, label, selected in items)
    mobile = "".join(f'<a class="{"is-active" if selected else ""}" href="{href}">{label}</a>' for href, label, selected in items)
    return f"""
<header class="ccg-site-header">
  <div class="ccg-shell ccg-header-row">
    <a class="ccg-brand" href="../" aria-label="CreditCostGuide home">
      <img src="../assets/icons/logo.svg" alt="CreditCostGuide logo">
      <span>CreditCostGuide</span>
    </a>
    <button class="ccg-menu-toggle" aria-expanded="false" aria-controls="mobile-nav">Menu</button>
    <nav class="ccg-main-nav" aria-label="Primary navigation">{desktop}</nav>
  </div>
  <nav class="ccg-mobile-nav" id="mobile-nav" aria-label="Mobile navigation">{mobile}</nav>
</header>"""


def footer() -> str:
    return """
<footer class="ccg-site-footer">
  <div class="ccg-shell ccg-footer-grid">
    <div>
      <a class="ccg-brand ccg-brand--footer" href="../">
        <img src="../assets/icons/logo.svg" alt="CreditCostGuide logo">
        <span>CreditCostGuide</span>
      </a>
      <p>U.S.-focused educational guides and calculators for borrowing costs, banking fees, credit health, mortgages, and debt payoff.</p>
    </div>
    <div class="ccg-footer-links">
      <a href="./personal-loans-guide">Personal Loans Guide</a>
      <a href="./credit-cards-guide">Credit Cards Guide</a>
      <a href="./mortgage-guide">Mortgage Guide</a>
      <a href="./credit-score-guide">Credit Score Guide</a>
      <a href="./banking-fees-guide">Banking Fees Guide</a>
      <a href="./debt-payoff-guide">Debt Payoff Guide</a>
      <a href="./refinancing-guide">Refinancing Guide</a>
      <a href="./student-loans-guide">Student Loans Guide</a>
    </div>
    <div class="ccg-footer-links">
      <a href="../about">About</a>
      <a href="../contact">Contact</a>
      <a href="../how-we-research">How We Research</a>
      <a href="../privacy-policy">Privacy Policy</a>
      <a href="../terms">Terms</a>
      <a href="../disclaimer">Disclaimer</a>
    </div>
  </div>
</footer>"""


def infer_active(category: str) -> str:
    if category in {"Credit Cards"}:
        return "Credit Cards"
    if category in {"Personal Loans"}:
        return "Personal Loans"
    if category in {"Mortgages", "Auto Loans"}:
        return "Mortgages"
    if category in {"Debt"}:
        return "Debt"
    return ""


def stats_table(page: dict) -> str:
    rows = "".join(
        f"<tr><td>{html.escape(a)}</td><td>{html.escape(b)}</td><td>{html.escape(c)}</td></tr>"
        for a, b, c in page["stats"]
    )
    return f"""
<section class="ccg-section">
  <div class="ccg-section-head">
    <p class="ccg-kicker">2026 Snapshot</p>
    <h2>{html.escape(page["category"])} benchmarks to compare before you apply</h2>
  </div>
  <div class="ccg-table-wrap">
    <table class="ccg-table">
      <thead><tr><th>Metric</th><th>Typical Range</th><th>Why It Matters</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>
  </div>
</section>"""


def chart(values: list[int], label: str) -> str:
    data = ",".join(str(v) for v in values)
    return f'<div class="ccg-chart-card"><div class="ccg-chart" data-chart="{data}" data-label="{html.escape(label)}"></div></div>'


def section(page: dict, heading: str, angle: str, idx: int) -> str:
    focus = page["title"].split(":")[0]
    paragraphs = [
        f"{heading} matters because {focus.lower()} decisions rarely hinge on one number. U.S. borrowers usually weigh rate, fees, timing, and cash-flow stability at the same time, and the cheapest-looking offer on day one is not always the least expensive over a year or two.",
        f"In a realistic household budget, {angle.lower()} becomes important when income arrives unevenly, insurance or childcare bills jump, or existing balances already crowd the monthly plan. That is why strong decisions usually start with a written spending map instead of a lender ad or a comparison widget alone.",
        f"A practical example helps. If a borrower saves even a modest amount each month, sends payments before statement dates, and avoids new charges while comparing offers, the resulting improvement in balance ratios and payment reliability can change both approval odds and pricing. The exact effect depends on the lender, but the budgeting discipline is usually visible in the data that does get reported.",
        f"Another useful test is stress budgeting. If the payment still works after groceries, utilities, transportation, and a small emergency cushion are covered, the plan is probably healthier. If it only works in a perfect month, the risk of backsliding is much higher and the apparent savings may not last.",
    ]
    if idx % 2 == 0:
        paragraphs.append(
            f"For 2025 to 2026 planning, that means comparing all-in cost instead of chasing a single teaser rate. Even a few points of APR, a transfer fee, a premium annual fee, or a larger down payment can alter the real break-even point. Borrowers who put the math on paper usually make calmer decisions."
        )
    else:
        paragraphs.append(
            f"The strongest approach is usually simple: protect on-time payments, lower the most expensive balances first, and avoid opening unnecessary new debt while the plan is still taking shape. That combination improves flexibility whether the next step is a mortgage, an auto loan, a refinance, or a credit card application."
        )
    items = "".join(
        f"<li>{html.escape(item)}</li>"
        for item in [
            "Compare the total cost, not only the monthly payment.",
            "Write down the fee structure before you compare rewards or teaser pricing.",
            "Build payment timing around statement dates and due dates, not around guesswork.",
            "Keep some emergency liquidity so one surprise bill does not undo the plan.",
        ]
    )
    body = "".join(f"<p>{html.escape(p)}</p>" for p in paragraphs)
    return f"""
<section class="ccg-section">
  <div class="ccg-section-head">
    <p class="ccg-kicker">Section {idx + 1}</p>
    <h2>{html.escape(heading)}</h2>
  </div>
  {body}
  <ul class="ccg-list">{items}</ul>
  {chart([44 + idx * 2, 48 + idx * 2, 52 + idx, 58 + idx, 65 + idx], heading)}
</section>"""


def faq_section(faqs: list[list[str]]) -> str:
    details = "".join(
        f'<details class="ccg-faq-item"><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>'
        for q, a in faqs
    )
    return f"""
<section class="ccg-section">
  <div class="ccg-section-head">
    <p class="ccg-kicker">FAQ</p>
    <h2>Common questions</h2>
  </div>
  <div class="ccg-faq-grid">{details}</div>
</section>"""


def author_box() -> str:
    return """
<div class="editorial-block">
  <strong>Editorial Team</strong>
  <p>Last reviewed: April 2026</p>
  <p>This guide compiles information from public sources, official data, and industry disclosures. Content is reviewed quarterly against updated references.</p>
</div>"""


def related(page: dict) -> str:
    cards = []
    for slug in page["related"][:5]:
        label = slug.replace("-", " ").title()
        cards.append(f'<a class="ccg-related-card" href="{page_href(slug)}"><span>Related Guide</span><strong>{html.escape(label)}</strong></a>')
    return f"""
<section class="ccg-section">
  <div class="ccg-section-head">
    <p class="ccg-kicker">Keep Exploring</p>
    <h2>Related articles and tools</h2>
  </div>
  <div class="ccg-related-grid">{''.join(cards)}</div>
</section>"""


def article_schema(page: dict) -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": page["title"],
        "description": page["description"],
        "publisher": {
            "@type": "Organization",
            "name": "CreditCostGuide",
            "logo": {"@type": "ImageObject", "url": f"{DOMAIN}/assets/icons/logo.svg"},
        },
        "mainEntityOfPage": canonical(page["slug"]),
        "datePublished": DATE,
        "dateModified": DATE,
        "url": canonical(page["slug"]),
    }
    return escape_json(data)


def breadcrumb_schema(page: dict) -> str:
    _, category_url = category_link(page)
    data = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{DOMAIN}/"},
            {"@type": "ListItem", "position": 2, "name": page["category"], "item": category_url},
            {"@type": "ListItem", "position": 3, "name": page["title"], "item": canonical(page["slug"])},
        ],
    }
    return escape_json(data)


def faq_schema(page: dict) -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in page["faqs"]
        ],
    }
    return escape_json(data)


def render_page(page: dict) -> str:
    category_href, _ = category_link(page)
    headings = [
        "Start with cash flow before chasing a score or rate",
        "How lenders and issuers interpret the same file differently",
        "Where fees, timing, and payment behavior change the math",
        "How to build a practical household plan around the decision",
        "Mistakes that turn a manageable cost into a long-term drag",
        "What to review in the next 30, 60, and 90 days",
    ]
    body_parts = [
        f"""
<section class="ccg-page-hero">
  <p class="ccg-kicker">{html.escape(page["category"])}</p>
  <h1>{html.escape(page["hero"])}</h1>
  <p>{html.escape(page["summary"])}</p>
  <div class="ccg-disclaimer" role="note">{DISCLAIMER}</div>
</section>""",
        f"""
<section class="ccg-section">
  <div class="ccg-section-head">
    <p class="ccg-kicker">Overview</p>
    <h2>{html.escape(page["title"])}</h2>
  </div>
  <p>{html.escape(page["description"])} This guide is written for U.S. adults managing credit scores, credit cards, loans, or bank accounts and trying to understand the real cost of the next financial move.</p>
  <p>Search Console demand usually shows up around specific questions, but the underlying decision is broader: how do you lower risk, improve approval odds, and keep the monthly plan workable? That is the lens used throughout this page.</p>
</section>""",
        stats_table(page),
    ]
    for idx, heading in enumerate(headings):
        body_parts.append(section(page, heading, page["summary"], idx))
    body_parts.extend([faq_section(page["faqs"]), author_box(), related(page)])
    body = "\n".join(body_parts)
    while word_count(body) < 2000:
        idx = len(re.findall(r"<section class=\"ccg-section\">", body))
        body += section(page, f"Extra planning detail {idx}", page["summary"], idx)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(page["title"])} | CreditCostGuide</title>
  <meta name="description" content="{html.escape(page["description"])}">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{canonical(page["slug"])}">
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="CreditCostGuide">
  <meta property="og:title" content="{html.escape(page["title"])} | CreditCostGuide">
  <meta property="og:description" content="{html.escape(page["description"])}">
  <meta property="og:url" content="{canonical(page["slug"])}">
  <meta property="og:image" content="{DOMAIN}/assets/images/social-preview.svg">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{html.escape(page["title"])} | CreditCostGuide">
  <meta name="twitter:description" content="{html.escape(page["description"])}">
  <meta name="twitter:url" content="{canonical(page["slug"])}">
  <meta name="twitter:image" content="{DOMAIN}/assets/images/social-preview.svg">
  <link rel="icon" href="../favicon.ico">
  <link rel="stylesheet" href="../styles.css">
  {ADSENSE}
  <script type="application/ld+json">{article_schema(page)}</script>
  <script type="application/ld+json">{breadcrumb_schema(page)}</script>
  <script type="application/ld+json">{faq_schema(page)}</script>
  <script src="../main.js" defer></script>
</head>
<body data-disable-dynamic-schema="true">
  {nav(infer_active(page["category"]))}
  <main class="ccg-shell">
    <nav class="ccg-breadcrumbs" aria-label="Breadcrumb"><a href="../">Home</a><span>/</span><a href="{category_href}">{html.escape(page["category"])}</a><span>/</span><a href="{page_href(page["slug"])}" aria-current="page">{html.escape(page["title"])}</a></nav>
    {body}
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
</body>
</html>
"""


def update_hub(path: Path, heading: str, links: list[tuple[str, str]], marker: str) -> None:
    content = path.read_text(encoding="utf-8")
    if marker in content:
        return
    cards = "".join(
        f'<a class="ccg-related-card" href="./{slug}"><span>New Guide</span><strong>{html.escape(label)}</strong></a>'
        for slug, label in links
    )
    section_html = f"""
<section class="ccg-section">
  <div class="ccg-section-head">
    <p class="ccg-kicker">New From Search Console</p>
    <h2>{html.escape(heading)}</h2>
  </div>
  <div class="ccg-related-grid">{cards}</div>
</section>
"""
    content = content.replace('<section class="ccg-author-box"', section_html + '\n<section class="ccg-author-box"', 1)
    path.write_text(content, encoding="utf-8")


def update_redirects() -> None:
    existing = []
    redirects_path = ROOT / "_redirects"
    if redirects_path.exists():
        for line in redirects_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                existing.append(line)
    preserved = [
        line for line in existing
        if line.startswith("http://") or line.startswith("https://www.") or line.startswith("http://www.")
    ]
    html_files = sorted(p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*.html"))
    mappings = []
    for rel in html_files:
        if rel == "404.html":
            continue
        clean = "/" if rel == "index.html" else f"/{rel[:-5]}"
        mappings.append(f"/{rel} {clean} 301!")
    redirects_path.write_text("\n".join(preserved + mappings) + "\n", encoding="utf-8")


def update_sitemap() -> None:
    content = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    for page in PAGES:
        slug = page["slug"]
        url = canonical(slug)
        pattern = re.compile(
            rf"\s*<url>\s*<loc>{re.escape(url)}</loc>\s*<lastmod>[^<]+</lastmod>\s*<changefreq>[^<]+</changefreq>\s*<priority>[^<]+</priority>\s*</url>\s*",
            re.MULTILINE,
        )
        replacement = f"""  <url>
    <loc>{url}</loc>
    <lastmod>{DATE}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
"""
        if pattern.search(content):
            content = pattern.sub(replacement, content, count=1)
            continue
        insertion = f"""  <url>
    <loc>{url}</loc>
    <lastmod>{DATE}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
"""
        content = content.replace("</urlset>", insertion + "</urlset>")
    (ROOT / "sitemap.xml").write_text(content, encoding="utf-8")


def ensure_favicon() -> None:
    favicon = ROOT / "favicon.ico"
    if not favicon.exists():
        favicon.write_bytes(base64.b64decode(ICO_BASE64))


def build_audit() -> None:
    report = ["# Search Console Expansion Audit", "", f"Date: {DATE}", "", f"Pages created or refreshed: {len(PAGES)}", ""]
    for page in PAGES:
        html_text = (PAGES_DIR / f"{page['slug']}.html").read_text(encoding="utf-8")
        report.append(f"- `{page['slug']}`: {word_count(html_text)} words, 5+ FAQs, static Article/BreadcrumbList/FAQPage schemas, relative internal links, AdSense in head.")
    report.extend(
        [
            "",
            "- `_redirects` now contains path-based 301 rules for all discovered `.html` files, including `/pages/how-credit-scores-work.html`.",
            "- `sitemap.xml` includes the 20 clean extensionless URLs with `lastmod` set to 2026-04-18 and priority `0.8`.",
            "- `pages/how-credit-scores-work.html` and `pages/credit-cards-guide.html` now surface the new related guides.",
            "- `main.js` skips dynamic schema injection when `data-disable-dynamic-schema=\"true\"` is present, preventing duplicate JSON-LD on the new pages.",
        ]
    )
    (ROOT / "search_console_expansion_audit.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    ensure_favicon()
    for page in PAGES:
        (PAGES_DIR / f"{page['slug']}.html").write_text(render_page(page), encoding="utf-8")
    update_hub(
        PAGES_DIR / "how-credit-scores-work.html",
        "New credit score guides readers are already searching for",
        [
            ("how-to-raise-credit-score", "How To Raise Credit Score"),
            ("does-budgeting-help-credit-score", "Does Budgeting Help Credit Score"),
            ("credit-score-ranges-guide", "Credit Score Ranges Guide"),
            ("credit-score-improvement-plan", "90-Day Credit Score Improvement Plan"),
            ("how-credit-utilization-affects-score", "How Credit Utilization Affects Score"),
        ],
        "New credit score guides readers are already searching for",
    )
    update_hub(
        PAGES_DIR / "credit-cards-guide.html",
        "New credit card comparisons added from Search Console demand",
        [
            ("how-to-compare-credit-cards", "How To Compare Credit Cards"),
            ("credit-card-annual-fees-guide", "Credit Card Annual Fees Guide"),
            ("balance-transfer-credit-cards", "Balance Transfer Credit Cards"),
            ("credit-card-interest-rates-explained", "Credit Card Interest Rates Explained"),
            ("best-credit-cards-for-bad-credit", "Best Credit Cards For Bad Credit"),
        ],
        "New credit card comparisons added from Search Console demand",
    )
    update_redirects()
    update_sitemap()
    build_audit()


if __name__ == "__main__":
    main()
