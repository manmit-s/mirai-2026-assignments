# 🧘 Life-OS Wellbeing Dashboard

A production-quality Streamlit dashboard for screen-time analysis with AI-powered coaching from Google's Gemini API. Built as a virtual internship project demonstrating SaaS-grade development practices.

## 📊 Features

- **Interactive Dashboard**: Clean, modern UI with real-time filtering and analytics
- **Screen-Time Analytics**: Track usage patterns across 14+ days with detailed breakdowns
- **AI Coaching**: Personalized, brutally honest coaching from Gemini based on your habits
- **Category Breakdown**: Visual analysis of time spent across different app categories
- **KPI Metrics**: Key performance indicators with goal tracking and delta comparisons
- **Shareable Accountability**: Generate shareable links to keep yourself accountable
- **Responsive Design**: Professional styling that feels like a real SaaS product

## 🛠️ Tech Stack

- **Frontend**: Streamlit with custom CSS styling
- **Data Processing**: Pandas for analytics and data manipulation
- **AI Integration**: Google Gemini API (google-genai)
- **Visualization**: Streamlit native charts + Plotly
- **Environment**: Python-dotenv for secure API key management

## 📁 Project Structure
```
life-os-wellbeing-dashboard/
├── app.py # Main Streamlit application
├── screentime.csv # Synthetic dataset (14+ days)
├── requirements.txt # Python dependencies
├── .env # Environment variables (not tracked)
├── .gitignore # Git ignore rules
├── README.md # Project documentation
├── assets/
│   └── logo.png # App logo placeholder
└── utils/
    ├── init.py # Package initializer
    ├── data_loader.py # Data loading and processing
    ├── ai_coach.py # Gemini API integration
    └── helpers.py # Utility functions
```


## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Git
- Google Gemini API key

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd life-os-wellbeing-dashboard
```

