from django.shortcuts import render,redirect
from django.http  import HttpResponse,Http404,HttpResponseRedirect
import datetime as dt
from .models import Article,NewsLetterRecipients
from .forms import NewsLetterForm,CreateUserForm,NewArticleForm
from .email import send_welcome_email
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required


from django.contrib.auth import authenticate,login,logout 
# Create your views here.

def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('login')
    context = {'form':form}
    return render(request,'registration/registration_form.html',context)

def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request, user)
            return redirect('newsToday')
    context = {}
    return render(request,'registration/login.html',context)

def logoutpage(request):
    logout(request)
    return redirect('login')



def news_of_day(request):
    date = dt.date.today()
    news = Article.todays_news()
    if request.method == 'POST':
        form = NewsLetterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['your_name']
            email = form.cleaned_data['email']

            recipient = NewsLetterRecipients(name = name,email=email)
            recipient.save()
            send_welcome_email(name,email)
            HttpResponseRedirect('news_of_day')
    else:
        form = NewsLetterForm()
    return render(request,'all-news/today-news.html',{"date":date,"news":news,"letterform":form})

def past_days_news(request,past_date):
    #converts data from the string url 
    try:
        #Converts data from the string Url
        date = dt.datetime.strptime(past_date,'%Y-%m-%d').date()

    except ValueError:
        # Raise 404 error when ValueError is thrown
        raise Http404()
    if date == dt.date.today():
        return redirect(news_of_day)

    news = Article.days_news(date)
    return render(request,'all-news/past-news.html',{"date":date,"news":news})


def search_results(request):
    if 'article' in request.GET and request.GET["article"]:
        search_term = request.GET.get("article")
        searched_articles = Article.search_by_title(search_term)
        message = f"{search_term}"

        return render(request,"all-news/search.html",{"message":message,"articles":searched_articles})
    else:
        message = "You haven't searched for any term"
        return render(request,'all-news/search.html',{"message":message})

@login_required(login_url='login')
def article(request,article_id):
    try:
        article = Article.objects.get(id= article_id)
    except DOESNOTEXIST:
        raise Http404

    return render(request,"all-news/article.html",{"article":article})

@login_required(login_url="login")
def new_article(request):
    current_user = request.user
    if request.method == 'POST':
        form = NewArticleForm(request.POST,request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.editor = current_user
            article.save()
        return redirect('newsToday')
    else:
        form = NewArticleForm()
    return render(request,'new_article.html',{"form":form})