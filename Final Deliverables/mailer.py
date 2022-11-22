from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def sendMailThroughSendGrid(id,reciever,status,agent):
    message = Mail(
        from_email='harikrishnac2002@gmail.com',
        to_emails=reciever,
        subject='Ticket Status Update',
        html_content="Your Ticket ID : "+id+" is "+status+(" by : " if status=="Approved" else " to : ")+agent)
    try:
        sg = SendGridAPIClient('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')
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)
