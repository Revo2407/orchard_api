# Orchard API

Orchard API is a Flask-based application designed to interact with the Aerobotics API. It fetches survey data, analyzes tree data, and identifies missing trees in orchards. This API provides a structured and easy-to-use interface for accessing orchard data.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Environment Variables](#environment-variables)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Fetch Survey Data**: Retrieves the latest survey data from the Aerobotics API.
- **Analyze Tree Data**: Identifies and lists missing trees in orchards.
- **Structured API**: Provides endpoints for easy access to processed orchard data.

## Installation

### Prerequisites

- Python 3.6+
- pip (Python package installer)
- Docker (optional, for containerized deployment)

### Local Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Revo2407/orchard_api.git
   cd orchard_api

2. Create and activate a virtual environment:
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

3. Install the required packages:
pip install -r requirements.txt

4. Set up environment variables:
AERO_AUTH=your_actual_token

5. Run the application:
python run.py

### Docker Setup
1. Build the Docker image:
docker build -t orchard_api .

2. Run the Docker container:
docker run -d -p 5000:5000 --name orchard_api_container orchard_api





