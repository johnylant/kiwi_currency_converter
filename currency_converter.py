import argparse
import requests

def provideArguments():
    '''
    Sets up and returns arguments for the application
    '''
    parser = argparse.ArgumentParser(description='Convert currencies')
    requiredArgs = parser.add_argument_group('required arguments')
    requiredArgs.add_argument('--amount', help='Amount to be Converted', required=True, type=float)
    requiredArgs.add_argument('--input_currency', help='Input Currency (triname or symbol)', required=True, type=str)
    parser.add_argument('--output_currency', help='Output Currency (triname or symbol)', default=None, type=str)
    args = parser.parse_args()
    return (args.amount, args.input_currency, args.output_currency)


def checkCurrencyInput(currency):
    '''
    Checks if specified string is currency symbol or triname
    '''
    symbols = { "$": "USD",
                "¥": "CNY",
                "£": "GBP",
                "฿": "THB",
                "€": "EUR",
                "₽": "RUB" }

    if len(currency) == 1:
        if currency in symbols:
            currency = symbols[currency]
        else:
            return 0
    elif len(currency) == 3:
        currency = currency.upper()
    else:
        return 0
    return currency


def handleInputs():
    '''
    Checks provided inputs and returns them
    '''
    # Gather values from the input arugemnts
    amount, input_currency, output_currency = provideArguments()
    if amount <= 0:
        print("Invalid amount provided")
        return 0
    else:
        # Check input currency
        input_currency = checkCurrencyInput(input_currency)
        if not input_currency:
            print("Input currency symbol not found or not triname entered")
            return 0
        # Check output currency (default is None)
        if output_currency:
            output_currency = checkCurrencyInput(output_currency)
            if not output_currency:
                print("Output currency symbol not found or not triname entered")
                return 0
        # Check if not the same currency provided
        if input_currency == output_currency:
            print("You can't convert to the same currency")
            return 0
    return (amount, input_currency, output_currency)


def getCurrencyJson(input_currency):
    '''
    Gets json with currency rates using external API
    '''
    url = 'https://api.fixer.io/latest?base=' + input_currency
    response = requests.get(url)
    if "error" in response.json():
        return 0
    return response.json()


def formatOutput(amount, input_currency):
    '''
    Prepares output json
    '''
    out_json = {}
    out_json['input'] = {}
    out_json['output'] = {}
    out_json['input']['amount'] = amount
    out_json['input']['currency'] = input_currency
    return out_json


def convert(amount, output_currency, currency_json, out_json):
    '''
    Converts currencies and updates output json
    '''
    # update out_json with all the currencies
    if not output_currency:
        for key in currency_json['rates']:
            out_json['output'][key] = round(amount * float(currency_json['rates'][key]), 4)
    # update only with specified currency
    elif output_currency in currency_json['rates']:
        out_json['output'][output_currency] = round(amount * float(currency_json['rates'][output_currency]), 4)
    else:
        return 0
    return 1



def main():
    try:
        # handleInputs returns inputs or 0
        amount, input_currency, output_currency  = handleInputs()
    except TypeError:
        return 0

    currency_json = getCurrencyJson(input_currency)
    if not currency_json:
        print("You have entered invalid input currency")
        return 0

    out_json = formatOutput(amount, input_currency)


    if not convert(amount, output_currency, currency_json, out_json):
        print("You have entered invalid output currency")
        return 0
    else:
        print(out_json)


if __name__ == "__main__":
    main()
