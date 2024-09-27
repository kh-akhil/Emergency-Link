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
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
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
            current = [float(ilng), float(ilat)]
            connection = connectDB()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                "SELECT vehicle_id, latitude, longitude "
                "FROM VehicleLocations "
                "WHERE timestamp >= NOW() - INTERVAL 20 MINUTE"
            )
            route = finalroute(current, destination)
            result = cursor.fetchall()
            vehicles = []
            if result:
                for coord in route:
                    for x in result:
                        pos = [float(x['longitude']), float(x['latitude'])]  
                        if proximity(pos, coord):
                            vehicles.append(x['vehicle_id'])
                
                if vehicles:
                    vehicle_str = ', '.join(map(str, vehicles))
                    return JsonResponse({'success': True, 'message': f"Vehicles found on route are {vehicle_str}"})
                else:
                    return JsonResponse({'success': False, 'message': "No vehicles found at the route"})
            else:
                return JsonResponse({'success': True, 'message':'No vehicles active at the moment'})              
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
        finally:
            cursor.close()
            connection.close()
    else:
        return JsonResponse({'success': False, 'message':'Invalid method'})
            
def proximity(coord1, coord2, threshold=0.0001):
    return abs(coord1[0] - coord2[0]) < threshold and abs(coord1[1] - coord2[1]) < threshold        
            
            