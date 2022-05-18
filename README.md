# Building a web based service from scratch for predicting price of apartment

#### This project was made as part of a course on the cycle of development and management of machine learning models.

## The goal of the project:
* To build a web based service using which it would be possible to predict prices of apartments for rent using selected machine learning model.

This README.md file contains information about:
* source data and some statistics
* models, choosen framework, hyperparams 
* how to install instructions and run app with virtual environment
* dockerfile and description of its content
* how to open the port in remote VM
* how to run app using docker and which port it uses

## a) Information about source data and some statistics

Data for the project was taken from [Yandex Reality classified](https://realty.yandex.ru) containing real estate listings for apartments in St. Petersburg and Leningrad Oblast from 2016 till the middle of August 2018.
Initial dataset consisted of 171186 observations and 17 columns.

The dataset has been cleared of outliers using interquantile range method. Cleaned dataset contains 105046 observations.

Based on EDA, features were chosen for be used in machine learning models.

Relationships between features and price of apartment for rent:

![Relationships between features and price of apartment](https://github.com/AnastasiaPanchenko1/gsom_predictor/blob/main/images/1.png) 

Relationship between price of apartment and whether it is possible to change the layout of the apartment:

![Relationships between features and price of apartment](https://github.com/AnastasiaPanchenko1/gsom_predictor/blob/main/images/2.png) 

Relationship between price of apartment and whether it is studio or not:

![Relationships between features and price of apartment](https://github.com/AnastasiaPanchenko1/gsom_predictor/blob/main/images/3.png) 

There is the example of how final dataset looks like:

![There is the example of how final dataset looks like:](https://github.com/AnastasiaPanchenko1/gsom_predictor/blob/main/images/4.png) 


I also have created the new variable which means the duration of time (in days) during which the house was exhibited. The longer the duration, the lower the price should be.

## b) Information about models, chosen framework, hyperparams 


I used a catboost model as the final choice for predicting prices based on this comparison of models (there are results on validation part of dataset):

|  Type of model        | Model without additional factors     | Model with additional factors  |
| :-------------------- | :-------------------                 | :--------------                | 
| DecisionTreeRegressor | 0.7397189578337247                   | 0.7306026581732368             |
| RandomForestRegressor | 0.7162246233690541                   | 0.7021463938153056             | 
| CatBoostRegressor     | *0.7119999158129939*                 | *0.7009136610665767*           | 
| LGBMRegressor         | 0.7164502290230126                   | 0.709216048526922              | 

The model without additional factors contains such features as:
* open_plan (means whether it is possible to change the layout of the apartment), 
* rooms (number of rooms), 
* studio (whether it is a studio), 
* area, 
* kitchen_area, 
* living_area, 
* agent_fee, 
* days_of_exposition.

And the model with additional factors has all the same information and also features:
* renovation (apartment renovation level)
* floor (number of floor of apartment).

Parameters were chosen based on GridSearchCV with 5 folds.
Such parameters were used in a catboost model:

```
catboost_optimized = CatBoostRegressor(iterations=1000, depth=8, learning_rate=0.01, random_seed=17)
```
Then I used Flask web framework to build a web based service.
File app.py supports two models (catboost with and without additional features) due to special parameter added to GET request as a model_version. It gives the opportunity to choose between two models for prediction of price.


## c) How to install instructions and run app with virtual environment

Create new environment:

    sudo apt install python3.8-venv
    python3 -m venv env

Activate the environment:
 
    source env/bin/activate

Also you need to pull the code from github to your directory.

To run app you need firstly to install requirements from file requirements.txt:

    pip install -r requirements.txt
    
The next command should be used to run the app:

    python app.py
    

## d) How to open the port in remote VM

Port 4444 was used:

      sudo ufw allow 4444

To have the prediction of price online, you should go to [the postman](https://www.postman.com/), make the account there and make a new request. You should use get method and enter such line using your own Public IP of virtual machine:

    XX.XX.XXX.XXX:4444/predict_price
    
After this you should provide all the required params for the model, also specify model version (1: without additional parameter or 2: with additional parameters) and press the Send button. Otherwise, if you do not specify all required params, service will return the error (500 Internal server error).
After you do it, you will see the predicted price for these specific parameters and model.

## e) Information about docker

There are also files in github: Dockerfile and .dockerignore.

Dockerfile allows you to build images for Docker. Its purpose is to simplify the creation of new images without the need to launch a container, perform some operations in it and commit.

You can use docker after you do some installation and post-installation procedures:

* [Install Docker Engine on Ubuntu](https://docs.docker.com/engine/install/ubuntu/)
* [Docker post-installation steps](https://docs.docker.com/engine/install/linux-postinstall/)

.dockerignore is used to ignore the specified files and folders when trying to create a Docker image.

## f) How to run app using docker and which port it uses
The docker image was created in [my dockerhub](https://hub.docker.com/r/panchenkoanastasiia/final_gsom_predictor/tags). Docker uses port 4444.
Yoc can pull it and run using such commands in your terminal:

    docker pull panchenkoanastasiia/final_gsom_predictor:v.0.5
    docker run --network host -it panchenkoanastasiia/final_gsom_predictor:v.0.5 /bin/bash
