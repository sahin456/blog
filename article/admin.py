from django.contrib import admin

from .models import Article,Comment # BURADA models.py İÇİNDEKİ Article git diyoruz...

# Register your models here.

#admin.site.register(Article)

admin.site.register(Comment)

@admin.register(Article)    # Admin panelini özelleştirmek için....
class ArticleAdmin(admin.ModelAdmin):

    list_display = ["title","author","created_date"] # Hangi bilgilerin gösterilmesini istiyorsak onları göst.
    
    list_display_links = ["title","author","created_date"] # Verdiğimiz özelliklere link eklemek için
    
    search_fields = ["title"] # Makaleler arasında arama yapmak için
    
    list_filter = ["created_date","title"] # filtreleme
    
    class Meta:
        model = Article

    