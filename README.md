# 🚀 Rick & Morty API Integration

This project is a **FastAPI-based integration** for the [Rick and Morty API](https://rickandmortyapi.com/).  
It provides endpoints to fetch, filter, and store **characters, locations, and episodes** asynchronously.


git clone https://github.com/yourusername/rick-and-morty-integration.git
cd rick-and-morty-integration


python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


pip install -r requirements.txt


uvicorn sample_app.rap_api:app --reload


GET /fetch/{entity}/

GET /filter-episodes?start_year=2017&end_year=2021