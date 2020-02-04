import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sprep.settings')

import django
django.setup()

import hashlib
import time

from datetime import datetime
from prep.models import Tag, Question, Response
from django.contrib.auth.models import User
from collections import OrderedDict
import random

def populate():
    def add_tag(name):
        if Tag.objects.filter(name=name).exists():
            c = Tag.objects.filter(name=name)[0]
        else:
            try:
                t_id = int(Tag.objects.latest('id').t_id) + 1
            except Exception as e:
                t_id = 1
            c = Tag.objects.create(t_id=t_id, name=name)
        return c


    def add_question(text, b, a, tag):
        if Question.objects.filter(text=text, b=b, a=a).exists():
            c = Question.objects.filter(text=text, b=b, a=a)[0]
        else:
            try:
                q_id = int(Question.objects.latest('id').q_id) + 1
            except Exception as e:
                q_id = 1
            c = Question.objects.create(q_id=q_id, text=text, b=b, a=a, tag=tag)
        return c


    def add_response(ques, res, user):
        if Response.objects.filter(ques=ques, res=res, user=user).exists():
            c = Response.objects.filter(ques=ques, res=res, user=user)[0]
        else:
            hash = hashlib.sha1()
            hash.update(str(time.time()).encode('utf-8'))
            r_id = hash.hexdigest()[:32]
            while Response.objects.filter(r_id=r_id).exists():
                hash = hashlib.sha1()
                hash.update(str(time.time() + 1).encode('utf-8'))
                r_id = hash.hexdigest()[:32]
            c = Response.objects.create(r_id=r_id, ques=ques, res=res, user=user)
        return c


    def add_user(email):
        if User.objects.filter(username=email).exists():
            c = User.objects.filter(username=email)[0]
        else:
            c = User.objects.create_user(username=email, email=email, password=None)
        return c


    user1 = add_user('test@gmail.com')

    for t in range(0,5):
        u = t + 1
        tag = add_tag('Tag'+str(u))
        for i in range(0,6):
            j = i + 1
            b = random.randrange((-3+i)*10, (-2+i)*10)/10
            a = random.randrange(0, 30)/10
            ques = add_question('Ques'+str(u)+'_'+str(j), b, a, tag)
            res = bool(random.getrandbits(1))
            add_response(ques, res, user1)


# Start execution here!
if __name__ == '__main__':
    print("Starting population script...")
    populate()
    print("Completed!")
