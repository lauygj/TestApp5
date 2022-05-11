# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 18:03:36 2022

This is a seriously floored proof of concept web app. It's purpose is to 
help prostate cancer patients make an informed decision about their treatment 
options. 

The main library in use here is Flask. 
https://flask.palletsprojects.com/en/2.1.x/quickstart/# 

The HTML templates inherit from a base.html template which uses a stylesheet 
taken from the web.

The return_cpg_score method uses an imported csv file
and is not robust to unexpected user input. 

Must make HTTP form inputs drop down boxes, not free text. 

@author: stubbinl
@author: lauj
"""

from flask import Flask, redirect, url_for, render_template, request, session
import pandas as pd 

app = Flask(__name__)

app.config['SECRET_KEY'] = 'a1e73095d9cd320cc32d2f59'

# read csv 
#path_csv = 'U:\Joanna Lau\Projects\ProstateWebApp\TestApp3\cpg_table.csv'
#df = pd.read_csv(path_csv)

df = pd.DataFrame({
    'CPG': [1,1,2,2,2,2,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5],
    'Grade Group': ['GG1','GG1','GG1','GG1','GG2','GG2','GG2','GG2','GG3','GG3','GG3','GG3','GG1','GG1','GG2','GG2','GG3','GG3','GG1','GG2','GG3','GG1','GG2','GG3','GG1','GG2','GG3','GG1','GG2','GG3','GG4','GG4','GG4','GG4','GG1','GG2','GG3','GG1','GG2','GG3','GG1','GG2','GG3','GG1','GG2','GG3','GG1','GG2','GG3','GG4','GG4','GG4','GG4','GG4','GG4','GG4','GG4','GG4','GG4','GG4','GG5','GG5','GG5','GG5','GG5','GG5','GG5','GG5','GG5','GG5','GG5','GG5','GG5','GG5','GG5'],
    'PSA': ['P<10','P<10','P10-20','P10-20','P<10','P<10','P10-20','P10-20','P<10','P<10','P10-20','P10-20','P>20','P>20','P>20','P>20','P>20','P>20','P<10','P<10','P<10','P10-20','P10-20','P10-20','P<10','P<10','P<10','P10-20','P10-20','P10-20','P<10','P<10','P10-20','P10-20','P>20','P>20','P>20','P>20','P>20','P>20','P<10','P<10','P<10','P10-20','P10-20','P10-20','P>20','P>20','P>20','P>20','P>20','P>20','P>20','P>20','P<10','P<10','P<10','P10-20','P10-20','P10-20','P<10','P<10','P<10','P<10','P<10','P10-20','P10-20','P10-20','P10-20','P10-20','P>20','P>20','P>20','P>20','P>20'],
    'Stage': ['T1','T2','T1','T2','T1','T2','T1','T2','T1','T2','T1','T2','T1','T2','T1','T2','T1','T2','T3a','T3a','T3a','T3a','T3a','T3a','T3b','T3b','T3b','T3b','T3b','T3b','T1','T2','T1','T2','T3a','T3a','T3a','T3b','T3b','T3b','T4','T4','T4','T4','T4','T4','T4','T4','T4','T1','T2','T3a','T3b','T4','T3a','T3b','T4','T3a','T3b','T4','T1','T2','T3a','T3b','T4','T1','T2','T3a','T3b','T4','T1','T2','T3a','T3b','T4'],
    'CRITERIA': ['GG1P<10T1','GG1P<10T2','GG1P10-20T1','GG1P10-20T2','GG2P<10T1','GG2P<10T2','GG2P10-20T1','GG2P10-20T2','GG3P<10T1','GG3P<10T2','GG3P10-20T1','GG3P10-20T2','GG1P>20T1','GG1P>20T2','GG2P>20T1','GG2P>20T2','GG3P>20T1','GG3P>20T2','GG1P<10T3a','GG2P<10T3a','GG3P<10T3a','GG1P10-20T3a','GG2P10-20T3a','GG3P10-20T3a','GG1P<10T3b','GG2P<10T3b','GG3P<10T3b','GG1P10-20T3b','GG2P10-20T3b','GG3P10-20T3b','GG4P<10T1','GG4P<10T2','GG4P10-20T1','GG4P10-20T2','GG1P>20T3a','GG2P>20T3a','GG3P>20T3a','GG1P>20T3b','GG2P>20T3b','GG3P>20T3b','GG1P<10T4','GG2P<10T4','GG3P<10T4','GG1P10-20T4','GG2P10-20T4','GG3P10-20T4','GG1P>20T4','GG2P>20T4','GG3P>20T4','GG4P>20T1','GG4P>20T2','GG4P>20T3a','GG4P>20T3b','GG4P>20T4','GG4P<10T3a','GG4P<10T3b','GG4P<10T4','GG4P10-20T3a','GG4P10-20T3b','GG4P10-20T4','GG5P<10T1','GG5P<10T2','GG5P<10T3a','GG5P<10T3b','GG5P<10T4','GG5P10-20T1','GG5P10-20T2','GG5P10-20T3a','GG5P10-20T3b','GG5P10-20T4','GG5P>20T1','GG5P>20T2','GG5P>20T3a','GG5P>20T3b','GG5P>20T4']})

# Error string
error_url = 'error_page'
# 
def return_cpg_score(df,g, psa, stage):
    ''' return CPG score from string input G, PSA & Stage'''
    #criteria = 'G'+g+'P'+psa+stage
    criteria = g+'P'+psa+stage
    try:
        df.loc[df['CRITERIA']==criteria]['CPG'].values[0]
    except IndexError:
        return error_url
    else:
        return str(df.loc[df['CRITERIA']==criteria]['CPG'].values[0])
 
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/'+error_url)
def error_page():
    return render_template('error_page.html')

@app.route('/cpg1', methods=('GET', 'POST'))
def cpg1():
    gradeval = session["gradeval"]
    psaval = session["psaval"]
    stageval = session["stageval"]
    if request.method == 'POST':
        return redirect(url_for('managementoptions1'))
    else:
        return render_template('cpg1.html',grade=gradeval,psa=psaval,stage=stageval)

@app.route('/cpg2', methods=('GET', 'POST'))
def cpg2():
    gradeval = session["gradeval"]
    psaval = session["psaval"]
    stageval = session["stageval"]    
    if request.method == 'POST':
        return redirect(url_for('managementoptions2'))
    else:
        return render_template('cpg2.html',grade=gradeval,psa=psaval,stage=stageval)

@app.route('/cpg3', methods=('GET', 'POST'))
def cpg3():
    gradeval = session["gradeval"]
    psaval = session["psaval"]
    stageval = session["stageval"]      
    if request.method == 'POST':
        return redirect(url_for('managementoptions3'))
    else:  
        return render_template('cpg3.html',grade=gradeval,psa=psaval,stage=stageval)

@app.route('/cpg4', methods=('GET', 'POST'))
def cpg4():
    gradeval = session["gradeval"]
    psaval = session["psaval"]
    stageval = session["stageval"]    
    if request.method == 'POST':
        return redirect(url_for('managementoptions4'))
    else:
        return render_template('cpg4.html',grade=gradeval,psa=psaval,stage=stageval)

@app.route('/cpg5', methods=('GET', 'POST'))
def cpg5():
    gradeval = session["gradeval"]
    psaval = session["psaval"]
    stageval = session["stageval"]    
    if request.method == 'POST':
        return redirect(url_for('managementoptions5'))
    else:
        return render_template('cpg5.html',grade=gradeval,psa=psaval,stage=stageval)

@app.route('/activesurveillance', methods=('GET', 'POST'))
def activesurveillance():
    if request.method == 'POST':
        buttAS = request.form['button']
        buttASDict = {
            'descriptionAS':'descriptionAS',
            'benefitsAS':'benefitsAS',
            'risksAS':'risksAS',
            'animationsAS':'animationsAS'
            }
        return redirect(url_for(buttASDict[buttAS]))       
    else:
        return render_template('activesurveillance.html')

@app.route('/managementoptions1', methods=('GET', 'POST'))
def managementoptions1():
    if request.method == 'POST':
        buttMO1 = request.form['button']
        buttMO1Dict = {
            'activesurveillance':'activesurveillance',
            'radicalprostectomy':'radicalprostectomy',
            'radbrach':'radbrach'
            }
        return redirect(url_for(buttMO1Dict[buttMO1]))
    else:
        return render_template('managementoptions1.html')

@app.route('/managementoptions2', methods=('GET', 'POST'))
def managementoptions2():
    if request.method == 'POST':
        buttMO2 = request.form['button']
        buttMO2Dict = {
            'activesurveillance':'activesurveillance',
            'radicalprostectomy':'radicalprostectomy',
            'RR6':'RR6',
            'RBB':'RBB'
            }
        return redirect(url_for(buttMO2Dict[buttMO2]))
    else:
        return render_template('managementoptions2.html')

@app.route('/managementoptions3', methods=('GET', 'POST'))
def managementoptions3():
    if request.method == 'POST':
        buttMO3 = request.form['button']
        buttMO3Dict = {
            'radicalprostectomy':'radicalprostectomy',
            'RR6':'RR6',
            'RBB':'RBB',
            'activesurveillance':'activesurveillance'
            }
        return redirect(url_for(buttMO3Dict[buttMO3]))
    else:
        return render_template('managementoptions3.html')

@app.route('/managementoptions4', methods=('GET', 'POST'))
def managementoptions4():
    if request.method == 'POST':
        buttMO4 = request.form['button']
        buttMO4Dict = {
            'radicalprostectomy':'radicalprostectomy',
            'RR6':'RR6',
            'RR3':'RR3',
            'RRB':'RRB'
            }
        return redirect(url_for(buttMO4Dict[buttMO4]))
    else:
        return render_template('managementoptions4.html')

@app.route('/managementoptions5', methods=('GET', 'POST'))
def managementoptions5():
    if request.method == 'POST':
        buttMO5 = request.form['button']
        buttMO5Dict = {
            'radicalprostectomy':'radicalprostectomy',
            'RR6':'RR6',
            'RR3':'RR3',
            'RBB':'RBB',
            'docchem':'docchem'
            }
        return redirect(url_for(buttMO5Dict[buttMO5]))
    else:
        return render_template('managementoptions5.html')

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
            grade = request.form['grade']
            psaInput = request.form['psa']
            F = float(psaInput)
            psa=''
            if F < 10:
                psa = '<10'
            elif F > 20:
                psa = '>20'
            else:
                psa = '10-20'
            stage = request.form['stage']
            session["gradeval"] = grade
            session["psaval"] = psaInput
            session["stageval"] = stage
            cpg_string = return_cpg_score(df, grade, psa, stage)
            if error_url not in cpg_string:
                return redirect(url_for('cpg'+cpg_string))
                #return redirect(url_for('cpg'+cpg_string, grade=grade, psa=psa, stage=stage))
                #return render_template('cpg'+cpg_string+'.html', grade=grade, psa=psa, stage=stage)
            else:
                return redirect(url_for(error_url))
    else:
        return render_template('create.html')

@app.route('/descriptionAS')
def descriptionAS():
    return render_template('descriptionAS.html')

@app.route('/benefitsAS')
def benefitsAS():
    return render_template('benefitsAS.html')

@app.route('/risksAS')
def risksAS():
    return render_template('risksAS.html')

@app.route('/animationsAS')
def animationsAS():
    return render_template('animationsAS.html')

@app.route('/radicalprostectomy', methods=('GET', 'POST'))
def radicalprostectomy():
    if request.method == 'POST':
        buttRP = request.form['button']
        buttRPDict = {
            'descriptionRP':'descriptionRP',
            'benefitsRP':'benefitsRP',
            'risksRP':'risksRP',
            'animationsRP':'animationsRP'
            }
        return redirect(url_for(buttRPDict[buttRP]))
    else:
        return render_template('radicalprostectomy.html')

@app.route('/radbrach', methods=('GET', 'POST'))
def radbrach():
    if request.method == 'POST':
        buttRB = request.form['button']
        buttRBDict = {
            'descriptionRB':'descriptionRB',
            'benefitsRB':'benefitsRB',
            'risksRB':'risksRB',
            'animationsRB':'animationsRB'
            }
        return redirect(url_for(buttRBDict[buttRB]))
    else:    
        return render_template('radbrach.html')

@app.route('/RR6', methods=('GET', 'POST'))
def RR6():
    if request.method == 'POST':
        buttRR6 = request.form['button']
        buttRR6Dict = {
            'descriptionRR6':'descriptionRR6',
            'benefitsRR6':'benefitsRR6',
            'risksRR6':'risksRR6',
            'animationsRR6':'animationsRR6'
            }
        return redirect(url_for(buttRR6Dict[buttRR6]))
    else:      
        return render_template('RR6.html')

@app.route('/RBB', methods=('GET', 'POST'))
def RBB():
    if request.method == 'POST':
        buttRBB = request.form['button']
        buttRBBDict = {
            'descriptionRBB':'descriptionRBB',
            'benefitsRBB':'benefitsRBB',
            'risksRBB':'risksRBB',
            'animationsRBB':'animationsRBB'
            }
        return redirect(url_for(buttRBBDict[buttRBB]))
    else:     
        return render_template('RBB.html')

@app.route('/RR3', methods=('GET', 'POST'))
def RR3():
    if request.method == 'POST':
        buttRR3 = request.form['button']
        buttRR3Dict = {
            'descriptionRR3':'descriptionRR3',
            'benefitsRR3':'benefitsRR3',
            'risksRR3':'risksRR3',
            'animationsRR3':'animationsRR3'
            }
        return redirect(url_for(buttRR3Dict[buttRR3]))
    else:  
        return render_template('RR3.html')

@app.route('/docchem', methods=('GET', 'POST'))
def docchem():
    if request.method == 'POST':
        buttDC = request.form['button']
        buttDCDict = {
            'descriptionDC':'descriptionDC',
            'benefitsDC':'benefitsDC',
            'risksDC':'risksDC',
            'animationsDC':'animationsDC'
            }
        return redirect(url_for(buttDCDict[buttDC]))
    else:
        return render_template('docchem.html')

@app.route('/descriptionRP')
def descriptionRP():
    return render_template('descriptionRP.html')

@app.route('/descriptionRB')
def descriptionRB():
    return render_template('descriptionRB.html')

@app.route('/descriptionRR6')
def descriptionRR6():
    return render_template('descriptionRR6.html')

@app.route('/descriptionRR3')
def descriptionRR3():
    return render_template('descriptionRR3.html')

@app.route('/descriptionRBB')
def descriptionRBB():
    return render_template('descriptionRBB.html')

@app.route('/descriptionDC')
def descriptionDC():
    return render_template('descriptionDC.html')

@app.route('/benefitsRP')
def benefitsRP():
    return render_template('benefitsRP.html')

@app.route('/benefitsRB')
def benefitsRB():
    return render_template('benefitsRB.html')

@app.route('/benefitsRR6')
def benefitsRR6():
    return render_template('benefitsRR6.html')

@app.route('/benefitsRR3')
def benefitsRR3():
    return render_template('benefitsRR3.html')

@app.route('/benefitsRBB')
def benefitsRBB():
    return render_template('benefitsRBB.html')

@app.route('/benefitsDC')
def benefitsDC():
    return render_template('benefitsDC.html')

@app.route('/risksRP')
def risksRP():
    return render_template('risksRP.html')

@app.route('/risksRB')
def risksRB():
    return render_template('risksRB.html')

@app.route('/risksRR6')
def risksRR6():
    return render_template('risksRR6.html')

@app.route('/risksRR3')
def risksRR3():
    return render_template('risksRR3.html')

@app.route('/risksRBB')
def risksRBB():
    return render_template('risksRBB.html')

@app.route('/risksDC')
def risksDC():
    return render_template('risksDC.html')

@app.route('/animationsRP')
def animationsRP():
    return render_template('animationsRP.html')

@app.route('/animationsRB')
def animationsRB():
    return render_template('animationsRB.html')

@app.route('/animationsRR6')
def animationsRR6():
    return render_template('animationsRR6.html')

@app.route('/animationsRR3')
def animationsRR3():
    return render_template('animationsRR3.html')

@app.route('/animationsRBB')
def animationsRBB():
    return render_template('animationsRBB.html')

@app.route('/animationsDC')
def animationsDC():
    return render_template('animationsDC.html')

if __name__ == "__main__":
	app.run()
