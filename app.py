import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from models import MicrolendingModel
import io
import base64
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def safe_get(dictionary, key, default=None):
    """Safely get a value from a dictionary with a default fallback."""
    return dictionary.get(key, default) if dictionary is not None else default

# Define brand colors from Magnify Cash website
BRAND_COLORS = {
    'primary': '#7C3AED',      # Main purple
    'secondary': '#6D28D9',    # Darker purple
    'accent1': '#9F67FF',      # Lighter purple
    'accent2': '#E9D5FF',      # Very light purple
    'text': '#000000',         # Black
    'background': '#FAF9FF'    # Light background
}

# Page configuration
st.set_page_config(
    page_title="Magnify Cash | Investment Deck",
    page_icon="💰",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Force light mode by disabling dark mode
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
    
    /* Add smooth scrolling behavior */
    html {
        scroll-behavior: smooth;
    }
    
    /* Basic styles */
    .main > div {
        padding: 1rem;
        max-width: 1200px;
        margin: 0 auto;
        font-family: 'Space Grotesk', sans-serif;
        background-color: #FAF9FF;
        color: #000000;
    }
    
    /* Navigation styles */
    div[data-testid="stToolbar"] {
        visibility: hidden;
    }
    .stApp > header {
        visibility: hidden;
    }
    .main .block-container {
        padding-top: 80px;
    }
    div.sticky-nav {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 999;
        background-color: #ffffff;
        padding: 1rem 2rem;
        border-bottom: 1px solid rgba(0,0,0,0.1);
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        display: flex;
        gap: 1rem;
        align-items: center;
        justify-content: center;
        flex-wrap: wrap;
    }
    .nav-link {
        background-color: #ffffff;
        padding: 0.75rem 1.5rem;
        border-radius: 12px;
        border: 1px solid rgba(0,0,0,0.1);
        cursor: pointer;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.9rem;
        color: #000000;
        text-decoration: none;
        transition: all 0.2s;
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
    }
    .nav-link:hover {
        background-color: #FAF9FF;
        border-color: #7C3AED;
        text-decoration: none;
    }
    .section-anchor {
        scroll-margin-top: 100px;
        padding-top: 20px;
    }
    
    /* Metrics and content styles */
    .stMetric {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 24px;
        margin-bottom: 1.5rem !important;
        border: 1px solid rgba(0,0,0,0.1);
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        min-height: 180px !important;
        width: 100% !important;
    }
    .highlight {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 24px;
        border-left: 4px solid #7C3AED;
        margin: 1rem 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .info-box {
        background-color: #ffffff;
        padding: 1.25rem;
        border-radius: 24px;
        margin: 1rem 0;
        border: 1px solid rgba(0,0,0,0.1);
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Space Grotesk', sans-serif;
        color: #000000;
        letter-spacing: -0.02em;
    }
    h1 { font-size: clamp(2rem, 5vw, 3rem); font-weight: 700; }
    h2 { font-size: clamp(1.5rem, 4vw, 2rem); font-weight: 600; }
    h3 { font-size: clamp(1.2rem, 3vw, 1.5rem); font-weight: 600; }
    
    /* Form controls */
    [data-testid="stNumberInput"] label, [data-testid="stSlider"] label {
        color: #000000 !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
    }
    [data-testid="stNumberInput"] input, [data-testid="stSlider"] input {
        background-color: #ffffff !important;
        color: #000000 !important;
        font-family: 'Space Grotesk', sans-serif !important;
    }
    
    /* Force light mode */
    .stApp, .main, .element-container, .stMarkdown {
        background-color: #FAF9FF !important;
        color: #000000 !important;
    }
    
    /* Ensure text contrast */
    .stSelectbox label, .stSlider label, .stNumberInput label {
        color: #000000 !important;
    }
    
    .stSelectbox select, .stSlider input, .stNumberInput input {
        color: #000000 !important;
        background-color: #ffffff !important;
    }
    
    /* Fix button text contrast */
    .stButton button {
        color: #000000 !important;
        background-color: #ffffff !important;
        border: 1px solid rgba(0,0,0,0.1) !important;
    }
    
    .stButton button:hover {
        border-color: #7C3AED !important;
        background-color: #FAF9FF !important;
    }
    
    /* Fix dropdown contrast */
    div[data-baseweb="select"] {
        background-color: #000000 !important;
    }
    
    /* Make select box text white */
    div[data-baseweb="select"] span {
        color: #ffffff !important;
    }
    
    /* Style the select dropdown options */
    div[role="listbox"] {
        background-color: #ffffff !important;
    }
    
    div[role="listbox"] div[role="option"] {
        color: #000000 !important;
    }
    
    /* Style the download button */
    .stDownloadButton button {
        color: #ffffff !important;
        background-color: #000000 !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
    }
    
    .stDownloadButton button:hover {
        color: #000000 !important;
        background-color: #ffffff !important;
        border-color: #7C3AED !important;
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .main > div {
            padding: 0.5rem;
        }
        .stMetric {
            min-height: 160px !important;
            padding: 1.25rem !important;
        }
        [data-testid="column"] {
            width: 100% !important;
            flex: none !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Initialize model and session state
if 'params' not in st.session_state:
    logger.info("Initializing session state with default parameters")
    st.session_state.params = {
        'loan_amount': 30.0,
        'term_days': 30,
        'interest_rate': 0.1875,
        'origination_fee_pct': 0.10,
        'revenue_split_company': 0.20,  # Platform gets 20% by default
        'growth_rate_yearly': {  # Growth rates matching provided numbers
            1: 1.0,   # 100% growth for Year 2
            2: 0.8,   # 80% growth for Year 3
            3: 0.6,   # 60% growth for Year 4
            4: 0.45,  # 45% growth for Year 5
            5: 0.0    # No growth after year 5
        },
        'initial_loans_monthly': 20000,  # Starting with 20,000 monthly loans
    }

if 'model_state' not in st.session_state:
    st.session_state.model_state = {}

def update_model():
    """Update all model calculations and metrics"""
    logger.info("Updating model with parameters: %s", st.session_state.params)
    
    try:
        model = MicrolendingModel(st.session_state.params)
        st.session_state.model_state['metrics'] = model.calculate_loan_metrics()
        st.session_state.model_state['projections'] = model.project_financials()
        st.session_state.model_state['staker_metrics'] = model.calculate_staker_metrics()
        st.session_state.model_state['investment_metrics'] = model.calculate_investment_metrics()
        st.session_state.model_state['platform_fee'] = st.session_state.params['revenue_split_company'] * 100
        
        # Calculate growth data from model projections
        projections = st.session_state.model_state['projections']
        annual_data = []
        
        # Calculate annual metrics
        current_monthly_loans = st.session_state.params['initial_loans_monthly']
        total_fee = st.session_state.model_state['metrics']['total_fee']
        
        for year in range(5):
            annual_loans = current_monthly_loans * 12
            total_fees = annual_loans * total_fee
            company_revenue = total_fees * st.session_state.params['revenue_split_company']
            staker_revenue = total_fees * (1 - st.session_state.params['revenue_split_company'])
            monthly_liquidity = current_monthly_loans * st.session_state.params['loan_amount']
            
            annual_data.append({
                'Year': f'Year {year + 1}',
                'Annual Loans': annual_loans,
                'Total Fees ($M)': total_fees / 1_000_000,
                'Company Revenue ($M)': company_revenue / 1_000_000,
                'Staker Revenue ($M)': staker_revenue / 1_000_000,
                'Monthly Liquidity ($M)': monthly_liquidity / 1_000_000
            })
            
            # Apply growth rate for next year
            if year < 4:  # Don't grow after year 5
                growth_rate = st.session_state.params['growth_rate_yearly'][year + 1]
                current_monthly_loans = int(current_monthly_loans * (1 + growth_rate))
        
        st.session_state.model_state['growth_data'] = pd.DataFrame(annual_data)
        logger.info("Model updated successfully")
        
    except Exception as e:
        logger.error("Error updating model: %s", str(e))
        raise

# Initial model calculation
update_model()

# Generate Excel data for export
output = io.BytesIO()
with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
    st.session_state.model_state['projections'].to_excel(writer, sheet_name='Detailed Projections', index=False)
    
    # Create metrics dataframe
    metrics_df = pd.DataFrame({
        'Component': ['Principal', 'Interest Fee', 'Origination Fee', 'Total Fee', 'Total Repayment'],
        'Amount': [
            st.session_state.params['loan_amount'],
            safe_get(st.session_state.model_state['metrics'], 'interest_fee', 0),
            safe_get(st.session_state.model_state['metrics'], 'origination_fee', 0),
            safe_get(st.session_state.model_state['metrics'], 'total_fee', 0),
            st.session_state.params['loan_amount'] + safe_get(st.session_state.model_state['metrics'], 'total_fee', 0)
        ]
    })
    metrics_df.to_excel(writer, sheet_name='Unit Economics', index=False)
    
    # Create growth data
    growth_data = st.session_state.model_state['growth_data']
    pd.DataFrame(growth_data).to_excel(writer, sheet_name='Growth Metrics', index=False)
    
    # Add investment metrics
    pd.DataFrame([st.session_state.model_state['investment_metrics']]).to_excel(writer, sheet_name='Investment Metrics', index=False)
    
    # Add staker metrics
    pd.DataFrame([st.session_state.model_state['staker_metrics']]).to_excel(writer, sheet_name='Staker Economics', index=False)

excel_data = output.getvalue()

# Navigation Bar with anchor links
st.markdown("""
    <div class="sticky-nav">
        <a href="#model-parameters" class="nav-link">
            📊 Model Parameters
        </a>
        <a href="#export-model" class="nav-link">
            📥 Export Model
        </a>
    </div>
""", unsafe_allow_html=True)

st.title("Magnify Cash: AI-Powered DeFi Microlending")
st.markdown("""
    <div class='highlight'>
    <h3>Investment Highlights</h3>
    • First-mover in AI-powered onchain microlending targeting $506B TAM by 2030<br>
    • 15.4K+ active users with 34% MoM growth<br>
    • 99% fraud reduction through biometric verification (Industry avg: 40%)<br>
    • 17.25% fee per loan with 80% to stakers
    </div>
""", unsafe_allow_html=True)

# Key Metrics Row
st.subheader("Key Performance Indicators")

# Update the custom_metric function for better spacing
def custom_metric(label, value, delta, help_text=None):
    st.markdown(f"""
        <div style="background-color: #ffffff; padding: 1.5rem; border-radius: 24px; 
                    margin-bottom: 1.5rem; border: 1px solid rgba(0,0,0,0.1); 
                    box-shadow: 0 1px 3px rgba(0,0,0,0.05); min-height: 180px; width: 100%;">
            <div style="font-family: 'Space Grotesk', sans-serif; font-size: 0.9rem; 
                        color: #000000; margin-bottom: 0.75rem; line-height: 1.4;
                        white-space: normal; overflow: visible; width: 100%;">{label}</div>
            <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.8rem; 
                        font-weight: 600; color: #000000; margin-bottom: 0.75rem;
                        line-height: 1.2; white-space: normal; overflow: visible;
                        width: 100%;">{value}</div>
            <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1rem; 
                        font-weight: 600; color: #10B981; display: flex; align-items: center;
                        gap: 4px; line-height: 1.4; white-space: normal; overflow: visible;
                        width: 100%;">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="margin-right: 4px;">
                    <path d="M12 5L12 19M12 5L6 11M12 5L18 11" stroke="#10B981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                {delta}
            </div>
            {f'<div style="margin-top: 0.5rem; font-size: 0.8rem; color: #6B7280; line-height: 1.4;">{help_text}</div>' if help_text else ''}
        </div>
    """, unsafe_allow_html=True)

# Create metrics in a 2x2 grid
col1, col2 = st.columns(2)
with col1:
    subcol1, subcol2 = st.columns(2)
    with subcol1:
        custom_metric(
            "Active Users",
            "15.4K+",
            "+34% MoM",
            "Monthly active users on the platform"
        )
    with subcol2:
        custom_metric(
            "Fraud Reduction",
            "99%",
            "Industry avg: 40%",
            "Fraud reduction through biometric verification"
        )

with col2:
    subcol1, subcol2 = st.columns(2)
    with subcol1:
        custom_metric(
            "Fee per Loan",
            f"${safe_get(st.session_state.model_state['metrics'], 'total_fee', 0):.2f}",
            f"{safe_get(st.session_state.model_state['metrics'], 'total_fee', 0)/st.session_state.params['loan_amount']*100:.1f}% of principal",
            "Average fee per loan"
        )
    with subcol2:
        custom_metric(
            "Staker Yield",
            f"{safe_get(st.session_state.model_state['metrics'], 'total_fee', 0) * (1 - st.session_state.params['revenue_split_company']) / st.session_state.params['loan_amount'] * 100:.1f}%",
            "Per loan cycle",
            "Yield for stakers per loan cycle"
        )

# Market Opportunity
st.header("Market Opportunity")
col1, col2 = st.columns([3, 2])
with col1:
    st.markdown("""
        <div class='info-box'>
        <h3>Addressing Financial Exclusion</h3>
        <p>• 1.4 billion adults remain unbanked globally</p>
        <p>• $506B projected market size for DeFi lending by 2030</p>
        <p>• 80% of microloan applicants are rejected by traditional lenders</p>
        <p>• 40-400% APR charged by payday lenders vs. our 17.25% fee</p>
        </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
        <div class='info-box'>
        <h3>Competitive Advantage</h3>
        <p>• AI-powered credit scoring with 99% fraud reduction</p>
        <p>• Biometric verification through World ID</p>
        <p>• Instant onchain loans with no collateral required</p>
        <p>• Decentralized capital from stakers earning 13.8% yield</p>
        </div>
    """, unsafe_allow_html=True)

# Financial Projections
st.header("Financial Projections")

# Revenue Growth Chart
fig = go.Figure()

# Convert monthly projections to annual data
annual_data = []
projections = st.session_state.model_state['projections']
for year in range(5):
    start_month = year * 12
    end_month = start_month + 12
    annual_total_fees = projections['total_fees'][start_month:end_month].sum()
    annual_company_revenue = projections['company_revenue'][start_month:end_month].sum()
    annual_staker_revenue = projections['staker_revenue'][start_month:end_month].sum()
    annual_data.append({
        'year': f'Year {year + 1}',
        'total_fees': annual_total_fees,
        'company_revenue': annual_company_revenue,
        'staker_revenue': annual_staker_revenue
    })

years = [d['year'] for d in annual_data]
total_fees = [d['total_fees'] for d in annual_data]
company_revenue = [d['company_revenue'] for d in annual_data]
staker_revenue = [d['staker_revenue'] for d in annual_data]

# Add traces with smoothed curves
fig.add_trace(go.Scatter(
    x=years,
    y=total_fees,
    mode='lines+markers',
    name='Total Revenue',
    line=dict(shape='spline', smoothing=1.3, color=BRAND_COLORS['accent1'], width=4),
    marker=dict(size=10)
))

fig.add_trace(go.Scatter(
    x=years,
    y=company_revenue,
    mode='lines+markers',
    name='Platform Revenue',
    line=dict(shape='spline', smoothing=1.3, color=BRAND_COLORS['primary'], width=3),
    marker=dict(size=8)
))

fig.add_trace(go.Scatter(
    x=years,
    y=staker_revenue,
    mode='lines+markers',
    name='Staker Revenue',
    line=dict(shape='spline', smoothing=1.3, color=BRAND_COLORS['secondary'], width=3),
    marker=dict(size=8)
))

# Update layout for better readability
fig.update_layout(
    title={
        'text': 'Projected Annual Revenue (5-Year Forecast)',
        'font': {'family': 'Space Grotesk', 'size': 24, 'color': '#000000'},
        'y': 0.95
    },
    xaxis_title='Year',
    yaxis_title='Revenue ($)',
    showlegend=True,
    template='plotly_white',
    height=450,
    margin=dict(l=40, r=40, t=60, b=40),
    paper_bgcolor='#ffffff',
    plot_bgcolor='#ffffff',
    font=dict(
        family='Space Grotesk',
        size=14,
        color='#000000'
    ),
    xaxis=dict(
        gridcolor='rgba(0,0,0,0.1)',
        tickfont=dict(
            family='Space Grotesk',
            size=12,
            color='#000000'
        ),
        title_font=dict(
            size=14,
            color='#000000'
        )
    ),
    yaxis=dict(
        gridcolor='rgba(0,0,0,0.1)',
        tickfont=dict(
            family='Space Grotesk',
            size=12,
            color='#000000'
        ),
        title_font=dict(
            size=14,
            color='#000000'
        ),
        tickformat='$,.0f'
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
        font=dict(
            family='Space Grotesk',
            size=12,
            color='#000000'
        ),
        bgcolor='rgba(255,255,255,0.9)',
        bordercolor='rgba(0,0,0,0.1)'
    )
)

st.plotly_chart(fig, use_container_width=True)

# Growth Metrics Table
st.subheader("5-Year Growth Projections")
st.markdown('<div class="table-container">', unsafe_allow_html=True)

# Format the growth data
styled_df = pd.DataFrame(st.session_state.model_state['growth_data']).style.format({
    'Annual Loans': '{:,.0f}',
    'Total Fees ($M)': '${:,.1f}M',
    'Company Revenue ($M)': '${:,.1f}M',
    'Staker Revenue ($M)': '${:,.1f}M',
    'Monthly Liquidity ($M)': '${:,.1f}M'
}).set_properties(**{
    'background-color': 'white',
    'color': BRAND_COLORS['text'],
    'font-family': 'Space Grotesk',
    'border-color': 'rgba(0,0,0,0.1)',
    'text-align': 'right'
}).set_table_styles([
    {'selector': 'th', 'props': [
        ('background-color', BRAND_COLORS['background']),
        ('color', BRAND_COLORS['text']),
        ('font-family', 'Space Grotesk'),
        ('font-weight', '600'),
        ('text-align', 'left')
    ]},
    {'selector': 'td', 'props': [
        ('text-align', 'right')
    ]},
    {'selector': 'td:first-child', 'props': [
        ('text-align', 'left')
    ]}
])

# Add a caption explaining the growth assumptions
st.table(styled_df)
st.markdown("""
    <div style='font-size: 0.9rem; color: #666; margin-top: 0.5rem;'>
    Growth assumptions: Year 1 starting with 20,000 monthly loans. 
    Year 2: 100% growth, Year 3: 80% growth, Year 4: 60% growth, Year 5: 45% growth. 
    Monthly to annual conversion uses 12× multiplier.
    </div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Unit Economics
st.header("Unit Economics")
col1, col2 = st.columns(2)

with col1:
    # Loan Waterfall Chart
    fig_waterfall = go.Figure(go.Waterfall(
        name="Unit Economics",
        orientation="v",
        measure=["absolute", "relative", "relative", "total", "total"],
        x=metrics_df['Component'],
        y=metrics_df['Amount'],
        connector={"line": {"color": "rgba(0,0,0,0.3)"}},
        decreasing={"marker": {"color": BRAND_COLORS['secondary']}},
        increasing={"marker": {"color": BRAND_COLORS['primary']}},
        totals={"marker": {"color": BRAND_COLORS['accent1']}}
    ))
    fig_waterfall.update_layout(
        title={
            'text': "Loan Economics Breakdown",
            'font': {'family': 'Space Grotesk', 'size': 20, 'color': '#000000'},
            'y': 0.95
        },
        showlegend=False,
        template='plotly_white',
        height=400,
        margin=dict(l=40, r=40, t=60, b=40),
        paper_bgcolor='#ffffff',
        plot_bgcolor='#ffffff',
        font=dict(
            family='Space Grotesk',
            size=14,
            color='#000000'
        ),
        xaxis=dict(
            gridcolor='rgba(0,0,0,0.1)',
            tickfont=dict(
                family='Space Grotesk',
                size=12,
                color='#000000'
            ),
            title_font=dict(
                size=14,
                color='#000000'
            )
        ),
        yaxis=dict(
            gridcolor='rgba(0,0,0,0.1)',
            tickfont=dict(
                family='Space Grotesk',
                size=12,
                color='#000000'
            ),
            title_font=dict(
                size=14,
                color='#000000'
            ),
            tickformat='$,.0f'
        )
    )
    st.plotly_chart(fig_waterfall, use_container_width=True)

with col2:
    # Loan parameters and staker returns
    st.markdown(f"""
        <div class='info-box'>
        <h3>Loan Parameters</h3>
        • Average Loan Size: ${st.session_state.params['loan_amount']}<br>
        • Loan Term: {st.session_state.params['term_days']} days<br>
        • Interest Rate: {st.session_state.params['interest_rate']*100:.2f}%<br>
        • Origination Fee: {st.session_state.params['origination_fee_pct']*100:.2f}%<br>
        • Revenue Split: {100-st.session_state.model_state['platform_fee']:.1f}% Stakers / {st.session_state.model_state['platform_fee']:.1f}% Platform
        </div>
    """, unsafe_allow_html=True)
    
    # Calculate staker metrics
    staker_cut = safe_get(st.session_state.model_state['metrics'], 'total_fee', 0) * (1 - st.session_state.params['revenue_split_company'])
    staker_yield = (staker_cut / st.session_state.params['loan_amount']) * 100
    monthly_revenue = staker_cut * st.session_state.params['initial_loans_monthly']
    
    st.markdown(f"""
        <div class='info-box'>
        <h3>Staker Returns</h3>
        • Fee per loan: ${staker_cut:.2f}<br>
        • Estimated Annual Yield: {staker_yield:.2f}%<br>
        • Monthly Revenue (initial): ${monthly_revenue:,.2f}<br>
        • Split: {100-st.session_state.model_state['platform_fee']:.1f}% of all fees<br>
        • Additional Income: Uniswap V4 fees
        </div>
    """, unsafe_allow_html=True)

# Add detailed unit economics breakdown
st.subheader("Detailed Unit Economics")
col1, col2 = st.columns(2)

with col1:
    # Per loan breakdown
    interest_fee = safe_get(st.session_state.model_state['metrics'], 'interest_fee', 0)
    origination_fee = safe_get(st.session_state.model_state['metrics'], 'origination_fee', 0)
    total_fee = safe_get(st.session_state.model_state['metrics'], 'total_fee', 0)
    platform_revenue = total_fee * st.session_state.params['revenue_split_company']
    staker_revenue = total_fee * (1 - st.session_state.params['revenue_split_company'])
    
    st.markdown(f"""
        <div class='info-box'>
        <h3>Per Loan Breakdown</h3>
        <table style="width:100%; border-collapse: collapse; font-family: 'Space Grotesk', sans-serif;">
            <tr>
                <td style="padding:8px; border-bottom:1px solid #eee;"><strong>Principal Amount</strong></td>
                <td style="padding:8px; border-bottom:1px solid #eee; text-align:right;">${st.session_state.params['loan_amount']:.2f}</td>
            </tr>
            <tr>
                <td style="padding:8px; border-bottom:1px solid #eee;"><strong>Interest Fee</strong></td>
                <td style="padding:8px; border-bottom:1px solid #eee; text-align:right;">${interest_fee:.2f}</td>
            </tr>
            <tr>
                <td style="padding:8px; border-bottom:1px solid #eee;"><strong>Origination Fee</strong></td>
                <td style="padding:8px; border-bottom:1px solid #eee; text-align:right;">${origination_fee:.2f}</td>
            </tr>
            <tr>
                <td style="padding:8px; border-bottom:1px solid #eee;"><strong>Total Fee</strong></td>
                <td style="padding:8px; border-bottom:1px solid #eee; text-align:right;"><strong>${total_fee:.2f}</strong></td>
            </tr>
            <tr>
                <td style="padding:8px; border-bottom:1px solid #eee;"><strong>Total Repayment</strong></td>
                <td style="padding:8px; border-bottom:1px solid #eee; text-align:right;"><strong>${st.session_state.params['loan_amount'] + total_fee:.2f}</strong></td>
            </tr>
        </table>
        </div>
    """, unsafe_allow_html=True)

with col2:
    # Revenue distribution
    st.markdown(f"""
        <div class='info-box'>
        <h3>Revenue Distribution</h3>
        <table style="width:100%; border-collapse: collapse; font-family: 'Space Grotesk', sans-serif;">
            <tr>
                <td style="padding:8px; border-bottom:1px solid #eee;"><strong>Total Fee per Loan</strong></td>
                <td style="padding:8px; border-bottom:1px solid #eee; text-align:right;">${total_fee:.2f}</td>
            </tr>
            <tr>
                <td style="padding:8px; border-bottom:1px solid #eee;"><strong>Platform Revenue ({st.session_state.model_state['platform_fee']:.1f}%)</strong></td>
                <td style="padding:8px; border-bottom:1px solid #eee; text-align:right;">${platform_revenue:.2f}</td>
            </tr>
            <tr>
                <td style="padding:8px; border-bottom:1px solid #eee;"><strong>Staker Revenue ({100-st.session_state.model_state['platform_fee']:.1f}%)</strong></td>
                <td style="padding:8px; border-bottom:1px solid #eee; text-align:right;">${staker_revenue:.2f}</td>
            </tr>
            <tr>
                <td style="padding:8px; border-bottom:1px solid #eee;"><strong>Fee as % of Principal</strong></td>
                <td style="padding:8px; border-bottom:1px solid #eee; text-align:right;">{total_fee/st.session_state.params['loan_amount']*100:.2f}%</td>
            </tr>
            <tr>
                <td style="padding:8px; border-bottom:1px solid #eee;"><strong>Annualized Yield</strong></td>
                <td style="padding:8px; border-bottom:1px solid #eee; text-align:right;">{staker_yield * (365/st.session_state.params['term_days']):.2f}%</td>
            </tr>
        </table>
        </div>
    """, unsafe_allow_html=True)

# Key metrics for unit economics
st.markdown("""
    <div class='highlight'>
    <h3>Key Unit Economics Metrics</h3>
    <div style="display: flex; flex-wrap: wrap; gap: 20px; justify-content: space-between;">
""", unsafe_allow_html=True)

metrics_col1, metrics_col2, metrics_col3 = st.columns(3)

with metrics_col1:
    custom_metric(
        "Fee per $1 Lent",
        f"${total_fee/st.session_state.params['loan_amount']:.2f}",
        f"{total_fee/st.session_state.params['loan_amount']*100:.1f}%",
        "Fee earned per dollar of principal"
    )
    
with metrics_col2:
    custom_metric(
        "Monthly Revenue per 1K Loans",
        f"${total_fee * 1000:,.0f}",
        f"${platform_revenue * 1000:,.0f} platform",
        "Total monthly revenue from 1,000 loans"
    )
    
with metrics_col3:
    custom_metric(
        "Annual Staker Yield",
        f"{staker_yield * (365/st.session_state.params['term_days']):.1f}%",
        f"{staker_yield:.1f}% per cycle",
        "Annualized yield for stakers"
    )

st.markdown("""
    </div>
    </div>
""", unsafe_allow_html=True)

# Technical Infrastructure
st.header("Technical Infrastructure")
st.markdown("""
    <div class='info-box'>
    <h3>Technology Stack</h3>
    <p><strong>AI-Powered Credit Scoring:</strong> Proprietary ML models for fraud detection</p>
    <p><strong>Biometric Verification:</strong> World ID integration for Sybil resistance</p>
    <p><strong>Blockchain Infrastructure:</strong> Secure, low-cost transactions</p>
    <p><strong>Capital Efficiency:</strong> Optimized liquidity management</p>
    </div>
""", unsafe_allow_html=True)

# Investment Opportunity
st.header("Investment Opportunity")
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div class='info-box'>
        <h3>Investment Thesis</h3>
        <p>• First-mover advantage in AI-powered DeFi microlending</p>
        <p>• Scalable business model with 80% YoY growth</p>
        <p>• Strong unit economics with 17.25% fee per loan</p>
        <p>• Addressing $506B market opportunity by 2030</p>
        </div>
    """, unsafe_allow_html=True)
    
with col2:
    st.markdown("""
        <div class='info-box'>
        <h3>Competitive Moat</h3>
        <p>• Proprietary AI credit scoring technology</p>
        <p>• Biometric verification with 99% fraud reduction</p>
        <p>• Network effects from growing user base (15.4K+)</p>
        <p>• Capital-efficient model with staker incentives</p>
        </div>
    """, unsafe_allow_html=True)

# Investment Terms
st.subheader("Investment Terms")
st.markdown("""
    <div class='highlight' style='background-color: white; border-left: 4px solid #7C3AED;'>
    <h3>Current Round</h3>
    <p style='font-size: 1.2rem;'>
    • <strong>$1.2M Seed Round</strong><br>
    • SAFE notes with 25% discount<br>
    • $100K minimum investment<br>
    • Strategic investors receive advisory roles
    </p>
    </div>

    <div class='info-box'>
    <h3>Allocation of Funds</h3>
    <div style="display: flex; align-items: center; margin-bottom: 1rem;">
        <div style="flex: 1;">
            <div style="height: 24px; background-color: #7C3AED; border-radius: 12px; width: 60%;"></div>
        </div>
        <div style="margin-left: 1rem; flex: 2;">
            <strong>Team Runway (60%)</strong><br>
            $720K - 18-month runway to launch V3 (AI reduces defaults to 5-8%, March 2025) and V4 (global scale, May 2025)
        </div>
    </div>
    
    <div style="display: flex; align-items: center; margin-bottom: 1rem;">
        <div style="flex: 1;">
            <div style="height: 24px; background-color: #9F67FF; border-radius: 12px; width: 20%;"></div>
        </div>
        <div style="margin-left: 1rem; flex: 2;">
            <strong>Liquidity Pool (20%)</strong><br>
            $240K - Seeds liquidity pool for 10,000 loans ($300K total), with $60K from Year 1 fee reinvestment
        </div>
    </div>
    
    <div style="display: flex; align-items: center; margin-bottom: 1rem;">
        <div style="flex: 1;">
            <div style="height: 24px; background-color: #E9D5FF; border-radius: 12px; width: 20%;"></div>
        </div>
        <div style="margin-left: 1rem; flex: 2;">
            <strong>Operations & Growth (20%)</strong><br>
            $240K - Handle compliance, analytics, and maintain flexibility as we grow and learn
        </div>
    </div>
    </div>

    <div class='info-box'>
    <h3>Investment Strategy</h3>
    <p><strong>Low Risk, High Upside:</strong> Only 20% goes to lending—enough to prove demand, not a gamble.</p>
    <p><strong>Team-Driven:</strong> 60% backs our tech crew, turning demand into a rock-solid platform.</p>
    <p><strong>Smart Flexibility:</strong> 20% reserve ensures we adapt to market shifts without stalling.</p>
    <p><strong>Demand Is Our Edge:</strong> Stakers earn 80% of our 17.25% loan fees—your investment funds the ecosystem that delivers these returns.</p>
    </div>
""", unsafe_allow_html=True)

# Call to Action
st.markdown("""
    <div class='highlight'>
    <h3>Next Steps</h3>
    <p>• Download our detailed financial model for comprehensive projections</p>
    <p>• Schedule a meeting with our team to discuss investment opportunities</p>
    <p>• Explore partnership possibilities in emerging markets</p>
    </div>
""", unsafe_allow_html=True)

# Footer with disclaimer
st.markdown("""
    <div style='margin-top: 2rem; padding: 1rem; border-top: 1px solid rgba(0,0,0,0.1); font-size: 0.8rem; color: #6B7280;'>
    <p>This presentation contains forward-looking statements and projections based on current assumptions. 
    Actual results may vary. This is not an offer to sell securities. 
    Please consult the full financial model for detailed assumptions and calculations.</p>
    </div>
""", unsafe_allow_html=True)

# Add the sections at the bottom of the page
st.markdown("""
    <div id="model-parameters" class="section-anchor"></div>
""", unsafe_allow_html=True)

st.header("Model Parameters & Scenario Analysis")
subcol1, subcol2 = st.columns(2)
with subcol1:
    loan_amount = st.number_input(
        "Loan Amount ($)",
        min_value=0.0,
        value=st.session_state.params['loan_amount'],
        step=5.0,
        help="Average loan size (default: $30)"
    )
    if loan_amount != st.session_state.params['loan_amount']:
        st.session_state.params['loan_amount'] = loan_amount
        update_model()
    
    interest_pct = st.slider(
        "Interest Rate (%)",
        min_value=0.0,
        max_value=100.0,
        value=float(st.session_state.params['interest_rate'] * 100),
        step=0.5,
        help="Interest rate charged on loans (default: 18.75%)"
    )
    if interest_pct/100 != st.session_state.params['interest_rate']:
        st.session_state.params['interest_rate'] = interest_pct / 100
        update_model()
    
with subcol2:
    growth_pct = st.slider(
        "First Year Growth Rate (%)",
        min_value=0.0,
        max_value=500.0,
        value=float(st.session_state.params['growth_rate_yearly'][1] * 100),
        step=5.0,
        help="Projected first year growth rate (default: 100%)"
    )
    if growth_pct/100 != st.session_state.params['growth_rate_yearly'][1]:
        st.session_state.params['growth_rate_yearly'][1] = growth_pct / 100
        update_model()
        
    st.markdown("""
        <div style='font-size: 0.9rem; color: #666; margin-top: 0.5rem;'>
        Growth rates for subsequent years:<br>
        • Year 2: 80% growth<br>
        • Year 3: 60% growth<br>
        • Year 4: 45% growth<br>
        • Year 5: No growth
        </div>
    """, unsafe_allow_html=True)
    
    initial_loans = st.number_input(
        "Initial Monthly Loans",
        min_value=0,
        value=st.session_state.params['initial_loans_monthly'],
        step=100,
        help="Monthly loan volume at start (default: 1,000)"
    )
    if initial_loans != st.session_state.params['initial_loans_monthly']:
        st.session_state.params['initial_loans_monthly'] = initial_loans
        update_model()

# Platform fee slider
platform_fee_input = st.slider(
    "Platform Fee (%)",
    min_value=0.0,
    max_value=100.0,
    value=float(st.session_state.params['revenue_split_company'] * 100),
    step=1.0,
    help="Percentage of fees retained by the platform (default: 20%)"
)
if platform_fee_input/100 != st.session_state.params['revenue_split_company']:
    st.session_state.params['revenue_split_company'] = platform_fee_input / 100
    update_model()

# Display split visually
fee_col1, fee_col2 = st.columns(2)
with fee_col1:
    st.markdown(f"""
        <div style='background-color: {BRAND_COLORS['primary']}; color: white; padding: 1rem; border-radius: 12px; text-align: center;'>
        <h4 style='margin:0; color: white;'>Platform: {st.session_state.model_state['platform_fee']:.1f}%</h4>
        </div>
    """, unsafe_allow_html=True)
with fee_col2:
    st.markdown(f"""
        <div style='background-color: {BRAND_COLORS['secondary']}; color: white; padding: 1rem; border-radius: 12px; text-align: center;'>
        <h4 style='margin:0; color: white;'>Stakers: {100-st.session_state.model_state['platform_fee']:.1f}%</h4>
        </div>
    """, unsafe_allow_html=True)

# Scenario section
st.markdown("### Scenario Analysis")
scenario = st.selectbox(
    "Select Scenario",
    ["Current", "Conservative Growth", "Aggressive Growth", "High Yield", "Low Fees"]
)

# Update parameters based on scenario selection
if scenario != "Current":
    params_updated = False
    new_params = st.session_state.params.copy()
    
    if scenario == "Conservative Growth":
        new_params.update({
            'growth_rate_yearly': {
                1: 0.40,
                2: 0.80,
                3: 0.60,
                4: 0.45,
                5: 0.0
            },
            'initial_loans_monthly': 500
        })
        params_updated = True
    elif scenario == "Aggressive Growth":
        new_params.update({
            'growth_rate_yearly': {
                1: 1.20,
                2: 0.80,
                3: 0.60,
                4: 0.45,
                5: 0.0
            },
            'initial_loans_monthly': 2000
        })
        params_updated = True
    elif scenario == "High Yield":
        new_params.update({
            'interest_rate': 0.25,
            'origination_fee_pct': 0.15
        })
        params_updated = True
    elif scenario == "Low Fees":
        new_params.update({
            'interest_rate': 0.15,
            'origination_fee_pct': 0.08
        })
        params_updated = True
        
    if params_updated:
        st.session_state.params = new_params
        update_model()

st.markdown("""
    <div id="export-model" class="section-anchor"></div>
""", unsafe_allow_html=True)

st.header("Export Financial Model")
st.download_button(
    label="Download Investment Deck (Excel)",
    data=excel_data,
    file_name="magnify_cash_financial_model.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

st.markdown("""
    <div class='info-box'>
    <h4>What's Included:</h4>
    • 5-Year Financial Projections<br>
    • Unit Economics Breakdown<br>
    • Investment Metrics & KPIs<br>
    • Staker Economics Analysis<br>
    • Growth Metrics & Assumptions
    </div>
""", unsafe_allow_html=True) 