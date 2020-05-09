# Trivia Game
A project that is part of the Udacity Full Stack Developer Nanodegree Program. It involved building a backend server that integrated with a pre-built front end that hosts the trivia app. Inside the app you are able to add and delete questions in various categories while also being able to quiz yourself on each category.

## API Reference
### Getting Started:
The trivia game API waswritten with REST principles in mind. The URL's are straightforward and returns are JSON encoded responses while also using standard HTTP response codes.

Base URL: `http://127.0.0.1:5000/`

### Error Handling:
Standard HTTP response codes. But these errors are returned as JSON objects in the following format.
```
{
    "success":False,
    "error":400,
    "message":"bad request"
}
```

The API will return these three types when failures occur.
* 400 - Bad request from the client
* 404 - Resource not found!
* 422 - Unprocessable

### Endpoint Library:
#### GET `/categories`
Returns a list of all the categories listed in the categories table. This returns a JSON object with the categories as a key:value pair.

Sample: `curl http://127.0.0.1:5000/categories`
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}
```
#### GET `/questions`
Returns a list of all the questions in the questions table with the use of pagination. A JSOON object is returned containing the list of questions, list of categories, current category, and the total number of questions.

Sample: `curl http://127.0.0.1:5000/questions`
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "currentCategory": 1,
  "questions": [
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved                           Lestat?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-                      bladed appendages?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }
  ],
  "success": true,
  "totalQuestions": 20
}
```
#### DELETE `/questions/{question_id}`
Will delete the question with the selected id and return a JSON object with an updated paginated list of questions.

Sample: `http://127.0.0.1:5000/questions/1 -X DELETE` 
```
{  
  "questions": [
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved                           Lestat?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-                      bladed appendages?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }
  ],
  "success": true
  }
  ```

#### POST `/questions`
A post request can have two responses depending on what is passed with the request. 

1. If a search term is provided the post request will cause the server to look for questions containing any part of the search term.

Sample: `curl -X POST -H "Content-Type: application/json" -d '{"searchTerm":"box"}' http://127.0.0.1:
5000/questions`
```
{
  "currentCategory": 1,
  "questions": [
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    }
  ],
  "success": true,
  "totalQuestions": 1
}
```
2. If no search term is provided the post request should involve parameters to add a new question to the database. These parameters are question,answer,category, and difficulty.

Sample: `curl -X POST -H "Content-Type: application/json" -d '{"question":"foo?","answer":"bar","category":1,"difficulty":1}' http://127.0.0.1:
5000/questions`
```
{
  "success": true
}
```
#### GET `/categories/{category_id}/questions`
Returns a list of questions within a specified category as well as the total number of questions in that category. The results are paginated.

Sample: `curl http://127.0.0.1:5000/categories/1/questions `
```
{
  "currentCategory": 1,
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },
    {
      "answer": "Sample",
      "category": 1,
      "difficulty": 1,
      "id": 24,
      "question": "Sample?"
    },
    {
      "answer": "yes",
      "category": 1,
      "difficulty": 1,
      "id": 26,
      "question": "Why?"
    }
  ],
  "success": true,
  "totalQuestions": 5
}
```
#### POST `/quizzes`
This endpoint provides the logic to be able to play a trivia game. It expects a list of previous questions and the current category to be provided in the body of the request.

Sample: `curl -X POST -H "Content-Type: application/json" -d '{"previous_questions": [], "quiz_catego ry": {"type": "Science", "id": 1}}' http://127.0.0.1:5000/quizzes`
```
{
  "currentQuestion": "Sample Question",
  "success": true
}
```
