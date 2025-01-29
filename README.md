Google OAuth 2.0 Flask Web Application - Implementation Report
1. Introduction
This report documents the implementation of a Flask web application that integrates Google OAuth 2.0 authentication using the Authlib library. The application allows users to sign in with their Google account and retrieve basic profile information (genders, birthdays) via the Google People API.
2. Project Structure
project/
│
├── app.py          # Main Flask application
├── .env            # Environment variables (Client ID, Secret, etc.)
└── templates/      # HTML templates
    └── home.html   # User interface
3. Prerequisites
Python 3 installed
Google Developer Account
Google OAuth 2.0 credentials (Client ID, Client Secret)
Flask and required dependencies installed
4. Environment Setup
4.1 Install Dependencies
Run the following command to install required Python libraries:
pip install flask authlib requests python-dotenv flask-session
4.2 Configure Environment Variables
Create a .env file and store the following credentials securely:
FLASK_SECRET=your_flask_secret_key
OAUTH2_CLIENT_ID=your_google_client_id
OAUTH2_CLIENT_SECRET=your_google_client_secret
OAUTH2_META_URL=https://accounts.google.com/.well-known/openid-configuration
FLASK_PORT=5000
5. Implementation Details
5.1 Flask App Configuration (app.py)
Loads environment variables using dotenv
Registers the Google OAuth app with appropriate scopes
Implements session management using Flask-Session
5.2 Authentication Flow
Google Login (/google-login)
Redirects users to Google sign-in page for authentication.
@app.route("/google-login")
def googleLogin():
    if "user" in session:
        abort(404)
    return oauth.myApp.authorize_redirect(redirect_uri=url_for("googleCallback", _external=True))
Callback Handling (/signin-google)
Fetches user’s access token and profile information.
@app.route("/signin-google")
def googleCallback():
    try:
        token = oauth.myApp.authorize_access_token()
        person_data_url = "https://people.googleapis.com/v1/people/me?personFields=genders,birthdays"
        response = requests.get(
            person_data_url,
            headers={"Authorization": f"Bearer {token['access_token']}"},
        )
        response.raise_for_status()
        token["personData"] = response.json()
        session["user"] = token
        return redirect(url_for("home"))
    except requests.exceptions.RequestException as e:
        return f"Error during API call: {e}", 500
Logout (/logout)
Clears the session and redirects to home.
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))
6. Running the Application
Ensure your .env file contains valid credentials.
Run the Flask application:
python app.py
Open http://localhost:5000 in your browser.
7. Challenges and Solutions
Issue
Solution
CSRF Error (MismatchingStateError)
Used Flask sessions for secure state handling.
Google API Access Denied
Enabled Google People API in the Google Cloud Console.
Session Loss on Restart
Configured Flask-Session to use a filesystem-based session.

8. Wrap UP!
This project successfully integrates Google OAuth 2.0 into a Flask web application, demonstrating authentication, API interaction, and session management. 
