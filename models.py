import numpy as np
import pandas as pd

class MicrolendingModel:
    """
    A financial model for a decentralized microlending platform.
    
    This class implements the core financial calculations and projections for the
    microlending platform, including loan metrics, volume projections, and financial
    analysis.
    
    Attributes:
        params (dict): Configuration parameters for the model including:
            - loan_amount (float): Principal amount of each loan
            - term_days (int): Duration of each loan in days
            - interest_rate (float): Interest rate per loan term
            - origination_fee_pct (float): Origination fee as percentage of principal
            - revenue_split_company (float): Platform's share of revenue (0-1)
            - growth_rate_yearly (dict): Annual growth rates by year
            - initial_loans_monthly (int): Starting monthly loan volume
    """
    
    def __init__(self, params):
        """
        Initialize the MicrolendingModel with configuration parameters.
        
        Args:
            params (dict): Model configuration parameters
        """
        self.params = params
        
    def calculate_loan_metrics(self):
        """
        Calculate basic loan-level metrics for a single loan.
        
        Computes fees, revenue splits, and other key metrics for an individual loan
        based on the configured parameters.
        
        Returns:
            dict: Dictionary containing:
                - interest_fee (float): Interest charged per loan
                - origination_fee (float): Origination fee per loan
                - total_fee (float): Total fees per loan
                - company_revenue (float): Platform's revenue per loan
                - staker_revenue (float): Stakers' revenue per loan
                - apr (float): Annualized percentage rate
        """
        interest_fee = self.params['loan_amount'] * self.params['interest_rate']
        origination_fee = self.params['loan_amount'] * self.params['origination_fee_pct']
        total_fee = interest_fee + origination_fee
        company_revenue = total_fee * self.params['revenue_split_company']
        staker_revenue = total_fee * (1 - self.params['revenue_split_company'])
        
        return {
            'interest_fee': interest_fee,
            'origination_fee': origination_fee,
            'total_fee': total_fee,
            'company_revenue': company_revenue,
            'staker_revenue': staker_revenue,
            'apr': (total_fee / self.params['loan_amount']) * (365 / self.params['term_days'])
        }
    
    def project_volumes(self, months=60):
        """
        Project loan volumes over a specified time period.
        
        Calculates monthly loan volumes based on initial volume and configured
        growth rates. Growth is applied at the end of each year.
        
        Args:
            months (int): Number of months to project (default: 60)
            
        Returns:
            pandas.DataFrame: DataFrame containing:
                - month: Month number (0-based)
                - loan_volume: Projected number of loans for each month
        """
        volumes = []
        current_volume = self.params['initial_loans_monthly']
        
        for month in range(months):
            volumes.append(current_volume)
            
            year = month // 12 + 1  # 1-based year
            month_in_year = month % 12
            
            # Only apply growth at the end of each year
            if month_in_year == 11 and year in self.params['growth_rate_yearly']:
                growth_rate = self.params['growth_rate_yearly'][year]
                current_volume = int(current_volume * (1 + growth_rate))
        
        return pd.DataFrame({
            'month': np.arange(months),
            'loan_volume': volumes
        })
    
    def project_financials(self, months=60):
        """
        Generate detailed financial projections.
        
        Combines loan metrics with volume projections to create comprehensive
        financial projections including revenue, fees, and cumulative metrics.
        
        Args:
            months (int): Number of months to project (default: 60)
            
        Returns:
            pandas.DataFrame: DataFrame containing monthly projections:
                - month: Month number
                - loan_volume: Number of loans
                - total_loan_value: Total principal lent
                - total_fees: Total fees generated
                - company_revenue: Platform revenue
                - staker_revenue: Staker revenue
                - cumulative_* metrics: Running totals
        """
        volumes_df = self.project_volumes(months)
        metrics = self.calculate_loan_metrics()
        
        df = volumes_df.copy()
        df['total_loan_value'] = df['loan_volume'] * self.params['loan_amount']
        df['total_fees'] = df['loan_volume'] * metrics['total_fee']
        df['company_revenue'] = df['loan_volume'] * metrics['company_revenue']
        df['staker_revenue'] = df['loan_volume'] * metrics['staker_revenue']
        
        # Calculate cumulative metrics
        df['cumulative_loans'] = df['loan_volume'].cumsum()
        df['cumulative_company_revenue'] = df['company_revenue'].cumsum()
        df['cumulative_staker_revenue'] = df['staker_revenue'].cumsum()
        
        return df
    
    def compare_to_payday(self, loan_amount=None):
        """
        Compare platform economics to traditional payday lenders.
        
        Calculates fees and APRs for both the platform and typical payday loans
        to demonstrate cost savings for borrowers.
        
        Args:
            loan_amount (float, optional): Override default loan amount
            
        Returns:
            dict: Comparison metrics including:
                - platform_fee: Total platform fees
                - platform_apr: Platform's APR
                - payday_fee: Typical payday loan fee
                - payday_apr: Typical payday loan APR
                - consumer_savings: Amount saved vs payday loan
        """
        if loan_amount is None:
            loan_amount = self.params['loan_amount']
            
        # Typical payday loan terms (can be adjusted)
        payday_fee_per_100 = 15
        payday_fee = (loan_amount / 100) * payday_fee_per_100
        
        platform_metrics = self.calculate_loan_metrics()
        
        return {
            'platform_fee': platform_metrics['total_fee'],
            'platform_apr': platform_metrics['apr'],
            'payday_fee': payday_fee,
            'payday_apr': (payday_fee / loan_amount) * (365 / self.params['term_days']),
            'consumer_savings': payday_fee - platform_metrics['total_fee']
        }
    
    def calculate_staker_metrics(self):
        """
        Calculate staker-specific metrics.
        
        Computes key metrics for stakers including required capital, revenue,
        and yield calculations.
        
        Returns:
            dict: Staker metrics including:
                - required_staking: Capital required from stakers
                - monthly_staker_revenue: Monthly revenue for stakers
                - annual_staker_revenue: Annual revenue for stakers
                - staker_yield: Annualized yield for stakers
                - capital_efficiency: Ratio of loans to staked capital
        """
        metrics = self.calculate_loan_metrics()
        
        # Calculate required staking capital (assume 2x coverage of monthly loan volume)
        monthly_loan_value = self.params['initial_loans_monthly'] * self.params['loan_amount']
        required_staking = monthly_loan_value * 2
        
        # Calculate annual yield
        annual_staker_revenue = metrics['staker_revenue'] * self.params['initial_loans_monthly'] * 12
        staker_yield = annual_staker_revenue / required_staking
        
        return {
            'required_staking': required_staking,
            'monthly_staker_revenue': metrics['staker_revenue'] * self.params['initial_loans_monthly'],
            'annual_staker_revenue': annual_staker_revenue,
            'staker_yield': staker_yield,
            'capital_efficiency': monthly_loan_value / required_staking
        }
    
    def calculate_investment_metrics(self):
        """
        Calculate key investment metrics.
        
        Computes important metrics for investors including revenue growth,
        CAGR, and unit economics.
        
        Returns:
            dict: Investment metrics including:
                - year_1_revenue: First year platform revenue
                - year_5_revenue: Fifth year platform revenue
                - revenue_cagr: Compound annual growth rate
                - gross_margin: Platform's gross margin
                - unit_economics: Revenue per dollar of fees
                - year_5_loan_volume: Annual loan volume in year 5
        """
        metrics = self.calculate_loan_metrics()
        projections = self.project_financials()
        
        # Calculate key metrics
        year_1_revenue = projections['company_revenue'].head(12).sum()
        year_5_revenue = projections['company_revenue'].tail(12).sum()
        cagr = (year_5_revenue / year_1_revenue)**(1/4) - 1
        
        return {
            'year_1_revenue': year_1_revenue,
            'year_5_revenue': year_5_revenue,
            'revenue_cagr': cagr,
            'gross_margin': 1.0,  # Platform takes no direct costs
            'unit_economics': metrics['company_revenue'] / metrics['total_fee'],
            'year_5_loan_volume': projections['loan_volume'].tail(12).sum()
        } 