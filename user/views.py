from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import mysql.connector
import json, os
from dotenv import load_dotenv
import datetime, jwt, uuid

load_dotenv()

# Create your views here.
def connectDB():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
    
@csrf_exempt
def list_locations(request):
    if request.method == 'GET':
        try:
            connection = connectDB()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Vehicles")
            result = cursor.fetchall()
            return JsonResponse({'success': True, 'message': result}, safe=False)
        except:
            return JsonResponse({'success': False, 'message': 'An Error has occured'}, safe=False)
        finally:
            cursor.close()
            connection.close()
    else:
        return JsonResponse({'success': False, 'message': 'Invalid method'}, safe=False)


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
               user_id = cursor.lastrowid
               secret_key = str(uuid.uuid4())
               cursor.execute("INSERT INTO Clients (vehicle_id, client_id) VALUES (%s, %s)", (user_id, secret_key))
               connection.commit()
               return JsonResponse({'success': True, 'message': 'User Added'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': 'An error occured', 'Exception': str(e)})
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
                secret = os.getenv("JWT_SECRET_KEY")
                TOKEN_EXPIRATION_TIME = 3600 
                payload = {
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=TOKEN_EXPIRATION_TIME)
                }
                token = jwt.encode(payload, secret, algorithm='HS256')
                return JsonResponse({'success': True, 'message': 'User logged In', 'token' : token, 'id': result['vehicle_id']})
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
        
        