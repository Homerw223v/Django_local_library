from django.test import TestCase
from ..models import Author, Book, Genre, BookInstance, Language


# Create your tests here.
class AuthorTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        Author.objects.create(first_name='Bob', last_name='Odenkirk', date_of_birth='1996-03-28')

    def test_first_name(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('first_name').verbose_name
        self.assertEquals(field_label, 'first name')

    def test_last_name(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('last_name').verbose_name
        self.assertEquals(field_label, 'last name')

    def test_date_of_birth(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_birth').verbose_name
        self.assertEquals(field_label, 'date of birth')

    def test_date_of_death_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_death').verbose_name
        self.assertEquals(field_label, 'Died')

    def test_first_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('first_name').max_length
        self.assertEquals(max_length, 100)

    def test_last_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('last_name').max_length
        self.assertEquals(max_length, 100)

    def test_object_name_is_last_name_comma_first_name(self):
        author = Author.objects.get(id=1)
        expected_object_name = '%s, %s' % (author.last_name, author.first_name)
        self.assertEquals(expected_object_name, str(author))

    def test_get_absolute_url(self):
        author = Author.objects.get(id=1)
        self.assertEquals(author.get_absolute_url(), '/catalog/author/1')


class GenreTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        Genre.objects.create(name='Drama')

    def test_name(self):
        genre = Genre.objects.get(id=1)
        field_label = genre._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')


class BookTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        Book.objects.create(title='The Brothers Karamazov',
                            author=AuthorTestClass.setUpTestData(),
                            summary='Although Dostoevsky began his first notes for The Brothers Karamazov in April 1878, the novel incorporated elements and themes from an earlier unfinished project he had begun in 1869 entitled The Life of a Great Sinner.',
                            isbn='9780385333849')

    book = Book.objects.get(id=1)

    def test_title(self):
        field_label = self.book._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'title')

    def test_title_max_length(self):
        max_length = self.book._meta.get_field('title').max_length
        self.assertEquals(max_length, 200)

    def test_author(self):
        field_label = self.book._meta.get_field('author').verbose_name
        self.assertEquals(field_label, 'author')

    def test_summary(self):
        field_label = self.book._meta.get_field('summary').verbose_name
        self.assertEquals(field_label, 'summary')

    def test_summary_max_length(self):
        max_length = self.book._meta.get_field('summary').max_length
        self.assertEquals(max_length, 1000)

    def test_isbn(self):
        field_label = self.book._meta.get_field('isbn').verbose_name
        self.assertEquals(field_label, 'ISBN')

    def test_isbn_max_length(self):
        max_length = self.book._meta.get_field('isbn').max_length
        self.assertEqual(max_length, 13)

    def test_get_absolute_url(self):
        self.assertEquals(self.book.get_absolute_url(), '/catalog/book/1')


