# Telegram MCQ Quiz Bot

This project is a Telegram bot that conducts multiple-choice quizzes using questions loaded from a JSON file. The bot presents questions to users, allows them to select answers, provides instant feedback with animations (emojis), explanations, and displays answer statistics for each question. The bot also tracks how many users selected each option for every question.

## Features

- Presents MCQ questions from a JSON file (`questions.json`)
- Lets users choose the starting question number
- Interactive answer selection with inline buttons
- Instant feedback with correct/wrong animations (✅/❌)
- Provides explanations for each answer
- Tracks and displays answer statistics for each question
- Supports multiple users independently
- Simple to set up and run locally

## Use Cases

- **Educational quizzes:** Teachers or trainers can use this bot to conduct quizzes for students.
- **Self-assessment:** Individuals can test their knowledge on various topics.
- **Group competitions:** Use in Telegram groups for friendly quiz competitions.
- **Survey/feedback:** Adapt the questions for quick surveys or feedback collection.

## Project Structure

```
bot.py           # Main bot code
questions.json   # MCQ questions and answers
stats.json       # Stores answer statistics (auto-generated)
README.md        # Project documentation
```

## Prerequisites

- Python 3.8 or higher
- Telegram account
- Telegram Bot Token (from [BotFather](https://core.telegram.org/bots#botfather))

## Setup Instructions

### 1. Clone the Repository

```sh
git clone https://github.com/your-username/Telegram_Bot_create.git
cd Telegram_Bot_create
```

Replace `your-username` with your actual GitHub username.

### 2. Install Dependencies

Install the required Python packages using pip:

```sh
pip install python-telegram-bot
```

> **Note:** If you encounter issues, ensure you have the latest version of `pip` and Python.

### 3. Add Your Telegram Bot Token

Open `bot.py` and replace the value of `TOKEN` with your own Telegram bot token:

```python
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
```

You can get a token by chatting with [@BotFather](https://t.me/BotFather) on Telegram.

### 4. Prepare Your Questions

Edit `questions.json` to add, remove, or modify quiz questions. Each question must follow this format:

```json
{
  "question": "Your question text?",
  "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
  "correct_answers": ["Correct Option Text"],
  "explanation": "Explanation for the correct answer."
}
```

### 5. Run the Bot

Start the bot by running:

```sh
python bot.py
```

You should see `Bot is running...` in your terminal.

### 6. Start Quizzing!

- Open Telegram and search for your bot (by its username).
- Send `/start` to begin.
- Enter the question number you want to start from (e.g., `1`).
- Select your answer by tapping the inline button.
- Get instant feedback, explanations, and see how others have answered.

## Example Interaction

```
User: /start
Bot: Welcome! Please enter the question number you want to start from (1-19):
User: 1
Bot: Q1: What is the primary goal of NASA’s Interstellar Mapping and Acceleration Probe (IMAP) mission?
      ⚪ To study black holes in deep space
      ⚪ To map the heliosphere’s boundary, trace energetic particles, and improve space weather forecasting
      ⚪ To explore the surface of Mars
      ⚪ To detect exoplanets beyond the solar system

(User selects an option)

Bot: ✅ Correct!
     Explanation: IMAP aims to study the outer boundary of the heliosphere, understand particle acceleration, and improve predictions of space weather affecting Earth.

     To map the heliosphere’s boundary, trace energetic particles, and improve space weather forecasting — 100.0%
     (other options) — 0.0%
     Total attempts: 1
```

## Customization

- **Add more questions:** Edit `questions.json` and restart the bot.
- **Reset statistics:** Delete `stats.json` and restart the bot.
- **Change feedback animations:** Edit the `CORRECT_ANIMATION` and `WRONG_ANIMATION` variables in `bot.py`.

## Troubleshooting

- If the bot does not respond, check your bot token and internet connection.
- Ensure `questions.json` is valid JSON.
- If you change the structure of `questions.json`, restart the bot.

## License

This project is for educational and personal use.

---

**Created by [your name or GitHub username]**
