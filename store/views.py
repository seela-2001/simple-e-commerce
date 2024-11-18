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
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
# Create your views here.



#product end points
@swagger_auto_schema(
    method='get',
    operation_summary="Retrieve all products",
    operation_description="This endpoint allows administrators to fetch all available products in the database. Only users with admin privileges can access this endpoint.",
    responses={
        200: openapi.Response(
            description="List of all products",
            examples={
                "application/json": [
                    {
                        "id": 1,
                        "name": "Product A",
                        "price": 100.00,
                        "description": "Description of Product A",
                        "stock": 20,
                    },
                    {
                        "id": 2,
                        "name": "Product B",
                        "price": 200.00,
                        "description": "Description of Product B",
                        "stock": 15,
                    }
                ]
            },
        ),
        400: openapi.Response(
            description="Bad Request - Error retrieving products"
        ),
    },
    security=[{"Bearer": []}]
)
@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_all_products(request):
    try:
        products = Product.objects.all()
        serializer = ProductSerializer(products,many = True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    


@swagger_auto_schema(
    method='get',
    operation_summary="Retrieve a specific product by ID",
    operation_description="This endpoint retrieves the details of a specific product using its unique ID. If the product does not exist, a 404 error is returned.",
    manual_parameters=[
        openapi.Parameter(
            'pk',
            openapi.IN_PATH,
            description="The ID of the product to retrieve",
            type=openapi.TYPE_INTEGER,
            required=True
        )
    ],
    responses={
        200: openapi.Response(
            description="Details of the requested product",
            examples={
                "application/json": {
                    "id": 1,
                    "name": "Product A",
                    "price": 100.00,
                    "description": "Description of Product A",
                    "stock": 20,
                }
            }
        ),
        404: openapi.Response(
            description="Not Found - The product with the specified ID does not exist"
        ),
        400: openapi.Response(
            description="Bad Request - Error occurred while processing the request"
        ),
    }
)


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
    


@swagger_auto_schema(
    method='post',
    operation_summary="Create a new product",
    operation_description=(
        "This endpoint allows administrators to create a new product. "
        "The authenticated admin's user ID is automatically associated with the product. "
        "Provide product details in the request body."
    ),
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "name": openapi.Schema(type=openapi.TYPE_STRING, description="The name of the product"),
            "price": openapi.Schema(type=openapi.TYPE_NUMBER, format="float", description="The price of the product"),
            "description": openapi.Schema(type=openapi.TYPE_STRING, description="A description of the product"),
            "stock": openapi.Schema(type=openapi.TYPE_INTEGER, description="The available stock of the product"),
        },
        required=["name", "price", "description", "stock"],
    ),
    responses={
        201: openapi.Response(
            description="Product successfully created",
            examples={
                "application/json": {
                    "id": 1,
                    "name": "Product A",
                    "price": 100.00,
                    "description": "Description of Product A",
                    "stock": 20,
                    "user": 1
                }
            },
        ),
        400: openapi.Response(
            description="Bad Request - Invalid input data or error during processing",
            examples={
                "application/json": {
                    "details": "error happen [error message]"
                }
            },
        ),
    },
    security=[{"Bearer": []}],
)


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
    


@swagger_auto_schema(
    method='put',
    operation_summary="Update an existing product",
    operation_description=(
        "This endpoint allows administrators to update the details of an existing product "
        "by providing the product ID and the updated data. Partial updates are supported."
    ),
    manual_parameters=[
        openapi.Parameter(
            'pk',
            openapi.IN_PATH,
            description="The ID of the product to update",
            type=openapi.TYPE_INTEGER,
            required=True,
        )
    ],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "name": openapi.Schema(type=openapi.TYPE_STRING, description="The updated name of the product"),
            "price": openapi.Schema(type=openapi.TYPE_NUMBER, format="float", description="The updated price of the product"),
            "description": openapi.Schema(type=openapi.TYPE_STRING, description="The updated description of the product"),
            "stock": openapi.Schema(type=openapi.TYPE_INTEGER, description="The updated stock of the product"),
        },
    ),
    responses={
        200: openapi.Response(
            description="Product successfully updated",
            examples={
                "application/json": {
                    "id": 1,
                    "name": "Updated Product A",
                    "price": 120.00,
                    "description": "Updated description of Product A",
                    "stock": 25,
                    "user": 1
                }
            },
        ),
        400: openapi.Response(
            description="Bad Request - Invalid input data",
            examples={
                "application/json": {
                    "name": ["This field is required."],
                    "price": ["This field must be a number."]
                }
            },
        ),
        404: openapi.Response(
            description="Not Found - The product with the specified ID does not exist",
            examples={
                "application/json": {
                    "error": "no such product"
                }
            },
        ),
    },
    security=[{"Bearer": []}],
)

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



@swagger_auto_schema(
    method='delete',
    operation_summary="Delete a product",
    operation_description=(
        "This endpoint allows administrators to delete a product by providing its ID. "
        "Only users with admin privileges can access this endpoint."
    ),
    manual_parameters=[
        openapi.Parameter(
            'pk',
            openapi.IN_PATH,
            description="The ID of the product to delete",
            type=openapi.TYPE_INTEGER,
            required=True,
        )
    ],
    responses={
        204: openapi.Response(
            description="Product successfully deleted",
        ),
        400: openapi.Response(
            description="Bad Request - Error occurred while attempting to delete the product",
            examples={
                "application/json": {
                    "error": "error message"
                }
            },
        ),
    },
    security=[{"Bearer": []}],
)
@permission_classes([IsAdminUser])
@api_view(['DELETE'])
def delete_product(request , pk):
    try:
        Product.objects.filter(id = pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Exception as ex:
        return Response({'error':f'{str(ex)}'})



@swagger_auto_schema(
    method='post',
    operation_summary="Upload an image for a product",
    operation_description=(
        "This endpoint allows authenticated users to upload an image for a specific product. "
        "The product is identified by its unique ID, provided in the path parameter. "
        "The image file should be included in the `image` field of the request."
    ),
    manual_parameters=[
        openapi.Parameter(
            'pk',
            openapi.IN_PATH,
            description="The ID of the product to upload the image for",
            type=openapi.TYPE_INTEGER,
            required=True,
        ),
    ],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'image': openapi.Schema(
                type=openapi.TYPE_STRING,
                format='binary',
                description="The image file to upload"
            )
        },
        required=['image'],
    ),
    responses={
        200: openapi.Response(
            description="Image successfully uploaded and associated with the product",
            examples={
                "application/json": {
                    "id": 1,
                    "name": "Product A",
                    "price": 100.00,
                    "description": "Description of Product A",
                    "stock": 20,
                    "image": "http://example.com/media/product_images/product_a.jpg"
                }
            }
        ),
        400: openapi.Response(
            description="Bad Request - No image file provided in the request",
            examples={
                "application/json": {
                    "error": "No image file found in the request."
                }
            }
        ),
        404: openapi.Response(
            description="Not Found - Product with the specified ID does not exist",
        ),
    },
    security=[{"Bearer": []}],
)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_image(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if 'image' not in request.FILES:
        return Response({"error": "No image file found in the request."},
                        status=status.HTTP_400_BAD_REQUEST)
    product.image = request.FILES['image']
    product.save()
    serializer = ProductSerializer(product)
    return Response(serializer.data, status=status.HTTP_200_OK)




@swagger_auto_schema(
    method='get',
    operation_summary="Search for products",
    operation_description=(
        "This endpoint allows authenticated users to search for products based on a search parameter. "
        "The search checks if the product's name or description contains the specified parameter (case-insensitive)."
    ),
    manual_parameters=[
        openapi.Parameter(
            'search_param',
            openapi.IN_PATH,
            description="The search parameter used to filter products by name or description",
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    responses={
        200: openapi.Response(
            description="A list of products matching the search parameter",
            examples={
                "application/json": [
                    {
                        "id": 1,
                        "name": "Product A",
                        "price": 100.00,
                        "description": "Description of Product A",
                        "stock": 20,
                        "image": "http://example.com/media/product_images/product_a.jpg",
                    },
                    {
                        "id": 2,
                        "name": "Product B",
                        "price": 150.00,
                        "description": "Description of Product B",
                        "stock": 10,
                        "image": "http://example.com/media/product_images/product_b.jpg",
                    }
                ]
            },
        ),
        401: openapi.Response(
            description="Unauthorized - Authentication credentials were not provided or invalid",
        ),
    },
    security=[{"Bearer": []}],
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_products(request,search_param ):
    products = Product.objects.filter(
        Q(name__icontains=search_param) | Q(description__icontains=search_param)
    )
    serializer = ProductSerializer(products, many=True) 
    return Response(serializer.data, status=status.HTTP_200_OK)

#-------------------------------------------------------------------------------------------------



@swagger_auto_schema(
    method="get",
    operation_summary="Get reviews for a product",
    operation_description=(
        "This endpoint allows authenticated users to retrieve all reviews for a specific product. "
        "The product is identified by its unique ID provided in the path parameter."
    ),
    manual_parameters=[
        openapi.Parameter(
            'pk',
            openapi.IN_PATH,
            description="The ID of the product whose reviews are to be retrieved",
            type=openapi.TYPE_INTEGER,
            required=True,
        )
    ],
    responses={
        200: openapi.Response(
            description="A list of reviews for the specified product",
            examples={
                "application/json": [
                    {
                        "id": 1,
                        "product_id": 10,
                        "user_id": 5,
                        "rating": 4,
                        "comment": "Great product!",
                        "created_at": "2024-11-18T10:30:00Z"
                    },
                    {
                        "id": 2,
                        "product_id": 10,
                        "user_id": 8,
                        "rating": 5,
                        "comment": "Highly recommend!",
                        "created_at": "2024-11-17T14:15:00Z"
                    }
                ]
            }
            ),
        400: openapi.Response(
            description="Bad Request - An error occurred while retrieving reviews",
        ),
        401: openapi.Response(
            description="Unauthorized - Authentication credentials were not provided or invalid",
        ),
    },
    security=[{"Bearer": []}],
)
@api_view(["GET"])    
@permission_classes([IsAuthenticated])
def get_product_reviews(request , pk) : 
    try : 
        reviews = Review.objects.filter(product_id = pk ) 
        serializer = ReviewSerializer(reviews , many = True) 
        return Response(serializer.data , status=200)
    except :
        return Response(status=400)




@swagger_auto_schema(
    method="post",
    operation_summary="Create a review for a product",
    operation_description=(
        "This endpoint allows authenticated users to create a review for a specific product. "
        "The review includes fields such as rating and comment. The product is identified by its unique ID "
        "provided in the path parameter, and the user's ID is automatically associated with the review."
    ),
    manual_parameters=[
        openapi.Parameter(
            'pk',
            openapi.IN_PATH,
            description="The ID of the product to review",
            type=openapi.TYPE_INTEGER,
            required=True,
        ),
    ],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "rating": openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description="The rating for the product (e.g., 1 to 5)",
                example=5,
            ),
            "comment": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="A comment or feedback about the product",
                example="This product is amazing!",
            ),
        },
        required=["rating"],
    ),
    responses={
        201: openapi.Response(
            description="Review successfully created",
            examples={
                "application/json": {
                    "id": 1,
                    "product": 10,
                    "user": 5,
                    "rating": 5,
                    "comment": "This product is amazing!",
                    "created_at": "2024-11-18T10:30:00Z"
                }
            }
        ),
        400: openapi.Response(
            description="Bad Request - Validation errors occurred while creating the review",
            examples={
                "application/json": {
                    "rating": ["This field is required."]
                }
            },
        ),
        401: openapi.Response(
            description="Unauthorized - Authentication credentials were not provided or invalid",
        ),
    },
    security=[{"Bearer": []}],
)
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


@swagger_auto_schema(
    method="put",
    operation_summary="Update a review",
    operation_description=(
        "This endpoint allows the creator of a review to update it. Access is restricted "
        "to the user who created the review. The review is identified by its ID."
    ),
    manual_parameters=[
        openapi.Parameter(
            'pk',
            openapi.IN_PATH,
            description="The ID of the review to be updated",
            type=openapi.TYPE_INTEGER,
            required=True,
        ),
    ],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "rating": openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description="The updated rating for the product (e.g., 1 to 5)",
                example=4,
            ),
            "comment": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="The updated comment for the product",
                example="Updated feedback about this product.",
            ),
        },
        required=["rating"],
    ),
    responses={
        200: openapi.Response(
            description="Review successfully updated",
            examples={
                "application/json": {
                    "id": 1,
                    "product": 10,
                    "user": 5,
                    "rating": 4,
                    "comment": "Updated feedback about this product.",
                    "created_at": "2024-11-18T10:30:00Z",
                }
            },
        ),
        400: openapi.Response(
            description="Bad Request - Validation errors occurred while updating the review",
        ),
        403: openapi.Response(
            description="Forbidden - The user is not authorized to update this review",
        ),
        404: openapi.Response(
            description="Not Found - The review with the specified ID does not exist",
        ),
    },
    security=[{"Bearer": []}],
)

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




@swagger_auto_schema(
    method="delete",
    operation_summary="Delete a review",
    operation_description=(
        "This endpoint allows an authenticated user to delete their own review for a product. "
        "Access is restricted to the user who created the review, as enforced by the `ReviewAuthentication` permission."
    ),
    manual_parameters=[
        openapi.Parameter(
            'pk',
            openapi.IN_PATH,
            description="The ID of the review to be deleted",
            type=openapi.TYPE_INTEGER,
            required=True,
        ),
    ],
    responses={
        204: openapi.Response(
            description="Review successfully deleted",
        ),
        400: openapi.Response(
            description="Bad Request - Error occurred while attempting to delete the review",
            examples={
                "application/json": {
                    "detail": "error happen [error details]"
                }
            },
        ),
        403: openapi.Response(
            description="Forbidden - The user is not authorized to delete this review",
        ),
        404: openapi.Response(
            description="Not Found - The review with the specified ID does not exist",
        ),
    },
    security=[{"Bearer": []}],
)
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



@swagger_auto_schema(
    method="get",
    operation_summary="Get all orders",
    operation_description=(
        "This endpoint allows admin users to retrieve a list of all orders in the system. "
        "Only users with admin privileges have access to this endpoint."
    ),
    responses={
        200: openapi.Response(
            description="A list of all orders",
            examples={
                "application/json": [
                    {
                        "id": 1,
                        "user": 5,
                        "total_price": 150.00,
                        "status": "completed",
                        "created_at": "2024-11-18T10:30:00Z"
                    },
                    {
                        "id": 2,
                        "user": 8,
                        "total_price": 220.00,
                        "status": "pending",
                        "created_at": "2024-11-17T14:15:00Z"
                    }
                ]
            }
        ),
        400: openapi.Response(
            description="Bad Request - Unauthorized access or other errors",
            examples={
                "application/json": {
                    "error": "you are not authorized"
                }
            }
        ),
        403: openapi.Response(
            description="Forbidden - The user does not have the necessary admin permissions",
        ),
    },
    security=[{"Bearer": []}],
)

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




@swagger_auto_schema(
    method="get",
    operation_summary="Get order details by ID",
    operation_description=(
        "This endpoint allows authenticated users to retrieve the details of an order. "
        "A user can view their own orders, or an admin (staff) can view any order. "
        "If the user is not authorized to view the order, a 406 error is returned."
    ),
    manual_parameters=[
        openapi.Parameter(
            'pk',
            openapi.IN_PATH,
            description="The ID of the order to retrieve",
            type=openapi.TYPE_INTEGER,
            required=True,
        ),
    ],
    responses={
        200: openapi.Response(
            description="Order details successfully retrieved",
            examples={
                "application/json": {
                    "id": 1,
                    "user": 5,
                    "total_price": 150.00,
                    "status": "completed",
                    "created_at": "2024-11-18T10:30:00Z",
                    "updated_at": "2024-11-18T12:00:00Z"
                }
            }
        ),
        406: openapi.Response(
            description="Not Acceptable - The user is not authorized to view this order",
            examples={
                "application/json": {
                    "detail": "Not authorized to view this order"
                }
            }
        ),
        404: openapi.Response(
            description="Order Not Found - The order with the specified ID does not exist",
            examples={
                "application/json": {
                    "detail": "Order not found"
                }
            }
        ),
    },
    security=[{"Bearer": []}],
)
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

        


@swagger_auto_schema(
    method="put",
    operation_summary="Update order status to paid",
    operation_description=(
        "This endpoint allows authorized users to mark an order as paid. "
        "The `OrderAuthentication` permission ensures that the user has the necessary rights to update the order status."
        "Once the order is marked as paid, the `is_paid` flag is set to `True` and the `paid_at` timestamp is updated."
    ),
    manual_parameters=[
        openapi.Parameter(
            'pk',
            openapi.IN_PATH,
            description="The ID of the order to update",
            type=openapi.TYPE_INTEGER,
            required=True,
        ),
    ],
    responses={
        200: openapi.Response(
            description="Order updated successfully",
            examples={
                "application/json": {
                    "details": "updated successfully"
                }
            }
        ),
        404: openapi.Response(
            description="Not Found - The order with the specified ID does not exist",
            examples={
                "application/json": {
                    "error": "error message describing the issue"
                }
            }
        ),
        403: openapi.Response(
            description="Forbidden - The user is not authorized to update the order",
        ),
    },
    security=[{"Bearer": []}],
)
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



@swagger_auto_schema(
    method="put",
    operation_summary="Update order status to delivered",
    operation_description=(
        "This endpoint allows admin users to update the order status to 'delivered'. "
        "The `is_delivered` flag is set to `True`, and the `delivered_at` timestamp is updated. "
        "This action can only be performed by an admin user."
    ),
    manual_parameters=[
        openapi.Parameter(
            'pk',
            openapi.IN_PATH,
            description="The ID of the order to update",
            type=openapi.TYPE_INTEGER,
            required=True,
        ),
    ],
    responses={
        200: openapi.Response(
            description="Order successfully marked as delivered",
            examples={
                "application/json": {
                    "details": "delivered successfully"
                }
            }
        ),
        404: openapi.Response(
            description="Order Not Found - The order with the specified ID does not exist",
            examples={
                "application/json": {
                    "error": "error message describing the issue"
                }
            }
        ),
        400: openapi.Response(
            description="Bad Request - The request cannot be processed due to a server error",
            examples={
                "application/json": {
                    "error": "error message describing the issue"
                }
            }
        ),
        403: openapi.Response(
            description="Forbidden - The user is not authorized to update the order",
        ),
    },
    security=[{"Bearer": []}],
)
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





@swagger_auto_schema(
    method="get",
    operation_summary="Get all orders for the authenticated user",
    operation_description=(
        "This endpoint allows authenticated users to retrieve all orders associated with their account. "
        "The response contains a list of orders placed by the authenticated user."
    ),
    responses={
        200: openapi.Response(
            description="List of orders retrieved successfully",
            examples={
                "application/json": [
                    {
                        "id": 1,
                        "user": 5,
                        "total_price": 150.00,
                        "status": "completed",
                        "created_at": "2024-11-18T10:30:00Z",
                        "updated_at": "2024-11-18T12:00:00Z"
                    }
                ]
            }
        ),
        400: openapi.Response(
            description="Bad Request - User is not authorized to view orders",
            examples={
                "application/json": {
                    "error": "you are not authorized"
                }
            }
        ),
    },
    security=[{"Bearer": []}],
)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_orders(request):
    try:
        order = Order.objects.filter(user = request.user)
        serializer = OrderSerializer(order,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    except:
        return Response({'error':'you are not authorized'},status=status.HTTP_400_BAD_REQUEST)






@swagger_auto_schema(
    method="post",
    operation_summary="Add order items and create a new order",
    operation_description=(
        "This endpoint allows authenticated users to create a new order by adding order items. "
        "It accepts order details including product name, quantity, price, shipping address, "
        "payment method, and additional charges like tax and shipping. The order items are validated "
        "against the products in the system and stock is adjusted accordingly. "
        "A new order is created, and the total price is calculated after deducting the tax price."
    ),
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'order_items': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'product': openapi.Schema(type=openapi.TYPE_STRING, description="Product name"),
                        'quantity': openapi.Schema(type=openapi.TYPE_INTEGER, description="Quantity of the product"),
                        'price': openapi.Schema(type=openapi.TYPE_NUMBER, description="Price of the product per unit")
                    }
                ),
                description="List of order items, each containing product, quantity, and price."
            ),
            'payment_method': openapi.Schema(type=openapi.TYPE_STRING, description="Method of payment (e.g., Credit Card, PayPal)"),
            'tax_price': openapi.Schema(type=openapi.TYPE_NUMBER, description="Tax price applied to the order"),
            'shipping_price': openapi.Schema(type=openapi.TYPE_NUMBER, description="Shipping price for the order"),
            'shipping_address': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'country': openapi.Schema(type=openapi.TYPE_STRING, description="Shipping country"),
                    'city': openapi.Schema(type=openapi.TYPE_STRING, description="Shipping city"),
                    'postal_code': openapi.Schema(type=openapi.TYPE_STRING, description="Shipping postal code"),
                },
                description="Shipping address for the order"
            ),
        },
        required=['order_items', 'payment_method', 'tax_price', 'shipping_address']
    ),
    responses={
        201: openapi.Response(
            description="Order created successfully",
            examples={
                "application/json": {
                    "id": 1,
                    "user": 5,
                    "total_price": 150.00,
                    "payment_method": "Credit Card",
                    "shipping_price": 50.00,
                    "tax_price": 20.00,
                    "status": "pending",
                    "created_at": "2024-11-18T10:30:00Z",
                    "updated_at": "2024-11-18T12:00:00Z",
                    "shipping_address": {
                        "country": "USA",
                        "city": "New York",
                        "postal_code": "10001"
                    },
                    "order_items": [
                        {
                            "product": "Product 1",
                            "quantity": 2,
                            "price": 50.00
                        }
                    ]
                }
            }
        ),
        400: openapi.Response(
            description="Bad Request - Missing or incorrect data in the request",
            examples={
                "application/json": {
                    "error": "Product with name Product 1 not found"
                }
            }
        ),
        404: openapi.Response(
            description="Product Not Found - A product mentioned in the order does not exist",
            examples={
                "application/json": {
                    "detail": "Product with name Product 1 not found"
                }
            }
        ),
    },
    security=[{"Bearer": []}],
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addOrderItems(request):
    try:
        user = request.user
        data = request.data

        order_items = data.get('order_items')
        if not order_items:
            return Response({'detail': 'No order items provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Create Order
        order = Order.objects.create(
            user=user,
            payment_method=data.get('payment_method'),
            tax_price=data.get('tax_price'),
            shipping_price=data.get('shipping_price', 50),  # Default to 50 if not provided
        )

        # Create Shipping Address
        ShippingAddress.objects.create(
            order=order,
            country=data['shipping_address']['country'],
            city=data['shipping_address']['city'],
            postal_code=data['shipping_address']['postal_code']
        )
        total_price = 0

        for item in order_items:
            try:
                product = Product.objects.get(name=item['product'])
            except Product.DoesNotExist:
                return Response({'detail': f'Product with name {item["product"]} not found'}, status=status.HTTP_404_NOT_FOUND)

            item_total = item['quantity'] * item['price']
            total_price += item_total

            order_item = OrderItem.objects.create(
                order=order,
                quantity=item['quantity'],
                price=item['price']
            )
            order_item.product.add(product)

            product.count_in_stock -= item['quantity']
            product.save()

        order.total_price = total_price - order.tax_price
        order.save()

        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except Exception as ex:
        return Response({'error': f'{str(ex)}'}, status=status.HTTP_400_BAD_REQUEST)
