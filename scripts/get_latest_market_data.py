import yfinance as yf
import akshare as ak
import json
import sys
import pandas as pd
from datetime import datetime
import warnings

# 忽略一些不必要的警告
warnings.filterwarnings("ignore")

def normalize_hk_ticker(ticker):
    """
    归一化港股代码供 Yahoo Finance 使用。
    """
    ticker = ticker.upper()
    if ticker.endswith(".HK"):
        code = ticker.split(".")[0]
        if len(code) == 5 and code.startswith("0"):
            return f"{code[1:]}.HK"
    return ticker

def get_ticker_data(ticker):
    ticker_upper = ticker.upper()
    
    # 尝试使用 akshare (针对 A股)
    if ticker_upper.endswith((".SS", ".SZ")):
        try:
            code = ticker_upper.split(".")[0]
            df = ak.stock_zh_a_spot_em()
            target = df[df["代码"] == code]
            if not target.empty:
                row = target.iloc[0]
                return {
                    "ticker": ticker_upper,
                    "current_price": float(row["最新价"]),
                    "open": float(row["今开"]),
                    "high": float(row["最高"]),
                    "low": float(row["最低"]),
                    "volume": int(row["成交量"]),
                    "pe_ratio": float(row["市盈率-动态"]) if row["市盈率-动态"] != "-" else "N/A",
                    "market_cap": float(row["总市值"]),
                    "timestamp": datetime.now().isoformat(),
                    "source": "akshare_a"
                }
        except Exception as e:
            # 如果 akshare 失败（如网络超时），记录错误并继续尝试 yfinance
            pass

    # 默认/回退使用 yfinance
    try:
        yf_ticker = normalize_hk_ticker(ticker_upper)
        data = yf.Ticker(yf_ticker)
        
        # 尝试 fast_info
        price, open_p, high, low, vol = None, None, None, None, None
        try:
            fast = data.fast_info
            price = fast['last_price']
            open_p = fast['open']
            high = fast['day_high']
            low = fast['day_low']
            vol = fast['last_volume']
        except:
            pass

        # 如果 fast_info 没拿到关键数据，用 info (慢但全)
        info = data.info
        if price is None:
            price = info.get('regularMarketPrice') or info.get('currentPrice')
        if open_p is None:
            open_p = info.get('regularMarketOpen') or info.get('open')
        if high is None:
            high = info.get('regularMarketDayHigh') or info.get('dayHigh')
        if low is None:
            low = info.get('regularMarketDayLow') or info.get('dayLow')
        if vol is None:
            vol = info.get('regularMarketVolume') or info.get('volume')

        return {
            "ticker": ticker_upper,
            "current_price": round(price, 2) if price else "N/A",
            "open": round(open_p, 2) if open_p else "N/A",
            "high": round(high, 2) if high else "N/A",
            "low": round(low, 2) if low else "N/A",
            "volume": vol if vol else "N/A",
            "pe_ratio": info.get('forwardPE', info.get('trailingPE', 'N/A')),
            "market_cap": info.get('marketCap', 'N/A'),
            "timestamp": datetime.now().isoformat(),
            "source": f"yfinance({yf_ticker})"
        }
    except Exception as e:
        return {"error": str(e), "ticker": ticker_upper}

if __name__ == "__main__":
    ticker_symbol = sys.argv[1] if len(sys.argv) > 1 else "TSLA"
    market_data = get_ticker_data(ticker_symbol)
    print(json.dumps(market_data, indent=2))
