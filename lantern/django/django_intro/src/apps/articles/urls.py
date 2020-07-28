from django.urls import path

from apps.articles.views import main_page, SearchResultsView, main_page_logged_id, ShowTitsView, ArticleDetailView, \
    ArticleUpdateImageView, delete_view, article_json, articles_list_json, NewArticleFormView, ArticleListView, new_article

app_name = 'articles'

urlpatterns = [
    path('search/<int:some_id>/', main_page_logged_id, name='main-page2'),
    path('search/', main_page, name='main-page'),
    path('results/', SearchResultsView.as_view(), name='search-results'),
    path('tits_list/', ShowTitsView.as_view(), name='tits'),
    path('<int:id>/', ArticleDetailView.as_view(), name='detail'),
    path('<int:id>/change_image/', ArticleUpdateImageView.as_view(), name='update-image'),
    path('delete/<int:id>/', delete_view),
    path('json/<int:id>/', article_json),
    path('list_json/', articles_list_json),
    path('new/', NewArticleFormView.as_view(), name='article-form'),
    path('new/article', new_article),
    path('all/', ArticleListView.as_view(), name='article-list'),
]
