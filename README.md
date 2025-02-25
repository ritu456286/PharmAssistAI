# PharmAssistAI

- From Symptoms to Solutions—Instantly.
# Features
# Architecture [architecture image from images folder]
# Future Enhancements
# Specifications for device

# Requirements to run the project
- Free Disk space of 7-8 GB to install llama3.2-vision:11b or 5-6 GB for Llava-7B model for OCR text extraction.
- Nvidia CUDA GPU, to run the OCR model.
- First install Ollama, from here: https://ollama.com/download
- To install llama3.2-vision:11b, 
```
ollama pull llama3.2-vision:11b
```
For more information, pls visit: https://ollama.com/library/llama3.2-vision:11b
- - To install llava:7b, 
```
ollama pull llava:7b
```
For more information, pls visit: https://ollama.com/library/llava:7b

# Setting up the project
- To setup this project in your device, first clone this repository using:
```
git clone : 
cd /PharmAssistAI
```
1. Let's set up the Backend. Go inside backend folder.
- Create a python virtual environment
```
python -m venv venv
```
- Install all requirements.
```
pip install -r requirements.txt
```
- Create a `.env` file in `/backend` folder with the following keys:
```
GEMINI_API_KEY= <your gemini-2.0 api key>
```
- Create an empty folder inside /src named `db` --> /src/db. Here the Sqlite and chromaDB will be stored.
- Setup for backend is complete, you can run the fastapi server now, by executing the following command:
```
run.sh
```

2. Next, setup the frontend.
- Create a python virtual environment
```
python -m venv venv
```
- Install all requirements.
```
pip install -r requirements.txt
```
- Create a `.env` file in `/frontend` folder with the following keys:
```
BASE_URL=<url where your fastapi backend server is running>
```
- Serve the ollama model(s), run this from terminal:
```
ollama serve
```
This will serve the model on "http://localhost:11434/api/generate". You can also change the port to serve the model, but then make sure to add this variable in your   `/frontend/.env` file:
```
OLLAMA_URL=<your hosted url for Ollama model>
```
- Setup for frontend is complete, you can run the streamlit app now, by executing the following command:
```
streamlit run main.py
```

- Now, your frontend should be running, backend should be running as well as Ollama models are also being served.
