from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response as Resp
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from prep.models import Tag, Question, Response, UserTheta
import random
import math
from prep.excel2 import Extract, Dump
import json
from prep.kola import Evaluate


def add_tag(name, link):
    if Tag.objects.filter(name=name, link=link).exists():
        c = Tag.objects.filter(name=name, link=link)[0]
    else:
        try:
            t_id = int(Tag.objects.latest('id').t_id) + 1
        except Exception as e:
            t_id = 1
        c = Tag.objects.create(t_id=t_id, name=name, link=link)
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


def index(request):
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(username=email).exists():
            main_user = User.objects.filter(username=email)[0]
        else:
            main_user = User.objects.create_user(username=email, email=email, password=None)
        ques_file = request.FILES['ques_file']
        relation_file = request.FILES['relation_file']
        tag_plan = Dump.dump(relation_file)
        data = Extract.extract(ques_file)
        datalen = len(data)
        peoplelen = int(datalen/10)
        for i in data:
            responselist = list()
            for k in range(0,peoplelen):
                if User.objects.filter(username='test'+str(k)+'@gmail.com').exists():
                    user = User.objects.filter(username='test'+str(k)+'@gmail.com')[0]
                else:
                    user = User.objects.create_user(username='test'+str(k)+'@gmail.com',email='test'+str(k)+'@gmail.com',
                                                password=None)
                boolval = bool(random.getrandbits(1))
                responselist.append({'user':user.email, 'response':boolval})
            i['response'] = responselist
        data = data
        for i in data:
            tag = add_tag(i['tag'], i['tag_link'])
            try:
                ques = add_question(i['text'], i['difficulty'], i['discrimination'], tag)
                for k in i['response']:
                    res = add_response(ques, k['response'], User.objects.filter(username=k['user'])[0])
            except Exception as e:
                pass
        return render(request, 'prep/index.html',{'data':json.dumps(data), 'tag_plan':tag_plan,'main_user':main_user.email})
    else:
        return render(request, 'prep/index.html', {})


class UserData(APIView):
    permission_classes = (AllowAny,)

    def get(self,request):
        try:
            user = User.objects.filter(username='test@gmail.com')[0]
        except Exception as e:
            user = User.objects.create_user(username='test@gmail.com',email='test@gmail.com',password=None)
        tags = Tag.objects.all()

        def evaluate():
            user_list = []
            for tag in tags:
                if UserTheta.objects.filter(user=user, tag=tag).exists():
                    theta = UserTheta.objects.filter(user=user, tag=tag)[0].theta
                    questions_tag = theta.questions.all()
                else:
                    theta = 1
                    questions_tag = None
                ques1_list = Question.objects.filter(tag=tag, b__range=[theta - 1, theta])
                if len(ques1_list) == 0:
                    ques1_list = Question.objects.filter(tag=tag, b__range=[math.floor(theta) - 1, math.floor(theta)])
                ques1 = ques1_list[random.randrange(0, len(ques1_list))]
                if questions_tag is not None:
                    jm = 0
                    while jm < len(questions_tag) - 1:
                        jm = 0
                        for qt in questions_tag:
                            if qt.q_id == ques1.q_id:
                                ques1 = ques1_list[random.randrange(0, len(ques1_list))]
                                break
                            jm = jm + 1
                ques2_list = Question.objects.filter(tag=tag, b__range=[theta, theta + 1])
                if len(ques2_list) == 0:
                    ques2_list = Question.objects.filter(tag=tag, b_range=[math.floor(theta), math.floor(theta) + 1])
                ques2 = ques2_list[random.randrange(0, len(ques2_list))]
                if questions_tag is not None:
                    jm = 0
                    while jm < len(questions_tag) - 1:
                        jm = 0
                        for qt in questions_tag:
                            if qt.q_id == ques2.q_id:
                                ques2 = ques2_list[random.randrange(0, len(ques2_list))]
                                break
                            jm = jm + 1
                diff_dif = abs(ques1.b) - abs(ques2.b)
                ques3 = Question.objects.filter(tag=tag, b__lte=theta+diff_dif).order_by('-b')[0]
                j = 1
                while ques3.b == ques1.b or ques3.b == ques2.b:
                    ques3 = Question.objects.filter(tag=tag, b__lte=theta + diff_dif).order_by('-b')[j]
                    j = j + 1
                if questions_tag is not None:
                    jm = 0
                    while jm < len(questions_tag) - 1:
                        jm = 0
                        for qt in questions_tag:
                            if qt.q_id == ques3.q_id:
                                diff_dif = abs(ques1.b) - abs(ques2.b)
                                ques3 = Question.objects.filter(tag=tag, b__lte=theta + diff_dif).order_by('-b')[0]
                                j = 1
                                while ques3.b == ques1.b or ques3.b == ques2.b:
                                    ques3 = Question.objects.filter(tag=tag, b__lte=theta + diff_dif).order_by('-b')[j]
                                    j = j + 1
                                break
                            jm = jm + 1
                ques_list = [ques1, ques2, ques3]
                for ques in ques_list:
                    res = add_response(ques, bool(random.getrandbits(1)), user)
                    user_list.append({'q_id':ques.q_id, 'a':ques.a, 'b':ques.b, 't_id':ques.tag.t_id, 'u':res.res})
            theta_list = list()
            for ut in UserTheta.objects.filter(user=user):
                theta_list.append({'t_id':ut.tag.t_id,'theta':ut.theta})
            batch1_thetas = Evaluate.logistic_model(user_list, theta_list)
            for bt in batch1_thetas:
                ut = UserTheta.objects.create(theta=bt['theta'],user=user,tag=Tag.objects.filter(bt['t_id'])[0])
                for q in user_list:
                    ut.questions.add(Question.objects.filter(q_id=q['q_id']))
                    ut.save()
            return [user_list,theta_list]
        batch1 = evaluate()
        batch2 = evaluate()
        return Resp({'batch1':batch1, 'batch2':batch2})
