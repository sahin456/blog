from django.shortcuts import render, HttpResponse, redirect, get_object_or_404,reverse
from .forms import ArticleForm
from .models import Article,Comment  # BULUNDUĞUMUZ KLASÖRDEKİ Article BURAYA DAHİL ET...
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

def articles(request):
    keyword = request.GET.get("keyword")

    if keyword:
        articles = Article.objects.filter(title__contains = keyword)
        return render(request, "articles.html", {"articles":articles})

    articles = Article.objects.all()

    return render(request, "articles.html", {"articles" : articles})

def index(request):
    #return HttpResponse("Anasayfa")
    return render(request,"index.html")

def about(request):
    return render(request, "about.html")


@login_required(login_url = "user:login") # ismi user olan login url'sine gitmek istiyorum dicez...
def dashboard(request):
    articles = Article.objects.filter(author = request.user)
    context = { "articles" : articles }

    return render(request, "dashboard.html", context)




@login_required(login_url = "user:login")
def addArticle(request):
    form = ArticleForm(request.POST or None , request.FILES or None) 

    if form.is_valid():
        article = form.save(commit = False)
        
        article.author = request.user
        article.save()

        messages.success(request, "Makale Başarıyla Oluşturuldu...")
        return redirect("article:dashboard")

    return render(request, "addarticle.html", {"form" : form})






def detail(request,id):
    #article = Article.objects.filter(id = id).first()
    article = get_object_or_404(Article, id = id)
    comments = article.comments.all()

    return render(request,"detail.html",{"article":article , "comments":comments})

    



@login_required(login_url = "user:login")
def updateArticle(request, id):
    article = get_object_or_404(Article, id = id)
    form = ArticleForm(request.POST or None , request.FILES or None , instance = article)
    if form.is_valid():
        article = form.save(commit = False)
        
        article.author = request.user
        article.save()

        messages.success(request, "Makale Başarıyla Güncellendi...")
        return redirect("article:dashboard")

    return render(request, "update.html" , {"form" : form})





@login_required(login_url = "user:login")
def deleteArticle(request, id):
    article = get_object_or_404(Article, id = id)
    article.delete()

    messages.success(request, "Makale Başarıyla Silindi...")
    return redirect("article:dashboard") # article altındaki dashboard git...


def addComment(request,id):
    article = get_object_or_404(Article, id = id)

    if request.method == "POST":
        comment_author = request.POST.get("comment_author")
        comment_content =request.POST.get("comment_content")

        newComment = Comment(comment_author = comment_author, comment_content = comment_content)
        newComment.article = article

        newComment.save()
    #return redirect("/articles/article/" + str(id))
    return redirect(reverse("article:detail", kwargs = {"id":id}))



