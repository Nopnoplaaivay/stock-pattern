from dotenv import load_dotenv
import warnings
from urllib3.exceptions import InsecureRequestWarning

# Suppress the warning
warnings.simplefilter("ignore", InsecureRequestWarning)

load_dotenv(".env")
