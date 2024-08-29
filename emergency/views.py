from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import mysql.connector, json, os
from geopy.geocoders import ArcGIS
import openrouteservice as ors
from dotenv import load_dotenv

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
def locations(request):
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
        except:
            return JsonResponse({'success': False, 'message': 'An error occured'})
        finally:
            cursor.close()
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
    return route['features'][0]['geometry']['coordinates'] 

@csrf_exempt
def alert(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            dest = data.get('destination')
            ilat = data.get('latitude')
            ilng = data.get('longitude')
            destination = destination_location(dest)
            current = [ilng, ilat]
            connection = connectDB()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                "SELECT vehicle_id, latitude, longitude"
                "FROM VehicleLocations "
                "WHERE timestamp >= NOW() - INTERVAL 5 MINUTE"
            )
            route = finalroute(current, destination)
            result = cursor.fetchall()
            print("result :"  , result)
            if result:
                vehicles = []
                for coord in route:
                    for x in result:
                        pos = [x['longitude'], x['latitude']]  
                        if pos == coord:
                            vehicles.append(x['vehicle_id'])
            else:
                return JsonResponse({'success': True, 'message':'No vehicles found in route'})
            return JsonResponse({'success': True, 'Vehicles found': vehicles})              
        except:
            return JsonResponse({'success': False, 'message':'error'})
        finally:
            cursor.close()
            connection.close()
    else:
        return JsonResponse({'success': False, 'message':'Invalid method'})
            
            
            
            