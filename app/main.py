from database.models import init_db, Devices
from dotenv import load_dotenv
import os
def main():
    
    Session = init_db()
    session = Session()

    load_dotenv()
    print(os.getenv("PASS_AC"))










if __name__ == '__main__':
    main()