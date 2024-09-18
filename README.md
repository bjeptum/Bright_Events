## Bright Events 

### Introduction

Bright Events is a platform for event organizers to create and manage different types of events.

### The Context

Completion of the same has contributed greatly to my learning towards becoming a software engineer as a portfolio project,concluding my [ALX -Software Engineering Foundations](https://www.alxafrica.com/learn/programming-development/)

### The Team
I worked on this project solely.
Follow me on [LinkedIn](https://www.linkedin.com/in/brenda-jeptum-8bab79120/)

### Usage

The project is entirely for educational purposes with no intention to release it for use by the public. However, in an ideal scenario, it would be used by event organizers as well as attendees  to have a one stop for registration and managing the logistics of an  event/events. Bright events is open to be used in any locality.

### Product Features
- Users can create an account and log in
- Users can create, view, update and delete an event
- Users can RSVP to an event
- Users can view who will be attending their event
- Users can search for events based on event location or event category

## Installation
The project is not deployed butcan be used locally following the below steps:

    #### Ubuntu Terminal:

1.  Clone the repository
`
    git clone git@github.com:bjeptum/Bright_Events.git
    `
2. Navigate to the project directory 
`
    cd Bright_Events/backend
    `
3. Setup a virtual environment
`
    python3 -m venv myenv
    source myenv/bin/activate
    `
    /* Note: to deactivate the environment type deactivate */
   
4. Install dependencies

   `
   pip install -r requirements.txt
   `
5. Set Up Environment Variables

   - Create a .env file in the root directory
   - Add required enviroment variables for example:
  
  ` 
  FLASK_APP=backend/app
  FLASK_ENV=development
  DATABASE_URL=sqlite:///app.db
  SECRET_KEY=your_secret_key
  `
  
6. Initialize the database

  `python3 -m flask shell`
  
7. Run the Flask application
   
 `
 python3 -m flask run
 `
 
8. Navigate to your web browser and have at it 
`
http://127.0.0.1:5000/
`

### Blog Post

Upon completion of the development phase of Bright Event, I wrote a blog post of my experience.
[........](...)


### Contribution 

Jeptum Brenda is the only contributorat this time 
