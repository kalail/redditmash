from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from redditmash.models import Post, StatsReddit, Stats, Choice

def index(request):
	# POST request
	if request.is_ajax() and request.method == 'POST':
		# Check if the choice is stale
		try:
			choice = Choice.objects.get(id = request.session['last_sent_choice_id'])
			# Send decision
			process_decision.delay(request.POST['winner_id'], choice.id)
		except Choice.DoesNotExist:
			# Choice is stale - Do nothing
			pass
		HttpResponseRedirect(reverse('redditmash.views.index'))

	# GET request
	if not request.session.get('choices_sent', None):
		request.session['choices_sent'] = []

	choices_active = Choice.objects.filter(is_active=True).order_by('-times_completed')
	for c in choices_active:
		if c.id not in request.session['choices_sent']:
			choice = c
			break
	# TODO Send template variables
	request.session['choices_sent'].append(choice.id)
	request.session.modified = True
	return render_to_response('index.html', context_instance=RequestContext(request))