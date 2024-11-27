

Welcome to Advanced E-Commerce API: A python Flask, SqlAlchemy API project by Grant Copeland


First, you need to clone down the project using this command here:

    git clone git@github.com:gcland/Advanced_E-Commerce_API-Mod13-Mini-Project.git

Next, enter the following commands into the terminal:

    python3 -m venv myenv
    source myenv/bin/activate
    pip install flask sqlalchemy flask-sqlalchemy flask-marshmallow marshmallow-sqlalchemy mysql-connector-python

Then, make sure your interpretter is in the virtual environment we just created:

> cmd + shift + p (mac)
> 	-> select virtual environment 

This project uses MySQL and Postman to operate the functions.
Start MySQL and enter the following command:

    CREATE DATABASE e-commerce_db;

This will create the database used within the python file.

Next, open the project folder. Within the 'password.py' file, enter your MySQL password. Save the file. 

Lastly, you will need to open Postman and create the requests. 
The navigate to the 'app.py' file, navigagte to the 'routes' folder. Create the endpoints for customerAccounts, customers, orders, and products as noted within each file of this folder. Example:
'customerAccountBP.py' has 'customerAccount_blueprint.route('/login', methods=['POST'])(login)' The url for this is 'http://127.0.0.1:5000/customerAccounts/login' and the method is "POST" .

For each request, select the appropriate method (GET/POST/PUT/DEL) per the endpoint. Then copy the url from the python code into the request URL.
Once all of the requests are set up per their respective endpoints, the project is ready to run.

Begin by navigating to the 'app.py' file and run the file. 

For a eye-friendly way to view the summary of each endpoint, view the project documentation created with swaggerUI:
http://127.0.0.1:5000/api/docs/#/

From here you will want to log in as an admin. Navigate to the login endpoint under the customerAccount model in postman. Enter the following information into the text body with the 'raw' radio-button selected:

{
    "username":"csA",
    "password":"passwordA"
}

This customerAccount has been initialized as the admin and will grant access to the all endpoints. 
On running this endpoint, the system will output an auth_token. Copy this auth_token. On any endpoint you wish to use, navigate to the 'Authorization' tab under the header of that endpoint. Under the select menu under 'Auth Type',
select 'Bearer Token'. The input on the right side of the screen will allow you to paste your auth_token. You should now be able to send the request as an admin with the required access. 

Please view the documentation listed above for more detailo f the documentation endpoints.

Available endpoints:

Customer - Get customers, add customers, update customers, delete customers, view customer by id
CustomerAccount - Login (generate auth_token), get customerAccounts, add customerAccount, updateCustomerAccount, delete customerAccount, view customerAccount by id
Product - Paginate view products, get products, add products, update products, delete products, view product by id
Order - Paginate view orders, get all orders by one customer, get orders, add orders, update orders, delete orders, view order by id

Thank you for viewing this project! 

- Grant Copeland


