import pytest
from django.urls import reverse

from students.models import Course
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST


#  тест получения первого курса
@pytest.mark.django_db
def test_first_course(client, course_factory):
    course_factory(_quantity=5)
    course_first = Course.objects.first()
    url = reverse('courses-detail', args=(course_first.id, ))
    response = client.get(url)
    assert response.status_code == HTTP_200_OK
    assert response.data['id'] == course_first.id
    assert response.data['name'] == course_first.name


#  тест получения списка курсов
@pytest.mark.django_db
def test_get_course_list(client, course_factory):
    course_factory(_quantity=25)
    url = reverse('courses-list')
    response = client.get(url)
    assert response.status_code == HTTP_200_OK
    assert len(response.data) == 25


#  фильтрация списка курсов по id
@pytest.mark.django_db
def test_get_course_filter_id(client, course_factory):
    course_factory(_quantity=5)
    course_first = Course.objects.first()
    url = reverse("courses-list") + f'?id={course_first.id}'
    response = client.get(url)
    assert response.status_code == HTTP_200_OK
    assert response.data[0].get('id') == course_first.id
    assert response.data[0].get('name') == course_first.name


#  фильтрация списка курсов по name
@pytest.mark.django_db
def test_get_course_filter_name(client, course_factory):
    course_factory(_quantity=5)
    course_first = Course.objects.first()
    url = reverse("courses-list") + f'?name={course_first.name}'
    response = client.get(url)
    assert response.status_code == HTTP_200_OK
    assert response.data[0].get('id') == course_first.id
    assert response.data[0].get('name') == course_first.name


#  успешное создание курса
@pytest.mark.django_db
def test_create_course(client):
    url = reverse("courses-list")
    data = {'name': 'Python',
            'stundents': []}
    response = client.post(url, data)
    assert response.status_code == HTTP_201_CREATED


#  успешное обновление курса
@pytest.mark.django_db
def test_update_course(client, course_factory):
    course_factory(_quantity=5)
    course = Course.objects.first()
    data_update = {'name': 'DjangoGo'}
    url = reverse("courses-detail", args=(course.id, ))
    response = client.patch(path=url, data=data_update, content_type='application/json')
    assert response.status_code == HTTP_200_OK


#  успешное удаление курса
@pytest.mark.django_db
def test_delete_course(client, course_factory):
    course_factory(_quantity=5)
    course_up = Course.objects.first()
    url = reverse("courses-detail", args=(course_up.id, ))
    response = client.delete(url)
    assert response.status_code == HTTP_204_NO_CONTENT


@pytest.mark.parametrize(
    ['quantity', 'status_code'],
    (
            (0, HTTP_400_BAD_REQUEST),
            (1, HTTP_200_OK)
    )
)
@pytest.mark.django_db
def test_max_students_per_course_validate(
        client, course_factory, student_factory, settings, quantity, status_code
):
    course = course_factory(_quantity=1)
    student = student_factory(_quantity=1)
    url = reverse('courses-detail', args=(course[0].id,))
    settings.MAX_STUDENTS_PER_COURSE = quantity
    data_patch = {'name': 'Python', 'students': [student[0].id]}
    resp = client.patch(path=url, data=data_patch, content_type='application/json')
    assert resp.status_code == status_code

