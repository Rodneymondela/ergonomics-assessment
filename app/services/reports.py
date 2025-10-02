from flask import render_template
def render_assessment_html(a):
    return render_template('assessments/print.html', a=a)
