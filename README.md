# Sparkle Regressor
Sparkle Regressor is a component of the Sparkle system, implemented in Python, and designed to forecast energy usage based on the provided data columns. This Python application serves as the dedicated regression module, and contains logic for creating personalized regression models incorporating for predicting future energy consumption patterns accurately. Sparkle Regressor is written in Python, using a modular layer approach.

**Key Features:**

- **Data-Driven Forecasting:** Sparkle Regressor utilizes the data columns provided to create personalized regression models for precise energy usage predictions.

- **Modular Design:** The application is meticulously designed in Python, following a modular approach, ensuring flexibility and maintainability.

## Getting Started

Follow these steps to get started with Sparkle Regressor:

1. **Data Preparation**: Ensure you have a `data.csv` file in the `Assets/` directory. The data should have an index column, and other columns should contain float values (without negative values). This file is named `train_data.csv`.

2. **Model Generation**: Run the script located in `utils/ModelGeneratorUtil.py`. This step generates prediction models based on the provided data.

   ```bash
   python utils/ModelGeneratorUtil.py
   ```

   Alternatively, if you have pre-generated models, you can skip this step or u can use API Input apporach.
   
   The regressor will create personalized prediction models for each column in the dataset for various time frames, such as [24 hours, 48 hours, 168 hours, and 720 hours].(in memory if u use alternative approach)

3. **API Input**: To use the API, provide a large dictionary of dates and values.(recommend a minimum data volume is one year)

4. **Running the Local Server**: Execute `Host.py` to run a dedicated local server.

   ```bash
   python Host.py
   ```

   The server can be accessed at `http://localhost:8080/docs`.

## Deployment

To deploy Sparkle Regressor, you have two options:

- **Docker**: Use the provided `Dockerfile` in the repository to build a Docker image and deploy it.

   ```bash
   docker build -t sparkle-regressor .
   docker run -p 8080:8080 sparkle-regressor
   ```

- **Manual Deployment**: If you prefer manual deployment, make sure to install the required packages from `requirements.txt` using:

   ```bash
   pip install -r requirements.txt
   ```

   Then, you can run the application using:

   ```bash
   python Host.py
   ```

   Access the server at `http://localhost:8080/docs`.

## Live Version

You can access the live version of Sparkle Regressor at [https://sparkle-regressor.onrender.com/docs](https://sparkle-regressor.onrender.com/docs).

## Version

The current version of Sparkle Core can be found there [https://github.com/norbertszsor/Sparkle.Regressor/releases](https://github.com/norbertszsor/Sparkle.Regressor/releases)
