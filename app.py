from flask import Flask, request, jsonify
from yahoo_fin.stock_info import get_quote_table
from yahoo_fin.stock_info import get_income_statement
import os

app = Flask(__name__)


@app.route('/indices')
def indices():
    dji = get_quote_table('^dji')
    dji['Change'] = dji['Quote Price'] - dji['Previous Close']
    dji['Percent Change'] = dji['Change'] / dji['Previous Close'] * 100

    sp = get_quote_table('^gspc')
    sp['Change'] = sp['Quote Price'] - sp['Previous Close']
    sp['Percent Change'] = sp['Change'] / sp['Previous Close'] * 100

    nasdaq = get_quote_table('^ixic')
    nasdaq['Change'] = nasdaq['Quote Price'] - nasdaq['Previous Close']
    nasdaq['Percent Change'] = nasdaq['Change'] / \
        nasdaq['Previous Close'] * 100
    major_indices = {'dji': dji, 'sp': sp, 'nadaq': nasdaq}

    return jsonify(major_indices), 200



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 4000))
    # app.run(host='0.0.0.0', port=port)
    app.run(host='0.0.0.0', port=4000, debug=True)
