# from django.shortcuts import redirect
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from main.forms import ReviewAdd,AddressBookForm
from django.db.models import Max,Min,Count,Avg
from django.template.loader import render_to_string
from django.contrib.auth import authenticate,login,logout
from main.models import Category,Brand,Product,ProductAttribute,ProductReview,Cartview
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponseBadRequest

def form(request):
    return render(request,"form.html")
def header(request):
    return render(request,"header.html")
def footer(request):
    return render(request,"footer.html")
def about(request):
    return render(request,"about.html")
def filter(request):
    return render(request,'filter.html')

def category(request):
    data=Category.objects.all().order_by('-id')
    return render(request,'category.html',{'data':data})

def brand(request):
    data=Brand.objects.all().order_by('-id')
    return render(request,'brand.html',{'data':data})

def product(request):
    total_data=Product.objects.count()
    data=Product.objects.all().order_by('-id')[:3]
    min_price=ProductAttribute.objects.aggregate(Min('price'))
    max_price=ProductAttribute.objects.aggregate(Max('price'))
    return render(request,'product.html',
		{
			'data':data,
			'total_data':total_data,
			'min_price':min_price,
			'max_price':max_price,
		}
		)
def category_product_list(request,cat_id):
	category=Category.objects.get(id=cat_id)
	data=Product.objects.filter(category=category).order_by('-id')
	return render(request,'category_product_list.html',{
			'data':data,
			})

# Product List According to Brand
def brand_product_list(request,brand_id):
	brand=Brand.objects.get(id=brand_id)
	data=Product.objects.filter(brand=brand).order_by('-id')
	return render(request,'category_product_list.html',{
			'data':data,
			})


def product_detail(request, slug, id):
    product = get_object_or_404(Product, id=id)
    related_products = Product.objects.filter(category=product.category).exclude(id=id)[:4]
    colors = ProductAttribute.objects.filter(product=product).values('color__id', 'color__title', 'color__color_code').distinct()
    reviewForm = ReviewAdd()

    # Check
    canAdd = True
    reviewCheck = 0
    if request.user.is_authenticated:
        reviewCheck = ProductReview.objects.filter(user=request.user, product=product).count()
        if reviewCheck > 0:
            canAdd = False
    else:
        canAdd = False
    # End

    # Fetch reviews
    reviews = ProductReview.objects.filter(product=product)
    # End

    # Fetch avg rating for reviews
    avg_reviews = ProductReview.objects.filter(product=product).aggregate(avg_rating=Avg('review_rating'))
    # End

    context = {
        'data': product,
        'related': related_products,
        'colors': colors,
        'reviewForm': reviewForm,
        'canAdd': canAdd,
        'reviews': reviews,
        'avg_reviews': avg_reviews,
    }

    return render(request, 'product_detail.html', context)

def load_more_data(request):
	offset=int(request.GET['offset'])
	limit=int(request.GET['limit'])
	data=Product.objects.all().order_by('-id')[offset:offset+limit]
	t=render_to_string('ajax/product-list.html',{'data':data})
	return JsonResponse({'data':t}
)  

def filter_data(request):
	colors=request.GET.getlist('color[]')
	categories=request.GET.getlist('category[]')
	brands=request.GET.getlist('brand[]')
	minPrice=request.GET['minPrice']
	maxPrice=request.GET['maxPrice']
	allProducts=Product.objects.all().order_by('-id').distinct()
	allProducts=allProducts.filter(productattribute__price__gte=minPrice)
	allProducts=allProducts.filter(productattribute__price__lte=maxPrice)
	if len(colors)>0:
		allProducts=allProducts.filter(productattribute__color__id__in=colors).distinct()
	if len(categories)>0:
		allProducts=allProducts.filter(category__id__in=categories).distinct()
	if len(brands)>0:
		allProducts=allProducts.filter(brand__id__in=brands).distinct()
	t=render_to_string('ajax/product-list.html',{'data':allProducts})
	return JsonResponse({'data':t})


def save_review(request, pid):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=pid)
        user = request.user
        review_text = request.POST['review_text']
        review_rating = request.POST['review_rating']
        
        # Create the review
        ProductReview.objects.create(
            user=user,
            product=product,
            review_text=review_text,
            review_rating=review_rating,
        )
        
        # Fetch avg rating for reviews
        ProductReview.objects.filter(product=product).aggregate(avg_rating=Avg('review_rating'))
        
        # Redirect back to the referring page
        return redirect(request.META.get('HTTP_REFERER', 'default-view-name'))
    else:
        return redirect('default-view-name')



# Create your views here.
def signaction(request):
    if request.method == "POST":
        username = request.POST.get("name")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 == password2:
            try:
                # Create the User object
                saveuser = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password1
                )
                saveuser.save()

                return render(request, 'signup_page.html', {
                    'form': UserCreationForm(),
                    'info': 'This user ' + username + ' is successfully created.'
                })
            except IntegrityError:
                return render(request, 'signup_page.html', {
                    'form': UserCreationForm(),
                    'info': 'This user ' + username + ' already exists.'
                })
        else:
            return render(request, 'signup_page.html', {
                'form': UserCreationForm(),
                'error': 'Passwords do not match.'
            })
    else:
        return render(request, 'signup_page.html')

def loginuser(request):
    if request.method=="POST":
        loginsuccess=authenticate(request,username=request.POST.get('name'),password=request.POST.get('password'))
        if loginsuccess is None:
            return render (request,'login_page.html',{'form':AuthenticationForm(),'error':'This name and password does not match'})
        else:
            login(request,loginsuccess)
            return redirect('welcome')
    else:
        return render (request,'login_page.html',{'form':AuthenticationForm()})

def welcomepage(request):
    data=Product.objects.filter(is_featured=True)
    return render(request,'welcome.html',{'data':data}) 
def profile(request):
    return render(request,'profile.html',{'user': request.user})
def savedata(request):
    
    return render(request,'signup_page.html')
@login_required
def signout(request):
    logout(request)
    return redirect('/')

def add_to_cart(request):
    if request.method == "POST":
        print(request.POST)  # Add this line for debugging
        product_id = request.POST.get('product_id')
        
        if not product_id:
            return HttpResponseBadRequest("Product ID is missing.")
        
        try:
            product_id = int(product_id)
        except ValueError:
            return HttpResponseBadRequest("Invalid Product ID format.")
        
        quantity = int(request.POST.get('quantity', 1))
        
        prod = get_object_or_404(Product, id=product_id)
        total_price = prod.price * quantity
        
        cart_item, created = Cartview.objects.get_or_create(
            user=request.user,
            product=prod,
            defaults={'quantity': quantity, 'total_price': total_price}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.total_price = cart_item.quantity * prod.price
            cart_item.save()
        
        return redirect('/cart/')
    
    return redirect('product_detail', id=product_id)

def cart_view(request):
    cart_items = Cartview.objects.filter(user=request.user)
    context = {
        'cart_item': cart_items
    }
    return render(request, 'cart.html',context)


# Delete Cart Item
# def delete_cart_item(request):
# 	p_id=str(request.GET['id'])
# 	if 'cartdata' in request.session:
# 		if p_id in request.session['cartdata']:
# 			cart_data=request.session['cartdata']
# 			del request.session['cartdata'][p_id]
# 			request.session['cartdata']=cart_data
# 	total_amt=0
# 	for p_id,item in request.session['cartdata'].items():
# 		total_amt+=int(item['qty'])*float(item['price'])
# 	t=render_to_string('ajax/cart-list.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})
# 	return JsonResponse({'data':t,'totalitems':len(request.session['cartdata'])})