# Simple-AI-Agent-streamlit
Search the dataset related to a specific subject
Voici la traduction en anglais de votre README :  

---

# **Data Scout**  

**Data Scout** is an interactive web application that allows users to search for datasets using AI Agent. The application leverages **CrewAI** and **Groq** to analyze user queries and find relevant datasets from various sources.  

## **Features**  
🔍 **Intelligent dataset search**  
📊 **Displays results with title, description, source, and date**  
💾 **Automatically saves search results to a SQLite database**  
🌡️ **AI temperature control to adjust the creativity of results**  
🔄 **Automatic API rate limit management**  

## **Installation**  

### **Clone the repository:**  
```bash
git clone https://github.com/your-username/data-scout.git
cd data-scout
```

### **Create a virtual environment and install dependencies:**  
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### **Create a `.env` file in the project's root directory with your API keys:**  
```
SERPER_API_KEY=your_serper_key
GROQ_API_KEY=your_groq_key
```

## **Usage**  

### **Run the application:**  
```bash
streamlit run app.py
```
Open your browser at the indicated address (usually [http://localhost:8501](http://localhost:8501)).  

- Enter your search query, adjust the number of desired results, and set the AI temperature as needed.  

## **Project Structure**  
```
data-scout/
├── app.py           # Main Streamlit application
├── agent.py         # AI agent configuration
├── model.py         # Database models
├── .env             # Environment variables
└── datasets.db      # SQLite database
```

## **Main Dependencies**  
- Streamlit  
- CrewAI  
- SQLAlchemy  
- Groq  
- Python-dotenv  

## **Configuration**  
- The SQLite database is automatically created on first launch.  
- Search results are stored in the `datasets` table.  
- AI temperature can be adjusted from **0 (more conservative)** to **1 (more creative)**.
  
