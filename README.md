# World Time Zone Application

This is a simple web application built with Python (Flask) that displays the current time in different time zones. Users first select a country from a dropdown menu. A second dropdown is then populated with specific cities or regions within that country. Upon selecting a city/region, the application displays the current time for that location. The displayed time automatically updates every second. Additionally, it now shows top news headlines from around the world, updated periodically.

The application is served using Gunicorn, a production-ready WSGI server, for improved performance and stability. Flask-Talisman is also integrated to automatically set various HTTP security headers, enhancing its resilience against common web vulnerabilities.

## Running with Docker

### Prerequisites
- Docker installed and running.

### Build the Docker Image
To build the Docker image for this application, navigate to the project's root directory (where the `Dockerfile` is located) and run:
```bash
docker build -t timezone-app .
```

### Run the Docker Container
Once the image is built, you can run the application in a Docker container. You need to provide your API key from [NewsData.io](https://newsdata.io) as an environment variable named `NEWSDATA_API_KEY`.

Example:
```bash
docker run -e NEWSDATA_API_KEY="YOUR_ACTUAL_API_KEY" -p 5000:5000 timezone-app
```
Replace `"YOUR_ACTUAL_API_KEY"` with the API key you obtained from NewsData.io.

This will start the Flask development server, and the application will be accessible at [http://localhost:5000](http://localhost:5000) in your web browser.
If the API key is not provided or is invalid, the headlines section will show an error message.

### Application Files
- `app.py`: The main Flask application file containing the server logic.
- `templates/index.html`: The HTML template for the user interface.
- `requirements.txt`: Python dependencies.
- `Dockerfile`: Instructions to build the Docker image.
