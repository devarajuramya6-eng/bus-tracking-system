"""
CityBus Enterprise Platform - Real-Time WebSocket & Socket.IO Manager
File: backend/websocket/socket_manager.py
"""

try:
    from flask_socketio import SocketIO, emit, join_room, leave_room
    HAS_SOCKETIO = True
    socketio = SocketIO(cors_allowed_origins="*", async_mode='threading')
except ImportError:
    HAS_SOCKETIO = False
    class MockSocketIO:
        def __init__(self, *args, **kwargs): pass
        def init_app(self, app): pass
        def on(self, event):
            def decorator(f): return f
            return decorator
        def emit(self, event, data=None, room=None, broadcast=False): pass
    socketio = MockSocketIO()


def init_socketio(app):
    """Binds SocketIO to Flask application if available."""
    if HAS_SOCKETIO:
        socketio.init_app(app)
        register_socket_events()
    return socketio


def register_socket_events():
    if not HAS_SOCKETIO:
        return

    from services.auth_service import AuthService
    from services.gps_service import GPSService

    @socketio.on('connect')
    def handle_connect(auth):
        token = auth.get('token') if auth else None
        if token:
            payload = AuthService.verify_token(token)
            if payload:
                role = payload.get('role', 'passenger')
                join_room(f"role:{role}")
                if role in ['dispatcher', 'admin', 'super_admin']:
                    join_room('dispatcher_radar')
        emit('connection_success', {'status': 'connected', 'service': 'CityBus Telemetry Stream'})

    @socketio.on('subscribe')
    def handle_subscribe(data):
        room = data.get('room')
        if room:
            join_room(room)
            emit('subscribed', {'room': room})

    @socketio.on('driver:telemetry')
    def handle_driver_telemetry(data):
        bus_id = data.get('bus_id')
        lat = data.get('latitude')
        lng = data.get('longitude')
        speed = data.get('speed', 0.0)
        heading = data.get('heading', 0.0)

        if bus_id and lat and lng:
            result, _ = GPSService.process_telemetry_ping(bus_id, lat, lng, speed, heading)
            if result:
                socketio.emit('gps:update', result['bus'], room=f"bus:{bus_id}")
                socketio.emit('gps:update', result['bus'], room='dispatcher_radar')


def broadcast_incident_alert(incident_dict):
    if HAS_SOCKETIO:
        socketio.emit('incident:broadcast', incident_dict, broadcast=True)


def broadcast_service_alert(alert_dict):
    if HAS_SOCKETIO:
        socketio.emit('alert:broadcast', alert_dict, broadcast=True)
