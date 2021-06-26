from flask import Flask, request, jsonify
from yahoo_fin.stock_info import get_quote_table
from yahoo_fin.stock_info import get_income_statement
import os

app = Flask(__name__)


@app.route('/indices')
def indices():
    dow = get_quote_table('^dji')
    dow['Change'] = dow['Quote Price'] - dow['Previous Close']
    dow['Percent Change'] = dow['Change'] / dow['Previous Close'] * 100

    sp500 = get_quote_table('^gspc')
    sp500['Change'] = sp500['Quote Price'] - sp500['Previous Close']
    sp500['Percent Change'] = sp500['Change'] / sp500['Previous Close'] * 100

    nasdaq = get_quote_table('^ixic')
    nasdaq['Change'] = nasdaq['Quote Price'] - nasdaq['Previous Close']
    nasdaq['Percent Change'] = nasdaq['Change'] / \
        nasdaq['Previous Close'] * 100

    major_indices = {'dow': dow, 'sp500': sp500, 'nasdaq': nasdaq}

    return jsonify(major_indices), 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 4000))
    app.run(host='0.0.0.0', port=port)
    # app.run(host='0.0.0.0', port=4000, debug=True)
