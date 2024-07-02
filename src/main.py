from config_loader import load_json
from etf_display import ETFDisplay
from investment_manager import InvestmentManager
import time

def main():
    # Load configuration and ETF symbols from JSON files
    config = load_json('../config/config.json')
    etf_symbols = load_json('../config/etf_list.json')["etf_symbols"]
    investment_amount = config.get('investment_amount', 10000)
    perform_purchase = config.get('perform_purchase', False)
    sell_etfs = config.get('sell_etfs', False)
    market_closed_display = config.get('market_closed_display', True)
    interval = config.get('interval', 60)

    # Initialize ETF display and investment manager
    etf_display = ETFDisplay(etf_symbols, config)
    investment_manager = InvestmentManager(investment_amount, '../output/investments.json', '../log/investment_log.json')

    while True:
        # Save and display ETF data regardless of market status
        etf_display.save_etf_data('../output/etf_data.json')
        etf_data_dict = load_json('../output/etf_data.json')
        
        # Display ETF data
        print(f"{'Symbol':<10}{'Name':<40}{'Last Price':<15}{'Volume':<10}{'1Y Change':<10}")
        print("="*85)
        for symbol, etf_data in etf_data_dict.items():
            name = etf_data["name"]
            last_price = etf_data["last_price"]
            last_volume = etf_data["last_volume"]
            change_percent_year = etf_data["change_percent_year"]
            print(f"{symbol:<10}{name:<40}{last_price:<15}{last_volume:<10}{change_percent_year:<10}")
        print("="*85)
        
        # Check if the market is open
        if not etf_display.is_market_open():
            if market_closed_display:
                etf_display.display_market_closed_message()
                break
        else:
            # Perform ETF purchase or sell all ETFs
            if sell_etfs:
                investment_manager.sell_all_etfs()
                print("All ETFs have been sold and the log files have been cleared.")
            elif perform_purchase:
                investment_manager.buy_etf(etf_data_dict)
                print("ETFs purchased and log updated.")

            # Calculate and display current portfolio value and performance
            current_value = investment_manager.calculate_current_value(etf_data_dict)
            profit_loss, performance = investment_manager.calculate_performance(etf_data_dict)
            print(f"\nCurrent portfolio value: ${current_value:.2f}")
            print(f"Performance since last request: ${profit_loss:.2f} ({performance:.2f}%)")

        # Wait for the specified interval before the next update
        time.sleep(interval)

if __name__ == "__main__":
    main()

