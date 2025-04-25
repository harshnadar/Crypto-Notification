Create a crypto notification service as an HTTP Rest API server

##Requirements
- Create a Notification (Input parameters: Current Price of Bitcoin, Daily Percentage Change, Trading Volume, etc)
- Send a notification to email/emails
- List notifications (Sent, Pending, Failed)
- Update/Delete notification

##Assumptions
- First assumption was 'How much scope do i need to target given the time constraints: 1 hour'
- Secondly, Have a global notifications variable which just stores all the notifications
- Third, since we need the notifications to be listed/filtered based on status, so we're assuming not to store the information based on emails
eg: a notification nf can be sent to multiple emails, but can fail for some. We have not segregated status based on emails.
- Considering the basic functionality is demanded, the code has not been made very modular or abstracted.
- A lot of checks could be added (eg: if a notification is sent to one email, can it be sent again, or if the status is already sent, then do we allow to send it again etc etc)
- Error handling could be improved


##Instructions to run
- Install the required dependencies and create a virtual environment
    ```bash
        python -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt
    ``` 
- ```bash
    flask run --port=8080
    ```

##Local Endpoints
- CREATE A NOTIFICATION
    POST http://localhost:8080/api/notifications
    request body: 
    {
        "current_price": 109288, 
        "daily_change_pct": 3999,
        "trading_volume": 10
    }
- UPDATE A NOTIFICATION
    PUT http://localhost:8080/api/notifications/:notification_id
    request body: 
    {
        "current_price": 109288, 
        "daily_change_pct": 3999,
        "trading_volume": 10
    }

- List Notifications
    GET http://localhost:8080/api/notifications?status=1
    available status values: 1 or 2 or 3

- DELETE a notification
    DELETE http://localhost:8080/api/notifications/:notification_id

- SEND a notification
    POST http://localhost:8080/api/notifications/:notification_id



