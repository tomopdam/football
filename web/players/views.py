from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.db.models import Q, F, Sum, Avg

from .models import Player
from .forms import SearchForm, TeamBuilderForm

from .utils import find_optimal_team

class HomeView(TemplateView):
    template_name = 'players/home.html'

class PlayerDetailView(DetailView):
    template_name = 'players/detail.html'
    model = Player


class SearchView(ListView):
    model = Player
    template_name = 'players/search.html'
    context_object_name = 'players'
    form_class = SearchForm

    ordering = ['-overall']
    paginate_by = 30

    
    def get_queryset(self):
        # set object_list to empty for now
        object_list = Player.objects.none()

        # user has submitted search form
        if self.request.GET.get('q', '') != '':
            form = SearchForm(self.request.GET)
            if form.is_valid():
                q = form.cleaned_data['q']
                search_by = form.cleaned_data['search_by']

                # perform search according to search_by radio select
                if search_by == 'name':
                    object_list = Player.objects.filter(name__icontains=q)
                elif search_by == 'club':
                    object_list = Player.objects.filter(club__icontains=q)
                elif search_by == 'nationality':
                    object_list = Player.objects.filter(nationality__icontains=q)
                else:
                    # default to search_by = 'all'
                    object_list = Player.objects.filter(
                        Q(name__icontains=q) |
                        Q(nationality__icontains=q) |
                        Q(club__icontains=q)
                    )
        return object_list.order_by('-overall')

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)

        # result of a search?
        if (self.request.GET.get('q')):
            # pre-fill with search params
            context['form'] = SearchForm(self.request.GET)
            context['result_count'] = len(self.object_list)
            context['performed_search'] = True
        else:
            # set default "Search by" to all
            context['form'] = SearchForm(initial={'search_by':'all'})
            context['performed_search'] = False
        return context

class TeamBuilderView(ListView):
    model = Player
    template_name = 'players/teambuilder.html'
    form_class = TeamBuilderForm
    context_object_name = 'team'

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        if (self.request.GET.get('budget')):
            context['form'] = TeamBuilderForm(self.request.GET)
            context['budget'] = self.request.GET.get('budget')
            # pass extra information about the team that we've built
            if (context['team']):
                context['total_score'] = context['team'].aggregate(Sum('overall'))['overall__sum']
                context['total_cost'] = context['team'].aggregate(Sum('cost'))['cost__sum']
                context['average_cost'] = context['team'].aggregate(Avg('cost'))['cost__avg']
                context['average_score'] = context['team'].aggregate(Avg('overall'))['overall__avg']
                context['leftover_budget'] = str(int(context['budget']) - int(context['total_cost']))
        else:
            context['form'] = TeamBuilderForm(initial={'budget':'100000'})
        return context

    def get_queryset(self):
        # set object_list to empty for now
        object_list = Player.objects.none()

        # user has submitted search form
        if self.request.GET.get('budget', '') != '':
            form = TeamBuilderForm(self.request.GET)
            if form.is_valid():
                budget = form.cleaned_data['budget']

                # get all eligible players: total cost must > 0
                player_pool = Player.objects.annotate(cost=F('wage') + F('release_clause')).filter(cost__gt=0).order_by('cost')
                
                team = find_optimal_team(budget=budget, players=player_pool)
                
                object_list = Player.objects.filter(id__in=team.players).annotate(cost=F('wage') + F('release_clause')).order_by('-cost')
        
        return object_list