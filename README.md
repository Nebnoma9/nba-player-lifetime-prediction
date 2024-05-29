# NBA Player Career Longevity Prediction

This project aims to predict whether an NBA player will last more than 5 years in the league using various player statistics and features.

## Project Structure
.\
├── app\
│ ├── main.py\
│ └── best_model_for_cautious_investors_v0.pkl\
├── data\
│ └── nba_logreg.csv\
├── test_examples\ 
│ ├── test0.json\
│ └── test1_batch.json\
├── workflow.ipynb\
├── server.ipynb\
├── Dockerfile\
├── requirements.txt\
└── README.md

## Steps to Build and Run the Docker Application

docker build -t nba-prediction-app .

docker run -p 8000:80 nba-prediction-app

## Usage
curl -X POST "http://127.0.0.1:8000/predict?batch=false" -H "Content-Type: application/json" -d @test_examples/test0.json

Notice there is a batch parameter in the url for batched requests