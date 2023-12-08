# Automated_AI_Based_ETL

# Automated AI-Based ETL Model (POC) documents QA

ETL stands for Extract, Transform, Load, which is a process used in data integration and data warehousing to move data from source systems to a target data store, such as a data warehouse.

AI-based Automated ETL:
- Efficiency: by automating repetitive and rule-based tasks 
- Accuracy: minimize the possible human risk 
- Scalability: AI-based ETL tools can scale quickly to handle large datasets
- Real-time Processing: AI-based ETL can be easily adapted with Data drift and ensures that the data pipeline is always up to date


### Implementation:  
- Implementing a POC using Open-AI ( GPT 3.5 ) GPT-3.5 can learn data drift in real time and update ETL pipelines automatically.

The essence of our demonstration lies in harnessing the capabilities of GPT-3.5, an AI model known for its ability to adapt to real-time data changes, thereby automating the ETL process. We have successfully implemented a foundational AI-driven ETL solution to showcase the untapped potential of AI in streamlining ETL workflows.

### Essential Requirements:
- OpenAI API Token: This token serves as the key to connect with the OpenAI platform.
- Python 3.8+: A prerequisite for running our AI-based ETL solution.
- Flask: We have employed Flask to create a user-friendly dashboard and graphical user interface.
- Pandas, Numpy: These data manipulation libraries are instrumental for parsing and analyzing datasets.
### Engine and Cost Efficiency:
- Within our project, we've chosen "text-davinci-003" as our GPT-3.5 model variant, which can effectively handle up to 4000 tokens. For our proof of concept, this variant is more than sufficient. Notably, the cost of utilizing this engine is approximately $0.002 per 1000 tokens, and this cost will be automatically computed and displayed during our live demonstration.
- By embracing the versatility and cost-effectiveness of GPT-3.5, we underscore the immense possibilities of automating the ETL process with AI.

### How to run:
- get an API token from Open-ai ( https://openai.com/blog/openai-api )
- python Etl_app.py
- open local host ( http://localhost:9009/)

### Demo: 
![REST_application](/Data/Babak_EA_2023_10_11.gif)




### Using Fast-API 
Cd Fast-API
bash start.sh
##### It will run the API on port 9009 , 
## test : 
- Localhost:9009/docs/

![Alt text](/Data/Screenshot 2023-10-12 134109.png)


### Python query :
Fast_API_query.ipynb

```
import requests

url = "http://127.0.0.1:9009/analyze/"  # Replace with the correct URL
api_key = "sk-EkqK*********************T0zU3"  # Replace with your API key
files = {
    'Raw_data': ('table_A.csv', open('./Data/table_A.csv', 'rb'), 'text/csv'),
    'Target_data': ('template.csv', open('./Data/template.csv', 'rb'), 'text/csv')
}

headers = {
    'accept': 'application/json',
}
params = {
    'api_key': api_key,
}
response = requests.post(url, headers=headers, params=params, files=files)

print(response.status_code)
print(response.json())
```
















