from flask import Flask, render_template
import WebToCSV

app = Flask(__name__)

# TODO: automate the app running on AWS -> this will be the hard part, installing the app
# TODO: have the ability to have the app return the csv for you


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/scrape')
def scrape_yelp():
    input_url = "https://www.yelp.ca/biz/rosalinda-toronto-3?page_src=related_bizes"
    csv_name = "reviews_from_flask2.csv"
    WebToCSV.main_scraper(input_url, csv_name)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)