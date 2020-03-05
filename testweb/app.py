from flask import Flask, render_template
import plotly.figure_factory as ff
import plotly
import json

import numpy as np
import pandas as pd

app = Flask(__name__)

# @는 밑에 def를 바로 실행시킴
@app.route('/')
def index():
    bar = create_gantt()
    return render_template('index.html', plot=bar)


def create_gantt():
    
    process_product = pd.read_excel(
        'data/Tumbler_Factory_revision.xlsx', sheet_name = 'EQP_PLAN',
        index='EQP_ID', usecols='B,F,H,I', header=0, encoding='utf-8')

                        
    process_product.rename(columns={process_product.columns[0]:'Task'}, inplace=True)
    process_product.rename(columns={process_product.columns[1]:'Resource'}, inplace=True)
    process_product.rename(columns={process_product.columns[2]:'Start'}, inplace=True)
    process_product.rename(columns={process_product.columns[3]:'Finish'}, inplace=True)

    process_product=process_product.to_dict('records')

    fig = ff.create_gantt(
        process_product, index_col='Resource', 
        title='Process by products', group_tasks=True,
        show_colorbar=True, bar_width=0.2, showgrid_x=True, showgrid_y=True)


    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

#단독으로 파이썬 명령이 들어왔을때만 포트 실행
if __name__ == '__main__':
    app.run(debug=True)
#개발할 때 항상 debug mode를 ON으로 하기!

