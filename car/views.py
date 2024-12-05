from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from . import forms
from . import models
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from .models import Car, Comment

# Add Car Using Class Based View
@method_decorator(login_required, name='dispatch')
class AddCarCreateView(CreateView):
    model = models.Car
    form_class = forms.CarForm
    template_name = 'add_car.html'
    success_url = reverse_lazy('add_car')
    def form_valid(self, form):
        messages.success(self.request, 'Car Added Successfully')
        form.instance.customer = self.request.user
        return super().form_valid(form)



# Edit Car Using Class Based View
@method_decorator(login_required, name='dispatch')
class EditCarView(UpdateView):
    model = models.Car
    form_class = forms.CarForm
    template_name = 'add_car.html'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('profile')
    def form_valid(self, form):
        messages.success(self.request, 'Car Edited Successfully')
        return super().form_valid(form)
        



@method_decorator(login_required, name='dispatch')
class DeleteCarView(DeleteView):
    model = models.Car
    template_name = 'delete_car.html'
    success_url = reverse_lazy('profile')
    pk_url_kwarg = 'id'
    def form_valid(self, form):
        messages.success(self.request, 'Car Delete Successfully')
        return super().form_valid(form)
    


class DetailsCarView(DetailView):
    model = models.Car
    pk_url_kwarg = 'id'
    template_name = 'car_details.html'

    def post(self, request, *args, **kwargs):
        comment_form = forms.CommentForm(data=self.request.POST)
        post = self.get_object()
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
        return self.get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            post = self.object #Post model er object store kora holo
            comments = post.comments.all()
            comment_form = forms.CommentForm()

            context["comments"] = comments
            context["comment_form"] = comment_form
            return context