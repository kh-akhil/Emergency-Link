from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import mysql.connector
import json

# Create your views here.
def connectDB():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="akhil007",
        database="V2V"
    )
    
@csrf_exempt
def list_locations(request):
    connection = connectDB()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Vehicles")
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return JsonResponse({'message': result}, safe=False)

@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            name = data.get('name')
            if not all([email, password, name]):
                return JsonResponse({'success': False, 'message':'Insufficient data'})
            connection = connectDB()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Vehicles WHERE email=%s", (email,))
            result = cursor.fetchall()
            if len(result) > 0:
                return JsonResponse({'success': False, 'message': 'Email already exists'})
            else:
               cursor.execute("INSERT INTO Vehicles (owner_name, email, password) VALUES (%s, %s, %s)", (name, email, password))
               connection.commit()
               return JsonResponse({'success': True, 'message': 'User Added'})
        except:
            return JsonResponse({'success': False, 'message': 'An error occured'})
        finally:
            cursor.close()
            connection.close()
    else:
        return JsonResponse({'success': False, 'message': 'Invalid METHOD'})
            
@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            if not all([email, password]):
                return JsonResponse({'success': False, 'message':'Insufficient data'})
            connection = connectDB()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Vehicles WHERE email=%s", (email,))
            result = cursor.fetchone()
            if result == None :
                return JsonResponse({'success': False, 'message': 'User does not exist'})
            if result['password'] == password:
                return JsonResponse({'success': True, 'message': 'User logged In'})
            else:
                return JsonResponse({'success': False, 'message': 'Invalid Credentials'})
        except:
            return JsonResponse({'success': False, 'message': 'An error occured'})
        finally:
            cursor.close()
            connection.close()
    else:
        return JsonResponse({'success': False, 'message': 'Invalid METHOD'})

@csrf_exempt
def insert_location(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            v_id = data.get('id')
            lat = data.get('lat')
            lng = data.get('lng')
            if not all([v_id, lat, lng]):
                return JsonResponse({'success': False, 'message':'Insufficient data'})
            connection = connectDB()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("INSERT INTO VehicleLocations (vehicle_id, latitude, longitude) VALUES (%s, %s, %s)" , (v_id, lat, lng))
            connection.commit()
            return JsonResponse({'success': True, 'message': 'New Location Added'})
        except:
            return JsonResponse({'success': False, 'message': 'An error occured'})
        finally:
            cursor.close()
            connection.close()
    else:
        return JsonResponse({'success': False, 'message': 'Invalid METHOD'})
        
        