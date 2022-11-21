from flask import Flask, request
from markupsafe import escape
from flask import render_template
from elasticsearch import Elasticsearch
import math

ELASTIC_PASSWORD = "Onsonr12354"

es = Elasticsearch("https://localhost:5601", http_auth=("elastic", ELASTIC_PASSWORD), verify_certs=False)
app = Flask(__name__,template_folder='template')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    page_size = 10
    game_type = request.args.get('game_type')
    keyword = request.args.get('keyword')
    if request.args.get('page'):
        page_no = int(request.args.get('page'))
    else:
        page_no = 1

    body = {
        'size': page_size,
        'from': page_size * (page_no-1),
        'query': {
            'multi_match': {
                'query': keyword,
                'type': "most_fields",
                'fuzziness': "auto",
                "fuzzy_transpositions": True,
                'slop': 12,
                'auto_generate_synonyms_phrase_query': True,
                'zero_terms_query': "none",
                'fields': ['Name', 'Bio', 'Type']
            }
        }
    }
    #res = es.search(index='products', doc_type='', body=body)
    res = es.search(index=game_type, body=body)
    hits = [{'Name': doc['_source']['Name'], 'Bio': doc['_source']['Bio'], 'File_name': doc['_source']['File_name'], 'Type': doc['_source']['Type'], 'Skills': doc['_source']['Skills']} for doc in res['hits']['hits']]
    page_total = math.ceil(res['hits']['total']['value']/page_size)
    return render_template('search.html', game_type=game_type, keyword=keyword, hits=hits, page_no=page_no, page_total=page_total)