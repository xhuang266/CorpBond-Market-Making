import pandas as pd
import numpy as np
import os
from src.models import MarketMicrostructureParams
from src.backtest import run_batch_backtest, generate_visual_report
from src.pricing_system import RFQPricingSystem

def main():
    # =========================================================================
    # 1. DATA LOADING & PREPARATION
    # =========================================================================
    # Adjust the path to where your rfq_data.csv is located
    data_path = r"D:/quant/BondMarketMaking/data/rfq_data.csv"
    
    if not os.path.exists(data_path):
        print(f"Error: Data file not found at {data_path}")
        return

    df_active = pd.read_csv(data_path)
    
    # =========================================================================
    # 2. PARAMETER CONFIGURATION (Market Microstructure Settings)
    # =========================================================================
    # These parameters define the Market Maker's risk appetite and the environment.
    my_params = MarketMicrostructureParams(
        gamma=0.001,   # Risk Aversion: Higher values mean faster inventory unloading.
        A=0.5,         # Order Intensity: Base rate of incoming orders.
        k_paper=1.0,   # Demand Decay: Client price sensitivity (Higher = more picky).
        beta_0=0.0,    # Intercept for fill probability (Sigmoid(0) = 50%).
        beta_1=-0.5,   # Price Sensitivity: Prob decreases as spread widens.
        beta_2=-0.0001 # Size Sensitivity: Larger orders are harder to fill.
    )

    # =========================================================================
    # 3. BACKTEST EXECUTION
    # =========================================================================
    print("\n" + "="*60)
    print("LOG: Starting Event-Driven Batch Backtest...")
    print("="*60)
    
    # Executing the simulation across all CUSIPs in the dataset
    report = run_batch_backtest(df_active, my_params)
    
    # Print the detailed breakdown for each bond (CUSIP)
    print("\n--- Detailed Backtest Report (Per Bond) ---")
    print(report)

    # =========================================================================
    # 4. PERFORMANCE SUMMARY
    # =========================================================================
    print("\n" + "="*60)
    print("            FINAL BACKTEST PERFORMANCE SUMMARY            ")
    print("="*60)
    print(f"💰 Total PnL (Realized + MtM):     ${report['total_pnl'].sum():,.2f}")
    print(f"📊 Avg PnL per Bond:               ${report['total_pnl'].mean():,.2f}")
    print(f"🔄 Avg Inventory Turnover:         {report['turnover_ratio'].mean():.2f}x")
    print(f"🎯 Avg Capture Rate (Hit Ratio):   {report['capture_rate'].mean()*100:.2f}%")
    print(f"🎯 Avg Captured Slippage (bps):    {report['avg_slippage_bps'].mean():.2f}")
    print("="*60)

    # =========================================================================
    # 5. VISUALIZATION
    # =========================================================================
    print("\nLOG: Generating visual analytics...")
    generate_visual_report(df_active, report)

    # =========================================================================
    # 6. LIVE QUOTE SIMULATION (Single RFQ Test Case)
    # =========================================================================
    print("\n" + "="*60)
    print("--- INDUSTRIAL PRICING ENGINE: SINGLE RFQ SIMULATION ---")
    print("="*60)
    
    # Simulating a typical WRDS bond data row
    sample_row = pd.Series({
        'cusip_id': '369604BV2',
        'pr': 100.25,      # Current Mid Price
        'mod_dur': 5.5,    # Modified Duration
        'prc_hi': 100.50,  # Intraday High for Vol Calculation
        'prc_lo': 100.00,  # Intraday Low
        'qvolume': 5000.0, # ADV in Millions
    })

    # Initialize a pricer with a specific inventory position (e.g., Long 50 units)
    # Using slightly different params for this specific simulation to show sensitivity
    sim_params = MarketMicrostructureParams(
        gamma=0.01, A=0.9, k_paper=0.3, 
        beta_0=2.0, beta_1=-0.5, beta_2=-0.0001
    )

    # Instantiate the pricing system with 50 units of current inventory
    pricer = RFQPricingSystem(sim_params, current_inventory=50.0)

    # Client sends an RFQ: "I want to BUY 2,000 units" (Dealer Sells)
    result = pricer.get_rfq_price(sample_row, rfq_size=2000, client_side='BUY')

    print(f"Simulation Setup: Current Inventory = 50.0 units, Client Side = BUY")
    print("-" * 30)
    for key, value in result.items():
        if isinstance(value, float):
            print(f"{key:20}: {value:>12.4f}")
        else:
            print(f"{key:20}: {value:>12}")

if __name__ == "__main__":
    main()