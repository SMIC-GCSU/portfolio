# SMIC Portfolio Analysis

Open source portfolio analysis and tracking software built by Joel Saucedo for the Student Managed Investment Committee (SMIC) at Georgia College & State University. This application provides comprehensive portfolio performance analysis, sector allocation tracking, and interactive visualizations for managing the university endowment fund with an initial investment of $100,000.

## Project Overview

The SMIC Portfolio Analysis system simulates a portfolio that starts with 100% Vanguard sector ETFs (equal-weighted across 11 sectors) and allows strategic swaps from ETFs to individual stocks within each sector. The system tracks portfolio performance, sector drift, and provides detailed analytics against the S&P 500 benchmark.

## Key Features

- **Portfolio Simulation**: Realistic modeling of ETF-to-stock swaps with natural sector weight drift
- **Performance Analytics**: Comprehensive metrics including CAGR, total returns, drawdowns, and sector allocation changes
- **Interactive Visualizations**: Professional Plotly charts for portfolio value, sector allocation, and performance comparisons
- **Cross-Platform Executables**: Standalone applications for Windows, macOS, and Linux (no Python required)
- **Automated Builds**: CI/CD pipeline via GitHub Actions for all platforms
- **Transaction Management**: Easy-to-use GUI for adding and managing portfolio transactions

## Mathematical Model

### Portfolio Construction

The portfolio simulation follows a realistic drift model:

1. **Initial State**: Portfolio starts with 100% allocation to 11 Vanguard sector ETFs, equal-weighted (9.09% each), representing the initial $100,000 university endowment investment
2. **ETF-to-Stock Swaps**: When a stock is purchased:
   - The corresponding sector ETF is sold (dollar-neutral swap)
   - The stock is purchased with the same dollar amount
   - Sector weight remains constant at the moment of swap
3. **Natural Drift**: After swaps, sector weights drift naturally based on relative performance of:
   - Remaining ETF holdings
   - Individual stock holdings
   - No rebalancing occurs (realistic buy-and-hold approach)

### Performance Calculations

**Portfolio Value**:
```
Portfolio_Value(t) = Σ(units_i(t) × price_i(t)) + Cash
```

**Cumulative Returns**:
```
Cumulative_Return(t) = (Portfolio_Value(t) / Portfolio_Value(0) - 1) × 100%
```

**CAGR (Compound Annual Growth Rate)**:
```
CAGR = (Final_Value / Initial_Value)^(1/years) - 1
```

**Sector Weights**:
```
Sector_Weight_i(t) = (Sector_Value_i(t) / Total_Portfolio_Value(t)) × 100%
```

Where:
- `Sector_Value_i(t)` = ETF value + sum of individual stock values in sector i
- Weights are calculated daily and naturally drift based on relative performance

### Benchmark Comparison

The S&P 500 (^GSPC) is used as the benchmark, normalized to the portfolio's initial value:
```
Benchmark_Value(t) = (S&P500_Price(t) / S&P500_Price(0)) × Initial_Portfolio_Value
```

This allows for direct dollar-for-dollar comparison while maintaining percentage return accuracy.

## Project Achievements

### Technical Achievements

**Automated Cross-Platform Builds**: Successfully implemented GitHub Actions workflows that automatically build executables for Windows, macOS, and Linux on every push

**Professional GUI Application**: Developed a polished PySide6-based desktop application with interactive Plotly visualizations

**Accurate Portfolio Simulation**: Implemented realistic portfolio modeling with proper handling of:
- ETF-to-stock swaps
- Natural sector weight drift
- Cash and fixed income allocations
- Daily portfolio valuation

**Comprehensive Analytics**: Built robust analysis engine that calculates:
- Portfolio performance metrics (CAGR, total returns, drawdowns)
- Sector allocation tracking over time
- ETF vs. individual stock breakdowns
- YTD and full-period comparisons

**Production-Ready Packaging**: Created PyInstaller spec file with proper dependency collection, resulting in self-contained executables (~300-400MB)

### Performance Metrics

- **Build Success Rate**: 100% across all platforms (Windows, macOS, Linux)
- **Code Quality**: Modular architecture with separation of concerns (GUI, analysis, data)
- **User Experience**: Intuitive interface with real-time analysis and interactive charts

## Getting Started

### Prerequisites

- Python 3.8+ (for development)
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/joel-saucedo/SMIC-Portfolio-Analysis.git
cd SMIC-Portfolio-Analysis
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main_app.py
```

### Using Pre-built Executables

Download the latest executables from [GitHub Actions](https://github.com/joel-saucedo/SMIC-Portfolio-Analysis/actions):
- Look for the "SMIC_Portfolio_Analysis-Downloads" artifact
- Extract and run the executable for your platform
- No Python installation required!

## Project Structure

```
SMIC/
├── main_app.py              # GUI application (PySide6)
├── analysis_core.py         # Core portfolio analysis engine
├── smic.py                  # Standalone analysis script
├── requirements.txt         # Python dependencies
├── SMIC_Portfolio_Analysis.spec  # PyInstaller configuration
├── data/
│   ├── transactions.csv     # Portfolio transaction data
│   └── *.csv                # Generated analysis reports
├── figs/                    # Generated charts (from smic.py)
├── .github/
│   └── workflows/           # CI/CD build workflows
└── build_executable*.sh     # Platform-specific build scripts
```

## Development

### Building Executables Locally

**Linux/macOS**:
```bash
./build_executable.sh        # Linux
./build_executable_macos.sh  # macOS
```

**Windows**:
```cmd
build_executable_windows.bat
```

### Running Analysis

The core analysis can be run independently:
```python
from analysis_core import generate_portfolio_analysis

report, figures, summary_df, ytd_df = generate_portfolio_analysis()
print(report)
```

## Future Development

We are actively working on implementing the following features to enhance the portfolio management capabilities:

### Planned Features

- **Rebalancing Functionality**: Automated rebalancing to target sector allocations with configurable thresholds
- **Stock Selling**: Support for selling individual positions with proper tracking of realized gains/losses
- **Tax-Loss Harvesting**: Identification of tax-loss harvesting opportunities
- **Advanced Analytics**: 
  - Risk metrics (Sharpe ratio, Sortino ratio, beta)
  - Correlation analysis between sectors
  - Attribution analysis (ETF vs. stock performance contribution)
- **Portfolio Optimization**: 
  - Efficient frontier analysis
  - Sector allocation optimization
  - Risk-adjusted return maximization
- **Reporting Enhancements**:
  - Automated PDF report generation
  - Email notifications for significant portfolio changes
  - Customizable report templates
- **Data Integration**:
  - Real-time price updates
  - Dividend tracking and reinvestment
  - Corporate action handling (splits, mergers)

### Contributing

We welcome contributions! Please see our development guidelines and feel free to submit pull requests or open issues for bugs and feature requests.

## Documentation

- **Packaging Guide**: See `PACKAGING.md` for detailed instructions on building executables
- **API Documentation**: Code is well-commented with docstrings explaining key functions
- **Workflow Documentation**: GitHub Actions workflows are documented inline

## License

This project is open source software developed for the Student Managed Investment Committee at Georgia College & State University. See LICENSE file for details.

## Author

**Joel Saucedo**  
Developer and maintainer of SMIC Portfolio Analysis

## Acknowledgments

- **Vanguard ETFs**: Sector-based ETF tracking
- **yfinance**: Market data retrieval
- **Plotly**: Interactive visualizations
- **PySide6**: Cross-platform GUI framework
- **Student Managed Investment Committee**: Georgia College & State University

## Support

For questions, issues, or contributions, please visit the [GitHub repository](https://github.com/joel-saucedo/SMIC-Portfolio-Analysis) or contact the development team.

---

**Last Updated**: November 2025  
**Version**: 1.0.0  
**Status**: Active Development
