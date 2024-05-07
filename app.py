from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    # Fetch your data
    data = get_data()
    # Pass data to the template
    return render_template('index.html', data=data)

def get_data():
    # Your code to fetch data
    data = list("ONE", "TWO", "THREE")
    return data

if __name__ == '__main__':
    app.run(debug=True)