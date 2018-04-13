"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from forms import LoginForm,SignUpForm,StockForm,SettingsForm
from models import User
from app.models import *
import requests
import json
import datetime


###
# Routing for your application.
###

# Stock symbols
dow = ['AXP', 'AAPL', 'BA', 'CAT', 'CSCO', 'CVX', 'XOM', 'GE', 'GS', 'HD', 'IBM', 'INTC', 'JNJ', 'KO', 'JPM', 'MCD', 'MMM', 'MRK', 'MSFT', 'NKE', 'PFE', 'PG', 'TRV', 'UNH', 'UTX', 'VZ', 'V', 'WMT', 'DIS', 'DWDP']
SP500 =  ['A', 'AA', 'AAPL', 'ABC', 'ABT', 'ACE', 'ACN', 'ADBE', 'ADI', 'ADM', 'ADP', 'ADSK', 'ADT', 'AEE', 'AEP', 'AES', 'AET', 'AFL', 'AGN', 'AIG', 'AIV', 'AIZ', 'AKAM', 'ALL', 'ALTR', 'ALXN', 'AMAT', 'AMD', 'AMGN', 'AMP', 'AMT', 'AMZN', 'AN', 'ANF', 'AON', 'APA', 'APC', 'APD', 'APH', 'APOL', 'ARG', 'ATI', 'AVB', 'AVP', 'AVY', 'AXP', 'AZO', 'BA', 'BAC', 'BAX', 'BBBY', 'BBT', 'BBY', 'BCR', 'BDX', 'BEAM', 'BEN', 'BF.B', 'BHI', 'BIG', 'BIIB', 'BK', 'BLK', 'BLL', 'BMC', 'BMS', 'BMY', 'BRCM', 'BRK.B', 'BSX', 'BTU', 'BWA', 'BXP', 'C', 'CA', 'CAG', 'CAH', 'CAM', 'CAT', 'CB', 'CBG', 'CBS', 'CCE', 'CCI', 'CCL', 'CELG', 'CERN', 'CF', 'CFN', 'CHK', 'CHRW', 'CI', 'CINF', 'CL', 'CLF', 'CLX', 'CMA', 'CMCSA', 'CME', 'CMG', 'CMI', 'CMS', 'CNP', 'CNX', 'COF', 'COG', 'COH', 'COL', 'COP', 'COST', 'COV', 'CPB', 'CRM', 'CSC', 'CSCO', 'CSX', 'CTAS', 'CTL', 'CTSH', 'CTXS', 'CVC', 'CVH', 'CVS', 'CVX', 'D', 'DD', 'DE', 'DELL', 'DF', 'DFS', 'DG', 'DGX', 'DHI', 'DHR', 'DIS', 'DISCA', 'DLTR', 'DNB', 'DNR', 'DO', 'DOV', 'DOW', 'DPS', 'DRI', 'DTE', 'DTV', 'DUK', 'DVA', 'DVN', 'EA', 'EBAY', 'ECL', 'ED', 'EFX', 'EIX', 'EL', 'EMC', 'EMN', 'EMR', 'EOG', 'EQR', 'EQT', 'ESRX', 'ESV', 'ETFC', 'ETN', 'ETR', 'EW', 'EXC', 'EXPD', 'EXPE', 'F', 'FAST', 'FCX', 'FDO', 'FDX', 'FE', 'FFIV', 'FHN', 'FII', 'FIS', 'FISV', 'FITB', 'FLIR', 'FLR', 'FLS', 'FMC', 'FOSL', 'FRX', 'FSLR', 'FTI', 'FTR', 'GAS', 'GCI', 'GD', 'GE', 'GILD', 'GIS', 'GLW', 'GME', 'GNW', 'GOOG', 'GPC', 'GPS', 'GS', 'GT', 'GWW', 'HAL', 'HAR', 'HAS', 'HBAN', 'HCBK', 'HCN', 'HCP', 'HD', 'HES', 'HIG', 'HNZ', 'HOG', 'HON', 'HOT', 'HP', 'HPQ', 'HRB', 'HRL', 'HRS', 'HSP', 'HST', 'HSY', 'HUM', 'IBM', 'ICE', 'IFF', 'IGT', 'INTC', 'INTU', 'IP', 'IPG', 'IR', 'IRM', 'ISRG', 'ITW', 'IVZ', 'JBL', 'JCI', 'JCP', 'JDSU', 'JEC', 'JNJ', 'JNPR', 'JOY', 'JPM', 'JWN', 'K', 'KEY', 'KIM', 'KLAC', 'KMB', 'KMI', 'KMX', 'KO', 'KR', 'KRFT', 'KSS', 'L', 'LEG', 'LEN', 'LH', 'LIFE', 'LLL', 'LLTC', 'LLY', 'LM', 'LMT', 'LNC', 'LO', 'LOW', 'LRCX', 'LSI', 'LTD', 'LUK', 'LUV', 'LYB', 'M', 'MA', 'MAR', 'MAS', 'MAT', 'MCD', 'MCHP', 'MCK', 'MCO', 'MDLZ', 'MDT', 'MET', 'MHP', 'MJN', 'MKC', 'MMC', 'MMM', 'MNST', 'MO', 'MOLX', 'MON', 'MOS', 'MPC', 'MRK', 'MRO', 'MS', 'MSFT', 'MSI', 'MTB', 'MU', 'MUR', 'MWV', 'MYL', 'NBL', 'NBR', 'NDAQ', 'NE', 'NEE', 'NEM', 'NFLX', 'NFX', 'NI', 'NKE', 'NOC', 'NOV', 'NRG', 'NSC', 'NTAP', 'NTRS', 'NU', 'NUE', 'NVDA', 'NWL', 'NWSA', 'NYX', 'OI', 'OKE', 'OMC', 'ORCL', 'ORLY', 'OXY', 'PAYX', 'PBCT', 'PBI', 'PCAR', 'PCG', 'PCL', 'PCLN', 'PCP', 'PCS', 'PDCO', 'PEG', 'PEP', 'PETM', 'PFE', 'PFG', 'PG', 'PGR', 'PH', 'PHM', 'PKI', 'PLD', 'PLL', 'PM', 'PNC', 'PNR', 'PNW', 'POM', 'PPG', 'PPL', 'PRGO', 'PRU', 'PSA', 'PSX', 'PWR', 'PX', 'PXD', 'QCOM', 'QEP', 'R', 'RAI', 'RDC', 'RF', 'RHI', 'RHT', 'RL', 'ROK', 'ROP', 'ROST', 'RRC', 'RRD', 'RSG', 'RTN', 'S', 'SAI', 'SBUX', 'SCG', 'SCHW', 'SE', 'SEE', 'SHW', 'SIAL', 'SJM', 'SLB', 'SLM', 'SNA', 'SNDK', 'SNI', 'SO', 'SPG', 'SPLS', 'SRCL', 'SRE', 'STI', 'STJ', 'STT', 'STX', 'STZ', 'SWK', 'SWN', 'SWY', 'SYK', 'SYMC', 'SYY', 'T', 'TAP', 'TDC', 'TE', 'TEG', 'TEL', 'TER', 'TGT', 'THC', 'TIE', 'TIF', 'TJX', 'TMK', 'TMO', 'TRIP', 'TROW', 'TRV', 'TSN', 'TSO', 'TSS', 'TWC', 'TWX', 'TXN', 'TXT', 'TYC', 'UNH', 'UNM', 'UNP', 'UPS', 'URBN', 'USB', 'UTX', 'V', 'VAR', 'VFC', 'VIAB', 'VLO', 'VMC', 'VNO', 'VRSN', 'VTR', 'VZ', 'WAG', 'WAT', 'WDC', 'WEC', 'WFC', 'WFM', 'WHR', 'WIN', 'WLP', 'WM', 'WMB', 'WMT', 'WPI', 'WPO', 'WPX', 'WU', 'WY', 'WYN', 'WYNN', 'X', 'XEL', 'XL', 'XLNX', 'XOM', 'XRAY', 'XRX', 'XYL', 'YHOO', 'YUM', 'ZION', 'ZMH']
nasdaq = ['AAL', 'AAPL', 'ADBE', 'ADI', 'ADP', 'ADSK', 'AKAM', 'ALGN', 'ALXN', 'AMAT', 'AMGN', 'AMZN', 'ATVI', 'AVGO', 'BIDU', 'BIIB', 'BMRN', 'CA', 'CELG', 'CERN', 'CHKP', 'CHTR', 'CTRP', 'CTAS', 'CSCO', 'CTXS', 'CMCSA', 'COST', 'CSX', 'CTSH', 'DISCA', 'DISCK', 'DISH', 'DLTR', 'EA', 'EBAY', 'ESRX', 'EXPE', 'FAST', 'FB', 'FISV', 'FOX', 'FOXA', 'GILD', 'GOOG', 'GOOGL', 'HAS', 'HSIC', 'HOLX', 'ILMN', 'INCY', 'INTC', 'INTU', 'ISRG', 'JBHT', 'JD', 'KLAC', 'KHC', 'LBTYK', 'LILA', 'LBTYA', 'QRTEA', 'MELI', 'MAR', 'MAT', 'MDLZ', 'MNST', 'MSFT', 'MU', 'MXIM', 'MYL', 'NCLH', 'NFLX', 'NTES', 'NVDA', 'PAYX', 'BKNG', 'PYPL', 'QCOM', 'REGN', 'ROST', 'SHPG', 'SIRI', 'SWKS', 'SBUX', 'SYMC', 'TSCO', 'TXN', 'TMUS', 'ULTA', 'VIAB', 'VOD', 'VRTX', 'WBA', 'WDC', 'XRAY', 'IDXX', 'LILAK', 'LRCX', 'MCHP', 'ORLY', 'PCAR', 'STX', 'TSLA', 'VRSK', 'WYNN', 'XLNX']


@app.route('/')
def home():
    
    """Render website's home page."""
    return render_template('home.html')
    
@app.route('/signup', methods=["GET", "POST"])
def signup():
    #Initialization
    form = SignUpForm()
    if request.method == "POST":
      
        if form.validate_on_submit():
            firstname = form.firstname.data
            lastname = form.lastname.data
            username = form.username.data
            password = form.password.data
        # Add to database
        user = User(firstname = firstname,lastname = lastname,username = username,password = password)
        db.create_all()
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for("profile")) 
    return render_template("signup.html", form=form)

@app.route("/login", methods=["GET", "POST"])
@login_required
def login():
    #Initialization
    form = LoginForm()
    if request.method == "POST":
      
        if form.validate_on_submit():
            
            username = form.username.data
            password = form.password.data
            
            user = User.query.filter_by(username=username,password=password).first()
            if user is None:
                flash("Sorry, there is no such user.","warning")
            else:
                login_user(user)
                return redirect(url_for("profile")) 
    return render_template("login.html", form=form)
    
    
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You were logged out.", "success")
    return redirect(url_for("home"))
    

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    
    #Initialization
    form = StockForm()
    
    # Default stock selection
    symbol = 'aapl'
    
    if request.method == "POST":
        if form.validate_on_submit():
            query = form.stock.data
            query = query.upper()
            if query in dow or query in SP500 or query in nasdaq:
                query = query.lower()
                symbol = query
            else:
                flash("Hmmm, stock symbol now found", "danger")
            
    url = "https://api.iextrading.com/1.0/stock/" + symbol + "/batch?types=quote,news,chart&range=1m&last=10"
    
    # Retrieve data
    page = requests.get(url)
    
    # Convert to json
    data = page.json()
    
    
    
    # Store retrieved data
    company = data['quote']
    symbol = company['symbol']
    name = company['companyName']
    price = company['latestPrice']
    open_price = company['open']
    change = company['change']
    change_percent = company['changePercent']
    market_cap = "{:,.2f}".format(company['marketCap'])
    close = company['close']
    volume = company['latestVolume']
    whigh = company['week52High']
    wlow = company['week52Low']
    pe_ratio = company['peRatio']
    
    # Retrieve settings
    user_id = current_user.id
    settings = Settings.query.filter_by(user_id = user_id).first()
    investor_type = settings.investor_type
    print(investor_type)
    return render_template('profile.html',form=form,symbol=symbol,name=name,price=price,open_price = open_price,change=change,change_percent=change_percent,market_cap=market_cap,close=close,volume=volume,whigh=whigh,wlow=wlow,pe_ratio=pe_ratio,investor_type=investor_type)
    
# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
    
@app.route('/settings', methods=["GET", "POST"])
def settings():
    """Render the website's settings page."""
    # Initialize form
    form = SettingsForm()
    
    if request.method == "POST":
        if form.validate_on_submit():
            user_id = current_user.id;
            investor_type = form.investor_type.data
            
            # Add to database
            settings = Settings(user_id = user_id,investor_type = investor_type)
            
            # If it doesn't exist, create a new one
            settings_check = settings.query.filter_by(user_id = user_id).first()
            
            if settings_check is None:
                db.create_all()
                db.session.add(settings)
                db.session.commit()
            else:
            # Otherwise update
                settings.investor_type = investor_type
                db.session.commit()
            
            return redirect(url_for("profile"))
            
    
    return render_template('settings.html',form=form)



###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
