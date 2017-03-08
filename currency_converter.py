import argparse
import requests

def provideArguments():
    parser = argparse.ArgumentParser(description='Convert currencies')
    requiredArgs = parser.add_argument_group('required arguments')
    requiredArgs.add_argument('--amount', help='Amount to be Converted', required=True, type=float)
    requiredArgs.add_argument('--input_currency', help='Input Currency (triname or symbol)', required=True, type=str)
    parser.add_argument('--output_currency', help='Output Currency (triname or symbol)', default=None, type=str)
    args = parser.parse_args()
    return (args.amount, args.input_currency, args.output_currency)


def handleInputs():
    symbols = { "$": "USD",
                "¥": "CNY",
                "£": "GBP",
                "฿": "THB",
                "€": "EUR",
                "₽": "RUB" }

    # Gather values from the input arugemnts
    amount, input_currency, output_currency = provideArguments()


    if amount <= 0:
        print("Invalid amount provided")
        return 0
    else:
        # Check input currency
        if len(input_currency) == 1:
            if input_currency in symbols:
                input_currency = symbols[input_currency]
            else:
                print("Input currency symbol not found")
                return 0
        elif len(input_currency) == 3:
            input_currency = input_currency.upper()
        else:
            print("Please specify symbol or currency triname to enter input currency")
            return 0
        # Check output currency
        if output_currency:
            if len(output_currency) == 1:
                if output_currency in symbols:
                    output_currency = symbols[output_currency]
                else:
                    print("Output currency symbol not found")
                    return 0
            elif len(output_currency) == 3:
                output_currency = output_currency.upper()
            else:
                print("Please specify symbol or currency triname to enter output currency")
                return 0
        # Check if not the same currency provided
        if input_currency == output_currency:
            print("You can't convert to the same currency")
            return 0

    return (amount, input_currency, output_currency)



# Gets json with currency rates
def getCurrencyJson(input_currency):
    url = 'https://api.fixer.io/latest?base=' + input_currency
    response = requests.get(url)
    if "error" in response.json():
        return 0
    return response.json()

# Prepares output json
def formatOutput(amount, input_currency):
    out_json = {}
    out_json['input'] = {}
    out_json['output'] = {}
    out_json['input']['amount'] = amount
    out_json['input']['currency'] = input_currency
    return out_json

# Converts currencies and updates output json
def convert(amount, output_currency, currency_json, out_json):
    if not output_currency:
        for key in currency_json['rates']:
            out_json['output'][key] = round(amount * float(currency_json['rates'][key]), 4)

    elif output_currency in currency_json['rates']:
        out_json['output'][output_currency] = round(amount * float(currency_json['rates'][output_currency]), 4)
    else:
        return 0
    return 1



def main():

    try:
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
