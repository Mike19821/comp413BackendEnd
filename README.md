# comp413BackendEnd

DermoScan backend 
For full documentation refer to https://docs.google.com/document/d/1FlFcBWK_iboTGFWYMGaGVx25KMaB_1p9Ta5WgcKC0q4/edit?usp=sharing

This repository contains the backend for dermoscan
Sure, here's a sample README.md file for the backend component of your cross-platform mobile app project:

```markdown
# Mobile App Backend

This repository contains the backend codebase for our cross-platform mobile application, built using Flask and Python. It provides a robust API and services to support the mobile app's functionalities.

## Technologies Used

- **Flask**: A lightweight and flexible Python web framework used for building the backend API and services.
- **MongoDB**: A scalable and flexible NoSQL database used for storing and querying application data.
- **Amazon S3**: A highly scalable and durable object storage service provided by AWS, used for storing and serving static assets such as images.

## Getting Started

### Prerequisites

- Python 3.7 or higher
- MongoDB installed and running
- AWS account with S3 bucket set up

### Installation

1. Clone the repository:

```
[git clone https://github.com/your-username/mobile-app-backend.git](https://github.com/Mike19821/comp413BackendEnd.git)
```

2. Navigate to the project directory:

```
3. Set up the environment variables:

```
export FLASK_APP=app.py
export MONGO_URI="mongodb://localhost:27017/your-database-name"
export AWS_ACCESS_KEY_ID="your-aws-access-key-id"
export AWS_SECRET_ACCESS_KEY="your-aws-secret-access-key"
export AWS_S3_BUCKET="your-s3-bucket-name"
```

### Running the Application

To start the Flask development server, run:

```
flask run
```

The backend API will be accessible at `http://localhost:5000`.

## API Documentation

Detailed API documentation can be found in https://docs.google.com/document/d/1FlFcBWK_iboTGFWYMGaGVx25KMaB_1p9Ta5WgcKC0q4/edit?usp=sharing
```

This README provides an overview of the backend project, lists the technologies used, and includes instructions for setting up the development environment, running the application, and accessing the API documentation. It also mentions the contribution guidelines and the project's license.

Note that you'll need to update the placeholders (e.g., `your-username`, `your-database-name`, AWS credentials, and S3 bucket name) with the appropriate values for your project. Additionally, you may want to include more details about the API routes, database models, and any other relevant information specific to your project.
