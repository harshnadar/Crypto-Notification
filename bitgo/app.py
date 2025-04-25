from flask import Flask, request, jsonify, abort
from uuid import uuid4
from notification_status import NotificationStatus
from email_notification import EmailNotification

app = Flask(__name__)

"""
Notification local memory storage
This is a dictionary that stores the notifications
The key is the notification id and the value is the notification object
The notification object contains the following fields
- id: the unique id of the notification
- notification_data: the data of the notification
        - current_price: the current price of the crypto
        - daily_change_pct: the daily change percentage of the crypto
        - trading_volume: the trading volume of the crypto
- notification_status: the status of the notification
"""
notifications = {}

notifier = EmailNotification()

@app.get('/api/ping')
def ping():
    """Just a healthcheck ping endpoint"""
    return jsonify({'message': 'endpoint working'}), 200


@app.post('/api/notifications')
def create_notification():
    """Create a new notification
    Takes in the data in the request body
    and creates a new notification, with a unique id, status and notification content
    returns the newly created notification object
    """
    data = request.json
    required = {"current_price", "daily_change_pct", "trading_volume"}
    if not data:
        abort(400, "Missing request body")
    if not required.issubset(data):
        abort(400, "Missing required request body")
    notification_body = {
        "id": str(uuid4()),
        "notification_data": data,
        "notification_status": NotificationStatus.PENDING.value
    }
    notifications[notification_body.get("id")] = notification_body
    return jsonify(notification_body), 200


@app.get('/api/notifications')
def get_notifications():
    """
    Retrieve the notifications based on the notification status. 
    if we do not send anything in the status, then simply return all the notifications
    if we send a status, then return the notifications with that status
    """
    status = request.args.get('status')
    response = []
    if not status:
        response = notifications
    else:
        try:
            if int(status) not in [NotificationStatus.FAILED.value, NotificationStatus.PENDING.value, NotificationStatus.SENT.value]:
                abort(400, "incorrect request params")
        except Exception as e:
            abort(400, "invalid request parameters")
        print(status)
        response = [notif for notif in notifications.values() if notif.get("notification_status") == int(status)]
    
    return jsonify(response), 200

    
@app.post('/api/notifications/<notification_id>/send')
def send_notification(notification_id):
    """
    sends notification to the emails 
    emails are sent in the request body in list format
    Once the notifications are sent perfectly fine, we update the notification status to SENT
    """
    notif = notifications[notification_id]
    if notif == {}:
        abort(404, "notification not found")
    data = request.json
    required = {"emails"}
    if not data:
        abort(400, "Missing request body")
    if not required.issubset(data):
        abort(400, "Missing required request body")
    
    response = notifier.send(data)
    if(response == NotificationStatus.SENT.value):
        notifications[notification_id]["notification_status"] = NotificationStatus.SENT.value
        return jsonify({"message": "notification sent successfully"}), 200
    elif(response == NotificationStatus.FAILED.value):
        notifications[notification_id]["notification_status"] = NotificationStatus.FAILED.value
        return jsonify({"message": "failed to send notification"}), 500
    

@app.route('/api/notifications/<notification_id>', methods = ['PUT'])
def update_notification(notification_id):
    """
    Update an existing notification
    If we don't have the notification with that ID, we throw a 404 error
    returns the updated notification object
    """
    notif = notifications.get(notification_id, {})
    if(notif == {}):
        abort(404, "notification not found")
    
    data = request.json
    required = {"current_price", "daily_change_pct", "trading_volume"}

    if not data:
        abort(400, "Missing request body")
    if not required.issubset(data):
        abort(400, "Missing required request body")
    notification_body = {
        "id": notification_id,
        "notification_data": data,
        "notification_status": NotificationStatus.PENDING.value
    }
    notifications[notification_id] = notification_body
    return jsonify(notification_body), 200


@app.route('/api/notifications/<notification_id>', methods = ['DELETE'])
def delete_notification(notification_id):
    """
    Delete an existing notification
    If we don't have the notification with that ID, we throw a 404 error
    returns a success message
    """
    notif = notifications.get(notification_id, {})
    if(notif == {}):
        abort(404, "notification not found")

    del notifications[notification_id]
    return jsonify({'message': "notification deleted successfully"}), 200

    

if __name__ == '__main__':
    app.run(port=8080)