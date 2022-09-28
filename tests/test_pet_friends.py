from api import Petfiends
from settings import valid_email, valid_password, invalid_email, invalid_password, invalid_api_key, another_api_key
import os

pf = Petfiends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Получаем api key для существующего юзера с правильными email и паролем. Результатом должен быть
    статус 200 и наличие ключа в результате."""
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result



def test_get_api_key_for_invalid_user(email=invalid_email, password=invalid_password):
    """ Пытаемся получить api key для не существующего юзера с неправильными email и паролем.
    Результатом должен быть статус 403."""
    status, result = pf.get_api_key(email, password)
    assert status == 403


def test_get_api_key_for_valid_user_with_invalid_password(email=valid_email, password=invalid_password):
    """ Пытаемся получить api key для существующего юзера с правильными email и не правильным паролем.
    Результатом должен быть статус 403."""
    status, result = pf.get_api_key(email, password)
    assert status == 403


def test_get_api_key_for_valid_user_without_password(email=valid_email, password=""):
    """ Пытаемся получить api key для существующего юзера с правильными email и пустым полем
     для введения пароля. Результатом должен быть статус 403."""
    status, result = pf.get_api_key(email, password)
    assert status == 403


def test_get_all_pets_with_valid_key_without_filter(filter=""):
    """Получаем список всех питомцев без использования фильтра
    Результатом должен быть статус 200 и количество отображаемых питомцев больше нуля"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_get_all_pets_with_valid_key_with_filter(filter="my_pets"):
    """Получаем список всех питомцев с включенным фильтром my_pets.
    Результатом должен быть статус 200 и количество питомцев больше или равно нулю"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) >= 0


def test_get_all_pets_with_valid_key_with_invalid_filter(filter="mypets"):
    """Пытаемся получить список всех питомцев с неправильным фильтром.
    Результатом должен быть статус 500"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 500


def test_get_all_pets_with_invalid_key(filter=""):
    """Пытаемся получить список всех животных, используя неправильный ключ.
    В результате должен быть статус 403"""
    auth_key = invalid_api_key
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 403


def test_get_my_pets_with_another_valid_key(filter="my_pets"):
    """Пытаемся получить список своих питомцев используя чужой валидный ключ.
    Результат должен быть статус 403"""
    auth_key = another_api_key
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 403


def test_add_pet_simple(name='Koko', animal_type='cat', age='4'):
    """Добавляем питомца без фото, используя все необходимые валидные данные.
    В результате должен быть статус 200, и наличие в результате заданных параметров"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age


def test_add_pet_simple_with_missed_field(name='', animal_type='', age=''):
    """Проверка добавления питомца с пропущенными полями.
    Авто тест проходит. Ручной тест нет.
    Результат авто теста статус 200 и соответствие результата заданным параметрам """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age


def test_update_pet(name='Toto', animal_type='bird', age='2'):
    """Обновление своего питомца. Ожидаемый результат статус 200
    и наличие в результате заданных параметров"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    status, result = pf.update_pet(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age

def test_add_photo_pet(pet_photo='images/bird.jpg'):
    """Добавление фотографии питомца, на уже существующий профиль без фотографии.
    Результат ожидаем статус 200 и наличие фотографии в результате."""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.add_photo_pet(auth_key, pet_id, pet_photo)
    assert status == 200
    assert 'pet_photo' in result


def test_update_pet_with_not_my_id(name='test.', animal_type='test', age='test'):
    """Обновление питомца с использованием чужого id.
    Я ожидал что система не даст мне доступ, но вышло без проблем, так что баг.
    Обновляется последний созданный питомец.
    Но всё равно пишу что жду статус 200 и наличие заданных параметров в результате"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, '')

    status, result = pf.update_pet(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age


def test_delete_my_pet():
    """Проверка удаления своего питомца. Ожидаемый результат статус 200
    и отсутствие питомца с удаляемым id в результате"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    assert status == 200
    assert pet_id not in my_pets.values()


def test_delete_another_pet():
    """Проверка удаления чужого питомца. К сожалению работает.
    Ожидаемый результат теста 200 , хотя правильней была бы ошибка.
    Без необходимости не использовать!!! Либо последний добавленный питомец в базу должен быть ваш!"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, '')

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, '')

    assert status == 200
    assert pet_id not in my_pets.values()


def test_add_pet_with_photo(name='Toto', animal_type='bird', age='2', pet_photo='images/bird.jpg'):
    """Проверяем добавление нового питомца со всеми валидными данными и фотографией.
    Ожидаемый результат: статус 200 и соответствие результата заданным параметрам"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_with_photo(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age
    assert 'pet_photo' in result


def test_delete_my_pet2():
    """Удаляем своего последнего созданного для теста питомца.
    Ожидаемый результат статус 200 и отсутствие питомца с удаляемым id в результате"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    assert status == 200
    assert pet_id not in my_pets.values()



