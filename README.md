# 🎯 The Sugar Trap — Snack Market Gap Analysis
**Client:** Helix CPG Partners (Strategic Food & Beverage Consultancy)

---

## A. Executive Summary

Analysis of 500,000 food products from the Open Food Facts database reveals a clear market gap in the healthy snacking aisle. 
After cleaning and categorizing 27,116 snack products across 8 categories, only 24.6% of all snacks fall in the High Protein + Low Sugar quadrant, confirming the market is overwhelmingly dominated by sugary, low-protein offerings. 
The biggest blue ocean opportunity lies in Bars & Granola, a category with growing consumer interest but still largely high in sugar. We recommend launching a product targeting 13g of protein and under 4g of sugar per 100g, formulated using Soy, Oat, and Sunflower as the primary protein sources — the three most common ingredients found in existing high-protein, low-sugar bars.

---

## B. Project Links

| Deliverable | Link |
|-------------|------|
| 📓 Notebook (Google Colab) | https://colab.research.google.com/drive/1qVLHFunBLXuHkMQpKaWwTjJBha65pv63?usp=sharing |
| 📊 Dashboard (Streamlit) | https://sugar-trap-dashboard.streamlit.app/ |
| 🎥 Video Walkthrough (Loom) | https://www.loom.com/share/109cbb8b9f714157bb9043adf3437d6e |

---

## C. Technical Explanation

### Data Cleaning
The raw dataset was loaded with `nrows=500,000` to avoid processing the full 12GB file, selecting only the 7 columns relevant to the analysis. Rows with null values in `product_name`, `sugars_100g`, or `proteins_100g` were dropped, reducing the dataset from 500,000 to 105,154 rows. Biologically impossible values (nutrients below 0g or above 100g per 100g of product) were removed, and duplicate product names were dropped, yielding a final clean dataset of 82,207 products. `fiber_100g` nulls were filled with 0 as a conservative assumption. Products with uncategorizable tags were excluded from visualization, leaving 27,116 snack products for analysis.

### Category Wrangling
The `categories_tags` column contained messy, comma-separated tags like `en:chocolate-chip-cookies-with-nuts`. A keyword-matching function was applied to assign each product to one of 8 high-level categories: Candy & Chocolate, Chips & Crisps, Cookies & Biscuits, Bars & Granola, Nuts & Seeds, Dairy Snacks, Meat Snacks, and Fruit Snacks. Products with unrecognizable tags were labeled "Other" and excluded from the dashboard.

---
### Candidate's Choice — Market Opportunity Score
I added a **Market Opportunity Score**, a composite metric that ranks each snack category by its untapped potential using the formula:
opportunity_score = (avg_protein / max_protein) - (avg_sugar / max_sugar) + (avg_fiber / max_fiber)

Rather than asking a client to interpret a scatter plot, this condenses the analysis into a single, boardroom-ready number per category. Bars & Granola scores highest, independently confirming our scatter plot recommendation. This addition demonstrates that data insights must be translated into actionable business language to drive real decisions.

---

## D. Pre-Submission Checklist

- [x] GitHub Repo is Public
- [x] `.ipynb` notebook file uploaded
- [x] PDF export of notebook uploaded
- [x] Raw dataset NOT uploaded
- [x] Code uses relative paths
- [x] Dashboard publicly accessible (verified in incognito)
- [x] Presentation/video publicly accessible
- [x] README updated with Executive Summary and technical notes
- [x] User Stories 1-4 completed
- [x] Candidate's Choice completed and explained






