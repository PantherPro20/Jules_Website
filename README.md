# World Time Zone Application

This is a simple web application built with Python (Flask) that displays the current time in different time zones. Users can select a time zone from a dropdown menu to see the corresponding time.

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
This will start the Flask development server, and the application will be accessible at [http://localhost:5000](http://localhost:5000) in your web browser.

### Application Files
- `app.py`: The main Flask application file containing the server logic.
- `templates/index.html`: The HTML template for the user interface.
- `requirements.txt`: Python dependencies.
- `Dockerfile`: Instructions to build the Docker image.
