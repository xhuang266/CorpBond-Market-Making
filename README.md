# Automated Corporate Bond Market Making via Stochastic Optimal Control

This project implements an **Event-Driven RFQ (Request for Quote) Quoting Engine** specifically designed for the US Corporate Bond market. The system leverages the **Guéant-Lehalle-Tapia (2013)** framework to provide liquidity while dynamically managing inventory risk in a fragmented, illiquid environment.

---

## 🚀 Key Features

Beyond the theoretical framework, this engine incorporates several "production-grade" enhancements to handle real-world trading constraints:

* **Dynamic Inventory Skewing:** Implements the closed-form solution for stochastic optimal control to calculate the optimal price deviation (skew) based on current position and risk aversion ($\gamma$).
* **Microstructure-Adjusted Pricing:**
    * **Square-Root Impact Law:** Quantifies the liquidity premium required for large block trades relative to Average Daily Volume (ADV).
    * **Logistic Execution Model:** Calibrates fill probability ($P_{fill}$) based on spread width and order size to prevent "quoting out of the market."
* **Robust Safety Valves:**
    * **Inventory Dampening:** Prevents "Panic Pricing" by clipping extreme inventory inputs, ensuring the model stays competitive even during high exposure.
    * **Volatility-Linked Stop-Loss:** Implements a dynamic "Maximum Give-up" floor based on real-time volatility to protect the book during regime shifts.

---

## 📂 Project Structure

```text
BondMarketMaking/
├── data/                    # Historical trade data (e.g., rfq_data.csv)
├── src/                     # Core Source Code
│   ├── __init__.py
│   ├── models.py            # Data structures & Market Microstructure parameters
│   ├── engines.py           # Mathematical engines (Guéant & Execution logic)
│   ├── pricing_system.py    # Logic aggregator & business rule integration
│   └── backtest.py          # Event-driven simulator & visualization suite
├── main.py                  # Entry point for running the full simulation
└── requirements.txt         # Dependency list (numpy, pandas, matplotlib, seaborn)