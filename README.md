1.0	INTRODUCTION
1.1	Purpose
Described the software development process for my second application activity for this course, specifically an inventory application.

1.2	Scope
The second application activity required a web-based Django application with the following features:
•	Admin controlled inventory management tool
•	Hosted on AWS
•	Include Topic, Comments
•	Connected to Relational Database Service
•	Application Load Balancing/Auto-Scaling
•	CDN (Cloudfront)
•	Static Storage

1.3	Overview
This document will focus on Component Design, Architecture and Deployment per the assignment instructions.  


1.4	Definitions and Acronyms
This section is optional. 
VPC = Virtual Private Cloud
RDS = Relational Database Service
S3 – Simple Storage Service
ASG – Auto Scaling Group
CDN – Content Delivery Network


2.0	SYSTEM OVERVIEW

•	Django Application – provides the inventory application and provides an admin tool.
•	Gunicorn – runs the application, turns http request into Python call and coordinates with Nginx 
•	Nginx  - web server, reverse proxy on Ports (80 or 443) serving my static files
•	RDS (MySQL) – hosts backend data
•	Cloudfront provides front end service


3.0	SYSTEM ARCHITECTURE

•	Django Application – provides the inventory, facilitating the html
•	Gunicorn – runs the application, turns http request into Python call and coordinates with Nginx 
•	Nginx  - web server, reverse proxy on Ports (80 or 443) serving my static files

3.1	Architectural Design











As noted in the system architecture, the presentation layer will be served by Nginx and Gunicorn which pull from the application (Django App).  AWS will serve the users via a DNS router, cloudfront and load balancer that will deliver the services from the EC2 instance that sits inside of the Auto Scaling Group (ASG).  MsSQL will store the user data, i.e. comments and topics that are entered in via the html front and processed by the application.


3.2	Decomposition Description

DNS router/load balancer route requests to the web application that provides the “logic” for the inventory application. The web application interprets the module inputs (models.py), i.e. topics and comments. Views.py provides instructions for the product list and searches. Django admin allows for managing users, and provides top level control over the content. 

3.3	Design Rationale
EC2 is requirement for hosting our applications. I previously tried to use beanstalk with application 1 (blog) and found that SSH push to EC2 and manual activation of services was easier. Django’s built in interface and python foundation make is an easy choice for web-apps.


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
