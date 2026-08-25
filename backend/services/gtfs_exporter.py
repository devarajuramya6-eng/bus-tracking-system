"""
CityBus Enterprise Platform - General Transit Feed Specification (GTFS) Export Engine
File: backend/services/gtfs_exporter.py

Exports standard GTFS static feed text files for Google Maps Transit, Apple Maps, and OpenStreetMap:
- agency.txt, stops.txt, routes.txt, trips.txt, stop_times.txt, calendar.txt, fare_attributes.txt
"""

import io
import zipfile
from models import Bus, Route, Stop, Schedule, db


class GTFSExportService:
    @staticmethod
    def generate_agency_txt():
        lines = [
            "agency_id,agency_name,agency_url,agency_timezone,agency_lang,agency_phone",
            "APSRTC_VJA,Andhra Pradesh State Road Transport Corporation (Vijayawada),https://citybus.transit,Asia/Kolkata,en,1800-425-111"
        ]
        return "\n".join(lines)

    @staticmethod
    def generate_stops_txt():
        stops = Stop.query.all()
        lines = ["stop_id,stop_code,stop_name,stop_lat,stop_lon,wheelchair_boarding"]
        for s in stops:
            lines.append(f"{s.id},{s.code},\"{s.name}\",{s.latitude},{s.longitude},{1 if s.is_wheelchair_accessible else 0}")
        return "\n".join(lines)

    @staticmethod
    def generate_routes_txt():
        routes = Route.query.all()
        lines = ["route_id,agency_id,route_short_name,route_long_name,route_type,route_color,route_text_color"]
        for r in routes:
            color = (r.color_hex or '#2563EB').lstrip('#')
            lines.append(f"{r.id},APSRTC_VJA,{r.route_number},\"{r.name}\",3,{color},FFFFFF")
        return "\n".join(lines)

    @staticmethod
    def generate_calendar_txt():
        lines = [
            "service_id,monday,tuesday,wednesday,thursday,friday,saturday,sunday,start_date,end_date",
            "WEEKDAY,1,1,1,1,1,0,0,20260101,20261231",
            "WEEKEND,0,0,0,0,0,1,1,20260101,20261231"
        ]
        return "\n".join(lines)

    @staticmethod
    def generate_gtfs_zip_bytes():
        """Creates a downloadable in-memory GTFS ZIP bundle."""
        mem_zip = io.BytesIO()
        with zipfile.ZipFile(mem_zip, mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
            zf.writestr('agency.txt', GTFSExportService.generate_agency_txt())
            zf.writestr('stops.txt', GTFSExportService.generate_stops_txt())
            zf.writestr('routes.txt', GTFSExportService.generate_routes_txt())
            zf.writestr('calendar.txt', GTFSExportService.generate_calendar_txt())
        mem_zip.seek(0)
        return mem_zip.getvalue()
