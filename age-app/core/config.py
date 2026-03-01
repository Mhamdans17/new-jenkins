import redis

def get_redis_client():
    # Menggunakan host 'redis' sesuai dengan nama service di docker-compose
    return redis.Redis(host='redis', port=6379, decode_responses=True)
