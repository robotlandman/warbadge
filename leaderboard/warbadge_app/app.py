#!/usr/bin/env python
"""
app.py is the main guts of the warbadge leaderboard site.
If flask is properly installed you should be able to run
"python app.py" to start the app locallly. You will need
to setup your database and provide the credential in
this file for the app to work.
"""
from __future__ import print_function  # In python 2.7
import json
import operator
import logging

from flask import Flask, render_template, request, abort
from pymysql.err import IntegrityError
from flaskext.mysql import MySQL
from netaddr import EUI, mac_unix
from flask_cache import Cache

# Begin Flask app setup

# pylint: disable=C0103

mysql = MySQL()
app = Flask(__name__)

# App configration
app.config.from_object('warbadge_app.settings')
app.config.from_envvar('WARBADGE_SETTINGS')

# Caching for API/HTTP routes. Simple is the built in
# caching mechanism for this module. It also supports
# things like Redis, memcache etc..
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

mysql = MySQL()
mysql.init_app(app)

# End Flask app setup

# The logging configuration below is taken from:
# https://medium.com/@trstringer/logging-flask-and-gunicorn-the-manageable-way-2e6f0b8beb2f
# If we are not in __main__ assume that we are running
# in gunicorn and configure logging accordingly.
log = app.logger

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    # Set the flask log handler to the same as gunicorn
    # for a consistent experience.
    app.logger.handlers = gunicorn_logger.handlers
    # Set the flask logger level to whatever we set the
    # gunicorn logger to.
    app.logger.setLevel(gunicorn_logger.level)
else:
    # If we are being run directly setup console logging
    # and set to DEBUG.
    app.logger.setLevel(logging.DEBUG)
    app.logger.handlers = logging.StreamHandler

# pylint: enable=C0103


def get_handle_for_mac(mac):
    """ For a given mac in XXXXXXXXXXXX format return a string with
        the handle associated with the mac address. In the event
        that we don't find a handle we return a string of dashes.
    """
    # Staff handles will be displayed as STAFF in the leaderboard.
    # TODO: Put this in config?
    staff = ['btm', 'Terry', 'effffn', 'ipl31', 'kencaruso', 'sandinak', 'robotlandman']
    missing_handle = "--------"
    query = "SELECT * FROM handles WHERE `badge_mac`='{0}'".format(mac)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    try:
        result = data[0][2].strip()
    except IndexError:
        result = missing_handle
    if result in staff:
        return "{0} *STAFF".format(result)
    return result


def get_top_ssids():
    """ Return the top 20 ssids in the DB """
    query = ("SELECT ssid, COUNT(ssid) AS popularity FROM entries"
             " GROUP BY ssid ORDER BY popularity DESC limit 20")
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data


def get_top_bssids():
    """ Return the top 20 bssids in the DB """
    query = ("SELECT bssid_mac, COUNT(bssid_mac) AS popularity "
             "FROM entries GROUP BY bssid_mac "
             "ORDER BY popularity DESC limit 20")
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data


def get_total_entries():
    """ Return a count of total rows in the entries table """
    query = " select COUNT(*) from entries"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchone()
    conn.close()
    return data


def get_unique_checkins():
    """ A checkin consists of (among other things) the mac of the sender
        and the mac of the bssid seen. This returns unique badge
        and bssid combos. Essentially we are deduping since badges can
        report the same mac many times."""
    query = ("SELECT badge_mac, bssid_mac FROM "
             "(SELECT DISTINCT badge_mac, bssid_mac FROM entries) "
             "AS internalQuery")
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data


def get_scoreboard_data():
    """ Returns the data used in scoreboard route """
    count = []
    data = get_unique_checkins()
    handles = {}
    for record in data:
        if record[0] not in handles.keys():
            handle = get_handle_for_mac(record[0])
            handles[record[0]] = handle
        if any(record[0] in x for x in count):
            continue
        result = [record[0],
                  sum(x.count(record[0]) for x in data),
                  handles[record[0]]]
        count.append(result)
    tally = {}
    for record in count:
        mac = EUI(record[0])
        # Change the mac to a more display friendly format
        # with a ":" every two characters.
        mac.dialect = mac_unix
        tally[str(mac)] = [record[1], record[2]]
    sorted_tally = sorted(tally.items(), key=operator.itemgetter(1))
    return list(reversed(sorted_tally))


@app.route("/")
@cache.cached(timeout=50)
def main():
    """ The main index/frontpage view of the app."""
    return render_template('index.html')


@app.route("/stats")
# Page rendering is cached for 60 seconds:
@cache.cached(timeout=60)
def stats():
    """ The view we use to display interesting stats """
    bssids = get_top_bssids()
    ssids = get_top_ssids()
    total = get_total_entries()
    return render_template('stats.html', bssids=bssids,
                           ssids=ssids, total=total)


@app.route("/scoreboard")
# Page rendering is cached for 60 seconds:
@cache.cached(timeout=60)
def scoreboard():
    """ The leaderboard displays scores of all contestants """
    scores = get_scoreboard_data()
    leader = scores[0][1][1]
    return render_template('scoresv2.html', leader=leader, scores=scores)


@app.route('/handles/')
def get_handles():
    """ Display a view of all the handles and macs """
    query = "SELECT * FROM handles"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    results = []
    for handle_record in data:
        results.append(handle_record)
    return json.dumps(data)


@app.route('/handle_for_mac/<badge_mac>', methods=['GET'])
def handle_for_mac(badge_mac):
    """ Return a handle for a badge mac address """
    return json.dumps(get_handle_for_mac(badge_mac))


@app.route('/handle/<badge_mac>', methods=['POST'])
def update_handle(badge_mac):
    """ This route creates a new entry for a handle to badge mac
    mapping.
    """
    log.info("update handle for %s", badge_mac)
    request_json = request.get_json()
    insert_template = (u"INSERT INTO handles (badge_mac, handle) "
                       "VALUES('{0}', '{1}')"
                       .format(badge_mac, request_json['handle']))
    update_template = (u"UPDATE handles SET handle = '{1}' WHERE badge_mac = '{0}'"
                       .format(badge_mac, request_json['handle']))
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        cursor.execute(insert_template)
        conn.commit()
        log.debug("Finished a transaction: %s", insert_template)
        return_code = 201
    except IntegrityError as exception:
        if exception[0] == 1062:
            log.info("handle %s: already exists switching to update", badge_mac)
            try:
                cursor.execute(update_template)
                conn.commit()
                log.debug("Finished a transaction")
                return_code = 201
            except Exception as exception:  # pylint: disable=W0703
                log.warn("issue updating handle for %s: %s", badge_mac, exception)
                return_code = 409
        else:
            log.error("badge_mac %s: MySQL ERROR: %s", badge_mac, exception)
            log.error("MySQL ERROR: %s", exception)
            return_code = 500
    else:
        log.info("handle %s: added", badge_mac)
    finally:
        conn.close()
    payload = json.dumps({'warbadging': True})
    content_type = {'ContentType': 'application/json'}
    return payload, return_code, content_type


@app.route("/checkin/<badge_mac>", methods=['POST'])
def checkin(badge_mac):
    """ This is the route clients/badges post to. They
        post to a URL with their MAC in the URL and the
        data in a JSON payload.

        Example payload:

{"TP-LINK_D7D6CA": {"c46e1fd7d6ca": -69}, "shmoocon": {"1864723fac40": -70, "186
4723fa180": -83}, "shmoocon-wpa": {"1864723fa181": -81, "1864723fac41": -69}, "S
L_Workshops": {"6238e0c732d1": -58}, "shmoocon-romp": {"1864723fac42": -71, "186
4723fa182": -83}, "D1721F072848": {"7cdd90e16d99": -86}, "honors-meeting": {"881
dfc9e1340": -68, "189c5dd58a20": -69, "881dfc913080": -79, "8478acdeff20": -59},
"ShmooLabs": {"6038e0c732d1": -66}}
    """

    # Checking the user-agent to grant access to post data is weak at best but
    # the only reasonable thing we could do given the time frame.
    user_agent = request.headers.get('User-Agent')
    if "WarBadge Experimental ShmooCon 2018" not in user_agent:
        log.error("Bad User-Agent: %s", user_agent)
        abort(403)
    insert_template = (u"INSERT INTO entries "
                       "(badge_mac, ssid, bssid_mac, rssi) "
                       "VALUES('{0}', '{1}', '{2}', {3})")

    conn = mysql.connect()
    cursor = conn.cursor()

    try:
        for ssid, entries in request.get_json().iteritems():
            for bssid_mac, rssi in entries.iteritems():
                insert = insert_template.format(badge_mac,
                                                conn.escape_string(ssid),
                                                bssid_mac, rssi)
                cursor.execute(insert)
                conn.commit()
    except NameError as exception:
        log.error("Bad SSID: %s", exception)
        return_code = 403
    # TODO: Find something more specific to catch.
    except Exception as exception:  # pylint: disable=W0703
        log.error("Caught Exception (unicode?) for %s: %s", badge_mac, exception)
        log.error(request.data)
        return_code = 500
    else:
        return_code = 201
        log.info("Successful checkin for %s", badge_mac)
    finally:
        conn.close()
    payload = json.dumps({'warbadging': True})
    content_type = {'ContentType': 'application/json'}
    return payload, return_code, content_type


if __name__ == "__main__":
    log.info("Starting warbadge leaderboard in development mode")
    app.run(host='127.0.0.1')
