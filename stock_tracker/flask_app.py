from flask import Flask, render_template_string
import httpx
from selectolax.parser import HTMLParser

app = Flask(__name__)

@app.route("/")
def display_table():
    # Fetch the HTML content
    url = 'https://www.5paisa.com/nifty-50-stocks-list'
    response = httpx.get(url, timeout=5.0)
    html_content = response.text

    # Parse the HTML using selectolax
    tree = HTMLParser(html_content)

    # Find the table
    table = tree.css_first(".table-responsive")

    if table:
        # Extract headers
        headers = [th.text(strip=True) for th in table.css('th')]

        # Extract rows
        rows = [
            [td.text(strip=True) for td in row.css('td')]
            for row in table.css('tr')[1:]  # Skip the header row
        ]

        # Render the table using Flask and Bootstrap
        return render_template_string(TABLE_TEMPLATE, headers=headers, rows=rows)
    else:
        return "<h1>No table found!</h1>"

# Bootstrap Table Template
TABLE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nifty 50 Stocks</title>
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container my-5">
        <h1 class="text-center mb-4">Nifty 50 Stocks</h1>
        <div class="table-responsive">
            <table class="table table-bordered table-hover table-striped">
                <thead class="table-dark">
                    <tr>
                        {% for header in headers %}
                        <th>{{ header }}</th>
                        {% endfor %}
                    </tr>
                </thead>
                <tbody>
                    {% for row in rows %}
                    <tr>
                        {% for cell in row %}
                        <td>{{ cell }}</td>
                        {% endfor %}
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

if __name__ == "__main__":
    app.run(debug=True)
