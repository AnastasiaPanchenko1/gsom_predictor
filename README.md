# Building a web based service from scratch for predicting house price

#### This project was made as part of a course on the cycle of development and management of machine learning models.

## Goal of the project:
* To build a web based service using which it would be possible to predict prices of apartments for rent using selected machine learning model.

This README.md file contains information about:
* source data and some statistics
* models, choosen framework, hyperparams 
* how to install instructions and run app with virtual environment
* dockerfile and description of its content
* how to open the port in remote VM
* how to run app using docker and which port it uses

### a) Information about source data and some statistics
 
 Data for the project was taken from [Yandex Reality classified](https://realty.yandex.ru) containing real estate listings for apartments in St. Petersburg and Leningrad Oblast from 2016 till the middle of August 2018.
Initial dataset consisted of 171186 observations and 17 columns.

The dataset has been cleared of outliers using interquantile range method. Cleaned dataset contains 105046 observations.

Based on EDA, features were chosen for be used in machine learning models.

![Relationships between features and price of apartment](/path/to/img.png) 

![Relationships between features and price of apartment](/path/to/img.png) 

![Relationships between features and price of apartment](/path/to/img.png) 

![There is the example of how final dataset looks like:](/path/to/img.png) 


I also have created the new variable which means the duration of time (in days) during which the house was exhibited. The longer the duration, the lower the price should be.

### b) Information about models, choosen framework, hyperparams 

I used a catboost model as the final choice for predicting prices.
DecisionTreeRegressor RMSE: 0.7306026581732368
RandomForestRegressor RMSE: 0.0.7021463938153056
CatBoostRegressor RMSE: 0.7009136610665767
LGBMRegressor RMSE: 0.709216048526922

|  Type of model        | Model without additional factors     | Model with additional factors  |
| :-------------------- | :-------------------                 | :--------------                | 
| DecisionTreeRegressor | Center-align                         | Right-align                    |
| RandomForestRegressor | Item 2                               | Item 3                         | 
| CatBoostRegressor     | Item 2                               | Item 3                         | 
| LGBMRegressor         | Item 2                               | Item 3                         | 

### c) How to install instructions and run app with virtual environment

To run app you need firstly to install requirements from file requirements.txt:
    pip install -r requirements.txt
    


### d) Information about dockerfile and description of its content

There are also files Dockerfile and .dockerignore.
Dockerfile will be helpful to run this web service in a container, .dockerignore. contains information what docker should ignore.

### e) How to open the port in remote VM

      sudo ufw allow 4444

### f) How to run app using docker and which port it uses
The docker image was created in [my dockerhub](https://hub.docker.com/r/panchenkoanastasiia/final_gsom_predictor/tags). Docker uses port 4444.
Yoc can pull it and run using such commands in your terminal:

    docker pull panchenkoanastasiia/final_gsom_predictor:v.0.5
    docker run --network host -it panchenkoanastasiia/final_gsom_predictor:v.0.5 /bin/bash
