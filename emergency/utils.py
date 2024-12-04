from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def send_alert_to_vehicle(vehicle_id, alert_message):
    channel_layer = get_channel_layer()
    
    # Ensure you're sending to the correct group, using the prefix "vehicle_"
    group_name = f"vehicle_{vehicle_id}"
    
    async_to_sync(channel_layer.group_send)(
        group_name,  # Send to the correct group name
        {
            "type": "send_alert",  # This corresponds to the "send_alert" method in your consumer
            "message": alert_message
        }
    )