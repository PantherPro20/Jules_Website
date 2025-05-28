# World Time Zone Application

This is a simple web application built with Python and the CherryPy framework that displays the current time in different time zones. Users first select a country from a dropdown menu. A second dropdown is then populated with specific cities or regions within that country. Upon selecting a city/region, the application displays the current time for that location. The displayed time automatically updates every second. The application also displays an embedded weather widget, allowing users to check weather conditions for various locations.

## Running with Docker

### Prerequisites
- Docker installed and running.

### Build the Docker Image
To build the Docker image for this application, navigate to the project's root directory (where the `Dockerfile` is located) and run:
```bash
docker build -t timezone-app .
```

### Run the Docker Container
Once the image is built, you can run the application in a Docker container using:
```bash
docker run -p 5000:5000 timezone-app
```
This will start the CherryPy server, and the application will be accessible at [http://localhost:5000](http://localhost:5000) in your web browser.

### Application Files
- `main.py`: The main CherryPy application file containing the server logic.
- `templates/index.html`: The HTML template for the user interface.
- `requirements.txt`: Python dependencies.
- `Dockerfile`: Instructions to build the Docker image.
