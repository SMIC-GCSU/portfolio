#!/usr/bin/env python3
"""
Generate static HTML website for GitHub Pages
Creates an interactive web dashboard with all portfolio analysis
"""

import os
import json
from datetime import datetime
import numpy as np
import pandas as pd
from analysis_core import generate_portfolio_analysis, generate_comparison_plot

class NumpyEncoder(json.JSONEncoder):
    """Custom JSON encoder for numpy arrays and pandas objects"""
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, (np.integer, np.floating)):
            return obj.item()
        if isinstance(obj, pd.Timestamp):
            return obj.strftime('%Y-%m-%d')
        if isinstance(obj, (pd.Series, pd.Index)):
            return obj.tolist()
        return super().default(obj)

def generate_website():
    """Generate complete static website for GitHub Pages"""
    
    # Create docs directory for GitHub Pages
    docs_dir = 'docs'
    os.makedirs(docs_dir, exist_ok=True)
    
    print("Generating portfolio analysis...")
    report_text, figures, summary_df, ytd_df, returns_data = generate_portfolio_analysis('data/transactions.csv')
    
    # Convert all main charts to JSON format for client-side rendering
    charts_data = {}
    for fig_name, fig in figures.items():
        fig_dict = fig.to_dict()
        charts_data[fig_name] = json.loads(json.dumps({
            'data': fig_dict['data'],
            'layout': fig_dict['layout']
        }, cls=NumpyEncoder))
    
    # Generate comparison charts for each sector
    comparison_charts_data = {}
    available_sectors = list(returns_data.get('sector_returns', {}).keys())
    
    for sector in available_sectors:
        # General period
        fig_gen = generate_comparison_plot(
            returns_data, sector=sector, 
            comparison_type='ETF_vs_Stocks', 
            period='General',
            transaction_dates=returns_data.get('transaction_dates', {})
        )
        # Store as JSON data for client-side rendering
        fig_dict_gen = fig_gen.to_dict()
        # Convert numpy arrays and timestamps to JSON-serializable format
        comparison_charts_data[f'{sector}_general'] = json.loads(json.dumps({
            'data': fig_dict_gen['data'],
            'layout': fig_dict_gen['layout']
        }, cls=NumpyEncoder))
        
        # YTD period
        fig_ytd = generate_comparison_plot(
            returns_data, sector=sector,
            comparison_type='ETF_vs_Stocks',
            period='YTD',
            transaction_dates=returns_data.get('transaction_dates', {})
        )
        fig_dict_ytd = fig_ytd.to_dict()
        comparison_charts_data[f'{sector}_ytd'] = json.loads(json.dumps({
            'data': fig_dict_ytd['data'],
            'layout': fig_dict_ytd['layout']
        }, cls=NumpyEncoder))
    
    # Equity vs S&P 500
    fig_equity_gen = generate_comparison_plot(
        returns_data, comparison_type='Equity_vs_SP500', 
        period='General', transaction_dates=returns_data.get('transaction_dates', {})
    )
    fig_dict_equity_gen = fig_equity_gen.to_dict()
    comparison_charts_data['equity_general'] = json.loads(json.dumps({
        'data': fig_dict_equity_gen['data'],
        'layout': fig_dict_equity_gen['layout']
    }, cls=NumpyEncoder))
    
    fig_equity_ytd = generate_comparison_plot(
        returns_data, comparison_type='Equity_vs_SP500',
        period='YTD', transaction_dates=returns_data.get('transaction_dates', {})
    )
    fig_dict_equity_ytd = fig_equity_ytd.to_dict()
    comparison_charts_data['equity_ytd'] = json.loads(json.dumps({
        'data': fig_dict_equity_ytd['data'],
        'layout': fig_dict_equity_ytd['layout']
    }, cls=NumpyEncoder))
    
    # Prepare summary data as JSON
    summary_json = summary_df.to_dict('records')
    ytd_json = ytd_df.to_dict('records')
    
    # Get current date
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Create main index.html
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SMIC Portfolio Analysis - GCSU</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: #f5f7fa;
            color: #1a1a1a;
            line-height: 1.6;
            margin: 0;
            padding: 0;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 40px 20px;
        }}
        header {{
            background: #ffffff;
            padding: 40px;
            margin-bottom: 30px;
            border-bottom: 1px solid #e1e8ed;
        }}
        h1 {{
            color: #1a1a1a;
            margin: 0 0 8px 0;
            font-size: 2em;
            font-weight: 600;
            letter-spacing: -0.5px;
        }}
        .subtitle {{
            color: #657786;
            font-size: 1em;
            margin: 0;
            font-weight: 400;
        }}
        .last-updated {{
            color: #aab8c2;
            font-size: 0.85em;
            margin-top: 12px;
        }}
        .tabs {{
            display: flex;
            background: #ffffff;
            border-bottom: 1px solid #e1e8ed;
            overflow-x: auto;
        }}
        .tab {{
            padding: 16px 24px;
            cursor: pointer;
            border: none;
            background: transparent;
            font-size: 0.95em;
            font-weight: 500;
            color: #657786;
            transition: all 0.2s;
            border-bottom: 2px solid transparent;
            white-space: nowrap;
        }}
        .tab:hover {{
            color: #1a1a1a;
            background: #f7f9fa;
        }}
        .tab.active {{
            color: #1a1a1a;
            border-bottom: 2px solid #1a1a1a;
        }}
        .tab-content {{
            display: none;
            background: #ffffff;
            padding: 40px;
            margin-bottom: 30px;
            border: 1px solid #e1e8ed;
            border-top: none;
        }}
        .tab-content.active {{
            display: block;
        }}
        .chart-container {{
            margin: 30px 0;
            background: #ffffff;
            padding: 0;
        }}
        .chart-container h3 {{
            margin: 0 0 20px 0;
            color: #1a1a1a;
            font-size: 1.25em;
            font-weight: 600;
        }}
        .report-box {{
            background: #f7f9fa;
            padding: 24px;
            font-family: 'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', monospace;
            white-space: pre-wrap;
            margin: 20px 0;
            border: 1px solid #e1e8ed;
            font-size: 0.9em;
            line-height: 1.8;
            color: #1a1a1a;
        }}
        .summary-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 0.95em;
        }}
        .summary-table th, .summary-table td {{
            padding: 14px 16px;
            text-align: left;
            border-bottom: 1px solid #e1e8ed;
        }}
        .summary-table th {{
            background: #f7f9fa;
            color: #1a1a1a;
            font-weight: 600;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .summary-table tr:hover {{
            background: #f7f9fa;
        }}
        .summary-table td {{
            color: #657786;
        }}
        .comparison-controls {{
            background: #f7f9fa;
            padding: 24px;
            margin-bottom: 24px;
            border: 1px solid #e1e8ed;
        }}
        .control-group {{
            margin: 16px 0;
            display: flex;
            align-items: center;
        }}
        .control-group label {{
            display: inline-block;
            width: 140px;
            font-weight: 500;
            color: #1a1a1a;
            font-size: 0.95em;
        }}
        .control-group select {{
            padding: 10px 16px;
            border: 1px solid #e1e8ed;
            background: #ffffff;
            font-size: 0.95em;
            min-width: 280px;
            color: #1a1a1a;
            cursor: pointer;
        }}
        .control-group select:focus {{
            outline: none;
            border-color: #1a1a1a;
        }}
        footer {{
            text-align: center;
            padding: 40px 20px;
            color: #657786;
            margin-top: 60px;
            font-size: 0.9em;
        }}
        @media (max-width: 768px) {{
            .container {{
                padding: 10px;
            }}
            h1 {{
                font-size: 1.8em;
            }}
            .tab {{
                padding: 10px 15px;
                font-size: 0.9em;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>SMIC Portfolio Analysis</h1>
            <p class="subtitle">Student Managed Investment Committee - Georgia College & State University</p>
            <p class="last-updated">Last Updated: {current_date}</p>
        </header>
        
        <div class="tabs">
            <button class="tab active" onclick="showTab('overview')">Overview</button>
            <button class="tab" onclick="showTab('performance')">Performance</button>
            <button class="tab" onclick="showTab('sector-allocation')">Sector Allocation</button>
            <button class="tab" onclick="showTab('comparisons')">Returns Comparisons</button>
            <button class="tab" onclick="showTab('statistics')">Statistics</button>
        </div>
        
        <div id="overview" class="tab-content active">
            <h2>Portfolio Overview</h2>
            <div class="report-box">{report_text}</div>
            
            <div class="chart-container">
                <h3>Portfolio Performance</h3>
                <div id="chart-performance" style="min-height: 800px;"></div>
            </div>
        </div>
        
        <div id="performance" class="tab-content">
            <div class="chart-container">
                <h3>Portfolio Value Over Time</h3>
                <div id="chart-performance-2" style="min-height: 800px;"></div>
            </div>
            
            <div class="chart-container">
                <h3>Sector Weight Drift</h3>
                <div id="chart-weight-drift" style="min-height: 600px;"></div>
            </div>
        </div>
        
        <div id="sector-allocation" class="tab-content">
            <div class="chart-container">
                <h3>Sector Allocation Over Time</h3>
                <div id="chart-sector-allocation" style="min-height: 600px;"></div>
            </div>
            
            <div class="chart-container">
                <h3>ETF vs Individual Stocks Breakdown</h3>
                <div id="chart-etf-vs-stocks" style="min-height: 800px;"></div>
            </div>
            
            <div class="chart-container">
                <h3>Final Allocation: ETF vs Stocks</h3>
                <div id="chart-bar-comparison" style="min-height: 600px;"></div>
            </div>
        </div>
        
        <div id="comparisons" class="tab-content">
            <div class="comparison-controls">
                <div class="control-group">
                    <label>Comparison Type:</label>
                    <select id="comparison-type" onchange="updateComparisonChart()">
                        <option value="ETF_vs_Stocks">ETF vs Stocks (Sector)</option>
                        <option value="Equity_vs_SP500">Equity Portfolio vs S&P 500</option>
                    </select>
                </div>
                <div class="control-group" id="sector-control">
                    <label>Sector:</label>
                    <select id="sector-select" onchange="updateComparisonChart()">
                        {' '.join([f'<option value="{s}">{s}</option>' for s in available_sectors])}
                    </select>
                </div>
                <div class="control-group">
                    <label>Period:</label>
                    <select id="period-select" onchange="updateComparisonChart()">
                        <option value="General">General (Since Beginning)</option>
                        <option value="YTD">Year to Date (YTD)</option>
                    </select>
                </div>
            </div>
            
            <div class="chart-container">
                <h3 id="comparison-title">Returns Comparison</h3>
                <div id="comparison-chart" style="min-height: 600px;">
                    <!-- Chart will be rendered here by JavaScript -->
                </div>
            </div>
        </div>
        
        <div id="statistics" class="tab-content">
            <h2>Performance Statistics</h2>
            <table class="summary-table">
                <thead>
                    <tr>
                        <th>Metric</th>
                        <th>Value</th>
                    </tr>
                </thead>
                <tbody>
                    {' '.join([f'<tr><td>{row["Metric"]}</td><td>{row["Value"]}</td></tr>' for row in summary_json])}
                </tbody>
            </table>
            
            <h2 style="margin-top: 40px;">YTD Sector Breakdown</h2>
            <table class="summary-table">
                <thead>
                    <tr>
                        <th>Sector</th>
                        <th>ETF Weight Start</th>
                        <th>ETF Weight End</th>
                        <th>Stocks Weight Start</th>
                        <th>Stocks Weight End</th>
                        <th>Total Sector Start</th>
                        <th>Total Sector End</th>
                    </tr>
                </thead>
                <tbody>
                    {' '.join([f'''<tr>
                        <td>{row['Sector']}</td>
                        <td>{row.get('ETF_Weight_Start (%)', 'N/A')}%</td>
                        <td>{row.get('ETF_Weight_End (%)', 'N/A')}%</td>
                        <td>{row.get('Stocks_Weight_Start (%)', 'N/A')}%</td>
                        <td>{row.get('Stocks_Weight_End (%)', 'N/A')}%</td>
                        <td>{row.get('Total_Sector_Start (%)', 'N/A')}%</td>
                        <td>{row.get('Total_Sector_End (%)', 'N/A')}%</td>
                    </tr>''' for row in ytd_json])}
                </tbody>
            </table>
        </div>
        
        <footer>
            <p>SMIC Portfolio Analysis - Georgia College & State University</p>
            <p>Official portfolio analysis and tracking software for the Student Managed Investment Committee</p>
        </footer>
    </div>
    
    <script>
        // Tab switching
        function showTab(tabName) {{
            // Hide all tabs
            document.querySelectorAll('.tab-content').forEach(tab => {{
                tab.classList.remove('active');
            }});
            document.querySelectorAll('.tab').forEach(tab => {{
                tab.classList.remove('active');
            }});
            
            // Show selected tab
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
        }}
        
        // Main charts data (embedded in page as JSON)
        const chartsData = {json.dumps(charts_data)};
        
        // Comparison chart data (embedded in page as JSON)
        const comparisonChartsData = {json.dumps(comparison_charts_data)};
        let currentComparisonChartId = null;
        
        // Render main charts on page load
        function renderMainCharts() {{
            if (!window.Plotly) {{
                setTimeout(renderMainCharts, 100);
                return;
            }}
            
            // Render performance chart
            if (chartsData.performance) {{
                Plotly.newPlot('chart-performance', chartsData.performance.data, chartsData.performance.layout, {{
                    responsive: true,
                    displayModeBar: true
                }});
                Plotly.newPlot('chart-performance-2', chartsData.performance.data, chartsData.performance.layout, {{
                    responsive: true,
                    displayModeBar: true
                }});
            }}
            
            // Render weight drift chart
            if (chartsData.weight_drift) {{
                Plotly.newPlot('chart-weight-drift', chartsData.weight_drift.data, chartsData.weight_drift.layout, {{
                    responsive: true,
                    displayModeBar: true
                }});
            }}
            
            // Render sector allocation chart
            if (chartsData.sector_allocation) {{
                Plotly.newPlot('chart-sector-allocation', chartsData.sector_allocation.data, chartsData.sector_allocation.layout, {{
                    responsive: true,
                    displayModeBar: true
                }});
            }}
            
            // Render ETF vs stocks chart
            if (chartsData.etf_vs_stocks) {{
                Plotly.newPlot('chart-etf-vs-stocks', chartsData.etf_vs_stocks.data, chartsData.etf_vs_stocks.layout, {{
                    responsive: true,
                    displayModeBar: true
                }});
            }}
            
            // Render bar comparison chart
            if (chartsData.bar_comparison) {{
                Plotly.newPlot('chart-bar-comparison', chartsData.bar_comparison.data, chartsData.bar_comparison.layout, {{
                    responsive: true,
                    displayModeBar: true
                }});
            }}
        }}
        
        function updateComparisonChart() {{
            const comparisonType = document.getElementById('comparison-type').value;
            const sectorSelect = document.getElementById('sector-select');
            const period = document.getElementById('period-select').value;
            const sectorControl = document.getElementById('sector-control');
            const chartContainer = document.getElementById('comparison-chart');
            const chartTitle = document.getElementById('comparison-title');
            
            let chartKey, titleText;
            
            // Show/hide sector control
            if (comparisonType === 'ETF_vs_Stocks') {{
                sectorControl.style.display = 'block';
                const sector = sectorSelect.value;
                chartKey = sector + '_' + period.toLowerCase();
                titleText = sector + ': Sector Aggregate vs ETF Benchmark (' + (period === 'General' ? 'Since Beginning' : 'YTD') + ')';
            }} else {{
                sectorControl.style.display = 'none';
                chartKey = 'equity_' + period.toLowerCase();
                titleText = 'Equity Portfolio vs S&P 500 Benchmark (' + (period === 'General' ? 'Since Beginning' : 'YTD') + ')';
            }}
            
            chartTitle.textContent = titleText;
            
            // Get chart data
            const chartData = comparisonChartsData[chartKey];
            if (chartData && window.Plotly) {{
                // Clear previous chart
                chartContainer.innerHTML = '';
                
                // Create unique div ID
                const divId = 'comparison-chart-' + Date.now();
                const div = document.createElement('div');
                div.id = divId;
                div.style.width = '100%';
                div.style.height = '600px';
                chartContainer.appendChild(div);
                
                // Render Plotly chart
                Plotly.newPlot(divId, chartData.data, chartData.layout, {{
                    responsive: true,
                    displayModeBar: true
                }});
                
                currentComparisonChartId = divId;
            }} else {{
                chartContainer.innerHTML = '<p style="padding: 20px; color: #666;">Chart data not available for this selection.</p>';
            }}
        }}
        
        // Initialize on page load
        document.addEventListener('DOMContentLoaded', function() {{
            // Render all main charts
            renderMainCharts();
            
            // Initialize comparison chart
            if (window.Plotly) {{
                updateComparisonChart();
            }} else {{
                // Retry after a short delay
                setTimeout(function() {{
                    if (window.Plotly) {{
                        updateComparisonChart();
                    }}
                }}, 500);
            }}
        }});
    </script>
</body>
</html>"""
    
    # Write index.html
    index_path = os.path.join(docs_dir, 'index.html')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✓ Website generated: {index_path}")
    print(f"✓ Charts embedded: {len(charts_data)} main charts")
    print(f"✓ Comparison charts: {len(comparison_charts_data)} sector comparisons")
    
    return index_path

if __name__ == '__main__':
    generate_website()

