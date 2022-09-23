import asyncio
from email.message import EmailMessage
import smtplib
import ssl
from prisma.models import Enquiry, User
import prisma
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time


def getData():
  # Gets all enquiries from the database
  async def find_all_enquiries():
      db = prisma.Prisma(auto_register=True)
      await db.connect()
      
      enquiry = await Enquiry.prisma().find_many(include={"user": True})
      return enquiry
  
  numOfAssignment = 0
  numOfConcession = 0

  numOfTCRecieved = 0
  numOfTCApproved = 0

  numOfAERecieved = 0
  numOfAEApproved = 0


  x = asyncio.run(find_all_enquiries())

  waiverDict = {}

  for enq in x:
      if enq.status == "Recieved" and enq.type == "AssignmentExtension":
          numOfAERecieved += 1
          numOfAssignment += 1
      elif enq.status == "Approved" and enq.type == "AssignmentExtension":
          waiverDict[enq.user.uctId] = "Assignment Extension"
          numOfAEApproved +=1
          numOfAssignment +=1
      elif enq.status == "Recieved" and enq.type == "TestConcession":
          numOfTCRecieved += 1
          numOfConcession += 1
      elif enq.status == "Approved" and enq.type == "TestConcession":
          waiverDict[enq.user.uctId] = "Test Concession"
          numOfTCApproved +=1
          numOfConcession +=1

  waiverString = ""

  for x in waiverDict:
      waiverString += "Student Number: " + str(x) + "  Assesment Type: " + str(waiverDict[x]) +  "<br> <br>"
  
  return [waiverString,numOfAERecieved, numOfTCRecieved]
    
def sendSummary(waiverString, numOfAERecieved, numOfTCRecieved, endOfMonth):
  # Define the HTML document
  # Sets up the email addresses and password.
  smtp_server = "smtp.gmail.com"
  sender_email = "capstonefinalproj@gmail.com"
  receiver_email = "dikatsoreaobaka@gmail.com"
  password = "lrxloxslxekocffo" 
  subject =" CS2ADMIN UPDATE"
  
  if endOfMonth == True:
    html = """
        <html>
            <div style="width: 100%; background-color: #f3f9ff; padding: 5rem 0">
            <div style="max-width: 700px; background-color: white; margin: 0 auto">
              <div style="width: 100%; background-color: white; padding: 20px 0">
              <a href="${process.env.CLIENT_URL}" ><img
                  src="https://projects.cs.uct.ac.za/honsproj/cgi-bin/view/2020/daniels_moeng_reay.zip/MORPH_SEGMENT/images/logo_computer_science.png"
                  style="width: 100%; height: 70px; object-fit: contain"
                /></a> 
              
              </div>
              <div style="width: 100%; gap: 10px; padding: 30px 0; display: grid">
                <p style="font-weight: 800; font-size: 1.2rem; padding: 0 30px">
                  CS2ADMIN
                </p>
                <div style="font-size: .8rem; margin: 0 30px">
                  <p>Hi Sonia :)</p>
                  <p><b>Here is your weekly summary update: <b></p>
                  <p>Number of unreviewed Assignment Extension requests: <b> """ + str(numOfAERecieved) + """ </b> </p>
                  <p>Number of unreviewed Test Concession requests: <b>""" + str(numOfTCRecieved) + """</b></p>
                  <p><b>List of waivers: <b><br> <br></p>
                  <p>""" + str(waiverString) + """</p>
                  <p>Kind Regards <br>CS2ADMIN</p>
                </div>
              </div>
            </div>
          </div>
        </html>
        """
        
  else:
    html = """
        <html>
            <div style="width: 100%; background-color: #f3f9ff; padding: 5rem 0">
            <div style="max-width: 700px; background-color: white; margin: 0 auto">
              <div style="width: 100%; background-color: white; padding: 20px 0">
              <a href="${process.env.CLIENT_URL}" ><img
                  src="https://projects.cs.uct.ac.za/honsproj/cgi-bin/view/2020/daniels_moeng_reay.zip/MORPH_SEGMENT/images/logo_computer_science.png"
                  style="width: 100%; height: 70px; object-fit: contain"
                /></a> 
              
              </div>
              <div style="width: 100%; gap: 10px; padding: 30px 0; display: grid">
                <p style="font-weight: 800; font-size: 1.2rem; padding: 0 30px">
                  CS2ADMIN
                </p>
                <div style="font-size: .8rem; margin: 0 30px">
                  <p>Hi Sonia :)</p>
                  <p>Here is your weekly summary update:</p>
                  <p>Number of unreviewed Assignment Extension requests: <b> """ + str(numOfAERecieved) + """ </b> </p>
                  <p>Number of unreviewed Test Concession requests: <b>""" + str(numOfTCRecieved) + """</b></p>
                  <p>Kind Regards <br>CS2ADMIN</p>
                </div>
              </div>
            </div>
          </div>
        </html>
        """
      
    

  # Create a MIMEMultipart class, and set up the From, To, Subject fields
  email_message = MIMEMultipart()
  email_message['From'] = sender_email
  email_message['To'] = receiver_email
  email_message['Subject'] = 'CS2ADMIN UPDATE'


  # Attach the html doc defined earlier, as a MIMEText html content type to the MIME message
  email_message.attach(MIMEText(html, "html"))
  
  # Convert it as a string
  email_string = email_message.as_string()

  # Connect to the Gmail SMTP server and Send Email
  context = ssl.create_default_context()
  with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
      server.login(sender_email, password)
      server.sendmail(sender_email, receiver_email, email_string)
      
def main():
  # Main function gets data from the database and sends weekly summary emails 
  # and a summary email along with a list of waivers at the end of the term
  dataList = getData()
  sendSummary(dataList[0], dataList[1], dataList[2], True)
  
  while True:
    for i in range(12):
      dataList = getData()
      sendSummary(dataList[0], dataList[1], dataList[2], False)
      time.sleep(604800)
    
    dataList = getData()
    sendSummary(dataList[0], dataList[1], dataList[2], True)
    
main()