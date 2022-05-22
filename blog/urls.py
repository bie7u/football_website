from django.urls import path
from .views import createEntry, detailEntry, manageBlog, showBlog, showCategoryEntries, UpdateEntry, deleteEntry, acceptEntry


urlpatterns = [
    path('menu_użytkownika/dodaj_artykuł/', createEntry.as_view(), name='add-article'),
    path('artykul/<int:pk>/', detailEntry.as_view(), name='detail-entry'),
    path('admin_panel/zarzadzaj_blogiem/', manageBlog.as_view(), name='manage-blog'),
    path('admin_panel/zarzadzaj_blogiem/<int:id>', UpdateEntry.as_view(), name='update-entry'),
    path('blog/', showBlog.as_view(), name='show-blog'),
    
    # HTMX
    path('blog_kategoria/<int:id>', showCategoryEntries, name='show-category-entries'),
    path('usun_wpis/<int:id>', deleteEntry, name='delete-entry'),
    path('accept_entry/<int:id>', acceptEntry, name='accept-entry'),
]
