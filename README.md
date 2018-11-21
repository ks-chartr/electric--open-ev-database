# opendata

The public facing website for people for open transit data in Delhi.


Instructions for setup
------------

- Clone the project

        git clone https://varun_bansal@bitbucket.org/traffickarma/opendata.git
        cd opendata


- Install the project's runtime requirements

    (use of virtualenv is recommended)
    
        virtualenv -p python3.x venv
        pip install -r requirements.txt

- Create .env
 
        cd Opendata
        touch .env
    add following in it.
    
        STATIC_DATA_FILES_URL=<proxy-url>
        REALTIME_DATA_FILE_PATH=<real-data-path>
        SECRET_KEY=<secret-key>
        DEBUG=False


- Migrations

        python manage.py makemigrations
        python manage.py migrate

- To run the server 
    
        python manage.py runserver

- Your blog app is running at 

        localhost:8000

   Open it in any web-browser.
    
- To log into admin panel

        localhost:8000/admin
    You can use your superuser login credentials here.





Issues
------------

Please report any bugs or requests that you have using the GitHub issue tracker!
