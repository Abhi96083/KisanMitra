# KisanMitra

#### An AI-driven platform offering crop recommendations, fertilizer suggestions, and disease detection for optimal farming.

## MOTIVATION

-   Farming is one of the major sectors that influences a country’s economic growth.

-   In country like India, majority of the population is dependent on agriculture for their livelihood. Many new technologies, such as Machine Learning and Deep Learning, are being implemented into agriculture so that it is easier for farmers to grow and maximize their yield.

-   In this project, I present a website in which the following applications are implemented; Crop recommendation, Fertilizer recommendation and Plant disease prediction, respectively.

    -   In the crop recommendation application, the user can provide the soil data from their side and the application will predict which crop should the user grow.

    -   For the fertilizer recommendation application, the user can input the soil data and the type of crop they are growing, and the application will predict what the soil lacks or has excess of and will recommend improvements.

    -   For the last application, that is the plant disease prediction application, the user can input an image of a diseased plant leaf, and the application will predict what disease it is and will also give a little background about the disease and suggestions to cure it.

## DATA SOURCE 📊

-   [Crop recommendation dataset ](https://www.kaggle.com/atharvaingle/crop-recommendation-dataset) (custom built dataset)
-   [Fertilizer suggestion dataset](https://github.com/Gladiator07/Harvestify/blob/master/Data-processed/fertilizer.csv) (custom built dataset)
-   [Disease detection dataset](https://www.kaggle.com/vipoooool/new-plant-diseases-dataset)

## Notebooks 📓

# Built with 🛠️

<code><img height="30" src="https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/python/python.png"></code>
<code><img height="30" src="https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/html/html.png"></code>
<code><img height="30" src="https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/css/css.png"></code>
<code><img height="30" src="https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/javascript/javascript.png"></code>
<code><img height="30" src="https://github.com/tomchen/stack-icons/raw/master/logos/bootstrap.svg"></code>
<code><img height="30" src="https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/git/git.png"></code>
<code><img height="30" src="https://symbols.getvecta.com/stencil_80/56_flask.3a79b5a056.jpg"></code>
<code><img height="30" src="https://cdn.iconscout.com/icon/free/png-256/heroku-225989.png"></code>

<code><img height="30" src="https://raw.githubusercontent.com/numpy/numpy/7e7f4adab814b223f7f917369a72757cd28b10cb/branding/icons/numpylogo.svg"></code>
<code><img height="30" src="https://raw.githubusercontent.com/pandas-dev/pandas/761bceb77d44aa63b71dda43ca46e8fd4b9d7422/web/pandas/static/img/pandas.svg"></code>
<code><img height="30" src="https://matplotlib.org/_static/logo2.svg"></code>
<code><img height="30" src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Scikit_learn_logo_small.svg/1280px-Scikit_learn_logo_small.svg.png"></code>
<code><img height="30" src="https://raw.githubusercontent.com/pytorch/pytorch/39fa0b5d0a3b966a50dcd90b26e6c36942705d6d/docs/source/_static/img/pytorch-logo-dark.svg"></code>

## DEPLOYMENT 🚀

-   Heruko was used for deployment.

## How to use 💻

-   Crop Recommendation system ==> enter the corresponding nutrient values of your soil, state and city. Note that, the N-P-K (Nitrogen-Phosphorous-Pottasium) values to be entered should be the ratio between them. Refer [this website](https://www.gardeningknowhow.com/garden-how-to/soil-fertilizers/fertilizer-numbers-npk.htm) for more information.
    Note: When you enter the city name, make sure to enter mostly common city names. Remote cities/towns may not be available in the [Weather API](https://openweathermap.org/) from where humidity, temperature data is fetched.

-   Fertilizer suggestion system ==> Enter the nutrient contents of your soil and the crop you want to grow. The algorithm will tell which nutrient the soil has excess of or lacks. Accordingly, it will give suggestions for buying fertilizers.

-   Disease Detection System ==> Upload an image of leaf of your plant. The algorithm will tell the crop type and whether it is diseased or healthy. If it is diseased, it will tell you the cause of the disease and suggest you how to prevent/cure the disease accordingly.
    Note that, for now it only supports following crops

<details>
  <summary>Supported crops
</summary>

-   Apple
-   Blueberry
-   Cherry
-   Corn
-   Grape
-   Pepper
-   Orange
-   Peach
-   Potato
-   Soybean
-   Strawberry
-   Tomato
-   Squash
-   Raspberry
</details>

## How to run locally 🛠️

-   Before the following steps make sure you have [git](https://git-scm.com/download), [Anaconda](https://www.anaconda.com/) or [miniconda](https://docs.conda.io/en/latest/miniconda.html) installed on your system
    ```
    git clone https://github.com/Abhi96083/Kishanmitra
    ```
-   `deploy` branch has only the code required for deploying the app (rest of the code that was used for training the models, data preparation can be accessed on `master` branch)
-   It is highly recommended to clone the deploy branch for running the project locally (the further steps apply only if you have the deploy branch cloned)
-   Once the project is cloned, open anaconda prompt in the directory where the project was cloned and paste the following block
    ```
    conda create -n kisanmitra python=3.6.12
    conda activate kisanmitra
    pip install -r requirements.txt
    ```
-   And finally run the project with
    ```
    python app.py
    ```
-   Open the localhost url provided after running `app.py` and now you can use the project locally in your web browser.
##  REQUIREMENT OF HARWARE FOR TAKING INPUTS FOR THIS PROJECT..
-   Here we will use the soil testor which is android base which has certain things mentioned below
-   What the Device Is
-   The SNS-08 is a portable, handheld soil sensor that connects directly to a phone or computer using a USB Type-C (also supports Micro-USB and USB). It’s designed to give farmers, gardeners, and researchers eight important soil measurements in one rugged tool, instead of needing separate instruments.

- ## What It Measures (8-in-1)
 - 1. Moisture – how much water is in the soil.
 - 2.Temperature – the heat level of the soil, important for seed germination and crop growth.
 - 3.Electrical Conductivity (EC) – indicates the concentration of salts and dissolved nutrients.
 - 4.Salinity – measures soil salt levels (derived from EC).
 - 5.pH – shows if the soil is acidic, neutral, or alkaline, which affects nutrient availability.
 - 6.Nitrogen (N) – one of the most vital nutrients for plant growth.
 - 7.Phosphorus (P) – supports root and flower development.
 - 8.Potassium (K) – essential for disease resistance and overall plant health.
 - 9.Together, N-P-K are the “fertility” indicators of soil

- ## How It Works
  - The device uses FDR technology (Frequency Domain Reflectometry), which is a reliable method to sense soil moisture and nutrients.
  - When inserted into soil (probe goes about 7 cm deep and reads a 7 cm diameter zone), it quickly detects conditions.
  - Data is shown on a connected Android phone, tablet, or Windows device using the app/software.
  - It does not require batteries – it draws power directly from the USB connection.

- ## Build and Durability
  - The body and electrodes are made of high-strength alloy to resist corrosion.
  - The enclosure is epoxy-sealed with IP67 waterproof rating, meaning it can handle water, dust, and tough field conditions.
  - It operates in extreme environments from –40 °C to 80 °C.
  
- ## Speed and Logging
  - It gives results in less than 5 seconds after insertion.
  - Data can be logged and exported for later trend analysis, which is useful in farm management or research studies.

- ## Why It’s Useful
  - Instead of guessing soil health or relying only on lab testing, this device provides instant, on-site analysis. That means farmers and gardeners can adjust fertilizers, water, and soil           - treatments immediately, saving time, improving yields, and reducing overuse of chemicals.

 
 - ![demo](https://drive.google.com/uc?export=view&id=1ojOroNTsUC8egvArtI_LucSGbzdzBe8m)


![demo](https://drive.google.com/uc?export=view&id=1zD33DEckaiXmQwUwUQXDvFYQAK0V7RCg)

  
## DEMO

-   ### Crop recommendation system

![demo](https://res.cloudinary.com/hackerraushan/image/upload/v1743626650/qy4sg0jqrzwiawdddc47.gif)

## Usage ⚙️

You can use this project for further developing it and adding your work in it. If you use this project, kindly mention the original source of the project and mention the link of this repo in your report.

## Further Improvements 📈

This was my first big project so there are lot of things to improve upon

-   CSS code is totally messed up :pensive: (some code in file and some inline)
-   Frontend can be made more nicer (PS: I suck at frontend development) :cry:
-   More data can be collected manually via web scrapping to make the system more accurate :monocle_face:
-   Additional plant images can be collected to make the disease detection part more robust and generalized :face_with_head_bandage:
-   Modularized code can be written instead of writing in Jupyter Notebooks (will follow this in upcoming projects)
