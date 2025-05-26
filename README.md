# Career Recommendation System

A Flask-based web application that analyzes resumes and provides career recommendations using AI.

## Features

- Resume parsing and analysis
- Career path recommendations
- Skills extraction
- Education history extraction
- Contact information extraction
- Match score calculation
- Detailed career progression paths
- Bulk resume processing

## Technologies Used

- Python
- Flask
- OpenAI GPT-4
- PyPDF2
- Regular Expressions
- HTML/CSS
- Waitress (WSGI server)

## Setup

1. Clone the repository:
```bash
git clone <your-repository-url>
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file with:
```
OPENAI_API_KEY=your_openai_api_key
GOOGLE_API_KEY=your_google_api_key
```

4. Run the application:
```bash
python production.py
```

The application will be available at `http://localhost:8080`

## Usage

1. Navigate to the homepage
2. Upload a resume (PDF or TXT format)
3. Enter your interests
4. Submit for analysis
5. View detailed career recommendations and analysis

## Production Deployment

The application uses Waitress as a production WSGI server. To run in production mode:

```bash
python production.py
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request