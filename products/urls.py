from django.urls import path
from products import views

app_name = 'products'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('page/create/', views.CreatePageView.as_view(), name='create-page'),
    path('cart/', views.view_cart, name='view_cart'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('page/<int:page_id>/detail/', views.PageDetailView.as_view(), name='page-detail'),
    path('page/<int:page_id>/edit/', views.PageUpdateView.as_view(), name='page-edit'),
    path('page/<int:page_id>/product/<int:product_id>/detail/', views.ProductDetailView.as_view(), name='product-detail'),
    path('page/mine/', views.MypagesListView.as_view(), name='page-mine'),
    path('search-results/', views.SearchResultsView.as_view(), name='search-results')
]
