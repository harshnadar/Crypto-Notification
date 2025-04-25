from i_notification import INotification
from notification_status import NotificationStatus

class EmailNotification(INotification):
    def __init__(self):
        pass

    def send(self, notification):
        try:
            msg = {
                "subject": "Crypto Notifications",
                "sender": "harsh",
                "recipients": notification["emails"]
            }
            print("SENDING EMAIL ", msg)
            return NotificationStatus.SENT.value
        except Exception as e:
            print("FAILED TO SEND EMAIL ", e)
            return NotificationStatus.FAILED.value


    
