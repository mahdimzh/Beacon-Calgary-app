# 📍 Beacon Calgary

Beacon Calgary is a community-driven interactive web application that maps and displays vital resources across Calgary, including shelters, food banks, healthcare services, mental health support, legal aid, and more.

The app includes an AI chatbot, Beacon Bot, to help users find the right support.

## 🚀 Features

- 🗺️ Interactive map with categorized service markers
- 📊 Service type statistics and live filtering
- 🤖 OpenAI-powered chatbot with real-time assistance
- 🔍 Filter services by category and status
- 💬 Chat history and dynamic suggestions

## 🛠️ Setup Instructions

1. Clone the repository:
   git clone https://github.com/your-username/beacon-calgary.git
   cd beacon-calgary

2. (Optional) Create and activate a virtual environment:
   python -m venv venv
   source venv/bin/activate     # On Windows: venv\Scripts\activate

3. Install dependencies:
   pip install -r requirements.txt

4. Add your OpenAI API Key to a `.env` file:
   OPENAI_API_KEY=sk-...

5. Run the app:
   streamlit run app.py

## 🧠 Requirements

See requirements.txt for the full list of dependencies.

## 🔑 OpenAI API

To use the chatbot, you must provide a valid OpenAI API key in your `.env` file and add the variable to `OPENAI_API_KEY`.
Get your key from https://platform.openai.com/account/api-keys.

## Run the app locally:
`streamlit run app.py`


## 🔒 Disclaimer

This app provides informational support and is not a substitute for professional or emergency services.
For emergencies, call 911. For mental health or housing support in Calgary, call 211.

## 👤 Author

Developed by Hadi and Mahdi — 2025.
Licensed under MIT License.
