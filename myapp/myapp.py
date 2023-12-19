import uuid
from myapp.models import Cart,Product
from django.db.models import Sum
def cart_id(request):
    if 'cart_id' not in request.session:
        request.session['cart_id']=str(uuid.uuid4())
    return request.session['cart_id']
def get_cart(request):
    return Cart.objects.filter(cart_id=cart_id(request))
def add_to_cart(request):
    product_id=request.form_data['product_id'] 
    quantity=request.form_data['quantity']
    p=Product.objects.get(id=product_id)
    c=get_cart(request)
    item=False
    for i in c:
        if i.product_id==product_id:
            i.quantity += int(quantity)  # Update quantity directly
            i.save()
            item = True

            #i.update_quantity(quantity)
            #item=True

    if not item:
        ca= Cart(cart_id=cart_id(request),price=p.price,quantity=quantity,product_id=product_id)  
        ca.save()  
def item_count(request):
    return get_cart(request).aggregate(count=Sum('quantity'))        

def total(request):
    items=get_cart(request)
    t=0
    for i in items:
        #t+=i.total()
        t += i.price * i.quantity
    return t
  

