import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'purrfectpets.settings')

import django
django.setup()
from purrfectpets_project.models import Pet, PetPhoto, Category, Comment
from django.contrib.auth.models import User
from random import randint

def populate():
    users = [               #list of users
        {'user':'Alex', 'email':'apaterson11.ap11@gmail.com', 'password':'password', 'first_name':'Alex', 'last_name':'Paterson'},
        {'user':'Sarah', 'email':'sarah@gmail.com', 'password':'password', 'first_name':'Sarah', 'last_name':'Paterson'},
        {'user':'Andrew', 'email':'andrew@gmail.com', 'password':'password', 'first_name':'Andrew', 'last_name':'Paterson'},
        {'user':'Jake', 'email':'jake@gmail.com', 'password':'password', 'first_name':'Jake', 'last_name':'Paterson'},
        {'user':'Joe', 'email':'joe@gmail.com', 'password':'password', 'first_name':'Joe', 'last_name':'Paterson'},
        {'user':'Beth', 'email':'beth@gmail.com', 'password':'password', 'first_name':'Beth', 'last_name':'Langlands'},
        ]
        
    for user in users:      #adds users
        add_user(user['user'], user['email'],  user['password'], user['first_name'], user['last_name'])
        
    for user in User.objects.all():         #prints users
        print(user)

    #lists of dictionaries of animals
    dogs = [
        {'animalType':'DO', 'name': 'Alex', 'owner': User.objects.get(username='Beth'), 'breed': 'Shih Tzu', 'awwCount':6, 'bio':'This dog belongs to Bradley Cooper.'},
        ]
    cats = [
        {'animalType':'CA', 'name': 'Henry', 'owner': User.objects.get(username='Joe'), 'breed': 'Tabby', 'awwCount':5, 'bio':'Bad cat.'},
        ]
    fish = [
        {'animalType':'FI', 'name': 'Robert', 'owner': User.objects.get(username='Jake'), 'breed': 'Clown Fish', 'awwCount':4, 'bio':'I cannot find him please help me.'},
        ]
    reptiles = [
        {'animalType':'RE', 'name': 'Anna', 'owner': User.objects.get(username='Andrew'), 'breed': 'Horn tailed firewhizzer', 'awwCount':3, 'bio':'Weird.'},
        ]
    rodents = [
        {'animalType':'RO', 'name': 'Ryan', 'owner': User.objects.get(username='Sarah'), 'breed': 'RAT', 'awwCount':2, 'bio':'What a lovely rat.'},
        ]
    other = [
        {'animalType':'OT', 'name': 'Bird', 'owner': User.objects.get(username='Alex'), 'breed': 'Parakeet', 'awwCount':1, 'bio':'Bird.'},
        ]
    
    #list of categories
    cats = {'dogs': {'category': dogs, 'views': 128, 'animalType':'DO'},
            'cats': {'category': cats, 'views': 64, 'animalType':'CA'}, 
            'fish': {'category': fish, 'views': 32, 'animalType':'FI'},
            'reptiles': {'category': reptiles, 'views': 1, 'animalType':'RE'},
            'rodents': {'category': rodents, 'views': 500, 'animalType':'RO'},
            'other': {'category': other, 'views': 0, 'animalType':'OT'},
            }
    
    #the code below goes through the cats dictionary, then adds each dictionary and then adds all associated pages for that category
    
    for cat, cat_data in cats.items():       
        c = add_cat(cat, cat_data['views'], cat_data['animalType'])      
        for p in cat_data['category']:
            add_pet(c, p['animalType'], p['name'], p['owner'], p['breed'], p['awwCount'], p['bio'], users)
            

    # print out the categories we have added
    for c in Category.objects.all():
        for p in Pet.objects.filter(category=c):
            print(f'- {c}: {p}')
    
    #list of comments
    comments = [
        {'commentMaker':User.objects.get(username='Alex'), 'commentAbout':Pet.objects.get(name='Alex'), 'timeDate':'2017-02-14', 'comment':'Nice!'},
        {'commentMaker':User.objects.get(username='Sarah'), 'commentAbout':Pet.objects.get(name='Henry'), 'timeDate':'2020-03-28', 'comment':'Cute dog!'},
        {'commentMaker':User.objects.get(username='Andrew'), 'commentAbout':Pet.objects.get(name='Anna'), 'timeDate':'2016-02-13', 'comment':'Lovely content thanks for sharing.'},
        {'commentMaker':User.objects.get(username='Joe'), 'commentAbout':Pet.objects.get(name='Ryan'), 'timeDate':'2020-02-14', 'comment':'WHere am I?'},
        {'commentMaker':User.objects.get(username='Jake'), 'commentAbout':Pet.objects.get(name='Robert'), 'timeDate':'2020-01-29', 'comment':'AAAAAAAAAAAAAAAAAAAAAAAaa'},
        {'commentMaker':User.objects.get(username='Beth'), 'commentAbout':Pet.objects.get(name='Bird'), 'timeDate':'2018-02-14', 'comment':'haha thanks very cool'},
        ]
        
    for dict in comments:
        add_comment(dict['commentMaker'], dict['commentAbout'], dict['timeDate'], dict['comment']) 
        
    for comment in Comment.objects.all():
        print(comment)
          
    pet_photos = [
        {'pet':Pet.objects.get(name='Alex'), 'img_address': "/static/images/alex.jpg"},
        {'pet':Pet.objects.get(name='Bird'), 'img_address': "/static/images/bird.jpg"},
        {'pet':Pet.objects.get(name='Robert'), 'img_address': "/static/images/robert.jpg"},
        {'pet':Pet.objects.get(name='Ryan'), 'img_address': "/static/images/ryan.jpg"},
        {'pet':Pet.objects.get(name='Henry'), 'img_address': "/static/images/henry.jpg"},
        {'pet':Pet.objects.get(name='Anna'), 'img_address': "/static/images/anna.jpg"},
        ]
        
    #for item in pet_photos:                                            #NOT WORKING
    #    add_pet_photo(item['pet'], item['img_address'])
        
def add_cat(name, views, animalType):
    cat = Category.objects.get_or_create(name=name)[0]
    cat.animalType = animalType
    cat.views = views
    cat.save()
    return cat
    
def add_pet(c, animalType, name, owner, breed, awwCount, bio, users):
    p = Pet.objects.get_or_create(category=c, name=name, owner=owner)[0]
    p.animalType = animalType
    p.breed=breed
    
    names = [li['user'] for li in users]   
    for i in range(0, awwCount):
        sender = User.objects.get(username=names[i])
        p.awwSenders.add(sender)
    
    p.awwSenders.add(owner)
    p.awwCount=awwCount
    p.bio=bio
    p.save()
    return p
    
def add_pet_photo(pet, img_address):
    p_p = PetPhoto.objects.get_or_create(photo=photo)[0]
    p_p.pet=pet
    p_p.save()
    return p_p
    
def add_comment(commentMaker, commentAbout, timeDate, comment):
    com = Comment.objects.get_or_create(comment=comment)[0]
    com.commentMaker=commentMaker
    com.commentAbout=commentAbout
    com.timeDate=timeDate
    com.save()
    return com
    
def add_user(user, email, password, first_name, last_name):
    u = User.objects.create_user(user, email, password)
    u.first_name = first_name
    u.last_name = last_name
    u.save()
    return u
    
if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()