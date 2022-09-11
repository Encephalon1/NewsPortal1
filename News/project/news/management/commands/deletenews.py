from django.core.management.base import BaseCommand, CommandError
from news.models import Post, Category


class Command(BaseCommand):
    help = 'Deleted all the news and articles from the category'

    def handle(self, *args, **options):
        cat = input('Enter the category: ')
        category = Category.objects.get(name_of_category=cat)
        if category in Category.objects.all():
            self.stdout.readable()
            self.stdout.write('Do you really want to delete all the news from the category? yes/no')
            answer = input()
            if answer == 'yes':
                Post.objects.filter(category=category).delete()
                self.stdout.write(self.style.SUCCESS('News deleted successfully!'))
                return
            self.stdout.write(self.style.ERROR('Access denied'))
        else:
            self.stdout.write(self.style.ERROR('There is no such category in base'))
