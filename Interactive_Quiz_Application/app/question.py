import requests

BASE_URL = "https://opentdb.com/api.php"

def fetch_quiz_questions(amount=5, category=None, difficulty=None):
    """
    Fetch quiz questions from Open Trivia DB.
    :param amount: Number of questions to fetch (default: 5).
    :param category: (Optional) Category ID for questions.
    :param difficulty: (Optional) Difficulty ('easy', 'medium', 'hard').
    :return: List of questions or an empty list on failure.
    """
    params = {
        "amount": amount,
        "type": "multiple"  # Fetch multiple-choice questions
    }
    if category:
        params["category"] = category
    if difficulty:
        params["difficulty"] = difficulty

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Raise exception for HTTP errors
        data = response.json()
        return data.get("results", [])
    except (requests.RequestException, ValueError) as e:
        print(f"Error fetching questions: {e}")
        return []
    