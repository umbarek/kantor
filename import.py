import requests
import csv
import pickle
from flask import Flask, render_template, request, redirect


app = Flask(__name__)

response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data = response.json()
rates = data[0].get('rates')


def get_codes():
    codes = []
    for data in rates:
        codes.append(data.get('code'))
    return sorted(codes)


def rates_to_csv():
    fieldnames = ['currency', 'code', 'bid', 'ask']
    with open('rates.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, delimiter=';', fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rates)


rates_to_csv()


@app.route('/form', methods=["GET", "POST"])
def form():
    codes = get_codes()
    if request.method == "POST":
        data = request.form
        currency = data.get('code')
        amount = data.get('amount')
        for data in rates:
            if data.get('code') == currency:
                ask = data.get('ask')
                break
        cost = (float(amount) * ask)
        return f"Koszt zakupu {amount} {currency} po cenie {ask} wyniesie: {cost}"
    return render_template("form.html")



