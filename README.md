🤖 AI Interview Coach

A smart, private, and non-judgmental AI coach that provides instant, actionable feedback on your behavioral interview answers.

The Problem

Based on research with university students, the biggest blocker to interview practice isn't what to say, but the anxiety of feeling "awkward" and "self-conscious" practicing out loud. Job seekers crave a private, non-judgmental space to rehearse and want specific, actionable metrics—not vague feedback.

This project was built to answer the question:

"How Might We use AI to give students instant, private, and actionable feedback so they can feel more confident in their verbal interview answers?"

✨ Features

Record & Transcribe: Simply click "Start" to record your answer and "Stop" when you're done. Your audio is instantly transcribed using OpenAI's Whisper.

Actionable STAR Analysis: Get a 1-5 score and concise, non-judgmental feedback on your answer's structure based on the industry-standard STAR (Situation, Task, Action, Result) method, powered by the Gemini API.

Filler Word Detection: Worried about saying "um," "ah," or "like"? The app provides a detailed count of common filler words so you know exactly what to work on.

Private & Instant: Your recordings are processed locally and are not stored. The feedback is for your eyes only, giving you a safe space to practice, fail, and improve without fear.

🚀 The App in Action

Here's what the feedback report looks like after you've submitted an answer:

(You should add a screenshot here! Just drag and drop an image into this README file on GitHub.)

🛠️ Tech Stack

Frontend: Plain HTML, CSS, and JavaScript

Backend: Python (Flask)

Speech-to-Text: OpenAI Whisper (running locally)

AI Analysis: Google's Gemini API (for STAR analysis)

🔧 How to Run Locally

Clone the repository:

git clone [https://github.com/TheSensibleLunatic/AI-interview-coach.git](https://github.com/TheSensibleLunatic/AI-interview-coach.git)
cd AI-interview-coach


Create and activate a Python virtual environment:
(You named yours coach, but the standard is venv)

# Windows
python -m venv coach
.\coach\Scripts\activate

# Mac/Linux
python3 -m venv coach
source coach/bin/activate


Install the required libraries:
(Note to developer: You should run pip freeze > requirements.txt in your terminal to create this file.)

pip install -r requirements.txt


(If you don't have that file, install the libraries manually:)

pip install flask flask-cors openai-whisper google-genai


Set up your API Key:

Get a free Gemini API key from Google AI Studio.

In the app.py file, find the line GEMINI_API_KEY = "YOUR_API_KEY_GOES_HERE" and paste your key inside the quotes.

Run the Flask Server:

python app.py


Your server will start on http://127.0.0.1:5000.

Open the App:

In your file explorer, find the index.html file.

Right-click it and choose "Open in browser" (or use the VS Code "Live Server" extension).

Start recording!

👤 Author

Aaradhya Verma - GitHub
