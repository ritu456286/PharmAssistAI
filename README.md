# PharmAssistAI

## 📽️ DEMO VIDEOS  

🔹 **[OCR - Previous approach using Ollama](https://youtu.be/U_z6CGe6b1k)** – Watch how the OCR Scanner extracts text effortlessly!  

🔹 **[Project Demo]([https://youtu.be/zUKhJ-bkMR4](https://youtu.be/GdKADB6fNX8))** – Get an overview of the project in action!  

----

## Overview  
This AI-powered assistant helps pharmacists automate prescription processing, medicine identification, and also efficiently manage inventory. It also provides reliable alternative medicine suggestions if medicines demanded are not available in the current stock and provide herbal remedy recommendations from trusted sources, ensuring pharmacists can assist customers more efficiently while maintaining trust.  

---

## 🚀 Features  
- **Prescription Processing** – Extracts text from handwritten prescriptions using LLM- Gemini-2.0-Flash-Exp, OCR technique.  
- **Alternative Medicine Suggestions** – Uses ChromaDB for vector-based search to find similar medicines.  
- **Herbal Remedies Recommendations** – Provides AI-powered herbal suggestions backed by verified sources like WHO, NIH, and Mayo Clinic.  
- **Inventory Management** – Helps pharmacists track medicine availability and manage stock using Dashboard, as well as Agentic AI.  
- **Chatbot Integration** – Powered by Gemini 2.0 Flash for answering customer queries.  

---

## 🏗 Architecture  
 <img src="/diagrams/Architecture-PharmAssistAI-latest.drawio.png" alt="Architecture Diagram">

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

#### **AI Models:**  
- **OCR** – Gemini-2.0-Flash-Exp for text extraction from prescriptions.  
- **Agentic AI** - Groq - mixtral-8x7b-32768
- **LLM** – Gemini-2.0-Flash for herbal remedy recommendations.  
---

## 📌 Future Enhancements  
- **OAuth Authentication** – Secure database modifications.  
- **Scaling** – Migrate from SQLite3 to PostgreSQL for large databases.
- **Better UI Control**: Migrate to React for better UI/UX.

---

## **Prerequisites**  
- Python 3.9+

---

## **Setting up the project**
- To setup this project in your device, first clone this repository using:
```
git clone https://github.com/ritu456286/PharmAssistAI.git
cd ./PharmAssistAI
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
GROQ_API_KEY= <your groq key>
```
- Create an empty folder inside /src named `db` --> /src/db. Here the Sqlite and chromaDB will be stored. ChromaDB will get seeded, and agent will get compiled on running the server.
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

- Setup for frontend is complete, you can run the streamlit app now, by executing the following command:
```
streamlit run main.py
```

- Now, your frontend should be running, backend should be running. Update your inventory with your own Pharmacy database.
