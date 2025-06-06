from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import mysql.connector, json, os
from geopy.geocoders import ArcGIS, Nominatim
import openrouteservice as ors
from dotenv import load_dotenv
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .utils import send_alert_to_vehicle
import paho.mqtt.client as mqtt

geolocator = Nominatim(user_agent="geoapi")

load_dotenv()

MQTT_BROKER = "3.220.33.61"
MQTT_PORT = 1883
MQTT_TOPIC = "traffic/light/control"
client = mqtt.Client()
connected = False

def connect_mqtt():
    global connected
    if not connected:
        try:
            client.connect(MQTT_BROKER, MQTT_PORT)
            client.loop_start()
            connected = True
            print("MQTT connected")
        except Exception as e:
            print(f"MQTT connection failed: {e}")

def send_msg_mqtt(message):
    if not connected:
        connect_mqtt()
    try:
        client.publish(MQTT_TOPIC, message)
        print(f"Published MQTT message: {message}")
    except Exception as e:
        print(f"MQTT publish failed: {e}")

# Create your views here.
def connectDB():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

@csrf_exempt
def locations(request):
    connection = None
    cursor = None
    if request.method == 'GET':
        try:
            connection = connectDB()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                "SELECT vehicle_id, latitude, longitude, timestamp "
                "FROM VehicleLocations "
                "WHERE timestamp >= NOW() - INTERVAL 5 MINUTE"
            )
            result = cursor.fetchall()
            return JsonResponse({'success': True, 'locations': result})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    else:
        return JsonResponse({'success': False, 'message': 'Invalid METHOD'})


def destination_location(dest):
    nom = ArcGIS()
    dest_coord = list(nom.geocode(dest))
    dest_coord = list(dest_coord[1])
    dest_coord[0], dest_coord[1] = dest_coord[1], dest_coord[0]
    return dest_coord

def finalroute(s, e):
    client = ors.Client(key = '5b3ce3597851110001cf6248a1038de5c5304bb39fdff93c8db3113d')
    coords = [s, e]
    route = client.directions(coordinates = coords,
                             profile = 'driving-car',
                             format = 'geojson')
    time = route['features'][0]['properties']['segments'][0]['duration']
    directions = route['features'][0]['geometry']['coordinates']
    return  time, directions

@csrf_exempt
def alert(request):
    connection = None
    cursor = None
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            dest = data.get('destination')
            ilat = data.get('latitude')
            ilng = data.get('longitude')
            ambulance_location = geolocator.reverse((float(ilat), float(ilng)))
            print("Ambulance Location: ", ambulance_location)
            if isinstance(dest, dict):
                destination = [float(dest['lng']), float(dest['lat'])]
            else:
                destination = destination_location(dest)
            print("Destination: ", destination)
            current = [float(ilng), float(ilat)]
            connection = connectDB()
            cursor = connection.cursor(dictionary=True, buffered=True)
            cursor.execute(
                "SELECT vehicle_id, latitude, longitude "
                "FROM VehicleLocations "
                "WHERE timestamp >= NOW() - INTERVAL 10 MINUTE"
            )
            result = cursor.fetchall()
            time, route = finalroute(current, destination)
            print(route)
            print("Result: ", result)
            vehicles = []
            if result:
                for coord in route:
                    for x in result:
                        pos = [float(x['longitude']), float(x['latitude'])]  
                        if proximity(pos, coord):
                            vehicles.append(x['vehicle_id'])
            
                print("Vehicles: ", vehicles)
                if vehicles:
                    unique = []
                    for v in vehicles:
                        if v not in unique:
                            unique.append(v)
                    vehicle_str = ', '.join(map(str, unique))
                    print("Vehicles in route: ",vehicle_str)
                    #cursor.execute("SELECT client_id FROM CLIENTS WHERE vehicle_id IN (%s)", vehicle_str)
                    #client_ids = cursor.fetchall()
                    send_msg_mqtt(f'AMBULANCE INCOMING IN {time} seconds')
                    for vehicle in unique:
                        try:
                            print(f"Sending alert to vehicle {vehicle}")
                            send_alert_to_vehicle(vehicle, f'Ambulance Incomings')
                        except  Exception as ve:
                            print(f"Error sending alert to vehicle {vehicle}: {ve}")
                    return JsonResponse({'success': True, 'message': f"Vehicles found on route are {vehicle_str}"})
                else:
                    return JsonResponse({'success': False, 'message': "No vehicles found at the route"})
            else:
                return JsonResponse({'success': True, 'message':'No vehicles active at the moment'})              
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
        finally:
            if cursor: 
                cursor.close()
            if connection:
                connection.close()
    else:
        return JsonResponse({'success': False, 'message':'Invalid method'})
    
@csrf_exempt
def test(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            vehicle_ids = body.get('vehicle_ids')
            message = body.get('message')

            if not vehicle_ids or not message:
                return JsonResponse({'error': 'vehicle_ids and message are required'}, status=400)

            send_alert_to_vehicles(vehicle_ids, message)
            return JsonResponse({'success': True, 'message': 'Alert sent'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=405)
            
def proximity(coord1, coord2, threshold=0.0001):
    return abs(coord1[0] - coord2[0]) < threshold and abs(coord1[1] - coord2[1]) < threshold   

def send_alert_to_vehicles(vehicle_ids, message):
    channel_layer = get_channel_layer()
    for vehicle_id in vehicle_ids:
        async_to_sync(channel_layer.group_send)(
            f'vehicle_{vehicle_id}',  # Group name for each vehicle
            {
                'type': 'send_alert',
                'message': message
            }
        )     
            
            