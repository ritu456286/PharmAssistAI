# PharmAssistAI

## Overview  
This AI-powered assistant helps pharmacists automate prescription processing, medicine identification, and also efficiently manage inventory. It also provides reliable alternative medicine suggestions if medicines demanded are not available in the current stock and provide herbal remedy recommendations from trusted sources, ensuring pharmacists can assist customers more efficiently while maintaining trust.  

---

## 🚀 Features  
- **Prescription Processing** – Extracts text from handwritten prescriptions using advanced OCR and NLP models.  
- **Alternative Medicine Suggestions** – Uses ChromaDB for vector-based search to find similar medicines.  
- **Herbal Remedies Recommendations** – Provides AI-powered herbal suggestions backed by verified sources like WHO, NIH, and Mayo Clinic.  
- **Inventory Management** – Helps pharmacists track medicine availability and manage stock.  
- **Chatbot Integration** – Powered by Gemini 2.0 Flash for answering customer queries.  

---

## 🏗 Architecture  
 <img src="/diagrams/ggh-pharmassisitai.drawio (2).png" alt="Architecture Diagram">

---

### 🔧 Technologies Used  
#### **Backend:**  
- FastAPI – Handles prescription processing, medicine lookup, and API integrations.  
- OpenCV – Image enhancement techniques for better OCR accuracy.  
- Ollama – Llama 3.2-Vision:11B for OCR (text extraction from prescriptions).  
- ChromaDB – Vector search for alternative medicine recommendations.  
- SQLite3 – Lightweight SQL database for inventory management.  
- SQLAlchemy – ORM for efficient database interaction.  
- Pydantic – Schema validation for data consistency.  

#### **Frontend:**  
- Streamlit – Rapid prototyping and demo interface.  
- Future Plan: Migrate to React for better UI/UX.  

#### **AI Models:**  
- **OCR** – Llama 3.2-Vision:11B for text extraction from prescriptions.  
- **NLP** – SpaCy’s BC5CDR model for medical text processing.  
- **LLM** – Gemini-2.0-Flash for herbal remedy recommendations.  

---

## 📌 Future Enhancements  
- **Agentic AI** – Automate CRUD operations and provide inventory insights.  
- **OAuth Authentication** – Secure database modifications.  
- **Lab Report Analysis** – Extract key medical insights from uploaded reports.  
- **Scaling** – Migrate from SQLite3 to PostgreSQL for large databases.  

---

## ⚠️ Limitations  
- The current OCR model (Llama 3.2-Vision:11B) takes ~20 minutes per image but provides high accuracy.  
- Requires an NVIDIA CUDA GPU for execution.  
- Large model size: ~7-8GB for Llama, 5GB for Llava 7B.  

---

## **Prerequisites**  
- Python 3.9+
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

---

## **Setting up the project**
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
