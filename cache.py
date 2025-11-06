"""
Cache management for video generation to avoid expensive API calls.
"""
import hashlib
import json
from pathlib import Path


CACHE_FILE = Path("cache.json")


def load_cache():
    """Carga el mapa de caché desde el archivo JSON."""
    if CACHE_FILE.exists():
        try:
            with CACHE_FILE.open('r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error al cargar caché: {e}")
            return {}
    return {}


def save_cache(cache):
    """Guarda el mapa de caché en el archivo JSON."""
    try:
        with CACHE_FILE.open('w') as f:
            json.dump(cache, f, indent=2)
    except Exception as e:
        print(f"Error al guardar caché: {e}")


def compute_cache_key(model, data_uri, prompt, duration_seconds):
    """Calcula el hash de los parámetros para usarlo como clave de caché."""
    cache_string = f"{model}|{data_uri}|{prompt}|{duration_seconds}"
    return hashlib.sha256(cache_string.encode('utf-8')).hexdigest()


def get_cached_video(cache_key):
    cache = load_cache()
    if cache_key in cache:
        cached_video_path = Path(cache[cache_key])
        if cached_video_path.exists():
            return str(cached_video_path)
        else:
            del cache[cache_key]
            save_cache(cache)

    return None


def cache_video(cache_key, video_path):
    cache = load_cache()
    cache[cache_key] = str(video_path)
    save_cache(cache)
