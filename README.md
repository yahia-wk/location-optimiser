# 🗺️ Location Optimiser

A simple Python project that finds optimal home locations in London by computing travel times to multiple office locations using the [TravelTime API](https://www.traveltime.com/). It allows users to evaluate commute times via public transport and choose the most convenient region to live in.

---

## 🚀 Features

- Calculates travel time from a single home location to multiple office locations  
- Uses **public transport + walking** modes  
- Option to use **default office/home locations** or enter your own  
- Async implementation for fast performance using TravelTime’s API  
- Built-in support for both **Conda** and **pip-based** environments  

---

## 📦 Setup Instructions

### ✅ Option 1 (recommended): Using Conda

Install Conda on your machine and create a separate environment for this program:

    conda env create -f env.yaml        # create the env  
    conda activate location-optimiser   # activate it  

---

### ✅ Option 2: Using pip only

If you're not using Conda, install the required packages manually:

    pip install traveltimepy python-dotenv fastapi uvicorn  

---

## 🔑 API Credentials

1. Sign up at [TravelTime](https://www.traveltime.com/signup)  
2. Find your **App ID** and **Application Key**  
3. Create a `.env` file in the project root directory:

    TIME_APP_ID=your_app_id_here  
    TIME_API_KEY=your_api_key_here  

These are required to authenticate requests to the TravelTime API.

---

## 🏃‍♀️ How to Run

1. **Start the FastAPI backend** (from the project root):

       uvicorn main:app --reload

   This starts the API server at `http://127.0.0.1:8000`.

2. **Open the frontend**:

   - Double-click `frontend/index.html` to open it in your browser **or**  
   - Serve the `frontend/` folder with a simple static server:

         cd frontend
         python -m http.server 8080

     Then visit `http://localhost:8080`.

3. Enter a home address and one or more office addresses → click **“Calculate & Show Map”** → view travel times and routes on the map.

---

## 📍 Default Locations (CLI version only)

If you select the default option when running the old CLI script, the following offices are used:

- Sloane Square, London  
- Holborn, London  
- Regents Place, London  

---

## 📤 Output

The web app displays an interactive Leaflet map:

- Straight lines (polylines) from home to each office  
- Pop-ups showing the minimum public-transport travel time (in minutes)

---

## 📎 License

This project is open-source and available under the **MIT License**.
