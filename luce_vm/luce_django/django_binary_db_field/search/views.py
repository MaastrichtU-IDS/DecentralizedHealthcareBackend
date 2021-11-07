from django.shortcuts import render

from datastore.models import Dataset
from .models import SearchQuery


def search_view(request):
	# Obtain query value from URL & set default
	query = request.GET.get('q', None)
	# Looks into the request.GET dictionary and looks for
	# key named `q`. If there is none, it will use `None`

	# We define context already so we can add elements to it below
	context = {"query": query}

	# Obtain user
	user = None
	if request.user.is_authenticated:
		user = request.user

	if query not in [None,""]:
		# Store query as db entry for log
		SearchQuery.objects.create(user=user, query=query)

		# Obtain matching search results
		results_list = Dataset.objects.search(query=query)
		# Only display published items
		results_list = results_list.published()

		# Add matching results to context dictionary
		context['results_list'] = results_list

	template = 'search/view.html'
	return render(request, template, context)

