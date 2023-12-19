from django.shortcuts import render,redirect
from django.http import HttpResponse
from myapp.models import Product,Cart,Buy,Wishlist,Reply, Category,FAQ,ContactMessage
from myapp.forms import CartForm
from django.urls import reverse
from django.shortcuts import render
from paypal.standard.forms import PayPalPaymentsForm
from django.contrib.auth.decorators import login_required
# Create your views here.
from myapp.myapp import *
from django.shortcuts import render

from django.shortcuts import redirect, get_object_or_404

def products(request,product_id,slug):
    p=Product.objects.filter(category=product_id)
    if request.GET.get('q'):
        query=request.GET.get('q')
        p=Product.objects.filter(title__contains=query)
    context={'p':p}
    return render(request,'index.html',context)
def detail(request,product_id,slug):
    d=Product.objects.get(id=product_id)
    reviews = Reply.objects.filter(product=d)
    if request.method=="POST":
        f=CartForm(request,request.POST)
        if f.is_valid():
            request.form_data=f.cleaned_data
            add_to_cart(request)
            #return HttpResponse('added to cart')
            return redirect('myapp:cart_view')
    f=CartForm(request,initial={'product_id':product_id})
    context={'d':d,'f':f,'reviews': reviews}
    return render(request,'detail.html',context)   
def cart_view(request):
    if request.method == "POST" and 'delete' in request.POST:
        item_id = request.POST.get('item_id')
        print(f"Received item_id: {item_id}")  # Add this line for debugging

        if item_id:  # Check if item_id is not empty before querying the database
            try:
                cd = Cart.objects.get(id=int(item_id))
                cd.delete()
            except Cart.DoesNotExist:
                print("Cart item does not exist")  # Add this line for debugging

    c = get_cart(request)
    t = total(request)
    co = item_count(request)
    context = {'c': c, 't': t}
    return render(request, 'cart.html', context)

def order(request):
    # What you want the button to do.
    items=get_cart(request)
    for i in items:
        b=Buy(product_id=i.product_id,quantity=i.quantity,price=i.price)
        b.save()
    paypal_dict = {
        "business": "sb-l7r2e28145955@business.example.com",
        "amount": total(request),
        "item_name":cart_id(request),
        "invoice": str(uuid.uuid4()),
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('myapp:return_view')),
        "cancel_return": request.build_absolute_uri(reverse('myapp:cancel_view')),
        "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form,"items":items,"total":total(request)}
    return render(request, "order.html", context)
def return_view(request):
    return HttpResponse('Transaction Succesful')
def cancel_view(request):
    return HTTpResponse('Trransaction Canclled')

from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect


def send_email(request):
    subject = request.POST.get("subject", "Hi Geld Bro")
    message = request.POST.get("message", "otp is 465625")
    from_email = request.POST.get("from_email", "chaitanya4656@gmail.com")
    if subject and message and from_email:
        try:
            send_mail(subject, message, from_email, ["admin@example.com"])
        except BadHeaderError:
            return HttpResponse("Invalid header found.")
        return HttpResponseRedirect("Mail sent to geld")
    else:
        # In reality we'd use a form class
        # to get proper validation errors.
        return HttpResponse("Make sure all fields are entered and valid.")
def add_reply(request, product_id):
    if request.method == "POST" and request.user.is_authenticated:
        reply_text = request.POST.get('reply_text')
        product = get_object_or_404(Product, id=product_id)
        
        if reply_text:
            ProductReply.objects.create(product=product, user=request.user, reply_text=reply_text)
            # Redirect back to the product detail page after adding the reply
            return redirect('myapp:detail', product_id=product_id, slug=product.slug)
    
    # Redirect to a specific page if there's an issue with adding the reply
    return redirect('myapp:some_error_page')

#===========================================================================rating and reviews code
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        review_content = request.POST.get('review_content')
        if review_content:
            user = request.user
            review = Reply.objects.create(user=user, content=review_content, product=product)
            # Perform any other actions you need after adding a review
            # Redirect to the product detail view after adding the review
            review.save()
            return redirect('myapp:detail', product_id=product.id, slug=product.slug)
    
    # If there's an issue adding the review, redirect to a specific page
    return HttpResponseRedirect(reverse('myapp:index'))
    
    # If there's an issue adding the review, redirect to a specific page
    return HttpResponseRedirect(reverse('myapp:index'))


#=============================== contact us
from .models import ContactMessage
from .forms import ContactForm

def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('myapp:contact_us_success')  # Redirect to a success page after form submission
    else:
        form = ContactForm()
    return render(request, 'contact_us.html', {'form': form})

def contact_us_success(request):
    return render(request, 'contact_us_sucess.html')

def category(request):
    c= Category.objects.all()
    context={'c':c}
    print(c)
    return render(request,'categories.html',context)
def faq_list(request):
    faqs = FAQ.objects.all()
    return render(request, 'faq_list.html', {'faqs': faqs})
