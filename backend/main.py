import uvicorn
from fastapi import FastAPI, status
from models import FrontendVehicle, FrontendDriver, Timespan
from modules import create_connection, update_database
from sqlalchemy.orm import Session


def main():
    connection = create_connection()
    api = FastAPI()

    @api.get('/update', status_code=status.HTTP_200_OK)
    def update():
        with Session(connection) as session:
            update_database(session)

    @api.post('/filter', status_code=status.HTTP_200_OK)
    def get_points_by_filter(vehicle: FrontendVehicle = None,
                             driver: FrontendDriver = None,
                             timespan: Timespan = None):
        pass

    uvicorn.run(api, port=12345)


if __name__ == '__main__':
    main()
