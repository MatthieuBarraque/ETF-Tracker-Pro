import json
import os
from datetime import datetime
from error_handler import InvestmentError
import logging

class InvestmentManager:
    def __init__(self, investment_amount, investments_filepath, investment_log_filepath):
        self.investment_amount = investment_amount
        self.investments_filepath = investments_filepath
        self.investment_log_filepath = investment_log_filepath
        self.investments = self.load_investments()

    def buy_etf(self, etf_data):
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            total_investment = self.investment_amount
            num_etfs = len(etf_data)
            investment_per_etf = total_investment / num_etfs

            for symbol, data in etf_data.items():
                last_price = data['last_price']
                quantity = investment_per_etf / last_price
                investment_record = {
                    "price": last_price,
                    "quantity": quantity,
                    "date": timestamp
                }

                if symbol in self.investments:
                    self.investments[symbol]['shares'] += quantity
                else:
                    self.investments[symbol] = {
                        "shares": quantity,
                        "initial_price": last_price
                    }

                self.log_investment(symbol, investment_record)

            self.save_investments()
            logging.info(f"Investments made: {self.investments}")
        except Exception as e:
            logging.error(f"Error buying ETFs: {e}")
            raise InvestmentError(f"Error buying ETFs: {e}")

    def log_investment(self, symbol, investment_record):
        try:
            log_directory = "../log"
            if not os.path.exists(log_directory):
                os.makedirs(log_directory)

            if os.path.exists(self.investment_log_filepath):
                with open(self.investment_log_filepath, 'r') as file:
                    investment_log = json.load(file)
            else:
                investment_log = {}

            if symbol not in investment_log:
                investment_log[symbol] = []

            investment_log[symbol].append(investment_record)

            with open(self.investment_log_filepath, 'w') as file:
                json.dump(investment_log, file, indent=4)
            logging.info(f"Logged investment for {symbol}")
        except Exception as e:
            logging.error(f"Error logging investment for {symbol}: {e}")
            raise InvestmentError(f"Error logging investment for {symbol}: {e}")

    def calculate_current_value(self, etf_data):
        try:
            total_value = 0
            for symbol, data in self.investments.items():
                current_price = etf_data[symbol]['last_price']
                total_value += data['shares'] * current_price
            return total_value
        except Exception as e:
            logging.error(f"Error calculating current value: {e}")
            raise InvestmentError(f"Error calculating current value: {e}")

    def calculate_performance(self, etf_data):
        try:
            total_initial_investment = sum(data['shares'] * data['initial_price'] for data in self.investments.values())
            current_value = self.calculate_current_value(etf_data)
            profit_loss = current_value - total_initial_investment
            performance = (profit_loss / total_initial_investment) * 100
            return profit_loss, performance
        except Exception as e:
            logging.error(f"Error calculating performance: {e}")
            raise InvestmentError(f"Error calculating performance: {e}")

    def sell_all_etfs(self):
        try:
            self.investments = {}
            self.save_investments()
            if os.path.exists(self.investment_log_filepath):
                os.remove(self.investment_log_filepath)
            logging.info("All ETFs have been sold and log files have been cleared.")
        except Exception as e:
            logging.error(f"Error selling all ETFs: {e}")
            raise InvestmentError(f"Error selling all ETFs: {e}")

    def save_investments(self):
        try:
            with open(self.investments_filepath, 'w') as file:
                json.dump(self.investments, file, indent=4)
            logging.info(f"Investments saved to {self.investments_filepath}")
        except Exception as e:
            logging.error(f"Error saving investments: {e}")
            raise InvestmentError(f"Error saving investments: {e}")

    def load_investments(self):
        try:
            if os.path.exists(self.investments_filepath):
                with open(self.investments_filepath, 'r') as file:
                    return json.load(file)
            return {}
        except Exception as e:
            logging.error(f"Error loading investments: {e}")
            raise InvestmentError(f"Error loading investments: {e}")