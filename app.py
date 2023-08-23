from flask import Flask, request, render_template, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'search' in request.form:
            search_input = request.form['searchInput']
            # Perform search logic
            # Save results to session
            session['searchResults'] = search_results

        elif 'scan' in request.form:
            # Perform scan logic
            scan_results = ["Station 1", "Station 2", "Station 3"]
            # Save results to session
            session['scanResults'] = scan_results

    return render_template('index.html', search_results=session.get('searchResults'), scan_results=session.get('scanResults'))

if __name__ == '__main__':
    app.run(debug=True)
