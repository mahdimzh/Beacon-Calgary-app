# 📍 Beacon Calgary

Beacon Calgary is a community-focused web application designed to support individuals and families experiencing homelessness in Calgary.

It brings together vital local services—emergency shelters, food banks, health clinics, mental health support, legal aid, and employment resources—into a single, easy-to-use platform. With an interactive city map and categorized filters, users can quickly find nearby services that match their needs.

Whether someone is seeking a warm place to stay, a meal, mental health support, or legal guidance, Beacon Calgary empowers them with accurate, location-based information and up-to-date service availability.

The app also features Beacon Bot, an AI-powered assistant that provides friendly, respectful, and non-judgmental guidance. Beacon Bot can answer questions, explain service options, and help users navigate difficult situations—especially for those who may feel overwhelmed or unsure where to begin.

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
