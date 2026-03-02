1.0	INTRODUCTION
1.1	Purpose
Described the software development process for my fourth application activity for this course, specifically an inventory application.

1.2	Scope
The fourth application activity requires the addition of OAuth to my web-based Django inventory application with the following features:
•	Admin controlled inventory management tool
•	Hosted on AWS
•	Include Topic, Comments
•	Connected to Relational Database Service
•	Application Load Balancing/Auto-Scaling
•	CDN (Cloudfront)
•	OAUTH / OIDC Authentication
•	Static Storage

1.3	Overview
This document will cover Component Design, Architecture and Deployment as noted in our instructions.


1.4	Definitions and Acronyms
This section is optional. 
VPC = Virtual Private Cloud
RDS = Relational Database Service
S3 – Simple Storage Service
ASG – Auto Scaling Group
CDN – Content Delivery Network
OIDC – Open ID Connect


2.0	SYSTEM OVERVIEW

•	Django Application – provides the inventory application and provides an admin tool.
•	Gunicorn – runs the application, turns http request into Python call and coordinates with Nginx 
•	Nginx  - web server, reverse proxy on Ports (80 or 443) serving my static files
•	RDS (MySQL) – hosts backend data
•	Cloudfront provides front end service
•	ALB - 


3.0	SYSTEM ARCHITECTURE

•	Django Application – provides the inventory, facilitating the html
•	Gunicorn – runs the application, turns http request into Python call and coordinates with Nginx 
•	Nginx  - web server, reverse proxy on Ports (80 or 443) serving my static files

3.1	Architectural Design











Previous notes from app 2: “As noted in the system architecture, the presentation layer will be 
served by Nginx and Gunicorn which pull from the application (Django App).  AWS will serve the users via a DNS router, cloudfront and load balancer that will deliver the services from the EC2 instance that sits inside of the Auto Scaling Group (ASG).  MsSQL will store the user data, i.e. comments and topics that are entered in via the html front and processed by the application.”

  Now when a user requests a protected page:
  1. Django redirects the browser to the Cognito Hosted UI
     (inventory-kunnas.auth.us-east-1.amazoncognito.com)
  2. The user authenticates with Cognito
  3. Cognito redirects back to /callback on the CloudFront domain
  4. Django's /callback route forwards the request to allauth
  5. allauth exchanges the authorization code for tokens at Cognito
  6. allauth validates the ID token and creates or updates the Django user
  7. The user is redirected to /inventory/


3.2	Decomposition Description

Previous app 2 description, “DNS router/load balancer route requests to the web application that provides the “logic” for the inventory application. The web application interprets the module inputs (models.py), i.e. topics and comments. Views.py provides instructions for the product list and searches. Django admin allows for managing users, and provides top level control over the content.”

Now my cognito user pool manages my user accounts and validates credentials. It provides an OIDC endpoint to authorize the user, token and endpoint. This is done confidentially with the authorization code grant, openID, email and profile. 

3.3	Design Rationale
Previous app 2 description, ,”EC2 is requirement for hosting our applications. I previously tried to use beanstalk with application 1 (blog) and found that SSH push to EC2 and manual activation of services was easier. Django’s built in interface and python foundation make is an easy choice for web-apps.”
I chose cognito because it was the OAUTH service offered by AWS the platform we are using for these assignments.


4.0	DATA DESIGN

4.1	Data Description
Data included user information, topics and comments, date entries etc… hosted in in the MySQL database. 

4.2	Data Dictionary
Department Number: Unique integer 
Department Name: character string input for the department
Product ID: unique value
Product Name: character string input for the product name
Product Number: unique integer
Product Date: date added 


5.0	COMPONENT DESIGN AND SUPPORTING CODE

 



https://github.com/Kunnaspe/InventoryProject/ – Github REPO

 
# models for departments


# models for products
 

## Activity 3 builds on this previous component design and adds OAUTH / OIDC (OpenID Connect). This app now uses an AWS Cognito login page which returns the users to the application page after successful authentication.”   


6.0	HUMAN INTERFACE DESIGN

6.1	Overview of User Interface

Very basic functionality with the core features matching the application requirements.

6.2	Screenshots
User interface as rendered via AWS. 





# admin view




Django Admin View








Department Entry View






 
Group, User, Department and Product Management 
 
 
## Required code change ISO of cognito

 
 

##Apps updated
### complete code updated in github
 
# Product View

6.3	Screen Objects and Actions

 

Search Feature
7.0 TOOLS, SERVICES, INFRASTRUCTURE, AND CODE   DEPLOYMENTS    
EC2: See screenshot. Runs the Django Inventory Application
Security: Group Policies: inbound / outbound rules for connections
RDS (MariaDb/MySQL): See Screenshot. Hosts the product data
Cloudfront: Distribution 
Gunicorn: WSGI Server
Nginx: Proxy 
Github: Code Repository for Deployment
Cognito User Pool: created using the AWS console wizard. Configured with and OpenID, and email. Callback URL: https://d10al5xqkgu4pk.cloudfront.net/callback.

     8.0    INFRASTRUCTURE CODE SCREENSHOTS AND VALIDATION 
 
## Cognito Login
 
## Sign-up page
 

 
## Cognito User Pool

 
## Cloud front Distrubtion


EC instance with URL/Public IP


Group policies with inbound / outbound rules enabling access to the SSH, database and public IP space.

My database (MariadDB engine – MySQL)
 

 
Auto scaling groups
 
 
Network usage
	


     9.0     CODE REFERENCES
See references. Also took integrated app feedback (VS) that noticed bug issues.
    10.0 SECURITY ISSUES AND VULNERABILITIES
Because of “disallowed hosts” issue I temporarily raised the risk by indicating “*” for allowed hosts. I fixed this later… I controlled access through my inbound / outbound rules;


     11.0 PRIVILEGED ACCESS AND ACCESS CONTROL LISTING
N/A

     12.0 APPENDICES 
This section is optional.

Appendices provide supporting details to aid in the understanding of the Software Design Document.
  13.0 REFERENCES 


AWS. Elastic Beanstalk deployment demonstrations. 
https://www.youtube.com/@amazonwebservices

AWS Deployment Guides,Geeks for Geeks,  Django on AWS EC2.
https://www.geeksforgeeks.org/python/how-to-deploy-django-application-in-aws-ec2/
#AWS – EC2 – Django guide

Codemy.com. Django Blog Tutorial Series. 
https://www.youtube.com/@Codemycom
# basic Django coding blog

Codemy.com. Deploy Django to AWS Elastic Beanstalk. 
https://www.youtube.com/watch?v=G26Prg-rXSY

Hankehly.  Elastic Beanstalk custom Django deployment example. 
https://github.com/hankehly/ebcustom

TestDriven.io. Django Elastic Beanstalk example application. 
https://github.com/testdrivenio/django-elastic-beanstalk
# Django – beanstalk repo.

Skydread1. Django blog deployed on AWS Elastic Beanstalk. 
https://github.com/skydread1/blog
# Django blog with AWS services, RDS and S3.

PragatiDev. Django Blog application. 
https://github.com/pragatidev/DjangoBlog
# Django blog implementation, baseline.

GeeksforGeeks - Django on AWS EC2
https://www.geeksforgeeks.org/python/how-to-deploy-django-application-in-aws-ec2/

