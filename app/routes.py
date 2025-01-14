from flask import render_template, request
from app import app
from .orientation_advisor import OrientationAdvisor

advisor = OrientationAdvisor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    description = request.form.get('description', '')
    result, sisr_score, slam_score = advisor.analyze(description)
    advice = advisor.get_advice(result, sisr_score, slam_score)
    return render_template('result.html', 
                           result=result,
                           sisr_score=f"{sisr_score:.2f}",
                           slam_score=f"{slam_score:.2f}",
                           advice=advice)

