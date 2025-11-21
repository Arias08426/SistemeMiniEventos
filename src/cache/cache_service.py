from typing import Optional, Dict, Any

class CacheService:
    """Servicio de caché en memoria simple"""
    
    def __init__(self):
        self._cache: Dict[str, Any] = {}
    
    def get(self, key: str) -> Optional[Any]:
        """Obtiene un valor del caché"""
        return self._cache.get(key)
    
    def set(self, key: str, value: Any) -> None:
        """Almacena un valor en el caché"""
        self._cache[key] = value
    
    def invalidate(self, key: str) -> None:
        """Invalida (elimina) una entrada del caché"""
        if key in self._cache:
            del self._cache[key]
    
    def clear(self) -> None:
        """Limpia todo el caché"""
        self._cache.clear()
    
    def has(self, key: str) -> bool:
        """Verifica si una clave existe en el caché"""
        return key in self._cache
