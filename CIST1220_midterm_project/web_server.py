from flask import Flask, render_template, request
import sqlite3

import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

print(f"dir_path = {dir_path}")


cwd = os.getcwd()

print(f"cwd = {cwd}")

app = Flask(__name__, template_folder=f"{cwd}")
db_path = 'my_database.db'

def run_query(input1, input2):
    # Connect to SQLite database
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Execute the query with inputs
    #result = c.execute(f"SELECT * FROM my_table WHERE column1 = ? AND column2 = ?", (input1, input2)).fetchall()
    with open('midterm.sql', 'r') as f:
        sql = f.read()
    result = c.execute(sql).fetchall()

    return result

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get form data
        input1 = request.form['input1']
        input2 = request.form['input2']

        # Run the query against the database
        result = run_query(input1, input2)

        # Render the template with the result
        return render_template('result.html', result=result)
    else:
        # Display the form
        return render_template('index.html')
        #return render_template(f"{cwd}\\index.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0')

