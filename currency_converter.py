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


def convert(amount, output_currency, resp_json, out_json):
    if not output_currency:
        for key in resp_json['rates']:
            out_json['output'][key] = round(amount * float(resp_json['rates'][key]), 4)

    elif output_currency in resp_json['rates']:
        out_json['output'][output_currency] = round(amount * float(resp_json['rates'][output_currency]), 4)
    else:
        print("You have entered invalid output currency")
        return 0
    return 1


def main():

    try:
        a, i, output_currency  = handleInputs()
    except TypeError:
        return 0


    out_json = {}
    out_json['input'] = {}
    out_json['output'] = {}

    out_json['input']['amount'] = a
    out_json['input']['currency'] = i
    url = 'https://api.fixer.io/latest?base=' + i
    response = requests.get(url)
    if "error" in response.json():
        print("You have entered invalid input currency")
        return 0


    if convert(a, output_currency, response.json(), out_json):
        print(out_json)


if __name__ == "__main__":
    main()
