from datetime import datetime


def get_content_table(content):
    table_head = [
        {'name': 'Заголовок', "id": "title"},
        {'name': 'Дата создания', "id": "date_created"},
        {'name': 'Дата публикации', "id": "date_pub"},
        {'name': 'Просмотры', "id": "number_of_views"},
        {'name': 'Опубликовано', "id": "pub"},
    ]
    table_row = [{"id": element.id,
                  "title": element.title,
                  "date_created": element.date_created,
                  "date_pub": element.date_pub,
                  "number_of_views": element.number_of_views,
                  "pub": element.pub}
                 for element in content]
    return table_head, table_row


def get_regular_schedule_table(content):
    table_head = [
        {'name': 'Время публикации', "id": "time_pub"},
        {'name': 'Тип контента', "id": "content_type"}
    ]
    table_row = [{"id": element.id,
                  "time_pub": element.time_pub,
                  "content_type": element.content_type.name
                  }
                 for element in content]
    return table_head, table_row


def get_content_schedule_table(content):
    table_head = [
        {'name': 'Дата публикации', "id": "datetime_pub"},
        {'name': 'Пост', "id": "content_id"}
    ]
    table_row = [{"id": element.content.id,
                  "datetime_pub": datetime.combine(
                      element.date_pub,
                      element.time_pub
                  ),
                  "content_type": element.content.title
                  }
                 for element in content]
    return table_head, table_row


def get_channel_table(content):
    table_head = [
        {'name': 'Название канала', "id": "name"},
        {'name': 'Краткое название', "id": "slug_name"},
        {'name': 'ID канала', "id": "channel_id"}
    ]
    table_row = [{"id": element.id,
                  "name": element.name,
                  "slug_name": element.slug_name,
                  "channel_id": element.channel_id,
                  # "statistics": element.content.title,
                  }
                 for element in content]
    return table_head, table_row
