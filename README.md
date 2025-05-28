# 🚗 Full Stack Django Cloud App – Car Dealership Reviews
A cloud-hosted web application for submitting and viewing reviews of car dealerships across the U.S.

📚 Background
This project was developed as part of the final Capstone Project in the IBM Full Stack Cloud Developer Professional Certificate program on Coursera. I was provided with a basic Django template as a starting point, but all major functionality had to be implemented by myself.

The general idea and layout were pre-defined, but the core logic, APIs, and integrations had to be built from scratch. Due to the course’s strict peer-review criteria, I focused mainly on the backend functionality and cloud deployment rather than UI/UX polish.

💡 Project Objective
The application allows users to:

Select a Best Cars dealership (a fictional company) from across the U.S.

View existing reviews of dealership vehicles

Submit new reviews

View sentiment analysis of reviews (positive / neutral / negative)

Navigate static “About” and “Contact” pages

The app was built using Django and deployed via IBM Cloud using Cloud Foundry and Kubernetes.

🛠 Architecture & Technologies
Frontend: HTML/CSS, Bootstrap (basic layout)

Backend: Django (Python), Django Admin

Databases:

IBM Cloudant: dealership and review data

SQLite: user and car data

Cloud Functions (IBM): 3 functions built to interface with Cloudant via API

Sentiment Analysis: IBM Watson NLU

🔧 Setup Instructions
Clone the repo:

git clone https://github.com/Foxer456/your-repo-name.git
cd your-repo-name/server
Install dependencies:

python -m pip install -r requirements.txt
Run Django migrations and server:

python manage.py makemigrations
python manage.py migrate
python manage.py runserver
Create a superuser for the admin panel:

python manage.py createsuperuser
☁️ Deployment to IBM Cloud
Install the IBM Cloud CLI

Configure the manifest.yml file

Deploy with:


ibmcloud cf push
