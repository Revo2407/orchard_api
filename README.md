
# Missing Trees Detection API

## Project Overview

**Project Name:** Missing Trees Detection API

**Description:**  
This Flask application provides an API for detecting missing trees in an orchard based on survey data. It fetches the latest survey data from an external API, processes the data to find missing trees using geospatial algorithms, and returns the results in a JSON format.

## Setup and Installation

### Prerequisites:
- Python 3.7+
- Docker (for containerized deployment)
- Access to the Aerobotics API (API token required)

### Local Setup:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
   ```

2. **Create a Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables:**
   Create a `.env` file in the root of the project and add your Aerobotics API token:
   ```
   AERO_AUTH=your_api_token_here
   ```

5. **Run the Application:**
   ```bash
   python run.py
   ```
   The application will be accessible at `http://localhost:5000`.

### Docker Setup:

1. **Build the Docker Image:**
   ```bash
   docker build -t your-image-name .
   ```

2. **Run the Docker Container:**
   ```bash
   docker run -p 5000:5000 your-image-name
   ```

## Usage

### API Endpoints:

- **GET /orchards/<orchard_id>/missing-trees**
  - **Description:** Retrieves missing tree data for the specified orchard.
  - **Parameters:**
    - `orchard_id` (int): The ID of the orchard.
  - **Response:**
    - `200 OK`: Returns a JSON object with missing tree coordinates.
    - `500 Internal Server Error`: Returns an error message if something goes wrong.

### Example Request:
```bash
curl http://localhost:5000/orchards/216269/missing-trees
```

### Example Response:
```json
{
  "missing_trees": [
    {"lat": -33.918861, "lng": 18.423300},
    {"lat": -33.919860, "lng": 18.424290}
  ]
}
```

## Development

### Project Structure:

```
/your-project
│
├── app/
│   ├── __init__.py  # Initializes the Flask app
│   ├── main.py      # Contains route definitions and core logic
│   └── utils.py     # (Optional) Utility functions
│
├── Dockerfile       # Docker configuration
├── requirements.txt # Python dependencies
├── run.py           # Entry point for the application
├── .env             # Environment variables (not checked into version control)
└── README.md        # Project documentation
```

### Key Components:

- **app/main.py:** Contains the core application logic, including API endpoints and functions for interacting with the external API and processing data.
- **run.py:** Entry point for running the Flask application.
- **Dockerfile:** Configuration for Docker containerization.

### Environment Variables:

- **AERO_AUTH:** API token for authenticating with the Aerobotics API.

## Testing

### Running Tests:

1. **Unit Tests:**
   - Add tests in a `tests` directory, structured similarly to the main application.
   - Use a testing framework like `unittest` or `pytest`.

2. **Example Test Command:**
   ```bash
   python -m unittest discover -s tests
   ```

### Integration Tests:

- Ensure the application can successfully connect to external services like the Aerobotics API and that it handles errors gracefully.

## Deployment

### Deploying with Docker:

1. **Push Docker Image to Registry:**
   ```bash
   docker tag your-image-name your-dockerhub-username/your-image-name
   docker push your-dockerhub-username/your-image-name
   ```

2. **Deploy to Hosting Platform:**
   - Use a platform like Render, AWS, or Heroku. Configure the environment variables and set up the deployment pipeline as needed.

### Environment Configuration:

- Set environment variables securely using the platform's configuration management tools.
