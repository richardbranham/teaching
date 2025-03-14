## System setup for CIST1220 midterm

### Overview
This document describes the necessary preparations to student computers for the CIST1220 midterm project. The steps below will enable you to create and execute SQL queries to meet the project requirements. **These steps have been tested on Windows.  The exact actions will vary slightly for macOS but the general steps are the same.**

### Prepare your computer for the CIST1220 midterm project.

#### 1. Copy the project files to your machine
Unzip midterm project files to your desired working directory.

#### 2. Install Python 3
It should be installable using the built-in software or package manager on your computer.  It is available in Microsoft Store, for example.  If a direct download and install is needed, Python 3 downloads are at this link:
https://www.python.org/downloads/

- Confirm that there are no errors with the installation.  
- Open a command window
    - On Windows click Start and then type "cmd", then press Enter.
- In the command window, change directory to the location where you unzipped the midterm project files.
- In the command window, run this command to confirm the Python version:
    `python -V`
- The latest version is 3.13, but any version greater than 3.10 should be ok.

#### 3. Install the Flask web framework using pip
- Execute the following command in the command window.
    `pip install flask`

#### 4. At this point your Python installation should be ready to go.

#### 5. SQLite3
- The necessary SQLite files for Windows are included in the project zip file and no further action related to SQLite should be needed.  
- For macOS it may be necessary to install SQLite using the usual procedure for installing software.
- For reference, the SQLite download page is linked here: https://www.sqlite.org/download.html

#### 6. Start the web server
- From the same command line, run:  
    `python web_server.py`
- It should not be necessary to change firewall rules to allow the web server to run.  Click "Cancel" if a prompt requesting firewall changes appears.
- After the server starts, a warning will be displayed in the command window indicating that this is a development server and it should not be used in production.  This error can be ignored.
- The command window should show output similar to this: 
\* Serving Flask app 'web_server'
\* Debug mode: off
\* WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
\* Running on all addresses (0.0.0.0)
\* Running on http://localhost:5000
\* Running on http://127.0.0.1:5000
\* Running on http://192.168.1.162:5000
\* Press CTRL+C to quit

#### 7. Load the project web page
- Open a browser and navigate to one of the "Running on http" locations from the previous step.  
    - Using the one for localhost will be easiest, although the others should also work.
    - localhost is the same as 127.0.0.1 but is easier to remember.  Any time 127.0.0.1 is working, localhost will also work.
    - Only 1 of these locations needs to be opened in the browser.  The locations will be similar to the "Running" examples in step 6.
