from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
import datetime
from .forms import RenewBookForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView


# Create your views here.
@login_required
def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()
    num_visit = request.session.get('num_visit', 1)
    request.session['num_visit'] = num_visit + 1
    return render(request, 'index.html', context={
        "num_books": num_books,
        "num_instances": num_instances,
        "num_instances_available": num_instances_available,
        "num_authors": num_authors,
        "num_visit": num_visit
    })


@login_required
@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """
    View function for renewing a specific BookInstance by librarian.
    """
    book_ins = get_object_or_404(BookInstance, pk=pk)
    if request.method == 'POST':
        form = RenewBookForm(request.POST)
        if form.is_valid():
            book_ins.due_back = form.cleaned_data['renewal_date']
            book_ins.save()
            return HttpResponseRedirect(reverse('all-borrowed'))
    else:
        proposed_renewal_data = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_data})
    return render(request, 'catalog/book_renew_librarian.html', context={
        "form": form,
        "bookinst": book_ins,
    })


class BookListView(LoginRequiredMixin, generic.ListView):
    model = Book
    paginate_by = 10

    # Добавление дополнительных переменных в шаблон
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context['new_data'] = 'Добавляем новую информацию'
        return context  # Возвращяем переменную


class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book


class AuthorListView(LoginRequiredMixin, generic.ListView):
    model = Author
    paginate_by = 10
    template_name = 'author_list'


class AuthorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Author


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class AllBorrowedBooksListView(LoginRequiredMixin, generic.ListView):
    permission_required = 'catalog.can_mark_returned'
    model = BookInstance
    template_name = 'catalog/borrowed_books_to_staff.html'

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')


class AuthorCreate(LoginRequiredMixin, CreateView):
    model = Author
    fields = '__all__'
    initial = {'date_of_death': '2016-04-03', 'date_of_birth': '2014-12-15'}
    success_url = reverse_lazy('authors')


class AuthorUpdate(LoginRequiredMixin, UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    success_url = reverse_lazy('authors')


class AuthorDelete(LoginRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('authors')


class BookCreate(LoginRequiredMixin, CreateView):
    model = Book
    fields = '__all__'


class BookUpdate(LoginRequiredMixin, UpdateView):
    model = Book
    fields = '__all__'


class BookDelete(LoginRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('books')
