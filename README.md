# roadrunner
Django powered project which acts as Bus and Taxi booking portal for Travel Firm Owners. Fully Restful API for future integration with websites and mobile applications.

## Features
- Bus Management
- Basic Bus seat configuration (user can book seats of their choice like in BookMyShow)
- Bus Ticket Booking
- Driver/Conductor Management
- Taxi Management
- Taxi-Driver Management
- Google Maps API integrated for fair and journey time calculations between cities
- User login/signup/password-reset features for accounts management
- User Authorization using access-tokens
- E-Wallet for bus-ticket/taxi-booking payments with pay-later option

## What this project includes
- Bus application for bus related tasks (bus)
- Taxi application for taxi related tasks (taxi)
- Payment application for e-wallet management (epay)
- Authorization application for user-authorization using tokens (e-auth)
- User accounts application (superuser)
- Centralized application which contains forms for basic testing of all apps

## How to setup roadrunner for development

If you want to contribute to roadrunner by improving the feautures or by testing its features then you'll have to set it up on your machine. Though you can run it globally but i would prefer you do all the development inside `virtualenv` so that it doesn't pollute your global packages.

Follow the steps as they are and you'll be good to use roadrunner

### Installations

1. install `pip`
  1. install python dependencies `sudo apt-get install python-setuptools python-dev build-essential`
  2. install pip `sudo easy_install pip `

2. install `virtualenv` by typing `sudo pip install --upgrade virtualenv`

3. create a _virtual environment_ by typing `virtualenv venv` inside your project directory

4. switch to the _virtual environment_ by typing `source venv/bin/activate` inside your project directory 

5. install the dependencies by running `pip install -r requirements.txt`

6. install mysql
  1. `sudo apt-get update`
  2. `sudo apt-get install mysql-server-5.5`
  

### Steps for setup

1. Clone roadrunner

2. Go to directory where you cloned roadrunner and create a virtual environment by typing `virtualenv roadrunner`

3. Go to roadrunner and activate the environment by typing `source bin/activate`

4. Create database tables by running `python manage.py makemigrations` and then `python manage.py migrate`

5. collect admin static files by running `python manage.py collectstatic`

### Testing the URL's

1. Run the Django's development server using `python manage.py runserver`

2. Open `localhost/admin/` in your browser

3. To exit the _virtual environment_ type `deactivate`

*If you encounter any error during the installation, setup or running the server then please inform about it. If you find some error which is easy to fix then also inform about it so that we can fix it in main code or in the above steps.*
