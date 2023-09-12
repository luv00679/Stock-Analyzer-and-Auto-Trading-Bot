# Stock Analyzer and Auto-Trading Bot

#### Description:
Welcome to the Stock Analyzer and Auto-Trading Bot! This Python program leverages various libraries and APIs to help you analyze stock data, identify potentially profitable stocks, and even place buy orders automatically. This README provides an overview of the program's functionalities, how to install and use it, and the configuration requirements.

## Table Of Contents
1. Dependencies
2. Installation
3. Usage
4. Configuration
5. Contributing

## Dependencies
Before you begin, make sure you have the following dependencies installed:

    requests (as rq)
    yfinance (as yf)
    pandas (as pd)
    numpy (as np)
    io
    SmartApi (custom module)
    pyotp

You can install these libraries using pip if they are not already installed.

## Installation
1. Clone the repository to your local machine:
```
git clone https://github.com/yourusername/your-repo.git
```
2. Navigate to the project directory:
```
cd your-repo
```
3. Install the required dependencies as mentioned above.


## Usage
To use the Stock Analyzer and Auto-Trading Bot, follow these steps:
1. Run the main() function by executing the program:
```
python program.py
```
2. The program will perform the following tasks:

    Retrieve a list of stocks from the Nifty 500 index.
    Collect and store the closing prices of these stocks over the past 10 years.
    Analyze the stocks based on a custom strategy.
    Identify the stock with the highest potential based on the strategy.
    Prompt you to enter your API key, Client ID, PIN, and the quantity you want to buy.
3. Follow the on-screen prompts to input your credentials and desired quantity.
4. The program will attempt to place a buy order for the selected stock on your behalf.

## Configuration
### API Keys and Credentials
To use the auto-trading feature, you need to configure the following credentials:
1. API Key: You should have access to a Smart API key.
2. Client ID: Your Angel One account's Client ID.
3. PIN: The PIN for your Angel One account.
### Custom Strategy
The program utilizes a custom stock analysis strategy. You can modify this strategy by adjusting the conditions within the strategy function in the code. The default conditions involve checking for a minimum compound interest rate, price comparisons, and percentage differences.

## Contributing
Contributions to this project are welcome. You can contribute by:

    Reporting issues or bugs.
    Suggesting new features or enhancements.
    Providing code improvements through pull requests.
