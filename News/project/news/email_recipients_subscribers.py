from .models import *


# Собираем все адреса почты подписчиков
email_recipients_subscribers = []

for us in PostCategory.objects.filter(id__in=[2, 3, 5, 10]). \
        select_related('category').values('categoryThrough__subscribers__email'):
    # Здесь идет преобразование: сначала из queryset извлекается значение, без ключа,
    # получаем объект типа dict_values,
    # затем dict_values преобразуем в список,
    # после чего адрес, лежащий в полученном списке, помещаем в список адресов.
    email_recipients_subscribers.append(*list(us.values()))

# Убираем дублирующиеся адреса
email_recipients_subscribers = set(email_recipients_subscribers)
