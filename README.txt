This project trains a kNN model to create champion recommendations based on 2.9k users champion mastery data.

How to run my project

To look at the model in action:
Run src/example.py

To train and run the model:
Run src/training.py
Run src/example.py

To look at the dataset then see how it performs on various models:
View src/visualization.ipynb
Run src/processing.ipynb (optional)
View model_selection.ipynb
View rank_metric.ipynb
Run src/unique_champions


What each file does

Files for using the model:
src/training.py - build dataset and user pool, then train models

src/example.py - example of model in action on users with partially hidden data

Files for testing model performance:
src/unique_champions.py - prints number of unique champions per model

src/rank_metric.py - checks how many champions are recommended from top 5 champions not in dataset and saves results to csv

src/model_selection.ipynb - Cross validation for choosing model and choosing parameters for SVD and kNN

File for visualizing model performance:

src/rank_metric.ipynb - Visualizes results of tests on champion recommendation system, including number of relevant guesses

File for visualizing dataset:
src/visualization.ipynb - explores champion mastery score distribution and whether certain champion players prefer other champions

File for processing dataset:
src/processing.ipynb - creates full dataset and smaller dataset for data analysis

File for gathering data:
riot_api.py - make requests to riot API, requires token


Data 
all_data is for the dataset where every mastery score was collected from users
25_data is for the dataset where 25 mastery scores were collected for each user

test_data - results of various tests from ipynb notebooks and python scripts

mastery_data.json - dataset where 25 mastery scores were collected for each user (5.9k users)

complete_mastery_info.json - dataset where all mastery scores were collected for each user (2.9k users)