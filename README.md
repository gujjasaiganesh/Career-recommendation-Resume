# 🎯 Career Recommendation System

> An **AI-powered** Flask web application that analyzes resumes and provides intelligent career recommendations.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1.1-green)](https://flask.palletsprojects.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-orange)](https://openai.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

## ✨ Key Features

- 📄 **Smart Resume Parsing**: Extracts information from PDF and TXT files
- 🎯 **AI-Powered Career Matching**: Get personalized career recommendations
- 🔍 **Skills Analysis**: Automatic skill extraction and categorization
- 📚 **Education History**: Intelligent education background analysis
- 📞 **Contact Information**: Automatic extraction of contact details
- 📊 **Match Score**: Precise career compatibility scoring
- 📈 **Career Progression**: Detailed career growth pathways
- 📦 **Bulk Processing**: Handle multiple resumes efficiently

## 🛠️ Technologies Used

- **Backend Framework**: Flask 3.1.1
- **AI/ML**: OpenAI GPT-4
- **PDF Processing**: PyPDF2
- **Text Analysis**: Regular Expressions
- **Frontend**: HTML5/CSS3
- **Server**: Waitress (Production WSGI)

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Git

### Installation

1. **Clone the repository**:
```bash
git clone https://github.com/gujjasaiganesh/Career-recommendation-Resume.git
cd Career-recommendation-Resume
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Configure environment**:
Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=your_openai_api_key
GOOGLE_API_KEY=your_google_api_key
```

4. **Launch the application**:
```bash
python production.py
```

🌐 Access the application at `http://localhost:8080`

## 💡 Usage Guide

1. 📥 **Upload Resume**
   - Navigate to the homepage
   - Click "Choose Resume" button
   - Select PDF or TXT file

2. ✏️ **Enter Interests**
   - Provide your career interests
   - Add relevant skills and preferences

3. 🔄 **Process and Analyze**
   - Click "Analyze Match" button
   - Wait for AI processing

4. 📊 **View Results**
   - See career match score
   - Review recommended career paths
   - Check extracted skills and education
   - Read personalized feedback

## 🌟 Features in Detail

### Resume Analysis
- **Format Support**: PDF and TXT
- **Data Extraction**: Contact info, skills, education
- **Text Processing**: Advanced NLP techniques

### Career Recommendations
- **AI-Powered Matching**: Using GPT-4
- **Skill Mapping**: Industry-standard skills database
- **Career Progression**: Entry to senior level paths

### User Interface
- **Responsive Design**: Mobile-friendly
- **Modern UI**: Clean and intuitive
- **Real-time Updates**: Instant feedback

## 🚀 Production Deployment

The application uses **Waitress** as a production WSGI server:

```bash
python production.py
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. 🍴 **Fork** the repository
2. 🌿 Create a **feature branch**: `git checkout -b feature/AmazingFeature`
3. 💾 **Commit** changes: `git commit -m 'Add AmazingFeature'`
4. 📤 **Push** to branch: `git push origin feature/AmazingFeature`
5. 🔄 Open a **Pull Request**

## 📝 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For support, please:
- 📧 Open an issue
- 🌟 Star the repository if you find it helpful
- 🤝 Contribute to the project

---
Made with ❤️ by [Sai Ganesh](https://github.com/gujjasaiganesh)
