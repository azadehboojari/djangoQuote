from django.db import models
import re, bcrypt
from datetime import datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9+-_.]+\.[a-zA-Z]+$')

# Create your models here.

class UserManager(models.Manager):
    def register(self, form_data):
        # print("inside of your models!!!", form_data)
        errors = []

        if len(form_data["first_name"]) < 1:
            errors.append("First Name is required")
        elif len(form_data["first_name"]) < 2:
            errors.append("First Name must be 2 letters or longer")

        if len(form_data["last_name"]) < 1:
            errors.append("Last Name is required")
        elif len(form_data["last_name"]) < 2:
            errors.append("Last Name must be 2 letters or longer")

        if len(form_data["email"]) < 1:
            errors.append("Email is required")
        elif not EMAIL_REGEX.match(form_data["email"]):
            errors.append("Invalid Email")
        else:
            if len(User.objects.filter(email=form_data["email"].lower())) > 0:
                errors.append("Email already in use") 

        if len(form_data["password"]) < 1:
            errors.append("Password is required")
        elif len(form_data["password"]) < 8:
            errors.append("Password must be 8 letters or longer")

        if len(form_data["confirm"]) < 1:
            errors.append("Confirm Password is required")
        elif form_data["password"] != form_data["confirm"]:
            errors.append("Confirm Password must match Password")

        if len(form_data["birth_date"]) < 1:
            errors.append("You must enter date of birth!")
        else:
            birthday = datetime.strptime(form_data["birth_date"], "%Y-%m-%d")
            if birthday > datetime.now():
                errors.append("Date of birth is not valid!")
        
        if len(errors) == 0:
            hashed_pw = bcrypt.hashpw(form_data["password"].encode(), bcrypt.gensalt())
            # print(str(hashed_pw))
            user = User.objects.create(
                first_name = form_data["first_name"],
                last_name = form_data["last_name"],
                email = form_data["email"].lower(),
                password = hashed_pw,
                birth_date = form_data['birth_date'],
            )
            return (True, user)
        else:
            return (False, errors)

    def login(self, form_data):

        errors = []

        if len(form_data["email"]) < 1:
            errors.append("Email is required")
        elif not EMAIL_REGEX.match(form_data["email"]):
            errors.append("Invalid Email")
        else:
            if len(User.objects.filter(email=form_data["email"].lower())) < 1:
                errors.append("Unknown email {}".format(form_data["email"])) 

        if len(form_data["password"]) < 1:
            errors.append("Password is required")
        elif len(form_data["password"]) < 8:
            errors.append("Password must be 8 letters or longer")


        if len(errors) > 0:
            return (False, errors)

        user = User.objects.filter(email=form_data["email"].lower())[0]
        hashed_pw = user.password.split("'")[1]

        if bcrypt.checkpw(form_data["password"].encode(), hashed_pw.encode()):
            return (True, user)
        else:
            errors.append("Incorrect password")
            return (False, errors)

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    birth_date=models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

class QuoteManager(models.Manager):
    def q(self, form_data):
        print (form_data)
        errors = []

        if len(form_data['quote']) < 10:
            errors.append("Thats not a quote")
      
        if len(form_data['quoted_by']) < 3:
            errors.append("You need to enter ")

        if len(errors) > 0:
            return (False, errors)

        else:
            quote = Quote.objects.create(
                quote = form_data['quote'],
                quoted_by = form_data['quoted_by'],
                addby_id = form_data['user_id']
            )
            return (True, quote)

class Quote(models.Model):
    quote=models.TextField(max_length=1500)
    quoted_by=models.CharField(max_length=255)
    addby=models.ForeignKey(User, related_name='sth', on_delete=models.CASCADE)

    
    objects=QuoteManager()

class AddManager(models.Manager):
    def add_quote(self, quote_id, adder_id ):
        quote = Quote.objects.get(id=quote_id)
        add_quotes=Add.objects.filter(quote_id=quote_id).filter(user_id=adder_id)
        if len(add_quotes)==0:
            Add.objects.create(quote_id=quote_id, user_id=adder_id)
    

class Add(models.Model):
    user=models.ForeignKey(User, related_name='add', on_delete=models.CASCADE)
    quote=models.ForeignKey(Quote, related_name='add', on_delete=models.CASCADE)

    objects=AddManager()


