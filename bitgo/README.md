# Crypto Notification Service

A HTTP REST API server for crypto price notifications.

## Requirements

- Create a Notification (Input parameters: Current Price of Bitcoin, Daily Percentage Change, Trading Volume, etc)
- Send a notification to email/emails
- List notifications (Sent, Pending, Failed)
- Update/Delete notification

## Assumptions

- First assumption was 'How much scope do i need to target given the time constraints: 1 hour'
- Secondly, Have a global notifications variable which just stores all the notifications
- Third, since we need the notifications to be listed/filtered based on status, so we're assuming not to store the information based on emails
  - Example: a notification can be sent to multiple emails, but can fail for some. We have not segregated status based on emails.
- Considering the basic functionality is demanded, the code has not been made very modular or abstracted.
- A lot of checks could be added (eg: if a notification is sent to one email, can it be sent again, or if the status is already sent, then do we allow to send it again etc etc)
- Error handling could be improved

## Setup Instructions

1. Install the required dependencies and create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Start the server:
```bash
flask run --port=8080
```

## API Endpoints

### Create a Notification
- **URL:** `POST http://localhost:8080/api/notifications`
- **Request Body:**
```json
{
    "current_price": 109288,
    "daily_change_pct": 3999,
    "trading_volume": 10
}
```

### Update a Notification
- **URL:** `PUT http://localhost:8080/api/notifications/{notification_id}`
- **Request Body:**
```json
{
    "current_price": 109288,
    "daily_change_pct": 3999,
    "trading_volume": 10
}
```

### List Notifications
- **URL:** `GET http://localhost:8080/api/notifications`
- **Query Parameters:** 
  - `status` (optional): Filter by status (1=Pending, 2=Sent, 3=Failed)
- **Example:** `GET http://localhost:8080/api/notifications?status=1`

### Delete a Notification
- **URL:** `DELETE http://localhost:8080/api/notifications/{notification_id}`

### Send a Notification
- **URL:** `POST http://localhost:8080/api/notifications/{notification_id}/send`
- **Request Body:**
```json
{
    "emails": ["recipient@example.com"]
}
```
