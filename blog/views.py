from pyexpat import model
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from datetime import datetime
from django.urls import reverse
from django.views import View
from .models import BlogEntry, EntryComment
from .forms import BlogEntryForm, EntryCommentForm
from user_panel.models import League
from django.core.paginator import Paginator
from user_panel.decorators import allowed_users
from django.utils.decorators import method_decorator

@method_decorator(allowed_users(allowed_roles=['admin', 'editor', 'user']), name='dispatch')
class createEntry(View):
    template_name = 'blog/create_blog_entry.html'
    form_class = BlogEntryForm

    def get(self, request):
        form = self.form_class
    
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
            
            if str(request.user.groups.get()) == 'admin':
                form.admin_agree = True
                form.publicate_at = datetime.now()
            else: 
                form.admin_agree = False

            form.save()
            return HttpResponseRedirect(reverse('user-home'))
        else:
            return HttpResponseRedirect(reverse('user-home'))


class detailEntry(View):
    model = BlogEntry
    template_name = 'blog/detail_entry.html'
    form_class = EntryCommentForm
    
    # This function delete duplicate article in view 
    def search_duplicate(self, qs, duplicate):
        for i in qs:
            if i == duplicate:
                qs.remove(i)
        return qs

    def get(self, request, pk):
        entry = self.model.objects.get(id=pk)
        latest_sponsor_articles = list(BlogEntry.objects.filter(article_type='1').order_by('-created_at'))[0:5]
        latest_articles = list(BlogEntry.objects.filter(article_type='2').order_by('-created_at'))[0:3]

        latest_articles = self.search_duplicate(latest_articles, entry)
        latest_sponsor_articles = self.search_duplicate(latest_sponsor_articles, entry)
        form = self.form_class # comment
        comments = EntryComment.objects.filter(entry=pk)
        
        context = {'latest_sponsor_articles': latest_sponsor_articles, 'latest_articles': latest_articles, 
                    'entry':entry, 'form': form, 'comments': comments}
        return render(request, self.template_name, context)

    def post(self, request, pk):
        form = self.form_class(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.entry = BlogEntry.objects.get(id=pk)
            form.save()

            return redirect('detail-entry', pk)

@method_decorator(allowed_users(allowed_roles=['admin', 'editor']), name='dispatch')
class manageBlog(View):
    model = BlogEntry
    template_name = 'blog/manage_blog.html'
    
    def get(self, request):
        entries = self.model.objects.filter(admin_agree=True).order_by('-created_at')
        pending_approval_articles = self.model.objects.filter(admin_agree=False)

        paginator = Paginator(entries, 10) 
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {'entries': page_obj, 'pending_approval_articles': pending_approval_articles}
        return render(request, self.template_name, context)  


class showBlog(View):
    model = BlogEntry
    template_name = 'blog/show_blog.html'

    def get(self, request):
        entries = self.model.objects.filter(admin_agree=True).order_by('-publicate_at')
        leagues = League.objects.all()

        context = {'entries': entries, 'leagues': leagues}
        return render(request, self.template_name, context)


@method_decorator(allowed_users(allowed_roles=['admin', 'editor']), name='dispatch')
class UpdateEntry(View):
    model = BlogEntry
    form_class = BlogEntryForm
    template_name = 'blog/update_blog_entry.html'

    def get(self, request, id):
        obj = get_object_or_404(self.model, id=id)
        form = self.form_class(instance=obj)
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, id):
        obj = get_object_or_404(self.model, id=id)
        form = self.form_class(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('manage-blog'))


# HTMX
def showCategoryEntries(request, id):
    leagues = League.objects.all()
    entries = BlogEntry.objects.filter(league=id, admin_agree=True).order_by('-publicate_at')

    context = {'leagues': leagues, 'entries': entries}
    return render(request, 'partials/show_blog_category.html', context)

def deleteEntry(request, id):
    obj = get_object_or_404(BlogEntry, id=id)
    obj.delete()
    response = HttpResponse()
    response["HX-Redirect"] = ''
    return response


def acceptEntry(request, id):
    obj = BlogEntry.objects.get(id=id)
    obj.admin_agree = True
    obj.publicate_at = datetime.now()
    obj.save()
    response = HttpResponse()
    response["HX-Redirect"] = ''
    return response