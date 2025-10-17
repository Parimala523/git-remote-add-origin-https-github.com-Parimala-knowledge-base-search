from flask import Flask, request, render_template
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT
from whoosh.qparser import QueryParser
import os

app = Flask(__name__)

schema = Schema(title=TEXT(stored=True), content=TEXT)

# Index setup
if not os.path.exists("index"):
    os.mkdir("index")
    ix = create_in("index", schema)
    writer = ix.writer()

    for filename in os.listdir("documents"):
        filepath = os.path.join("documents", filename)
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
            writer.add_document(title=filename, content=content)
    writer.commit()
else:
    ix = open_dir("index")

# Search route
@app.route("/", methods=["GET", "POST"])
def search():
    results = []
    if request.method == "POST":
        query_str = request.form["query"]
        with ix.searcher() as searcher:
            query = QueryParser("content", ix.schema).parse(query_str)
            results = searcher.search(query)
    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)
