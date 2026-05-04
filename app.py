import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter

# ── Page Config ────────────────────────────────────────────────────
st.set_page_config(
    page_title="Sugar Trap | Market Gap Analysis",
    page_icon="🎯",
    layout="wide"
)

# ── Load Data ───────────────────────────────────────────────────────
@st.cache_data
def load_data():
    return pd.read_csv('snack_data_clean.csv')

df = load_data()

# ── Header ──────────────────────────────────────────────────────────
st.title("🎯 The Sugar Trap — Snack Market Gap Analysis")
st.markdown("*Identifying the Blue Ocean in the healthy snacking aisle for Helix CPG Partners*")
st.divider()

# ── Sidebar Filter ──────────────────────────────────────────────────
st.sidebar.header("Filters")
all_cats = sorted(df['primary_category'].unique())
selected_cats = st.sidebar.multiselect(
    "Select Categories",
    options=all_cats,
    default=all_cats
)

filtered = df[df['primary_category'].isin(selected_cats)]

# ── KPI Row ─────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
blue_ocean = filtered[(filtered['proteins_100g'] >= 10) & (filtered['sugars_100g'] <= 10)]

col1.metric("Total Products Analyzed", f"{len(filtered):,}")
col2.metric("Blue Ocean Products", f"{len(blue_ocean):,}")
col3.metric("Blue Ocean %", f"{len(blue_ocean)/len(filtered)*100:.1f}%")
col4.metric("Categories Selected", len(selected_cats))

st.divider()

# ── Story 3: Scatter Plot ────────────────────────────────────────────
st.subheader("📊 Nutrient Matrix — Sugar vs Protein")

color_map = {
    'Candy & Chocolate': '#e74c3c',
    'Chips & Crisps': '#e67e22',
    'Cookies & Biscuits': '#f39c12',
    'Bars & Granola': '#2ecc71',
    'Nuts & Seeds': '#27ae60',
    'Dairy Snacks': '#3498db',
    'Meat Snacks': '#9b59b6',
    'Fruit Snacks': '#1abc9c',
}

fig = px.scatter(
    filtered,
    x='sugars_100g',
    y='proteins_100g',
    color='primary_category',
    hover_data=['product_name'],
    opacity=0.5,
    labels={
        'sugars_100g': 'Sugar per 100g (g)',
        'proteins_100g': 'Protein per 100g (g)',
        'primary_category': 'Category'
    },
    color_discrete_map=color_map,
    height=550
)

fig.add_hline(y=10, line_dash="dash", line_color="black",
              annotation_text="High Protein threshold (10g)",
              annotation_position="bottom right")
fig.add_vline(x=10, line_dash="dash", line_color="gray",
              annotation_text="Low Sugar threshold (10g)",
              annotation_position="top right")

fig.add_annotation(
    x=5, y=70,
    text="🎯 BLUE OCEAN<br>High Protein + Low Sugar<br>(Underserved Market)",
    showarrow=False,
    font=dict(size=12, color="darkgreen"),
    bgcolor="lightgreen",
    bordercolor="darkgreen",
    borderwidth=1,
    opacity=0.85
)

fig.update_layout(
    xaxis_range=[0, 100],
    yaxis_range=[0, 100],
    legend_title="Category",
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# ── Story 4: Key Insight Box ─────────────────────────────────────────
st.subheader("💡 Key Insight")
st.success(
    """
    **Based on the data, the biggest market opportunity is in Bars & Granola**, 
    specifically targeting products with **13g of protein** and less than **4g of sugar** per 100g.
    
    Only 24.6% of all analyzed snacks fall in the High Protein + Low Sugar quadrant — 
    confirming a massive underserved market gap.
    """
)

st.divider()

# ── Story 5: Protein Sources ─────────────────────────────────────────
st.subheader("🔬 Hidden Gem — Top Protein Sources in High-Protein Bars")

protein_keywords = ['whey', 'peanut', 'soy', 'almond', 'egg',
                    'casein', 'hemp', 'chickpea', 'lentil', 'quinoa',
                    'oat', 'milk', 'rice', 'sunflower', 'pea protein']

blue_ocean_bars = df[
    (df['primary_category'] == 'Bars & Granola') &
    (df['proteins_100g'] >= 10) &
    (df['sugars_100g'] <= 10) &
    (df['ingredients_text'].notna())
]

counts = Counter()
for text in blue_ocean_bars['ingredients_text']:
    text_lower = text.lower()
    for kw in protein_keywords:
        if kw in text_lower:
            counts[kw] += 1

ingredients_df = pd.DataFrame(counts.most_common(8), columns=['Ingredient', 'Products'])

fig2 = px.bar(
    ingredients_df,
    x='Products',
    y='Ingredient',
    orientation='h',
    color='Products',
    color_continuous_scale='Greens',
    title='Most Common Protein Sources in High-Protein, Low-Sugar Bars',
    labels={'Products': 'Number of Products'}
)
fig2.update_layout(yaxis={'categoryorder': 'total ascending'}, showlegend=False)
st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ── Candidate's Choice: Market Opportunity Score ──────────────────────
st.subheader("⭐ Candidate's Choice — Market Opportunity Score by Category")
st.markdown(
    "*A composite score ranking each category by its untapped potential: "
    "higher protein + lower sugar + higher fiber = higher opportunity.*"
)

opportunity = df.groupby('primary_category').agg(
    avg_protein=('proteins_100g', 'mean'),
    avg_sugar=('sugars_100g', 'mean'),
    avg_fiber=('fiber_100g', 'mean'),
    product_count=('product_name', 'count')
).reset_index()

max_protein = opportunity['avg_protein'].max()
max_sugar = opportunity['avg_sugar'].max()
max_fiber = opportunity['avg_fiber'].max()

opportunity['opportunity_score'] = (
    (opportunity['avg_protein'] / max_protein) -
    (opportunity['avg_sugar'] / max_sugar) +
    (opportunity['avg_fiber'] / max_fiber)
).round(3)

opportunity = opportunity.sort_values('opportunity_score', ascending=False)

fig3 = px.bar(
    opportunity,
    x='primary_category',
    y='opportunity_score',
    color='opportunity_score',
    color_continuous_scale='RdYlGn',
    title='Market Opportunity Score by Snack Category',
    labels={
        'primary_category': 'Category',
        'opportunity_score': 'Opportunity Score'
    }
)
fig3.update_layout(showlegend=False, xaxis_tickangle=-20)
st.plotly_chart(fig3, use_container_width=True)

st.caption("Analysis by Helix CPG Partners | Data: Open Food Facts")