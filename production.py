from waitress import serve
from app import app
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('production.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('waitress')

if __name__ == '__main__':
    # Production server configuration
    host = '0.0.0.0'  # Listen on all available interfaces
    port = 8080
    threads = 4  # Number of worker threads
    
    logger.info(f"Starting production server on http://{host}:{port}")
    
    serve(
        app,
        host=host,
        port=port,
        threads=threads,
        url_scheme='http',
        channel_timeout=300,
        cleanup_interval=30,
        ident='Career Recommendation Server'
    ) 