import logging

# Configuration de la journalisation
logging.basicConfig(
    filename='../log/app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class ConfigError(Exception):
    pass

class MarketClosedError(Exception):
    pass

class RequestError(Exception):
    pass

class InvestmentError(Exception):
    pass

class ConfigurationError(Exception):
    pass
