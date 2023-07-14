import pytest
from django.core.exceptions import ValidationError
from .models import Category, BlogPost


@pytest.mark.django_db
def test_category_model_str_representation():
    # Create a Category object
    category = Category(name='Technology')

    # Assert that the string representation of the object is as expected
    assert str(category) == 'Technology'


@pytest.mark.django_db
def test_category_model_unique_name():
    # Create a Category object with the name 'Technology'
    Category.objects.create(name='Technology')

    # Try to create another Category object with the same name
    # Expect a ValidationError to be raised
    with pytest.raises(ValidationError):
        Category.objects.create(name='Technology')


@pytest.mark.django_db
def test_blog_post_model_str_representation():
    # Create a BlogPost object
    blog_post = BlogPost(title='Hello World')

    # Assert that the string representation of the object is as expected
    assert str(blog_post) == 'Hello World'


@pytest.mark.django_db
def test_blog_post_model_slug_generation():
    # Create a BlogPost object with the title 'Hello World'
    blog_post = BlogPost(title='Hello World')

    # Save the object to trigger the slug generation
    blog_post.save()

    # Assert that the generated slug matches the expected value
    assert blog_post.slug == 'hello-world'


@pytest.mark.django_db
def test_blog_post_model_relationship_with_category():
    # Create a Category object
    category = Category.objects.create(name='Technology')

    # Create a BlogPost object with the created Category as the foreign key
    blog_post = BlogPost.objects.create(title='Hello World', category=category)

    # Assert that the category of the BlogPost matches the created Category
    assert blog_post.category == category
