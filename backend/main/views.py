# Create your views here.
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from models import Archive, Title, Volume, Section, Page, Article, Paragraph


def index(request):
    return HttpResponse("This is a Search Page.")


class IndexView(ListView):
    template_name = 'main/index.html'
    model = Archive
    queryset = Archive.objects.all()


class SearchResultsView(ListView):
    model = Article
    paginate_by = 10
    context_object_name = 'articles_list'
    template_name = "main/search_results_list.html"

    def get_queryset(self):
        # search_string = request.GET['q']
        search_string = self.request.GET['q']
        queryset = Article.objects.filter(paragraphs__extracted_text__icontains=search_string).order_by('id')
        return queryset


class ResultDetailView(DetailView):
    model = Article
    template_name = 'main/article_detail.html'