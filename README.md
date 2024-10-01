# Order Management System


The **Order Management System** is a Django-based web application designed to handle customer orders for restaurants. It includes features such as placing orders, assigning orders, and updating the order status using background tasks with Django Q.





## **Features**

Customers can place orders from restaurants.

Restaurants can manage and update order statuses.

Order status updates are handled asynchronously using Django Q.

Caching of order details using Redis.






## **Technologies**

**Backend:** Django 3.2, Django REST Framework

**Task Queue:** Django Q

**Cache:** Redis

**Database:** SQLite

**Others:** Python 3.11






## **Installation**

**1. Clone the repository:**
  1. https://github.com/Akshay78980/order-management-system.git
```     
cd order-management-system
```

**2. Create or activate a virtual environment**
```
virtualenv .venv
source .venv/bin/activate
```

**3. Install dependencies:**
```
pip install -r requirements.txt
```

**4. Set up the database:**
  1. Configure the database settings in settings.py.
  2. Run migrations:
```        
python manage.py migrate
```
    
**5. Set up Redis:**
  1. Make sure Redis is running locally at localhost:6379.
  2. If needed, adjust the Redis location in settings.py

**6. Run the development server:**
```
python manage.py runserver
```
    
**7. Start Django Q Cluster:**
```
python manage.py qcluster
```



## **Usage**

To use the Order Management System, start by creating customers, restaurants, and items using the Django admin interface




## **API Endpoints**

Here are the key API endpoints:

### **Place an Order**

```
POST /api/orders/create/
```

Request body:
```
{
  "customer_id": 1,
  "restaurant_id": 2,
  "items": [
    {
      "item_id": 4,
      "quantity": 2
    },
    {
      "item_id": 5,
      "quantity": 1
    }
  ]
}
```

### **Update Order Status**

```
PATCH /api/orders/<order_id>/update_status/
```

Request body:

```
{
  "order_status": "picked"
}
```

### **Detailed View of Order**

```
GET /api/orders/<order_id>/
```



## **Background Task Implementation**

The order status update is handled using Django Q's background tasks. You can find the task definition in tasks.py.

### **Example task for updating order status:**

```
def update_order_status(order_id, new_status):
    print("Updating the order status.")
    order = Order.objects.get(id=order_id)
    
    if order:
        order.order_status = new_status
        order.save()
        
        return "Order status updated."
    else:
        return "Order doesnot exist."
```


To schedule an order status update, the UpdateOrderStatusView in views.py uses Django Q’s schedule function:

```
schedule(
    'orders.tasks.update_order_status',
    order_id,
    new_status,
    schedule_type='O'  # Runs once
)
```






 
