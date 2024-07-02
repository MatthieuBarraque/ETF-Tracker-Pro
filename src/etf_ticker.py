import yfinance as yf
from error_handler import RequestError
import logging

class ETFTicker:
    def __init__(self, symbol, display):
        self.symbol = symbol
        self.ticker = yf.Ticker(symbol)
        self.display = display

    def get_current_price(self):
        try:
            todays_data = self.ticker.history(period='1d')
            if not todays_data.empty and 'Close' in todays_data.columns:
                return todays_data['Close'].iloc[-1]
            else:
                return "No closing price data available"
        except Exception as e:
            logging.error(f"Error fetching data for {self.symbol}: {e}")
            raise RequestError(f"Error fetching data for {self.symbol}: {e}")

    def get_latest_data(self):
        try:
            if self.display.is_market_open():
                last_price = self.get_current_price()
                last_volume = self.ticker.info.get('regularMarketVolume', 'N/A')
            else:
                last_hist = self.ticker.history(period='1d')
                last_price = last_hist['Close'].iloc[-1] if not last_hist.empty else 'N/A'
                last_volume = last_hist['Volume'].iloc[-1] if not last_hist.empty else 'N/A'

            name = self.ticker.info.get('longName', self.symbol)
            change_percent_year = self.ticker.info.get('52WeekChange', 'N/A')
            if change_percent_year != 'N/A':
                change_percent_year = f"{change_percent_year * 100:.2f}%"
            
            return name, last_price, last_volume, change_percent_year
        except Exception as e:
            logging.error(f"Error getting latest data for {self.symbol}: {e}")
            raise RequestError(f"Error getting latest data for {self.symbol}: {e}")
