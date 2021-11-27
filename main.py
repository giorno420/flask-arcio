import requests
import os, json
from coins import coinsDB
from flask import Flask, redirect, url_for, render_template, request, send_from_directory
from flask_discord import DiscordOAuth2Session, requires_authorization


with open("settings.json", 'r') as configjson:
    config = json.load(configjson)

app = Flask(__name__)

app.secret_key = os.urandom(24)
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = config['insecuretransport']
app.config["DISCORD_CLIENT_ID"] = config['id']
app.config["DISCORD_CLIENT_SECRET"] = config['secret']
app.config["DISCORD_REDIRECT_URI"] = config['redirect_uri']
app.config['DISCORD_BOT_TOKEN'] = config['token']
discord = DiscordOAuth2Session(app)


@app.route('/login')
def login():
    return discord.create_session()


@app.route('/callback')
def callback():
    discord.callback()
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    discord.revoke()
    return redirect(url_for('index'))


@app.route('/')
def index():

	if discord.authorized:
		user = discord.fetch_user()
        
		return f"hey there {user.username}#{user.discriminator} click <a href=\"/earn\">here</a> to make coins :D"

	elif not discord.authorized:
		return "hey there click <a href=\"/login\">here</a> to login"


@app.route('/earn', methods=["POST", "GET"])
def earncoins():

	if discord.authorized:

		user = discord.fetch_user()

		if type(request.get_json()) is None:
			pass

		elif type(request.get_json()) is dict:
			coinsDB.addCoins(str(user.id))

		return render_template("earning.html")

	elif not discord.authorized:
		return redirect(url_for("login"))


@app.route("/arc-sw.js")
def arcserviceworker():
	return send_from_directory(app.static_folder, "js/arc-sw.js")



app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
