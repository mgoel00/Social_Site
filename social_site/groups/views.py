from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.urls import reverse
from django.views import generic
from .models import Group
from django.shortcuts import get_object_or_404
from django.contrib import messages
# Create your views here.


class CreateGroup(LoginRequiredMixin,generic.CreateView):
    fields= ('name','description')
    model = Group


class SingleGroup(generic.DetailView):
    model = Group

class ListGroups(generic.ListView):
    model = Group

class JoinGroup(LoginRequiredMixin,generic.RedirectView):

    def get_redirect_url(self,*args,**kwargs):
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})

    def get(self,request,*args,**kwargs):
        group = get_object_or_404(Group,slug=self.kwargs.get('slug'))

        try:
            GroupMember.objects.create(user=self.request.user,group=group)
        except:
            messages.warning(self.request,"Warning! Already a Member")
        else:
            messages.success(self.request,"You are now Member")
        return super().get(request,*args,**kwargs)


class LeaveGroup(LoginRequiredMixin,generic.RedirectView):

    def get_redirect_url(self,*args,**kwargs):
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})

    def get(self,request,*args,**kwargs):
        # group = get_object_or_404(Group,slug=self.kwargs.get('slug'))

        try:
            membership = models.GroupMember.objects.filter(user=self.request.user, group__slug=self.kwargs.get('slug')).get()
            # GroupMember.objects.create(user=self.request.user,group=group)
        except models.GroupMember.DoesNotExist:
            messages.warning(self.request,"Warning! You are not in this group.")
        else:
            membership.delete()
            messages.success(self.request,"You have legt the group")
        return super().get(request,*args,**kwargs)
