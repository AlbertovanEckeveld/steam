from flask import render_template

def page_not_found(error):
    return render_template('error.html', error_code=404, error_description=error), 404