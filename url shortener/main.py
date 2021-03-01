from flask import Flask, render_template, request, redirect
import pymongo
import random as rand
from pymongo import message
import validators as vald

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
mycol = mydb["link"]


def rnd():
    return str(hex(rand.randrange(0, 0xffff))).replace("0x", "").rjust(4, "0")


def handel(link):
    if vald.url(link):
        myquery = {"link": link}
        if mycol.count_documents(myquery) == 0:
            id = rnd()
            while mycol.count_documents({"_id": id}) != 0:
                rand.seed(10)
                id = rnd()
            new_link = {"_id": id, "link": link}
            mycol.insert_one(new_link)
            print(f'id:{id} link:{link}')
            return id
        else:
            item = mycol.find_one(myquery)
            print(f'id:{item.get("_id")} link:{item.get("link")}')
            return item.get("_id")
    else:
        return False


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html', message='SHORTEN YOUR LINK 8---D')


@app.route('/shorten', methods=['POST'])
def shorten():
    link = request.form["link"]
    a = handel(link)
    if not a:
        return render_template('index.html', message='not a link')
    else:
        return render_template('index.html', message=a)


@app.route("/<id>")
def redir(id):
    myquery = {"_id": id}
    if mycol.count_documents(myquery) != 0:
        item = mycol.find_one(myquery)
        return redirect(item.get("link"))
    else:
        return "no such link"


if __name__ == "__main__":
    app.run(debug=True)
