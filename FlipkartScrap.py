from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import logging
import pymongo
logging.basicConfig(filename="newscrapper.log" , level=logging.INFO)

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def home():
    return render_template("index.html")

@app.route('/search', methods = ['GET','POST'])
def search():
    if request.method == 'POST':
        try:
            reviews = []
            q = request.form['content'].replace(" ","-")
            flipkart_url = "https://www.flipkart.com/search?q=" + q
            urlclient = urlopen(flipkart_url)
            flipkart_page = urlclient.read()
            flipkart_html = bs(flipkart_page, "html.parser")
            outpg_box = flipkart_html.find_all("div", {"class" : "_1xHGtK _373qXS"})
            for box in outpg_box[0:10]:
                link = ("https://www.flipkart.com/search?q=" + box.a['href'])
                urlclient = urlopen(link)
                prdt_page = urlclient.read()
                prdt_html = bs(prdt_page, "html.parser")

                try:
                    find_brand = prdt_html.find("span", {"class" : "G6XhRU"})
                    brand = find_brand.text

                except:
                    find_brand = 'No brand'
                    logging.info(find_brand)

                try:
                    find_prdt_name = prdt_html.find("span", {"class" : "B_NuCI"})
                    prdt_name = find_prdt_name.text

                except:
                    prdt_name = 'Nothing'
                    logging.info(prdt_name)

                try:

                    find_prdt_price = prdt_html.find("div", {"class" : "_30jeq3 _16Jk6d"})
                    prdt_price = find_prdt_price.text

                except:
                    prdt_price = 'Nothing'
                    logging.info(prdt_price)

                try:
                    find_prdt_rating = prdt_html.find("div", {"class" : "_3LWZlK _3uSWvT"})
                    prdt_rating = find_prdt_rating.text

                except:
                    prdt_rating = 'None'
                    logging.info(prdt_rating)
                    
                mydict = {"search": q,"Brand": brand, "Name": prdt_name, "Price": prdt_price, "Rating": prdt_rating, "Buy": link}
                reviews.append(mydict)
            return render_template('result.html', reviews=reviews[0:(len(reviews)-1)])
        except Exception as e:
            logging.info(e)
            return 'something is wrong'
        # return "print('het')"


    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(host="0.0.0.0")