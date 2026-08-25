"""
CityBus Enterprise Platform - WebSocket Package Init
File: backend/websocket/__init__.py
"""

from websocket.socket_manager import socketio, init_socketio

__all__ = ['socketio', 'init_socketio']
