# ################################## I M P O R T S ############################################################

from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth import logout,authenticate
from django.contrib.auth.models import User
import uuid
from .models import Question,Answer,Like
# ################################## I M P O R T S ############################################################

#          V I E W S  S T A R T S  H E R E

# user registration method
def signup(request):
    # if request.session.get('user_id'):
        if request.method == 'POST':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            password = request.POST['password']
            existing_user = User.objects.filter(email=email).first()
            if existing_user:
                error_message = "An account with this email already exists."
                return render(request, 'signup.html', {'error_message': error_message,'email_value':email,'first_name':first_name,'last_name':last_name})
            unique_id =  str(uuid.uuid4().hex)

            user = User(email=email, password=make_password(password),username=unique_id,first_name=first_name,last_name=last_name)
            user.save()
            return redirect('askcenter')  
        if not request.session.get('user_id'):
            return render(request, 'signup.html')
        return redirect('/askcenter')
    
    
# user login method
def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        is_user = User.objects.filter(email=email)
        is_user = is_user.first() if is_user else False
        request.username=is_user.username
        user = authenticate(request, username=is_user.username, password=password)
        if user is not None:
            request.session['user_id'] = user.id
            return redirect('/askcenter')  
        else:
            error_message = 'Invalid username or password'
            return render(request, 'login.html', {'error_message': error_message,'email_value':email})
    if not request.session.get('user_id'):
        return render(request, 'login.html')
    return redirect('/askcenter')
 
    return render(request, 'login.html')


# user logout method
def user_logout(request):
    logout(request)
    return redirect('/askcenter/login')

# home page 
def askcenter(request):
    if request.session.get('user_id'):
        return render(request, "askcenter.html", {"all_posts": Question.objects.all().order_by('-id')})
    return render(request, 'login.html')

# method to  display all user posts
def user_posts(request):
    if request.session.get('user_id'):
        if request.method == 'POST':
            content = request.POST['user_posts']
            if not content.strip():
                return render(request, "askcenter.html", {"all_posts": Question.objects.all().order_by('-id')})
            Question.objects.create(content=content, user=User.objects.get(
                    id=request.session.get("user_id")))
            return render(request, "askcenter.html", {"all_posts": Question.objects.all().order_by('-id')})
        return redirect('/askcenter/login')
    return redirect('/askcenter/login')

# method to display answers for particular question
def user_answers(request,q_id=None):
    if request.session.get('user_id'):
        if q_id:
            question_obj=Question.objects.filter(id=q_id).first()
            all_answers = Answer.objects.filter(question=q_id).order_by('-id')
        else:
            return redirect('/askcenter')
        if request.method == 'POST':
            answer = request.POST['user_answer']
            question = Question.objects.filter(id=q_id).first()
            user = User.objects.get(id=request.session.get("user_id"))
            Answer.objects.create(content=answer, user=user,question=question)
            return render(request, "answer.html", {"all_answers": all_answers,'question':question_obj})
        return render(request, "answer.html",{"all_answers": all_answers,'question':question_obj})
    return redirect('/askcenter/login')
    
    # method to handle user likes on particular answers
def user_like(request,a_id=None):
    if request.session.get('user_id'):
        if request.method == 'POST':
            if a_id:
                like_obj=Like.objects.filter(answer=a_id,user=request.session.get('user_id')).first()
                ans_obj=Answer.objects.get(id=a_id)
                if like_obj:
                    like_obj.delete()
                    ans_obj.count=ans_obj.count-1
                    ans_obj.save()
                    all_answers = Answer.objects.filter(question=ans_obj.question.id).order_by('-id')
                    return render(request, "like.html", {"all_answers": all_answers,'like':like_obj})
                else:
                    user = User.objects.get(id=request.session.get("user_id"))
                    answer = Answer.objects.filter(id=a_id).first()
                    like_obj=Like.objects.create(answer=answer,user=user)
                    ans_obj.count=ans_obj.count+1
                    ans_obj.save()
                    all_answers = Answer.objects.filter(question=ans_obj.question.id).order_by('-id')
                    return render(request, "like.html", {"all_answers": all_answers,'like':like_obj})
            return redirect('/askcenter/answer')
        return redirect('/askcenter/answer')
    return redirect('/askcenter/login')
        

