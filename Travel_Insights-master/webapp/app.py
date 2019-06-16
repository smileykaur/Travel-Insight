from flask import Flask, render_template, url_for, request
from flask import Flask, jsonify, abort, request, make_response
import pandas as pd
import math

app = Flask(__name__)

# read data source
df = pd.read_csv("./data/nlp_processed_corpus.csv")  # For NER
topics_df=pd.read_csv("./data/topics_by_submissionid.csv")  # For Topics

# -----------------
# Error Handling
# -----------------
@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Check Input parameter'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'No Items in list'}), 404)


@app.errorhandler(408)
def not_found(error):
    return make_response(jsonify({'error': 'Invalid submission Id'}), 408)


# --- NER Processing --
# ---------------------
def get_NER(choice, input_submission_id):
    """
    Generate NER entities for given submission Id from developer
    :param choice: Option from User - Can be either Destination / Organization/ Product
    :param input_submission_id: Reddit Submission Id
    :return: List of items
    """
    results = None

    # If Destination parameter
    if choice == 'destination':
        destination = df.query('submission_id=="{sub_id}"'.
                               format(sub_id=input_submission_id))['top_destination'].values[0]
        try:
            results = destination.split(',')
        except:
            results = ["There are no destinations"]

    # If Organization parameter
    if choice == 'organization':
        organization = df.query('submission_id=="{sub_id}"'.
                                format(sub_id=input_submission_id))['top_organization'].values[0]
        try:
            results = organization.split(',')
        except:
            results = ["There are no organizations"]

    # If Product parameter
    if choice == 'product':
        product = df.query('submission_id=="{sub_id}"'.
                           format(sub_id=input_submission_id))['top_product'].values[0]
        try:
            results = product.split(",")
        except:
            results = ["There are no product entities"]

    # If Topic parameter
    if choice == 'topic':
        try:
            topic = topics_df.query('submission_id=="{sub_id}"'.
                                    format(sub_id=input_submission_id))['topics'].values[0].split(',')
            results = []
            cnt = 1
            for i in range(0, len(topic), 5):
                results.append(("Topic-{0}".format(cnt), topic[i:i + 5]))
                cnt += 1
        except:
            results=["There are no topics in this submission_id"]

    return results


# If NER processing needed
def ner_processing(choice, submisison_id):
    # check if valid Submission_id
    if df['submission_id'].isin([submisison_id]).any():
        results = get_NER(choice, submisison_id)
        print(results)
        return results
    else:
        abort(408)


# If Topic Modelling needed
def topic_processing(text):
    results = text
    return results


# ---- POST Requests: Web Application -----
# ------------------------------------------------
# Sample Id - 8h6aao
@app.route('/process', methods=['POST'])
def process():
    if request.method == 'POST':
        # input parameters
        user_choice = request.form['taskoption'].strip()
        text_field = request.form['submission_id'].strip()

        results = ["There is some error processing your request"]

        #if user_choice == "topic":
        #    results = topic_processing(text_field)  # Topic Modelling
        #else:
        results = ner_processing(user_choice, text_field)  # NER Processing

        return render_template("index.html", results=results, num_of_results=len(results))


# ---- GET Requests: Developer API -----
# ------------------------------------------
@app.route('/travelinsight/api/v1/NER/', methods=['GET'])
def get_ner_list():
    """
    Sample request  -
    curl -i -H "Content-Type: application/json" -X GET -d '{"taskoption":"topic", "submission_id":"8h6aao"}' http://localhost:5000/travelinsight/api/v1/NER/
    """
    if not request.json or not 'submission_id' in request.json or not 'taskoption' in request.json:
        abort(400)
    else:
        choice = request.json['taskoption']
        submission_id = request.json['submission_id']

        # NER Processing
        results = ner_processing(choice, submission_id)
        return jsonify({choice: results})


# ---- Home -----
# ----------------
@app.route('/')
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
