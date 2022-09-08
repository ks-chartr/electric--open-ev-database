# opendata

The public facing website for people for open transit data in Delhi.


Instructions for setup
------------

- Clone the project

        git https://gitlab.com/chartrmobility/electric/open-ev-database.git
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
        
        # postgreSQL config
        DB_NAME=<db-name>
        DB_USER=<db-user>
        DB_PASSWORD=<user-pwd>
        DB_HOST=<db-host-ip>
        DB_PORT=<db-port>


- Static data file for download 
        copy excel/ csv file in 'static/assets'
        
- Migrations

        python manage.py makemigrations
        python manage.py migrate

- To run the server 
    
        python manage.py runserver

- Your app is running at 

        localhost:8000

   Open it in any web-browser.
    
- To log into admin panel

        localhost:8000/admin
    You can use your superuser login credentials here.





Issues
------------

Please report any bugs or requests that you have using the GitHub issue tracker!
