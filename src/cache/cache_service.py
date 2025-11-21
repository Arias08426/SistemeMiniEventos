import os
import json
from typing import Optional, Any
import redis
from redis.exceptions import RedisError, ConnectionError as RedisConnectionError


class CacheService:
    """Servicio de caché con Redis (con fallback a memoria)"""
    
    def __init__(self, redis_url: Optional[str] = None):
        """
        Inicializa el servicio de caché
        
        Args:
            redis_url: URL de conexión a Redis (ej: redis://localhost:6379/0)
                      Si no se proporciona, usa variables de entorno o fallback a memoria
        """
        self._memory_cache = {}  # Fallback a memoria si Redis no está disponible
        self._use_redis = False
        self._redis_client = None
        
        # Obtener URL de Redis desde parámetro o variables de entorno
        redis_url = redis_url or os.getenv('REDIS_URL', 'redis://localhost:6379/0')
        
        try:
            # Intentar conectar a Redis
            self._redis_client = redis.from_url(
                redis_url,
                decode_responses=True,
                socket_connect_timeout=2,
                socket_timeout=2
            )
            # Verificar conexión
            self._redis_client.ping()
            self._use_redis = True
            print(f"✓ Cache: Conectado a Redis en {redis_url}")
        except (RedisError, RedisConnectionError, Exception) as e:
            print(f"⚠ Cache: Redis no disponible ({e}), usando caché en memoria")
            self._use_redis = False
    
    def get(self, key: str) -> Optional[Any]:
        """Obtiene un valor del caché"""
        if self._use_redis:
            try:
                value = self._redis_client.get(key)
                if value is not None:
                    return json.loads(value)
                return None
            except (RedisError, Exception):
                # Fallback a memoria si Redis falla
                return self._memory_cache.get(key)
        else:
            return self._memory_cache.get(key)
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """
        Almacena un valor en el caché
        
        Args:
            key: Clave del caché
            value: Valor a almacenar
            ttl: Tiempo de vida en segundos (solo para Redis)
        """
        if self._use_redis:
            try:
                serialized = json.dumps(value)
                if ttl:
                    self._redis_client.setex(key, ttl, serialized)
                else:
                    self._redis_client.set(key, serialized)
            except (RedisError, Exception):
                # Fallback a memoria si Redis falla
                self._memory_cache[key] = value
        else:
            self._memory_cache[key] = value
    
    def invalidate(self, key: str) -> None:
        """Invalida (elimina) una entrada del caché"""
        if self._use_redis:
            try:
                self._redis_client.delete(key)
            except (RedisError, Exception):
                # Fallback a memoria si Redis falla
                if key in self._memory_cache:
                    del self._memory_cache[key]
        else:
            if key in self._memory_cache:
                del self._memory_cache[key]
    
    def clear(self) -> None:
        """Limpia todo el caché"""
        if self._use_redis:
            try:
                self._redis_client.flushdb()
            except (RedisError, Exception):
                # Fallback a memoria si Redis falla
                self._memory_cache.clear()
        else:
            self._memory_cache.clear()
    
    def has(self, key: str) -> bool:
        """Verifica si una clave existe en el caché"""
        if self._use_redis:
            try:
                return self._redis_client.exists(key) > 0
            except (RedisError, Exception):
                # Fallback a memoria si Redis falla
                return key in self._memory_cache
        else:
            return key in self._memory_cache
    
    def is_using_redis(self) -> bool:
        """Retorna True si está usando Redis, False si usa memoria"""
        return self._use_redis
