from server import app
#"python run.py" on terminal to run the app
#terminal must point to "backend" directory
#http://localhost:5000/

#admin@bank.com
#25e1aa3a944800e28879e6890e8f6dc0

#to create the database type in the terminal:
#python
#from server import app, db
#app.app_context().push()
#db.create_all()

#to add entry to the database using terminal:
#python
#from server import app, db
#from server.models import Bot
#app.app_context().push()
#bot = Bot(name="Sunum Botu", price=25, info="Proje sunumu için hazırlanmış bot.")
#db.session.add(bot)
#db.session.commit()

#to view the database:
#https://inloop.github.io/sqlite-viewer/

#to install required libraries for this project
#pip install -r requirements.txt

#pip freeze > requirements.txt

#to view the bots transactions:
#https://testnet.binancefuture.com





if __name__ == '__main__':
    app.run(debug=False)