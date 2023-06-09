from django.test import TestCase, Client
from ..models import Author
from django.contrib.auth.models import User, Permission
from django.urls import reverse, reverse_lazy
import datetime
from django.utils import timezone
from ..models import Book, BookInstance, Genre, Language
from pprint import pprint


# Create your tests here.

# class AuthorListViewTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         # Create 13 authors for pagination tests
#         number_of_authors = 14
#         for author_num in range(number_of_authors):
#             Author.objects.create(first_name='Christian %s' % author_num,
#                                   last_name='Surname %s' % author_num)
#
#     def setUp(self):
#         self.client.force_login(User.objects.get_or_create(username='testuser')[0])
#
#     def test_view_url_exists_at_desired_location(self):
#         resp = self.client.get('/catalog/authors/')
#         self.assertEquals(resp.status_code, 200)
#
#     def test_view_url_accessible_by_name(self):
#         resp = self.client.get(reverse('authors'))
#         self.assertEquals(resp.status_code, 200)
#
#     def test_view_uses_correct_template(self):
#         resp = self.client.get(reverse('authors'))
#         self.assertEquals(resp.status_code, 200)
#         self.assertTemplateUsed(resp, 'catalog/author_list.html')
#
#     def test_pagination_is_ten(self):
#         resp = self.client.get(reverse('authors'))
#         self.assertEquals(resp.status_code, 200)
#         self.assertTrue('is_paginated' in resp.context)
#         self.assertTrue(resp.context['is_paginated'] == True)
#         self.assertTrue(len(resp.context['author_list']) == 10)
#
#     def test_lists_all_authors(self):
#         # Get second page and confirm it has (exactly) remaining 3 items
#         resp = self.client.get(reverse('authors') + '?page=2')
#         self.assertEquals(resp.status_code, 200)
#         self.assertTrue('is_paginated' in resp.context)
#         self.assertTrue(resp.context['is_paginated'] == True)
#         self.assertTrue(len(resp.context['author_list']) == 4)
#
#
# class LoanedBookInstanceByUserListViewTest(TestCase):
#     def setUp(self):
#         test_user1 = User.objects.create_user(username='testuser1', password='zxasqw12321')
#         test_user2 = User.objects.create_user(username='testuser2', password='zxasqw12321')
#         test_author = Author.objects.create(first_name='Jhon', last_name='Smith')
#         test_genre = Genre.objects.create(name='Fantasy')
#         test_language = Language.objects.create(name='English')
#         test_book = Book.objects.create(title='Book Title',
#                                         summary='My book summary',
#                                         isbn='125465895478546',
#                                         author=test_author,
#                                         language=test_language)
#         genre_objects_for_book = Genre.objects.all()
#         test_book.genre.set(genre_objects_for_book)
#         test_book.save()
#         # Создание 30 объектов BookInstance
#         number_of_book_coppies = 30
#         for book_copy in range(number_of_book_coppies):
#             return_date = timezone.now() + datetime.timedelta(days=book_copy % 5)
#             if book_copy % 2:
#                 the_borrower = test_user1
#             else:
#                 the_borrower = test_user2
#             status = 'm'
#             BookInstance.objects.create(book=test_book,
#                                         imprint='Unlikely Imprint, 2016',
#                                         due_back=return_date,
#                                         borrower=the_borrower,
#                                         status=status)
#
#     def test_redirect_if_not_logged_in(self):
#         resp = self.client.get(reverse('my-borrowed'))
#         self.assertRedirects(resp, '/accounts/login/?next=/catalog/mybooks/')
#
#     def test_logged_in_user_correct_template(self):
#         login = self.client.login(username='testuser1', password='zxasqw12321')
#         resp = self.client.get(reverse('my-borrowed'))
#         self.assertEquals(str(resp.context['user']), 'testuser1')
#         self.assertEquals(resp.status_code, 200)
#         self.assertTemplateUsed('catalog/bookinstance_list_borrowed_user.html')
#
#     def test_only_borrowed_books_in_list(self):
#         login = self.client.login(username='testuser1', password='zxasqw12321')
#         resp = self.client.get(reverse('my-borrowed'))
#         self.assertEquals(str(resp.context['user']), 'testuser1')
#         self.assertEquals(resp.status_code, 200)
#         self.assertTrue('bookinstance_list' in resp.context)
#         self.assertEquals(len(resp.context['bookinstance_list']), 0)
#         get_ten_books = Book.objects.all()[:10]
#         for copy in get_ten_books:
#             copy.status = 'o'
#             copy.save()
#         resp = self.client.get(reverse('my-borrowed'))
#         self.assertEquals(str(resp.context['user']), 'testuser1')
#         self.assertEquals(resp.status_code, 200)
#         self.assertTrue('bookinstance_list' in resp.context)
#         for bookitem in resp.context['bookinstance_list']:
#             self.assertEquals(resp.context['user'], bookitem.borrower)
#             self.assertEquals('o', bookitem.status)
#
#     def test_pages_ordered_by_due_date(self):
#         for copy in BookInstance.objects.all():
#             copy.status = 'o'
#             copy.save()
#         login = self.client.login(username='testuser1', password='zxasqw12321')
#         resp = self.client.get(reverse('my-borrowed'))
#         self.assertEquals(str(resp.context['user']), 'testuser1')
#         self.assertEquals(resp.status_code, 200)
#         self.assertEquals(len(resp.context['bookinstance_list']), 10)
#         last_date = 0
#         for copy in resp.context['bookinstance_list']:
#             if last_date == 0:
#                 last_date = copy.due_back
#             else:
#                 self.assertTrue(last_date <= copy.due_back)
#
#
# class RenewBookInstanceViewTest(TestCase):
#     def setUp(self):
#         test_user1 = User.objects.create_user(username='testuser1', password='zxasqw12321')
#         test_user2 = User.objects.create_user(username='testuser2', password='zxasqw12321')
#         test_user1.save()
#         test_user2.save()
#         permission = Permission.objects.get(name='Set book as returned')
#         test_user2.user_permissions.add(permission)
#         test_user2.save()
#         test_author = Author.objects.create(first_name='John', last_name='Smith')
#         test_genre = Genre.objects.create(name='Fantasy')
#         test_language = Language.objects.create(name='English')
#         test_book = Book.objects.create(title='Book Title', summary='My book summary', isbn='ABCDEFG',
#                                         author=test_author, language=test_language, )
#         # Создание жанра Create genre as a post-step
#         genre_objects_for_book = Genre.objects.all()
#         test_book.genre.set(genre_objects_for_book)
#         test_book.save()
#         return_date = datetime.date.today() + datetime.timedelta(days=5)
#         self.test_bookinstance1 = BookInstance.objects.create(book=test_book,
#                                                               imprint='Unlikely Imprint, 2016',
#                                                               due_back=return_date,
#                                                               borrower=test_user1,
#                                                               status='o')
#         return_date = datetime.date.today() + datetime.timedelta(days=5)
#         self.test_bookinstance2 = BookInstance.objects.create(book=test_book,
#                                                               imprint='Unlikely Imprint, 2016',
#                                                               due_back=return_date,
#                                                               borrower=test_user2,
#                                                               status='o')
#
#     def test_redirect_if_not_logged_in(self):
#         resp = self.client.get(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}))
#         self.assertEquals(resp.status_code, 302)
#         self.assertTrue(resp.url.startswith('/accounts/login/'))
#
#     def test_redirect_if_logged_in_but_not_correct_permission(self):
#         login = self.client.login(username='testuser1', password='zxasqw12321')
#         resp = self.client.get(reverse('renew-book-librarian',
#                                        kwargs={'pk': self.test_bookinstance1.pk}))
#         self.assertEquals(resp.status_code, 302)
#         self.assertTrue(resp.url.startswith('/accounts/login'))
#
#     def test_logged_in_with_permission_borrowed_book(self):
#         login = self.client.login(username='testuser2', password='zxasqw12321')
#         resp = self.client.get(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance2.pk}))
#         self.assertEquals(resp.status_code, 200)
#
#     def test_logged_in_with_permission_another_users_borrowed_book(self):
#         login = self.client.login(username='testuser2', password='zxasqw12321')
#         resp = self.client.get(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}))
#         self.assertEquals(resp.status_code, 200)
#
#     def test_HTTP404_for_invalid_book_if_logged_in(self):
#         import uuid
#         test_uid = uuid.uuid4()
#         login = self.client.login(username='testuser2', password='zxasqw12321')
#         resp = self.client.get(reverse('renew-book-librarian', kwargs={'pk': test_uid}))
#         self.assertEquals(resp.status_code, 404)
#
#     def test_user_correct_template(self):
#         login = self.client.login(username='testuser2', password='zxasqw12321')
#         resp = self.client.get(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}))
#         self.assertEquals(resp.status_code, 200)
#         self.assertTemplateUsed(resp, 'catalog/book_renew_librarian.html')
#
#     def test_form_renewal_date_initially_has_date_three_weeks_in_future(self):
#         login = self.client.login(username='testuser2', password='zxasqw12321')
#         resp = self.client.get(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}))
#         self.assertEquals(resp.status_code, 200)
#         date_3_weeks_in_future = datetime.date.today() + datetime.timedelta(weeks=3)
#         self.assertEqual(resp.context['form'].initial['renewal_date'], date_3_weeks_in_future)
#
#     def test_redirect_to_all_borrowed_book_list_on_success(self):
#         login = self.client.login(username='testuser2', password='zxasqw12321')
#         valid_date_in_future = datetime.date.today() + datetime.timedelta(weeks=2)
#         resp = self.client.post(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}),
#                                {'renewal_date': valid_date_in_future})
#         self.assertRedirects(resp, reverse('all-borrowed'))
#
#     def test_form_invalid_renewal_date(self):
#         login = self.client.login(username='testuser2', password='zxasqw12321')
#         date_in_past = datetime.date.today() - datetime.timedelta(weeks=1)
#         resp = self.client.post(reverse('renew-book-librarian', kwargs={'pk':self.test_bookinstance1.pk}),
#                                 {'renewal_date': date_in_past})
#         self.assertEquals(resp.status_code, 200)
#         self.assertFormError(resp, 'form', 'renewal_date', 'Invalid date - renewal in past')
#
#     def test_form_invalid_renewal_date_future(self):
#         login = self.client.login(username='testuser2', password='zxasqw12321')
#         date_in_future = datetime.date.today() + datetime.timedelta(weeks=5)
#         resp = self.client.post(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}),
#                                 {'renewal_date': date_in_future})
#         self.assertEquals(resp.status_code, 200)
#         self.assertFormError(resp, 'form', 'renewal_date', 'Invalid date - renewal more than 4 weeks ahead')


class AuthorCreateViewstest(TestCase):
    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1', password='zxasqw12321')
        test_user2 = User.objects.create_user(username='testuser2', password='zxasqw12321', is_superuser=True)
        test_user1.save()
        test_user2.save()

    def test_user_not_logged(self):
        response = self.client.get(reverse('author_create'))
        self.assertEquals(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login'))

    def test_template_used_form(self):
        login = self.client.login(username='testuser1', password='zxasqw12321')
        response = self.client.get(reverse('author_create'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/author_form.html')

    def test_success_create_author(self):
        login = self.client.login(username='testuser2', password='zxasqw12321')
        response = self.client.post(reverse('author_create'), kwargs={'first_name': 'Jack',
                                                                      'last_name': 'Sparrow'})
        # self.assertRedirects(response, reverse('authors'))
        pprint(response.status_code)
