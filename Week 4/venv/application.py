# main.py
from flask import Flask, render_template, request
import pickle
from function import ask_user, calculate_price_and_profit

application = Flask(__name__, template_folder='C:/Users/HP/Desktop/dataGlaciers_week2/Flask/templates')

@application.route('/')
def index():
    return render_template('index.html')

@application.route('/calculate', methods=['POST'])
def calculate():
    distance = float(request.form['distance'])
    company = request.form['company']
    revenue, profit = calculate_price_and_profit(distance, company)
    return render_template('result.html', revenue=revenue, profit=profit)

if __name__ == '__main__':
    application.run(debug=True)
