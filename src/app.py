from api import DefiOneclickAirdropsService
from serializer import Serializer


def main():
    service = DefiOneclickAirdropsService(Serializer.default())
    service.create_excel_file()


if __name__ == '__main__':
    main()
