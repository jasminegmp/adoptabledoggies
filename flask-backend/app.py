import json
import flask
import pandas as pd

app = flask.Flask(__name__,
            static_url_path='',
            static_folder='build')

@app.route("/")
def index():
    df = pd.read_csv('90001_90083_test/90001_90083_breed_count.csv')
    chart_data = df.to_dict(orient='records')
    chart_data = json.dumps(chart_data, indent=2)
    data = {'chart_data': chart_data}
    return flask.render_template("index.html", data=data, token="HELLO!!!")


if __name__ == "__main__":
    app.run(debug=True)