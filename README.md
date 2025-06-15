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

### ✅ Option 1 (recomennded): Using Conda
Install Conda on your machine and create a seperate environment for this program in a conda terminal by:

1. Create the environment:
   ```bash
   conda env create -f env.yaml
   ```

2. Activate it:
   ```bash
   conda activate location-optimiser
   ```

---

### ✅ Option 2: Using pip only

If you're not using Conda, install the required packages manually, e.g.:

```bash
pip install traveltimepy python-dotenv
```

---

## 🔑 API Credentials

1. Sign up at [TravelTime](https://www.traveltime.com/signup)
2. Find your App ID and your Application Key
3. Create a `.env` file in the project root directory:

```env
TIME_APP_ID=your_app_id_here
TIME_API_KEY=your_api_key_here
```

These are required to authenticate requests to the TravelTime API.

---

## 🏃‍♀️ How to Run

```bash
python main.py
```

You'll be prompted:

- **Use default locations?** Choose "yes" to use built-in defaults.
- Or enter your own **custom office** and **home** addresses interactively.

---

## 📍 Default Locations

If you select the default option, the following locations are used:

- **Offices**:
  - Sloane Square, London
  - Holborn, London
  - Regents place, London


---

## 📤 Output

The program returns the estimated public transport travel times (in minutes) from your home to each office, e.g.:

```
office_1: 15.38 minutes
office_2: 31.13 minutes
office_3: 37.95 minutes
```

---

## 📎 License

This project is open-source and available under the MIT License.
