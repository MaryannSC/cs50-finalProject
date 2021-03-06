import os
import re

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
# db = SQL("sqlite:///finance.db")
db = SQL("sqlite:///swimTracker.db")

# Make sure API key is set
# if not os.environ.get("API_KEY"):
#     raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    
    # get users name from database
    rows = db.execute(
        "SELECT firstName FROM users WHERE userid=?", session["user_id"])
    print("db row = {} ".format(rows))

    return render_template("summary.html", firstName=firstName )


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # get stock symbol entered by user
        buySymbol = request.form.get("symbol")
        if buySymbol == '':
            return apology("You must enter a stock symbol", 400)

        # lookup data for company
        data = lookup(buySymbol)
        if data == None:
            return apology("Symbol not found", 400)

        # get number of shares entered by user
        shares = request.form.get("shares")
        if shares == '':
            return apology("You must enter a value for number of shares", 400)

        if shares.find("-") > -1:
            return apology("You must enter a positive number of shares", 400)

        if not shares.isdigit():
            return apology("You must enter an integer number of shares", 400)

        # check if user has enough cash for purchase
        rows = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        cash = rows[0]["cash"]

        if float(shares) * data["price"] > cash:
            return apology("You do not have enough cash for that purchase!", 400)

        # Make puchase, insert into transactions table
        else:
            db.execute("INSERT INTO transactions (userid, symbol, shares, price) VALUES(?, ?, ?, ?)",
                       session["user_id"], data["symbol"], int(shares), data["price"])
            # update cash in user table
            db.execute("UPDATE users SET cash = ? WHERE id = ?", cash - float(shares)*data["price"], session["user_id"])

            # Redirect user to home page
            return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # get stock info from database
    activity = db.execute("SELECT symbol, shares, price, timestamp FROM transactions WHERE userid=?", session["user_id"])
    for transaction in activity:
        transaction['price'] = usd(transaction['price'])

    return render_template("history.html", activity=activity)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure email was submitted
        if not request.form.get("email"):
            return apology("must provide email", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE email = ?", request.form.get("email"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["userid"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        symbol = request.form.get("symbol")
        if symbol == '':
            return apology("You must enter a stock symbol")

        data = lookup(symbol)
        if data == None:
            return apology("Symbol not found", 400)

        return render_template("quoted.html", data=data)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Get data from form:
        email = request.form.get("email")
        first = request.form.get("first")
        last = request.form.get("last")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure username was submitted
        if not email:
            return apology("must provide email", 400)

        # Ensure first name was submitted
        if not first:
            return apology("must provide first name", 400)

        # Ensure last name was submitted
        if not last:
            return apology("must provide last name", 400)

        # Ensure password was submitted
        if not password:
            return apology("must provide password", 400)

        # Ensure password confirmation was submitted
        if not confirmation:
            return apology("must reenter password to confirm", 400)

        # Query database to check if username already exists
        rows = db.execute("SELECT * FROM users WHERE email = ?", email)

        if len(rows) == 1:
            return apology("email already exists", 400)

        # Check if passwords match
        if password != confirmation:
            return apology("passwords must match", 400)

        # Check strength of password: must have at least 8 characters, 1 uppercase, 1 lowercase, 1 special character

        # Check length of password
        if len(password) < 8:
            return apology("passwords must have at least 8 characters", 400)

        upperRegex = re.compile(r'[A-Z]')
        lowerRegex = re.compile(r'[a-z]')
        numberRegex = re.compile(r'\d')
        specialRegex = re.compile(r'\W')

        if(upperRegex.search(password) == None):
            return apology("passwords must contain at least 1 uppercase character", 400)

        if(lowerRegex.search(password) == None):
            return apology("passwords must contain at least 1 lowercase letter", 400)

        if(numberRegex.search(password) == None):
            return apology("passwords must contain a least 1 number", 400)

        if(specialRegex.search(password) == None):
            return apology("passwords must contain at least 1 special character", 400)

        # Add user to database
        db.execute("INSERT INTO users (email, hash, firstName, lastName) VALUES(?, ?, ?, ?)", email,
                   generate_password_hash(password), first, last)

        # Query database to get user's id for session
        rows = db.execute("SELECT * FROM users WHERE email = ?", request.form.get("email"))

        session["user_id"] = rows[0]["userid"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

@app.route("/logSwims", methods=["GET", "POST"])
@login_required
def logSwims():

    return apology("TODO Log Swims", 400)

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # get user's stock info from database
    holdings = db.execute(
        "SELECT symbol, SUM(shares) FROM transactions WHERE userid=? GROUP BY symbol HAVING SUM(shares) > 0", session["user_id"])

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        sellSymbol = request.form.get("symbol")
        if sellSymbol == None:
            return apology("Please select a stock symbol")

        sellShares = request.form.get("shares")
        if sellShares == '':
            return apology("Please enter number of shares")
        sellShares = int(sellShares)
        if sellShares < 0:
            return apology("Number of shares must be greater than 0")

        for stock in holdings:
            if stock['symbol'] == sellSymbol:
                ownShares = stock['SUM(shares)']

        # check if user owns sufficient shares
        if sellShares > ownShares:
            return apology(f"You can't sell {sellShares}, you only own {ownShares} shares!")

        # complete transaction
        else:
            # get current price of stock
            data = lookup(sellSymbol)
            if data == None:
                return apology("Symbol not found", 400)

            # update transactions with negative shares of stock
            db.execute("INSERT INTO transactions (userid, symbol, shares, price) VALUES(?, ?, ?, ?)",
                       session["user_id"], data["symbol"], (-1) * int(sellShares), data["price"])

            # get current user CASH
            rows = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
            cash = rows[0]['cash']

            # add to user cash
            db.execute("UPDATE users SET cash = ? WHERE id = ?", cash + float(sellShares)*data["price"], session["user_id"])

            # Redirect user to home page
            return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    # Display dropdown of stocks available to sell and get how many shares to sell
    else:
        stockList = []

        for stock in holdings:
            stockList.append(stock['symbol'])

        return render_template("sell.html", stockList=stockList)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
