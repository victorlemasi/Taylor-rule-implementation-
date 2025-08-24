import MetaTrader5 as mt5
import requests
import time

# MetaTrader 5 Initialization
mt5.initialize()

# Function to get the latest economic data (CPI, Unemployment, NFP, GDP, etc.)
def get_economic_data():
    url = "https://api.tradingeconomics.com/historical/country/united-states"
    params = {"c": "YOUR_API_KEY"}  # Replace with your Trading Economics API key
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        
        # Extract the latest data for various indicators
        latest_cpi = data[0]['value']  # Consumer Price Index (CPI)
        latest_unemployment = data[1]['value']  # Unemployment Rate
        latest_nfp = data[2]['value']  # Non-Farm Payrolls (NFP)
        latest_gdp_growth = data[3]['value']  # GDP Growth Rate
        latest_core_pce = data[4]['value']  # Core PCE Inflation
        latest_retail_sales = data[5]['value']  # Retail Sales
        latest_consumer_confidence = data[6]['value']  # Consumer Confidence Index (CCI)
        
        return latest_cpi, latest_unemployment, latest_nfp, latest_gdp_growth, latest_core_pce, latest_retail_sales, latest_consumer_confidence
    else:
        print("Failed to fetch economic data.")
        return None, None, None, None, None, None, None

# Refined Taylor Rule-based decision function
def taylor_rule(cpi, unemployment, gdp_growth, r_neutral=2, target_inflation=2, potential_gdp_growth=2.0, natural_unemployment_rate=4.5):
    """
    Apply the Taylor Rule to calculate the target federal funds rate based on CPI, GDP growth, and unemployment.
    """
    # Inflation gap: CPI - target inflation
    inflation_gap = cpi - target_inflation
    
    # Output gap: Unemployment gap (difference from natural unemployment rate)
    output_gap = unemployment - natural_unemployment_rate
    
    # GDP gap: GDP growth compared to potential growth
    gdp_gap = gdp_growth - potential_gdp_growth
    
    # Taylor Rule Formula
    # i = r_neutral + inflation_gap + 0.5 * inflation_gap + 0.5 * output_gap + 0.25 * gdp_gap
    interest_rate = r_neutral + inflation_gap + 0.5 * inflation_gap + 0.5 * output_gap + 0.25 * gdp_gap
    
    # Return the calculated federal funds rate
    return interest_rate

# Function to decide Buy or Sell based on economic conditions and Taylor Rule
def decision_based_on_economic_data(cpi, unemployment, nfp, gdp_growth, core_pce, retail_sales, consumer_confidence):
    """
    Decide whether to buy, sell, or hold based on the Taylor Rule calculation and economic conditions.
    """
    # Calculate the target federal funds rate using the Taylor Rule
    interest_rate = taylor_rule(cpi, unemployment, gdp_growth)
    
    # Economic decision-making based on Taylor Rule output
    print(f"Calculated Interest Rate from Taylor Rule: {interest_rate}%")
    
    # Decision-making logic:
    # 1. If inflation is high (CPI > 2.5), unemployment is low (below 5%), and GDP growth is strong (> 2%),
    #    the Fed may raise rates, suggesting a Sell.
    if cpi > 2.5 and unemployment < 5 and gdp_growth > 2:
        return "SELL"
    
    # 2. If inflation is low (CPI < 1.5), unemployment is high (above 7%), and GDP growth is weak (< 1%),
    #    the Fed may lower rates, suggesting a Buy.
    elif cpi < 1.5 and unemployment > 7 and gdp_growth < 1:
        return "BUY"
    
    # 3. If inflation is moderate (CPI between 2% and 2.5), unemployment is around natural levels (5-6.5%),
    #    and GDP growth is moderate, we suggest a Hold.
    elif 2 <= cpi <= 2.5 and 5 <= unemployment <= 6.5 and 1 <= gdp_growth <= 2:
        return "HOLD"
    
    # 4. Default hold if no conditions fit well
    else:
        return "HOLD"

# Function to execute trade on MetaTrader 5
def execute_trade(action, symbol="EURUSD", lot_size=0.1):
    """
    Executes a trade on MetaTrader 5 based on the Buy/Sell signal from the strategy.
    """
    if action == "BUY":
        price = mt5.symbol_info_tick(symbol).ask
        order = mt5.ORDER_TYPE_BUY
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot_size,
            "type": order,
            "price": price,
            "deviation": 10,
            "magic": 234000,
            "comment": "Buy order based on economic indicators",
            "type_filling": mt5.ORDER_FILLING_IOC,
            "type_time": mt5.ORDER_TIME_GTC
        }
        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print(f"Failed to place BUY order: {result.comment}")
        else:
            print("Buy order executed.")
    
    elif action == "SELL":
        price = mt5.symbol_info_tick(symbol).bid
        order = mt5.ORDER_TYPE_SELL
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot_size,
            "type": order,
            "price": price,
            "deviation": 10,
            "magic": 234000,
            "comment": "Sell order based on economic indicators",
            "type_filling": mt5.ORDER_FILLING_IOC,
            "type_time": mt5.ORDER_TIME_GTC
        }
        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print(f"Failed to place SELL order: {result.comment}")
        else:
            print("Sell order executed.")

# Main loop for real-time decision making and trading
while True:
    # Get the latest economic data (CPI, Unemployment, NFP, GDP, etc.)
    latest_cpi, latest_unemployment, latest_nfp, latest_gdp_growth, latest_core_pce, latest_retail_sales, latest_consumer_confidence = get_economic_data()
    
    if latest_cpi is None or latest_unemployment is None or latest_nfp is None:
        print("Skipping trade decision due to missing data.")
    else:
        print(f"Latest CPI: {latest_cpi}, Latest Unemployment Rate: {latest_unemployment}, NFP: {latest_nfp}")
        print(f"Latest GDP Growth: {latest_gdp_growth}, Core PCE: {latest_core_pce}, Retail Sales: {latest_retail_sales}")
        print(f"Consumer Confidence: {latest_consumer_confidence}")
        
        # Make a decision (BUY/SELL/HOLD) based on economic data and Taylor Rule
        action = decision_based_on_economic_data(latest_cpi, latest_unemployment, latest_nfp, latest_gdp_growth, latest_core_pce, latest_retail_sales, latest_consumer_confidence)
        print(f"Decision: {action}")
        
        # Execute trade based on the decision
        if action != "HOLD":
            execute_trade(action)
    
    # Wait for the next cycle (e.g., 10 minutes)
    time.sleep(600)

# Shutdown MetaTrader 5 connection after the loop ends
mt5.shutdown()
