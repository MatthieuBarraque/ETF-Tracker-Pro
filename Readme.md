## Description

Ce projet permet de gérer les investissements dans les ETF en utilisant des données de marché en temps réel. Il inclut des fonctionnalités pour acheter et vendre des ETF, afficher des informations sur les ETF, et suivre la performance des investissements.

## Structure du projet

```
project_root/
├── config
│   ├── config.json
│   └── etf_list.json
├── log
│   └── app.log
├── output
│   ├── etf_data.json
│   ├── investment_log.json
│   └── investments.json
├── src
│   ├── __pycache__
│   ├── config_loader.py
│   ├── etf_display.py
│   ├── etf_ticker.py
│   ├── investment_manager.py
│   ├── error_handler.py
│   └── main.py
├── requirements.txt
└── README.md
```

## Configuration

### config/config.json

```
{
    "investment_amount": 10000,
    "perform_purchase": false,
    "sell_etfs": false,
    "timezone": "Europe/Paris",
    "interval": 60,
    "market_closed_display": true
}
```

### config/etf_list.json

```
{
    "etf_symbols": ["INDICES"]
}
```

## Installation

1. Clonez le dépôt.
2. Installez les dépendances Python :

```
pip install -r requirements.txt
```

## Utilisation

1. Assurez-vous que les fichiers de configuration dans le dossier `config` sont correctement configurés.

2. Exécutez le script principal :

```
python main.py
```

## Gestion des erreurs

Les erreurs sont gérées de manière centralisée dans le fichier `src/error_handler.py` et sont journalisées dans le fichier `log/app.log`.

## Journaux

Tous les mouvements et erreurs du code sont enregistrés dans le fichier `log/app.log` pour une traçabilité complète.
