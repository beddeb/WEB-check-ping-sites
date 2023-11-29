from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import get_template


from main.forms import SiteCommentCreate, SiteSearchForm, RatingForm, GraphImageForm
from main.models import Sites, UserSite, SiteComment, SiteRating

import pdfkit

values_number = 24


# Site section
class SiteDetailView(LoginRequiredMixin, DetailView):
	model = Sites
	template_name = "main/site.html"
	context_object_name = "site"
	comment_form_class = SiteCommentCreate
	comments = SiteComment
	rating_form_class = RatingForm
	ratings = SiteRating
	graph_form_class = GraphImageForm

	def post(self, request, *args, **kwargs):
		rate_instance = self.ratings.objects.get_or_create(site=self.get_object(), user=request.user)[0]
		comment_form = self.comment_form_class(request.POST)
		rating_form = self.rating_form_class(request.POST or None, instance=rate_instance)
		graph_form = self.graph_form_class(request.POST)

		if list(request.POST)[-1] in ['1', '2', '3', '4', '5']:
			site = self.get_object()
			rating_form.instance.rate = int(list(request.POST)[-1])
			rating_form.instance.user = request.user
			rating_form.instance.site = site
			rating_form.save()
			return redirect(f'/site/{site.id}/')

		if request.POST.get('make-pdf') is not None:
			site = self.get_object()
			graph_form.is_valid()
			base_64_images = graph_form.cleaned_data['graph']
			base_64_images = base_64_images.split('data:image/png;base64,')

			context = {"images": base_64_images, "site": site}
			report_page = get_template('main/report.html').render(context)
			pdf = pdfkit.from_string(report_page, False, options={"enable-local-file-access": ""})

			response = HttpResponse(pdf, content_type='application/pdf')
			response['Content-Disposition'] = f'attachment; filename={site.name}.pdf'
			return response

		if request.POST.get('site-report') is not None:
			site = self.get_object()
			messages.warning(request, 'Вы сообщили о недоступности!')
			reps = site.reports
			last_time = list(reps.keys())[-1]
			reps[last_time] += 1
			site.save()
			return redirect(f'/site/{site.id}/')

		if comment_form.is_valid():
			site = self.get_object()
			comment_form.instance.user = request.user
			comment_form.instance.site = site
			comment_form.save()
			return redirect(f'/site/{site.id}/')

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context['form'] = self.comment_form_class
		context['graph_image_form'] = self.graph_form_class
		context['comments'] = self.comments.objects.all().filter(site=self.get_object()).order_by('-date')
		context['rating'] = self.ratings.objects.all().filter(site=self.get_object())
		return context


class SiteListView(ListView):
	model = Sites
	template_name = "main/main.html"
	context_object_name = "sites"
	paginate_by = 20
	search_form = SiteSearchForm

	def get_queryset(self):
		search_form = self.search_form(self.request.GET)
		if search_form.is_valid():
			sites = Sites.objects.filter(name__icontains=search_form.cleaned_data['keywords'])
		else:
			sites = Sites.objects.all()
		return sites

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context['form'] = self.search_form
		return context


class DeleteComment(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = SiteComment
	template_name = "main/delete-comment.html"
	context_object_name = "comment"

	def test_func(self):
		comment = self.get_object()
		self.success_url = f'/site/{comment.site.id}/'
		if comment.user == self.request.user:
			return True
		else:
			return False


# End site section


# User site section
class UserSiteDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
	model = UserSite
	template_name = "main/user-site.html"
	context_object_name = "site"

	graph_form_class = GraphImageForm

	def post(self, request, *args, **kwargs):
		graph_form = self.graph_form_class(request.POST)
		if request.POST.get('make-pdf') is not None:
			site = self.get_object()
			graph_form.is_valid()
			base_64_images = graph_form.cleaned_data['graph']
			base_64_images = base_64_images.split('data:image/png;base64,')

			context = {"images": base_64_images, "site": site}
			report_page = get_template('main/report.html').render(context)
			pdf = pdfkit.from_string(report_page, False, options={"enable-local-file-access": ""})

			response = HttpResponse(pdf, content_type='application/pdf')
			response['Content-Disposition'] = f'attachment; filename={site.name}.pdf'
			return response

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context['graph_image_form'] = self.graph_form_class
		return context

	def test_func(self):
		site = self.get_object()
		if site.owner == self.request.user:
			return True
		return False


class UserSiteListView(LoginRequiredMixin, ListView):
	model = UserSite
	template_name = "main/user-sites.html"
	context_object_name = "sites"
	paginate_by = 20

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		sites = UserSite.objects.all().filter(owner=user)
		return sites


class UserSiteCreate(LoginRequiredMixin, CreateView):
	model = UserSite
	fields = ["name", "url"]
	template_name = "main/create-site.html"
	context_object_name = "site"

	def form_valid(self, form):
		form.instance.owner = self.request.user
		return super().form_valid(form)


class UserSiteUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = UserSite
	fields = ["name", "url"]
	template_name = "main/update-site.html"
	context_object_name = "site"

	def form_valid(self, form):
		form.instance.owner = self.request.user
		return super().form_valid(form)

	def test_func(self):
		site = self.get_object()
		if self.request.user == site.owner:
			return True
		return False


class UserSiteDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = UserSite
	template_name = "main/delete-site.html"
	context_object_name = "site"

	def test_func(self):
		site = self.get_object()
		self.success_url = f'/user-site/user/{self.request.user}'
		if self.request.user == site.owner:
			return True
		return False


def about(request):
	context = {
		'title': 'about',
	}
	return render(request, 'main/about.html', context=context)


def help_view(request):
	context = {
		'title': 'help',
	}
	return render(request, 'main/help.html', context=context)


def contact(request):
	context = {
		'title': 'constact',
	}
	return render(request, 'main/contact.html', context=context)
