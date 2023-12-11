# Mash-On-Dash
*A data mashup tool to support data processing on the web.*

**Keywords**: *Data processing, workflows, web tool, data mashups, getting data from different sources and formats,
data cleaning, transformations*

**Objective**: Develop a tool to retrieve and facilitate the process of combining data from disparate sources and
services (data mashups).

**Figma Prototype**: https://www.figma.com/file/bbskKWmLnWhFUcr0b7hp36/Material-Dashboard-2-for-MOD?node-id=1224%3A40369

**Figma Prototype PDF**: https://drive.google.com/file/d/1F1JnEXCyL2ACq11VlVQ0748pt7qfV_Qm/view?usp=sharing

### Description
- The tool created is based on the concept of data mashup in which it concerns the use of different data sources and
functionalities to create a new application.   
  

- This tool can be applied in various scenarios where processing and data analysis are useful to facilitate the 
understanding of scope of interest.   
  

- **Solution Architecture**:
    - The execution of data processing is thought of as a task subdivided into stages, where each stage has a well-defined
    responsibility in the process.
    - Each step (just like in data processing), has an input, and a linked output.
    - The order to execution of these steps in processing is established by the end user from a set of available 
      resources (from the solution) allowing a combination of these features and creating a *workflow*.   


- **Packages used**: 
    - *Ntlk* - Processing library of natural language in english text. Used for analysis of the language and data mining.
    - *Tweepy* - Encapsulates the use of Twitter API for data retrieval. For this functionality to work, might need to 
      create twitter access tokens from twitter developer platform.
    - *Flask* - a micro-framework that provides the main features for web development.
    - *Dash framework* - A plotly framework for creating visualisation and interactive web applications.
    - *Beautiful Soup* - Screen scraping.
    - *Celery* - For asynchronous queue management.
    - *Redis* - an open source, in-memory data structure store which is used as a database cache and message broker.
    - *Emoji* - Emoji for python : `pip install emoji --upgrade`.
    - *Npm* - Might need to install npm in your environment (for `gulpfile.js`) using `npm install`.
      

- **Installation instructions (OSX)**:
    - Install all the above mentioned libraries in your virtual environment using `pip` package manager.
      <br>
      <br>
    - *Note* - In case you are facing an error - `ModuleNotFoundError: No module named 'eventlet'`, then run `pip install eventlet`.
      <br>
      <br>
    - Open the terminal inside the project's root directory:<br><br>
      - Command to start redis service: `sudo service redis-server start`. For OSX, please refer to this github gist - 
        https://gist.github.com/tomysmile/1b8a321e7c58499ef9f9441b2faa0aa8
        <br>
        <br>
      - Command to start celery worker: `celery -A workflow_manager.celery_worker.celery worker --loglevel=info -P eventlet`
        <br>
        <br>
      - Command to delete all messages from worker: `celery -A workflow_manager.celery_worker.celery purge -f`
        <br>
        <br>
      - Command to start the web application: `python cli.py`   
  

**Inspirations**: TrendsMap, Zapier, IFTTT, Mentionlytics, Intel mash maker, Karma, Wordpress.

**Forked from** - https://github.com/willsimoes/projeto-final 


