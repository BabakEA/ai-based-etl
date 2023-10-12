# ai-based-etl

# Automated AI-Based ETL Model (POC)documents QA

ETL stands for Extract, Transform, Load, which is a process used in data integration and data warehousing to move data from source systems to a target data store, such as a data warehouse.

AI-based Automated ETL:
- Efficiency: by automating repetitive and rule-based tasks 
- Accuracy: minimize the possible human risk 
- Scalability: AI-based ETL tools can scale easily to handle large datasets
- Real-time Processing: AI-based ETL can be easily adapt with Data drift and ensures that the data pipeline is always up to date


### Implementation:  
- Implementing a POC using Open-AI ( GPT 3.5 ) GPT-3.5 can learn data drift in real-time and update ETL pipelines automatically.

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
- get a API token from Open-ai ( https://openai.com/blog/openai-api )
- python Etl_app.py
- open local host ( http://localhost:9009/)

### Demo: 
[Link to My Video](Babak_EA_2023_10_11.mp4)









