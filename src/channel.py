import json
import os

from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    api_key = os.getenv('API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.__channel = self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.__title = self.__channel['items'][0]['snippet']['title']
        # self.__description = self.__channel['items'][0]['snippet']['title']
        self.__url = f'https://www.youtube.com/channel/{self.__channel_id}'
        self.__subscriber_count = self.__channel['items'][0]['statistics']['subscriberCount']
        self.__video_count = self.__channel['items'][0]['statistics']['videoCount']
        self.__view_count = self.__channel['items'][0]['statistics']['viewCount']

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.__channel, indent=2, ensure_ascii=False))

    @property
    def channel_id(self) -> str:
        """Геттер возвращает id канала"""
        return self.__channel_id

    @channel_id.setter
    def channel_id(self, channel_id):
        """Сеттер возвращает id канала"""
        raise AttributeError("Channel_id' of 'Channel' object has no setter")

    @classmethod
    def get_service(cls):
        """
        Класс-метод, возвращающий объект для работы с YouTube API
        """
        return cls.youtube

    def to_json(self, file_name: str) -> None:
        """
        Метод, сохраняющий в файл значения атрибутов экземпляра `Channel`
        """
        with open(file_name, 'w', encoding='utf-8') as file_json:
            json.dump(self.__dict__, file_json, ensure_ascii=False)

    def __str__(self):
        return f'{self.__title} ({self.__url})'

    def __add__(self, other: 'Channel') -> int:
        """
        Магический метод для сложения (сравнения кол-во подписчиков)
        """
        return self.__subscriber_count + other.__subscriber_count

    def __sub__(self, other: 'Channel') -> int:
        """
        Магический метод для вычитания (сравнение кол-во подписчиков)
        """
        return self.__subscriber_count - other.__subscriber_count

    def __rsub__(self, other):
        """
        Магический метод отраженного вычитания (сравнение кол-во подписчиков)
        """
        return self.__subscriber_count - other.__subscriber_count

    def __ge__(self, other):
        """
        Магический метод для сравнения >= (сравнение кол-во подписчиков)
        """
        return self.__subscriber_count >= other.__subscriber_count
