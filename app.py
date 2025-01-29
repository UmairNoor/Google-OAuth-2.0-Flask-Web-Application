import os
import json
import requests
from flask import Flask, abort, redirect, render_template, session, url_for
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Flask app configuration
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET")

# OAuth app configuration
oauth = OAuth(app)
oauth.register(
    "myApp",
    client_id=os.getenv("OAUTH2_CLIENT_ID"),
    client_secret=os.getenv("OAUTH2_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email https://www.googleapis.com/auth/user.birthday.read https://www.googleapis.com/auth/user.gender.read",
        "code_challenge_method": "S256",  # PKCE enabled for additional security
    },
    server_metadata_url=os.getenv("OAUTH2_META_URL"),
)

# Route: Home Page
@app.route("/")
def home():
    user_session = session.get("user")
    return render_template(
        "home.html",
        session=user_session,
        pretty=json.dumps(user_session, indent=4) if user_session else None,
    )

# Route: Google Sign-in Callback
@app.route("/signin-google")
def googleCallback():
    try:
        # Fetch access token and ID token using the authorization code
        token = oauth.myApp.authorize_access_token()

        # Fetch user data via Google People API
        person_data_url = "https://people.googleapis.com/v1/people/me?personFields=genders,birthdays"
        response = requests.get(
            person_data_url,
            headers={"Authorization": f"Bearer {token['access_token']}"},
        )
        response.raise_for_status()  # Raise error for bad responses
        
        # Add user data to session
        token["personData"] = response.json()
        session["user"] = token

        return redirect(url_for("home"))
    except MismatchingStateError: # type: ignore
        return "Error: CSRF Warning! Mismatching state.", 400
    except requests.exceptions.RequestException as e:
        return f"Error during API call: {e}", 500


# Route: Google Login
@app.route("/google-login")
def googleLogin():
    if "user" in session:
        abort(404)  # User already logged in
    return oauth.myApp.authorize_redirect(redirect_uri=url_for("googleCallback", _external=True))

# Route: Logout
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))

# Main driver
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("FLASK_PORT", 5000)), debug=True)
