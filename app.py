from flask import Flask, request, jsonify
from yahoo_fin.stock_info import get_quote_table
from yahoo_fin.stock_info import get_income_statement
import os

app = Flask(__name__)

def _change(quote):
  return quote['Quote Price'] - quote['Previous Close']

def _range(range):
  range_map = map(lambda x: float(x.replace(',','')), range.split(' - '))
  low_end, high_end = list(range_map)
  return {'lowEnd': low_end, 'highEnd': high_end}

def _transform_data(quote):
  day_range = quote['Day\'s Range']
  year_range = quote['52 Week Range']

  data = {
    'yearRange': _range(year_range),
    'dayRange': _range(day_range),
    'averageVolume': quote['Avg. Volume'],
    'open': quote['Open'],
    'previousClose': quote['Previous Close'],
    'price': quote['Quote Price'],
    'volume': quote['Volume'],
    'change': _change(quote),
    'percentChange': _change(quote) / quote['Previous Close'] * 100
  }

  return data


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

@app.route('/api/v2/indices')
def indices_v2():
  dow_quote = get_quote_table('^dji')
  sp_500_quote = get_quote_table('^gspc')
  nasdaq_quote = get_quote_table('^ixic')
  russell_2000_quote = get_quote_table('^rut')



  return jsonify({
    'dow': _transform_data(dow_quote),
    'nasdaq': _transform_data(nasdaq_quote),
    'sp500': _transform_data(sp_500_quote),
    'russell2000': _transform_data(russell_2000_quote)
  }), 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 4000))
    app.run(host='0.0.0.0', port=port)
    # app.run(host='0.0.0.0', port=4000, debug=True)
