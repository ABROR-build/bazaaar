from django.views import View
from django.views.generic import DeleteView, ListView
from django.shortcuts import render, get_object_or_404, redirect
from .models import Pages, Products, SavedProduct, CartItem, Images
from products import forms
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q


class HomePageView(View):
    def get(self, request):
        products = Products.objects.all().order_by('-id')
        context = {
            'products': products,
        }
        return render(request, 'home.html', context=context)


class SearchResultsView(ListView):
    model = Products
    template_name = 'search_results.html'
    context_object_name = 'products'

    def get_queryset(self):
        query = self.request.GET.get("q")
        object_list = Products.objects.filter(
            Q(name__icontains=query) | Q(price__icontains=query)
        )
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = Images.objects.filter(
            product__in=self.get_queryset()
        )
        return context


class MypagesListView(View):
    def get(self, request):
        pages = Pages.objects.filter(account=request.user)
        context = {
            'pages': pages
        }
        return render(request, 'my_pages.html', context=context)


class CreatePageView(View):
    def get(self, request):
        create_page_form = forms.PagesForm()
        context = {
            'create_page_form': create_page_form
        }
        return render(request, 'create_page.html', context=context)

    def post(self, request):
        create_page_form = forms.PagesForm(request.POST, request.FILES)
        if create_page_form.is_valid():
            new_page = create_page_form.save(commit=False)
            new_page.account = request.user
            new_page.save()
            # print("New Page ID:", new_page.id)
            return redirect('products:page-detail', page_id=new_page.id)
        else:
            # print("Form Errors:", create_page_form.errors)
            context = {
                'create_page_form': create_page_form
            }
            return render(request, 'create_page.html', context=context)


class PageDetailView(View):
    def get(self, request, *args, **kwargs):
        page_id = kwargs.get('page_id')
        page = get_object_or_404(Pages, id=page_id)
        products = Products.objects.filter(page_id=page_id)
        context = {
            'page': page,
            'products': products
        }
        return render(request, 'page_detail.html', context=context)


class PageUpdateView(View):
    def get(self, request, page_id):
        page = get_object_or_404(Pages, pk=page_id)
        form = forms.PagesForm(instance=page)
        context = {
            'form': form
        }
        return render(request, 'page_update.html', context=context)

    def post(self, request, page_id):
        page = get_object_or_404(Pages, pk=page_id)
        form = forms.PagesForm(request.POST, instance=page)
        if form.is_valid():
            form.save()
            return redirect('products:page-detail', page_id=page_id)
        context = {
            'form': form
        }
        return render(request, 'page_update.html', context=context)


class ProductDetailView(View):
    def get(self, request, page_id, product_id, *args, **kwargs):
        page = get_object_or_404(Pages, id=page_id)
        product = get_object_or_404(Products, pk=product_id)
        productsave = SavedProduct.objects.filter(product=product)
        context = {
            'page': page,
            'product': product,
            'productsave': productsave,
        }
        return render(request, 'product_detail.html', context=context)


class ProductUpdateView(View):
    def get_object(self):
        pk = self.kwargs.get("pk")
        return get_object_or_404(Products, pk=pk)

    def get(self, request, pk):
        product = get_object_or_404(Products, pk=pk)
        update_form = forms.ProductsForm(instance=product)
        context = {
            'form': update_form
        }
        return render(request, 'product_update.html', context=context)

    def post(self, request, pk):
        product = get_object_or_404(Products, pk=pk)
        update_form = forms.ProductsForm(request.POST, request.FILES, instance=product)
        if update_form.is_valid():
            update_form.save()
            return redirect('products:home')
        else:
            context = {
                'form': update_form
            }
            return render(request, 'product_update.html', context=context)


class ProductDeleteView(DeleteView):
    model = Products
    template_name = 'post_delete.html'
    success_url = reverse_lazy('products:home')


class SavedProductView(View):
    def get(self, request):
        savedproduct = SavedProduct.object.filter(user=request.user)
        context = {
            'savedproduct': savedproduct,
        }
        return render(request, 'savedproducts.html', context=context)


def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price_discount * item.quantity for item in cart_items)
    context = {
        'cart_items': cart_items,
        'total_price': total_price
    }
    return render(request, 'cart.html', context=context)


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    quantity = int(request.GET.get('quantity', 1))

    cart_item, created = CartItem.objects.get_or_create(product=product, user=request.user)
    cart_item.quantity += quantity
    cart_item.save()

    return redirect('products:view_cart')


def remove_from_cart(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.delete()
    return redirect('products:view_cart')
