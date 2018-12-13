## Serenity
Serenity is a Marist Capping project which provides a readable and intuitive dashboard
as an alternative for viewing a Marist student's degree completion progress.



## Screenshots
<img src="/static/img/serenityLogoScreenshot.png" alt="Serenity Logo" width="300" height="200"/>

## Tech/framework used
<b>Built with</b>
- [Flask](http://flask.pocoo.org)
- [Selenium](https://selenium-python.readthedocs.io)
- [Nginx](https://nginx.org/en/)
- Containerized with [Docker](https://www.docker.com)

## System Flow
Below is a simple diagram describing the overall flow of the application.
<img src="/static/img/serenitySystemFlow.png" alt="Serenity System Flow" width="300" height="250"/>



## Set up for future contributions
In order to get your machine set up for adding to the project the following things must be installed:
1. Regardless on whichever machine you are running on, the latest [Python ](https://www.python.org/downloads/) must be downloaded. Although macOS systems include Python 2.7 out of the box, our web application runs on the latest version of Python.  
2. Pip, a tool for installing and managing Python packages, must be used as our application has several Python-based dependencies. With the latest versions of Python, pip is already installed. Using the following command, "pip3 install [package name]" or "pip3 install [package name] as [alias name]" install the following packages:
    - Flask
    - Pandas
    - re
    - numpy
    - datetime
    - sys
    - beautifulsoup4
    - selenium
3. If utilizing Flask's server in order to run an instance of our web application on a local server on your machine, running the routes file through python will allow you to do so: "python3 routes.py"
4. In order to access the internal Docker configurations, an ssh connection must be established(while on-campus wifi): 'ssh serenity@10.11.12.22'.


## Deployment through Docker
Our service is run through a containerization process done by [Docker](https://www.docker.com). Here are a few points to help facilitate that process.
1. Dockerfile (available in master) are basically used to create *images*, which are called to run *containers* which host your application. Consider the following docker file for our project.
```
FROM tiangolo/uwsgi-nginx-flask:python3.7
EXPOSE 80

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

CMD python main.py
```
2. Line by line:
    - ```FROM``` : calls the image you are basing your image on
    - ```EXPOSE``` : for ports
    - ```COPY``` : to copy current file directory into the images/containers app directory
    - ```WORKDIR``` : to instantiate which directory you start in
    - ```RUN``` : to run shell commands
    - ```CMD``` : as the command to run
3. To build an image based on this Dockerfile, in the same directory run command:
``` sudo docker build -t without- expose:latest .  ```
    - ```-t``` : tag name of image
    - ```without-expose```: is the placeholder, you can put any name you like.
4. To run a container based on any image that you created, or pulled via
    ``` sudo docker pull imagename ```
5. ``` sudo docker run —name CONTAINER_NAME -p##:## IMAGENAME ```
    - Where ```-p``` indicates port number.
    - ```--name``` indicates container name
    - and ```IMAGENAME``` indicates the image(reference *sudo docker image ls* if you forget the image name)
6. This will create a container listed in ```sudo docker ps```
    - Open at whatever port. You should then be able to view your application at 10.11.12.22:PORT # (If it is correctly running)
## FAQ's
- What is serenity?
    - Serenity is a dashboard created by Marist College seniors to give a simpler and more aesthetic degreeworks page for students to follow their progress.
- How does it work?
    - You need to be a currently enrolled student to use this service. While connected to on campus wifi, go to the [Serenity](http://degreasy.capping.ecrl.marist.edu) page and click continue to go to the log-in page.
    - Input your Marist-login credentials (your Marist email account or user name).
    - After a few seconds, it should bring you to our dashboard.
- After logging in with my proper credentials I get a username/password incorrect message: how come?
    - This issue might pop up, and is most likely an internal issue. Try re-loading the webpage with the error message, this might solve it.
- Does Serenity store any user-data?
    - Your data is not saved anywhere in our servers. It is designed to eliminate your credentials as soon as the application uses it to scrape your data, and the dashboard data is locally rendered and disappears when you end the session.
- Can I save my Serenity dashboard?
    - Absolutely! In the dashboard on the top right hand corner, a "Save as PDF" button will appear to allow you to save the dashboard information.
- Why was Serenity created?
    - Serenity was created in order to help students understand their degree progress without wading through a complicated degreeworks page as a quick glance.
- Is this open source?
    - It is open source free software and will always be free and accessible to Marist Students.


## Credits
* Project Manager: Natnael Mengistu
* IT Lead: Phaelan Koock
* Software Developers: Gary Coltrane, Alexa Layosa Javellana, Ariel Camilo


## License
Copyright 2018

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
