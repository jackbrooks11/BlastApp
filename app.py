from flask import Flask, render_template, request
from wtforms.widgets import TextArea
from wtforms import StringField, validators, Form
from Bio.Blast import NCBIWWW, NCBIXML
app = Flask(__name__)

class SearchForm(Form):
    sequence = StringField('sequence', [validators.Regexp(r"^[>][\w.:*#]+( [\S]+)+((\r)?\n[ACGTURYKMSWBDHVN-]+)+$")])

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', form=SearchForm())

@app.route('/retrieve_results', methods=['GET'])
def retrieve_results():
    form = SearchForm(request.args)
    if form.validate():
        sequence = request.args['sequence']
        results = NCBIWWW.qblast("blastn", "nt", sequence)
        hits = NCBIXML.read(results).descriptions
        if not hits:
            return render_template('index.html', empty=True, form=form)
        hits.sort(key=lambda x: x.score, reverse=True)
        return render_template('index.html', hits=hits, form=form)
    return render_template('index.html', form=form)

if __name__ == "__main__":
   app.run(debug=True)