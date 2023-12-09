from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from utils.response_message import Message

login = swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Your name'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Your password'),
                'role': openapi.Schema(type=openapi.TYPE_INTEGER, description='Your role'),
            },
            required=['name', 'password','role'],
        ),
        responses={status.HTTP_201_CREATED: Message.login_success},
        operation_description="Login instance with email and password."
    )


signup = swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Your email'),
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Your name'),
                'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description='Your name'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Your password'),
                'confirm_password': openapi.Schema(type=openapi.TYPE_STRING, description='Your password'),
                'document': openapi.Schema(type=openapi.TYPE_ARRAY,items=openapi.Schema(
                type=openapi.TYPE_STRING  # Replace with the actual type of items in the array
            )),
                'occupation': openapi.Schema(type=openapi.TYPE_STRING),
                'is_salaried': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                'own_business': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                'role': openapi.Schema(type=openapi.TYPE_INTEGER),
            },
            required=['name', 'password','role'],
        ),
        responses={status.HTTP_201_CREATED: Message.signup},
    )



manage_property_post = swagger_auto_schema(
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'ul_pin': openapi.Schema(type=openapi.TYPE_STRING, description='Your email'),
            'pincode': openapi.Schema(type=openapi.TYPE_INTEGER, description='Your name'),
            'property_name': openapi.Schema(type=openapi.TYPE_STRING, description='Your name'),
            'address': openapi.Schema(type=openapi.TYPE_STRING, description='Your password'),
            'lattitude': openapi.Schema(type=openapi.TYPE_STRING, description='Your password'),
            'units': openapi.Schema(type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'unit_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'base_rent': openapi.Schema(type=openapi.TYPE_INTEGER),
                'cost': openapi.Schema(type=openapi.TYPE_INTEGER),
            },
            required=['unit_id', 'base_rent', 'cost'],
        )),
            
            'features': openapi.Schema(type=openapi.TYPE_OBJECT),
        },
    ),
    responses={status.HTTP_201_CREATED: Message.property_created},
)


manage_property_get = swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER),
            openapi.Parameter('item', openapi.IN_QUERY, description="Item number", type=openapi.TYPE_INTEGER),
            openapi.Parameter('search', openapi.IN_QUERY, description="search", type=openapi.TYPE_STRING,required=False),
            openapi.Parameter('id', openapi.IN_QUERY, description="id", type=openapi.TYPE_INTEGER,required=False),

        ],
        operation_summary='Manage Property API',
        operation_description='API endpoint to manage properties get',
    )


manage_tenant_get = swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER),
            openapi.Parameter('item', openapi.IN_QUERY, description="Item number", type=openapi.TYPE_INTEGER),
            openapi.Parameter('search', openapi.IN_QUERY, description="search", type=openapi.TYPE_STRING,required=False),
            openapi.Parameter('id', openapi.IN_QUERY, description="id", type=openapi.TYPE_INTEGER,required=False),

        ],
        operation_summary='Manage Tenant API',
        operation_description='API endpoint to manage tenant get',
    )



manage_tenant_post = swagger_auto_schema(
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
           'email': openapi.Schema(type=openapi.TYPE_STRING, description='Your email'),
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Your name'),
                'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description='Your name'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Your password'),
                'confirm_password': openapi.Schema(type=openapi.TYPE_STRING, description='Your password'),
                'document': openapi.Schema(type=openapi.TYPE_ARRAY,items=openapi.Schema(
                type=openapi.TYPE_STRING  
            )),
                'occupation': openapi.Schema(type=openapi.TYPE_STRING),
                'is_salaried': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                'own_business': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                'role': openapi.Schema(type=openapi.TYPE_INTEGER),
            },
        
    ),
    responses={status.HTTP_201_CREATED: Message.property_created},
)



manage_tenant_propertypost = swagger_auto_schema(
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
                'tenant': openapi.Schema(type=openapi.TYPE_INTEGER, description='Your tenant'),
                'properties': openapi.Schema(type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'property': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'duration_days': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'monthly_rent': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'aggrement_date': openapi.Schema(type=openapi.TYPE_STRING),
                },
        )),
                
            },
        
    ),
    responses={status.HTTP_201_CREATED: Message.property_created},
)