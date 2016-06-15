from flask import Flask, render_template_string
from flask.ext import breadcrumbs

breadcrumbs_tpl = """
{%- for breadcrumb in breadcrumbs -%}
{{ breadcrumb.text}}, {{ breadcrumb.url}};<br/>
{%- endfor -%}
"""

app = Flask(__name__)

# Initialize Flask-Breadcrumbs
breadcrumbs.Breadcrumbs(app=app)

@app.route('/')
@breadcrumbs.register_breadcrumb(app, '.', 'Home')
def index():
    """
    Home, /;
    """
    return render_template_string(breadcrumbs_tpl)

@app.route('/topic1.html')
@breadcrumbs.register_breadcrumb(app, '.topic1', 'Home')
def topic1():
    """
    Home,/;
    Home,/topic1.html;
    """
    return render_template_string(breadcrumbs_tpl)

@app.route('/topic1/topic2.html')
@breadcrumbs.register_breadcrumb(app, '.topic1.topic2', 'Home')
def topic2():
    """
    Home, /;
    Home, /topic1.html;
    Home, /topic1/topic2.html;
    """
    return render_template_string(breadcrumbs_tpl)

if __name__ == '__main__':
    app.run(debug=True)
