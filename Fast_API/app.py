from time import *
from datetime import *

import os

import openai
import json
import numpy as np
from numpy import array
import re

from fastapi import FastAPI, UploadFile, File, HTTPException, Query
import pandas as pd
from pydantic import BaseModel
import io
import logging



#######################
######## Open API ######

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

    
#################################
########### FastAPI#############

app = FastAPI()

# Model for the API request
class APIRequest(BaseModel):
    api_key: str

# Route for uploading CSV files and API key
@app.post("/analyze/")
async def analyze(api_key: str = Query(..., description="Your API key"), Raw_data: UploadFile = File(...), Target_data: UploadFile = File(...)):
    logger = logging.getLogger("my_logger")

    logger.info(api_key)

    try:
        Raw_data = await Raw_data.read()
        Target_data = await Target_data.read()

        Raw_df = pd.read_csv(io.StringIO(Raw_data.decode('utf-8')))
        Target_df = pd.read_csv(io.StringIO(Target_data.decode('utf-8')))
        Start=datetime.now()
        Data,Cost=_Column_Analyser(Raw_df=Raw_df,Target_df=Target_df,api_key=api_key)
        processing_time=datetime.now()-Start
        Number_of_Rows=Raw_df.shape[0]
        
        


        # Perform your analysis here

        response = {
            "message": "CSV files processed successfully",
            "Number_of_Rows":Number_of_Rows,
            "Totoal_token":Cost["Total_tokens"],
            "Processing_Cost":Cost["Total_cost"],
            "cleaned_data": Data.to_dict(orient="list")
            
        }
        return response
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

        
        
        
