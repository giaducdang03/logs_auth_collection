from __future__ import annotations

from datetime import datetime, timedelta
from ipaddress import ip_address
import json
import logging
from typing import Dict, Optional, Tuple
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


_CACHE: Dict[str, Tuple[datetime, Dict[str, Optional[str]]]] = {}
_CACHE_TTL = timedelta(hours=6)
_NEGATIVE_CACHE_TTL = timedelta(minutes=10)
_LOGGER = logging.getLogger(__name__)


def _empty_payload(location_label: str = "Unknown") -> Dict[str, Optional[str]]:
    return {
        "country": None,
        "region": None,
        "city": None,
        "org": None,
        "location_label": location_label,
    }


def _is_private_ip(value: str) -> bool:
    try:
        return ip_address(value).is_private
    except ValueError:
        return False


def _from_cache(ip: str) -> Optional[Dict[str, Optional[str]]]:
    cached = _CACHE.get(ip)
    if not cached:
        return None

    expires_at, payload = cached
    if datetime.utcnow() >= expires_at:
        _CACHE.pop(ip, None)
        return None

    return payload


def _save_cache(
    ip: str,
    payload: Dict[str, Optional[str]],
    ttl: timedelta = _CACHE_TTL,
) -> Dict[str, Optional[str]]:
    _CACHE[ip] = (datetime.utcnow() + ttl, payload)
    return payload


def lookup_ip_geolocation(ip: Optional[str]) -> Dict[str, Optional[str]]:
    """Lookup location/provider info for an IP address with fallback values."""
    if not ip:
        return _empty_payload(location_label=None)

    cached = _from_cache(ip)
    if cached:
        return cached

    if _is_private_ip(ip):
        return _save_cache(
            ip,
            _empty_payload(location_label="Private Network") | {"country": "Private Network"},
        )

    for provider in (_lookup_from_ipwhois, _lookup_from_ipinfo, _lookup_from_ipapi):
        payload = provider(ip)
        if payload:
            return _save_cache(ip, payload)

    return _save_cache(ip, _empty_payload(), ttl=_NEGATIVE_CACHE_TTL)


def _request_json(url: str) -> Dict[str, object]:
    request = Request(url, headers={"User-Agent": "logs-auth-collection/1.0"})
    with urlopen(request, timeout=2.5) as response:
        return json.loads(response.read().decode("utf-8"))


def _build_payload(
    country: Optional[str],
    region: Optional[str],
    city: Optional[str],
    org: Optional[str],
) -> Dict[str, Optional[str]]:
    parts = [part for part in [city, region, country] if part]
    location_label = ", ".join(parts) if parts else "Unknown"
    return {
        "country": country,
        "region": region,
        "city": city,
        "org": org,
        "location_label": location_label,
    }


def _lookup_from_ipwhois(ip: str) -> Optional[Dict[str, Optional[str]]]:
    try:
        data = _request_json(f"https://ipwho.is/{ip}")
        if data.get("success") is False:
            return None

        return _build_payload(
            country=data.get("country") if isinstance(data.get("country"), str) else None,
            region=data.get("region") if isinstance(data.get("region"), str) else None,
            city=data.get("city") if isinstance(data.get("city"), str) else None,
            org=data.get("connection", {}).get("isp") if isinstance(data.get("connection"), dict) else None,
        )
    except (HTTPError, URLError, TimeoutError, ValueError, json.JSONDecodeError):
        return None


def _lookup_from_ipinfo(ip: str) -> Optional[Dict[str, Optional[str]]]:
    try:
        data = _request_json(f"https://ipinfo.io/{ip}/json")
        return _build_payload(
            country=data.get("country") if isinstance(data.get("country"), str) else None,
            region=data.get("region") if isinstance(data.get("region"), str) else None,
            city=data.get("city") if isinstance(data.get("city"), str) else None,
            org=data.get("org") if isinstance(data.get("org"), str) else None,
        )
    except (HTTPError, URLError, TimeoutError, ValueError, json.JSONDecodeError):
        return None


def _lookup_from_ipapi(ip: str) -> Optional[Dict[str, Optional[str]]]:
    try:
        data = _request_json(f"https://ipapi.co/{ip}/json/")
        if data.get("error") is True:
            return None

        return _build_payload(
            country=data.get("country_name") if isinstance(data.get("country_name"), str) else None,
            region=data.get("region") if isinstance(data.get("region"), str) else None,
            city=data.get("city") if isinstance(data.get("city"), str) else None,
            org=data.get("org") if isinstance(data.get("org"), str) else None,
        )
    except (HTTPError, URLError, TimeoutError, ValueError, json.JSONDecodeError):
        _LOGGER.debug("ipapi lookup failed for ip=%s", ip)
        return None