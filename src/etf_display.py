import datetime
import json
from pytz import timezone
from etf_ticker import ETFTicker
from error_handler import MarketClosedError, ConfigurationError
import logging

class ETFDisplay:
    def __init__(self, symbols, config):
        try:
            self.market_timezone = timezone(config.get('timezone', 'Europe/Paris'))
            self.market_open_hour = 9
            self.market_close_hour = 17.5
            self.etf_list = [ETFTicker(symbol, self) for symbol in symbols]
            self.market_closed_display = config.get('market_closed_display', True)
        except Exception as e:
            raise ConfigurationError(f"Error in ETFDisplay configuration: {e}")

    def is_market_open(self):
        now = datetime.datetime.now(self.market_timezone)
        if now.weekday() >= 5:
            return False
        market_open_time = now.replace(hour=9, minute=0, second=0, microsecond=0)
        market_close_time = now.replace(hour=17, minute=30, second=0, microsecond=0)
        return market_open_time <= now <= market_close_time

    def get_etf_data_as_dict(self):
        etf_data_dict = {}
        now = datetime.datetime.now(self.market_timezone).isoformat()
        for etf in self.etf_list:
            name, last_price, last_volume, change_percent_year = etf.get_latest_data()
            etf_data_dict[etf.symbol] = {
                "name": name,
                "last_price": last_price,
                "last_volume": last_volume,
                "change_percent_year": change_percent_year,
                "request_time": now
            }
        return etf_data_dict

    def convert_to_native_types(self, data):
        if isinstance(data, dict):
            return {k: self.convert_to_native_types(v) for k, v in data.items()}
        elif isinstance(data, (list, tuple)):
            return type(data)(self.convert_to_native_types(v) for v in data)
        elif hasattr(data, 'item'):
            return data.item()
        else:
            return data

    def save_etf_data(self, filepath):
        try:
            etf_data_dict = self.get_etf_data_as_dict()
            etf_data_dict = self.convert_to_native_types(etf_data_dict)
            with open(filepath, 'w') as file:
                json.dump(etf_data_dict, file, indent=4)
            logging.info(f"ETF data saved to {filepath}")
        except Exception as e:
            logging.error(f"Error saving ETF data: {e}")
            raise

    def display_market_closed_message(self):
        message = """
        ****************************************
        *                                      *
        *    The market is currently closed.   *
        *  No transactions will be performed.  *
        *                                      *
        ****************************************
        """
        print(message)
        logging.info("Market is closed message displayed")
