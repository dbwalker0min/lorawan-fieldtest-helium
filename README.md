# Lorawan Fieldtest

## Overview
Lorawan Fieldtest is a FastAPI application designed for managing and testing LoRaWAN devices. This project integrates a database to store and manage data related to field tests.

## Project Structure
```
lorawan-fieldtest
├── app
│   ├── main.py
│   ├── api
│   │   └── endpoints.py
│   ├── db
│   │   ├── database.py
│   │   └── models.py
│   └── core
│       └── config.py
├── requirements.txt
└── README.md
```

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/lorawan-fieldtest.git
   cd lorawan-fieldtest
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the database**
   Update the database configuration in `app/core/config.py` with your database URL.

5. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

## Usage
Once the application is running, you can access the API documentation at `http://127.0.0.1:8000/docs`. Here you can test the available endpoints.

## Contributing
Feel free to submit issues or pull requests for improvements and features. 

## License
This project is licensed under the MIT License.