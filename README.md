# **PharmAssistAI**

## 📑 **Table of Contents**
1. [📽️ Demo Videos](#demo-videos)
2. [Overview](#overview)
3. [🚀 Features](#features)
4. [🏗 Architecture](#architecture)
5. [🔧 Tech Stack](#tech-stack)
6. [📌 Future Enhancements](#future-enhancements)
7. [Prerequisites](#prerequisites)
8. [🔧 Setting Up the Project](#setting-up-the-project)
   - [🐳 Docker Compose Setup](#docker-compose-setup)
   - [⚙️ Manual Setup](#manual-setup)

---
<a id="demo-videos"></a>
## 📽️ Demo Videos


- **[Project Demo](https://youtu.be/GdKADB6fNX8)** – Overview of the project in action.  
- **[OCR Testing Video](https://youtu.be/KNCIHKGJ1IQ)** – Demonstration of Gemini OCR extracting text from handwritten prescriptions.  
- **[OCR - Previous approach using Ollama](https://youtu.be/U_z6CGe6b1k)** – Comparison of previous OCR approach with Ollama.  

---

## **Overview**
PharmAssistAI is an AI-powered assistant designed to **automate pharmacy operations**, making them faster, more efficient, and **error-free**.  

- **Prescription processing** via advanced **OCR** and **LLMs**  
- **AI-powered medicine alternatives** using **vector search**  
- **Automated invoice generation & management**  
- **Quick stock alerts** based on sales.  
- **Agentic AI** for intelligent **SQL query execution**  
- **Home remedies chatbot** for customer engagement  
- **Interactive dashboard** with inventory insights  

---
<a id="features"></a>
## 🚀 Features

- **Prescription Processing** – Extracts text from handwritten prescriptions using **Gemini-2.0-Flash-Exp OCR**.  
- **Alternative Medicine Suggestions** – Uses **ChromaDB** for vector-based search to suggest similar medicines.  
- **Home Remedies Recommendations** – Uses **LLM (Gemini-2.0-Flash)** AI-powered chatbot provides natural remedy suggestions from **trusted sources** like WHO, NIH, and Mayo Clinic.  
- **Inventory Management** – Track medicine stock levels, visualize data, and get **real-time stock alerts** via dashboard.  
- **Agentic AI for SQL** – Enables **natural language interaction** with the database, eliminating manual SQL queries.  
- **Invoice Management** – Automatically generates, stores, and prints invoices, with options to delete outdated records.  
- **Alert System** – Allows you to set **custom stock thresholds** and provides **low-stock alerts** based on medicine available quantity.  
- **Data Insights & Visualization** – Real-time analytics on sales and stock trends.  

---
<a id="architecture"></a>
## **🏗 Architecture**
![Architecture Diagram](/diagrams/Architecture-PharmAssistAI-latest.drawio.png)

---
<a id="tech-stack"></a>
## **🔧 Tech Stack**

### **Backend:**
- **FastAPI** – Backend server for prescription processing and API management.  
- **OpenCV** – Image enhancement for better OCR accuracy.  
- **Ollama** – Llama 3.2-Vision:11B for OCR (previous approach).  
- **ChromaDB** – Vector search for alternative medicine recommendations.  
- **SQLite3** – Lightweight SQL database for pharmacy inventory.  
- **SQLAlchemy** – ORM for efficient database interactions.  
- **Pydantic** – Schema validation for data consistency.  

### **Frontend:**
- **Streamlit** – Rapid prototyping and interactive UI.  
- **Plotly** – Data visualization for inventory trends.  
- **Pandas** – Structuring and processing data in the frontend.  

### **Agentic AI:**
- **Groq [Mixtral-8x7b-32768]** – AI model for intelligent SQL query execution.  
- **LangChain & LangGraph** – Frameworks for AI-driven automation.  

### **Vector Search & Embeddings:**
- **ChromaDB** – Vector database for retrieving semantically similar medicines.  
- **Sentence-Transformers** – Converts medicine data into embeddings for better search.  

### **OCR & Image Processing:**
- **Gemini-2.0-Flash-Experimental** – OCR model for text extraction from prescriptions.  

### **Herbal Remedies & NLP:**
- **Gemini-2.0-Flash** – AI model for herbal remedy suggestions.  

---
<a id="future-enhancements"></a>
## 📌 **Future Enhancements**
- **OAuth Authentication** – Secure user access and database modifications.  
- **Scalability** – Migrate from SQLite3 to PostgreSQL for handling large datasets.  
- **Enhanced UI/UX** – Migrate frontend from Streamlit to **React** for better control and usability.  

---

## **Prerequisites**
- Python **3.9+**  

---
<a id="setting-up-the-project"></a>
## **🔧 Setting Up the Project**

Below are two ways to set up the project — using **Docker Compose (recommended)** or **manual setup**.

---
<a id="docker-compose-setup"></a>
## 🐳 1️⃣ **Recommended: Docker Compose Setup**

> Seamlessly run the entire application stack (FastAPI + Streamlit) in isolated containers with a single command.

### ✅ **Prerequisites**
- Docker: [Install Docker](https://docs.docker.com/get-docker/)
- Docker Compose: [Install Docker Compose](https://docs.docker.com/compose/install/)

---

### ⚙️ **Steps**

#### 1. **Clone the Repository**
```bash
git clone https://github.com/ritu456286/PharmAssistAI.git
cd PharmAssistAI
```

#### 2. **Create Environment Files**
- Create a `.env` file inside `/backend` and add:  
```sh
GEMINI_API_KEY= <your_gemini_api_key>
GROQ_API_KEY= <your_groq_api_key>
```

- Create a `.env` file inside `/frontend` and add:  
```sh
BASE_URL=http://backend:8000/
```

#### 3. **Build & Start the Application**
```sh
docker-compose up --build

```

#### 4. **Access the Application**
* Frontend (Streamlit UI): http://localhost:8501
* Backend (FastAPI docs): http://localhost:8000/docs

---
<a id="manual-setup"></a>
## ⚙️ 2️⃣ Manual Setup (Without Docker)


### ⚙️ Steps

### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/ritu456286/PharmAssistAI.git
cd PharmAssistAI
```

### **2️⃣ Backend Setup**
Navigate to the backend folder:  
```sh
cd backend
```

- Create a **Python virtual environment**  
```sh
python -m venv venv
```
- Activate the virtual environment  
  - **Windows:** `venv\Scripts\activate`  
  - **Mac/Linux:** `source venv/bin/activate`  

- Install dependencies  
```sh
pip install -r requirements.txt
```

- Create a `.env` file inside `/backend` and add:  
```sh
GEMINI_API_KEY= <your_gemini_api_key>
GROQ_API_KEY= <your_groq_api_key>
```

- Create an empty `/src/db` folder where SQLite and ChromaDB will be stored.  

- Start the FastAPI server  
```sh
sh run.sh
```

---

### **3️⃣ Frontend Setup**
Navigate to the frontend folder:  
```sh
cd frontend
```

- Create a **Python virtual environment**  
```sh
python -m venv venv
```
- Activate the virtual environment  
  - **Windows:** `venv\Scripts\activate`  
  - **Mac/Linux:** `source venv/bin/activate`  

- Install dependencies  
```sh
pip install -r requirements.txt
```

- Create a `.env` file inside `/frontend` and add:  
```sh
BASE_URL=<url_where_your_backend_server_is_running>
```

- Start the Streamlit app  
```sh
streamlit run main.py
```

---

### **4️⃣ Run the Application**
- Ensure both **backend** and **frontend** servers are running.  
- Update the inventory with your **pharmacy database**.  
- Explore **real-time stock tracking, automated billing, AI recommendations, and more!**  

---
