class ErrorMessages:
    INVALID_DATE = "Tanggal tidak valid!"
    FUTURE_DATE = "Kok ngisi tanggal masa depan? Mesin waktu belum diciptakan!"
    API_SUCCESS_STATUS = "Sukses"

class AppConstants:
    REDIS_HIT_KEY = "hits_umur"
    REDIS_ERROR_MSG = "Error (Redis Mati)"
    AGE_RESULT_FORMAT = "{tahun} Tahun, {bulan} Bulan"
