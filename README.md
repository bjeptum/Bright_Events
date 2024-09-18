## Bright Events 

This project provides a platform for event organizers to create and manage different types of events while making them easily accessible to target markets.
 
### Challenge statement

This project is broken down into 4 challenges whose completion would contribute greatly to my learning towards becoming a full-stack developer. Upon completion, I would have built a world-class full-stack (frontend and backend) Python and JavaScript events application.

### Usage

The project is entirely for educational purposes with no intention to release it for use by the public. However, in an ideal scenario, it would be used by event organizers as well as attendees  to have a one stop for registration and managing the logistics of an  event/events. Bright events is open to be used in any locality.

### Product Features
- Users can create an account and log in
- Users can create, view, update and delete an event
- Users can RSVP to an event
- Users can view who will be attending their event
- Users can search for events based on event location or event category

## Guide to running the Flask Application

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
   pip install -r Bright_Events/backend/requirements.txt
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
 
8. Navigate to your web browser 
`
http://127.0.0.1:5000
`
