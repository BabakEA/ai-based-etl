



from time import *
from datetime import *


from flask import Flask, request, render_template, redirect,send_file,url_for
import pandas as pd
import os

import openai
import json
import numpy as np
from numpy import array
import re

##################

def extract_array(text,Columns):
    # Use regular expressions to find the desired array
    pattern = r'\[.*\]'
    match = re.search(pattern, text, re.DOTALL)

    if match:
        extracted_array = match.group()
        #extracted_array=pd.DataFrame(data=eval(extracted_array),columns=Columns)

        return eval(extracted_array)
    else:
        return "Array not found in the text."



def _Column_Analyser(Raw_df:pd.DataFrame,Target_df:pd.DataFrame,api_key:str):
    Columns=Target_df.columns.tolist()

    # Specify the prompt for GPT-3.5
    prompt = f""" i have the following data,  data:\n{list(Raw_df.values)}\n\n
    and I want to remove the unvanted and doplicated columns and select the columns that are similar to the traget_data ,
    target_data:\n{list(Target_df[:3].values)}\n\n .
    data in the selected columns may have extra characters, please remove them and format the data the same as target_data. """

    # Send a completion request to GPT-3.5
    response = openai.Completion.create(
        engine="text-davinci-003",  # You can specify the engine you prefer
        prompt=prompt,
        max_tokens=400,  # Adjust this based on the expected response length
        api_key=api_key
    )
    Total_tokens=response.usage["total_tokens"]
    Total_cost=Total_tokens*0.000003

    Cost={"Total_tokens":Total_tokens,"Total_cost":Total_cost}

    # Extract the suggestions and reformatted dataset from the response
    suggestions_and_reformatted_data = response.choices[0].text
    try:
        DF=extract_array(suggestions_and_reformatted_data,Columns)
        #Columns=Target_df.columns.tolist()
        DF=pd.DataFrame(data=DF,columns=Columns)
        return DF,Cost
    except:
        return pd.DataFrame(),Cost


app = Flask(__name__)


Download = "./Download"

if not os.path.exists(Download):
    os.makedirs(Download)

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['Download'] = 'Download'  # Define the download folder

# @app.route('/download')
# def download_file():
#     file_path = os.path.join(app.config['Download'], f'competed_{str(date.today()).replace("-", "_")}.csv')
#     return send_file(file_path, as_attachment=True)




# @server.route("/download/<path:path>")
# def download(path):
#     """Serve a file from the upload directory."""
#     return send_from_directory(downloads, path, as_attachment=True)



# def file_download_link(filename):
#     """Create a Plotly Dash 'A' element that downloads a file from the app."""
#     location = "/download/{}".format(urlquote(filename))
#     return html.A(filename, href=location)

@app.route('/Download')
def download_file():
    path = f"Download/competed_{str(date.today()).replace('-','_')}.csv"

    return send_file(path, as_attachment=True)



@app.route('/')
def index():
    return render_template('ETL_dashboard.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    Counter=0
    api_key = request.form.get('api_key')
    file1 = request.files['file_upload_1']
    file2 = request.files['file_upload_2']
    #file2.save(os.path.join(app.config['UPLOAD_FOLDER'], 'Target.csv'))


    if file1 and file2:
        file1.save(os.path.join(app.config['UPLOAD_FOLDER'], 'file1.csv'))
        file2.save(os.path.join(app.config['UPLOAD_FOLDER'], 'Target.csv'))

        Raw_df = pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], 'file1.csv'))
        Target_df = pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], 'Target.csv'))

        #sleep(2)
        Start=datetime.now()
        Data,Cost=_Column_Analyser(Raw_df=Raw_df,Target_df=Target_df,api_key=api_key)
        Linke_to_Return=""
        if len(Data)>=3 and Counter<=2:

            Procceing_time=datetime.now()-Start
            Data.to_csv(os.path.join(app.config['Download'], f'competed_{str(date.today()).replace("-","_")}.csv'))

            Number_of_Rows=Raw_df.shape[0]

            Linke_to_Return=os.path.join(app.config['Download'], f'competed_{str(date.today()).replace("-","_")}.csv')


            describe_text = f"""
            Raw_df:<br>{Raw_df.head().to_html()}<br><br>

            Cleaned data:<br>{Data.head().to_html()}"""

            INFO_Cost= f"""
            Total Rows : {Number_of_Rows}   ********* Total Tokens : {Cost["Total_tokens"]} *********Total Cost : {Cost["Total_cost"]}  US$ <hr><br>
            """

        elif len(Data)<=1 and Counter>=2:
            Counter+=1
            Data,Cost=_Column_Analyser(Raw_df=Raw_df,Target_df=Target_df,api_key=api_key)
        else:
            describe_text = "I cannot connect with the API, Pleas check the API-key and try it again."
            INFO_Cost=""
            Linke_to_Return=""
            #break
    else:
        describe_text = "No file uploaded."
        INFO_Cost=""

    return render_template('ETL_dashboard.html', describe_text=describe_text,Api_key=INFO_Cost,DL=Linke_to_Return)

if __name__ == '__main__':
    app.run(debug=False,port=9009)




