import yfinance as yf
import json
import sys
from datetime import datetime

def get_ticker_data(ticker):
    try:
        data = yf.Ticker(ticker)
        # 获取实时报价
        price = data.fast_info['last_price']
        # 获取基础指标
        info = data.info
        
        result = {
            "ticker": ticker,
            "current_price": round(price, 2),
            "open": round(data.fast_info['open'], 2),
            "high": round(data.fast_info['day_high'], 2),
            "low": round(data.fast_info['day_low'], 2),
            "volume": data.fast_info['last_volume'],
            "pe_ratio": info.get('forwardPE', 'N/A'),
            "market_cap": info.get('marketCap', 'N/A'),
            "timestamp": datetime.now().isoformat()
        }
        return result
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    ticker_symbol = sys.argv[1] if len(sys.argv) > 1 else "TSLA"
    market_data = get_ticker_data(ticker_symbol)
    print(json.dumps(market_data, indent=2))
