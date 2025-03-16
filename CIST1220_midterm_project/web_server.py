from flask import Flask, render_template, request
import sqlite3
import csv
import io

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
    # Your SQL should be saved in midterm.sql, which will be read from the file and executed in the "with" statement below.
    with open('midterm.sql', 'r') as f:
        for sql in f:
            if sql.strip().startswith("#"):
                print(f"Ignoring comment:  {sql}")
            else:
                print(f"Executing SQL:  {sql}")
                result = c.execute(sql, (input1, input2)).fetchall()

    return result

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get form data from index.html
        input1 = request.form['input1']
        input2 = request.form['input2']

        # Run the query against the database
        result = run_query(input1, input2)

        # Render the template with the result
        return render_template('result.html', result=result)
    else:
        # Display the form
        return render_template('index.html')

@app.route('/csv', methods=['GET', 'POST'])
def csv_export():
    # Connect to SQLite database
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    with open('midterm.sql', 'r') as f:
        for sql in f:
            if sql.strip().startswith("#"):
                print(f"Ignoring comment:  {sql}")
            else:
                print(f"Executing SQL:  {sql}")
                sql = "select * from my_table"
                result = c.execute(sql).fetchall()

                csv_output = io.StringIO()
                csv_writer = csv.writer(csv_output)
                csv_writer.writerows(result)
                csv_string = csv_output.getvalue()
                csv_output.close()
                conn.close()
                print(csv_string)

    return csv_string.replace("\n", "<br />")

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0')

