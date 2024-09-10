# from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from .models import Product,Order,Review,OrderItem,ShippingAddress
from django.shortcuts import get_object_or_404
from .serializers import ProductSerializer,OrderSerializer,ReviewSerializer,OrderItemSerializer
from rest_framework.permissions import IsAuthenticated,IsAdminUser,BasePermission
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from datetime import datetime
from decimal import Decimal
# Create your views here.



#product end points
@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_all_products(request):
    try:
        products = Product.objects.all()
        serializer = ProductSerializer(products,many = True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
def get_product(request,pk):
    try:
        product = Product.objects.get(id = pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data ,status=status.HTTP_200_OK)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_product(request):
    user = request.user
    data = request.data
    data['user'] = user.id
    try:
        serialezer = ProductSerializer(data = data)
        if serialezer.is_valid():
            serialezer.save()
            return Response(serialezer.data,status=status.HTTP_201_CREATED)
        else :
            return Response(serialezer.errors,status=status.HTTP_400_BAD_REQUEST)
    except Exception as ex:
        return Response({'details' : f'error happen {str(ex)}'} ,status=status.HTTP_400_BAD_REQUEST)
    

@permission_classes([IsAdminUser])
@api_view(['PUT'])
def update_product(request , pk):
    try :
        data = request.data
        product = Product.objects.get(id = pk)
        data['user'] = request.user.id
        serializer = ProductSerializer(data = data ,instance = product ,partial= True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_200_OK)
        else : 
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
    except Product.DoesNotExist:
        return Response({'error':'no such product'},status=status.HTTP_404_NOT_FOUND)



@permission_classes([IsAdminUser])
@api_view(['DELETE'])
def delete_product(request , pk):
    try:
        Product.objects.filter(id = pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Exception as ex:
        return Response({'error':f'{str(ex)}'})



@permission_classes([IsAuthenticated])
@api_view(['POST'])
def upload_image(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if 'image' not in request.FILES:
        return Response({"error": "No image file found in the request."},
                        status=status.HTTP_400_BAD_REQUEST)
    product.image = request.FILES['image']
    product.save()
    serializer = ProductSerializer(product)
    return Response(serializer.data, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def search_products(request,search_param ):
    products = Product.objects.filter(
        Q(name__icontains=search_param) | Q(description__icontains=search_param)
    )
    serializer = ProductSerializer(products, many=True) 
    return Response(serializer.data, status=status.HTTP_200_OK)

#-------------------------------------------------------------------------------------------------


@api_view(["GET"])    
def get_product_reviews(request , pk) : 
    try : 
        reviews = Review.objects.filter(product_id = pk ) 
        serializer = ReviewSerializer(reviews , many = True) 
        print(serializer.data)
        return Response(serializer.data , status=200)
    except :
        return Response(status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_review(request,pk):
    data = request.data
    data['product'] = pk
    data['user'] = request.user.id
    serializer = ReviewSerializer(data = data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=201)
    else:
        return Response(serializer.errors,status=400)

class ReviewAuthentication(BasePermission):
    def has_permission(self,request,view):
        pk = view.kwargs['pk']
        review = Review.objects.get(id = pk)
        user_id = review.user_id
        user = request.user
        if user_id == user.id:
            return True
        else:
            return False



@api_view(['PUT'])
@permission_classes([ReviewAuthentication])
def update_review(request,pk):
    data = request.data
    review = Review.objects.get(id = pk)
    data['user'] = review.user_id
    data['product'] = review.product_id
    serializer = ReviewSerializer(data = data ,instance = review ,partial= True)
    if serializer.is_vlalid():
        serializer.save()
        return Response(serializer.data,status = 200)
    else:
        return Response(serializer.errors,status=400)


@api_view(["DELETE"])
@permission_classes([ReviewAuthentication])
def delete_review(request , pk) : 
    try : 
        Review.objects.filter(id = pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Exception as ex : 
        return Response({"detail" : f"error happen {str(ex)}"} , status=400)

#-------------------------------------------------------------------------------
#order functionalities =>


@permission_classes([IsAdminUser])
@api_view(['GET'])
def get_all_orders(request):
    try:
        order = Order.objects.all()
        serializer = OrderSerializer(order,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    except:
        return Response({'error':'you are not authorized'},status=status.HTTP_400_BAD_REQUEST)

class OrderAuthentication(BasePermission):
    def has_permission(self,request,view):
        pk = view.kwargs['pk']
        order = Order.objects.get(id = pk)
        user_id = order.user.id
        user = request.user
        if user_id == user.id:
            return True
        else:
            return False

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_order_by_id(request, pk):
    try:
        order = Order.objects.get(id=pk)
        if request.user == order.user or request.user.is_staff:
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Not authorized to view this order'}, status=status.HTTP_406_NOT_ACCEPTABLE)

    except Order.DoesNotExist:
        return Response({'detail': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

        
@permission_classes([OrderAuthentication])
@api_view(['PUT'])
def UpdateOrderToPaid(request,pk):
    try:
        order = Order.objects.get(id = pk)
        order.is_paid = True
        order.paid_at = datetime.now()
        order.save()
        return Response({'details':'updated successfully'},status=status.HTTP_200_OK)
    except Exception as ex:
        return Response({'error':f'{str(ex)}'},status=status.HTTP_404_NOT_FOUND)



@permission_classes([IsAdminUser])
@api_view(['PUT'])
def UpdateOrderToDelievered(request,pk):
    try:
        order = Order.objects.get(id = pk)
        order.is_delivered = True
        order.delivered_at = datetime.now()
        order.save()
        return Response({'details':'delievered successfully'},status=status.HTTP_200_OK)
    except Order.DoesNotExist:
        return Response({'error':f'{str(ex)}'},status=status.HTTP_404_NOT_FOUND)
    except Exception as ex:
        return Response({'error':f'{str(ex)}'},status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_orders(request):
    try:
        order = Order.objects.filter(user = request.user)
        serializer = OrderSerializer(order,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    except:
        return Response({'error':'you are not authorized'},status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addOrderItems(request):
    try:
        user = request.user
        data = request.data
        order_items = data.get('order_items')
        if not order_items:
            return Response({'detail': 'No order items provided'}, status=status.HTTP_400_BAD_REQUEST)
        order = Order.objects.create(
            user=user,
            payment_method=data.get('payment_method'),
            tax_price=data.get('tax_price'),
            shipping_price=data.get('shipping_price'),
            total_price=data.get('total_price')
        )
        ShippingAddress.objects.create(
            order=order,
            country=data['shipping_address']['country'],
            city=data['shipping_address']['city'],
            postal_code=data['shipping_address']['postal_code']
        )
        for item in order_items:
            try:
                product = Product.objects.get(id=item['product'])
            except Product.DoesNotExist:
                return Response({'detail': f'Product with id {item["product"]} not found'}, status=status.HTTP_404_NOT_FOUND)
            order_item = OrderItem.objects.create(
                order=order,
                quantity=item['quantity'],
                price=item['price']
            )
            order_item.product.add(product)
            product.count_in_stock -= item['quantity']
            product.save()
        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as ex:
        return Response({'error':f'{str(ex)}'},status=status.HTTP_400_BAD_REQUEST)
