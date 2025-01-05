import requests

def fetch_questions(amount=5, category=None, difficulty=None):
    """
    Fetch questions from Open Trivia DB API.

    Args:
        amount (int): Number of questions to fetch. Defaults to 5.
        category (int, optional): ID of the category for questions.
        difficulty (str, optional): Difficulty level of questions ('easy', 'medium', 'hard').

    Returns:
        list: A list of questions if the API call is successful, otherwise an empty list.
    """
    base_url = "https://opentdb.com/api.php"
    params = {
        "amount": amount,
        "type": "multiple"  # Requesting multiple-choice questions
    }
    if category:
        params["category"] = category  # Adding category filter if specified
    if difficulty:
        params["difficulty"] = difficulty  # Adding difficulty filter if specified

    response = requests.get(base_url, params=params)  # Sending GET request to the API
    if response.status_code == 200:  # Checking if the response is successful
        data = response.json()  # Parsing response as JSON
        if data["response_code"] == 0:  # Checking if the API returned valid questions
            return data["results"]  # Returning the list of questions
    return []  # Returning an empty list if API call fails or no questions found
