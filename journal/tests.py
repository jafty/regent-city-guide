from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse

from .models import Category, Post


class PostModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='La Bonne Chère', slug='la-bonne-chere')

    def test_post_creation_and_string_representation(self):
        post = Post.objects.create(
            category=self.category,
            title='Le Cassoulet a-t-il une Âme ?',
            slug='le-cassoulet-a-t-il-une-ame',
            excerpt='Enquête au cœur du Lauragais.',
            content='Contenu complet de l\'article.',
            image_url='https://example.com/cassoulet.jpg',
            is_published=True,
        )

        self.assertEqual(str(post), 'Le Cassoulet a-t-il une Âme ?')
        self.assertEqual(post.slug, 'le-cassoulet-a-t-il-une-ame')
        self.assertTrue(post.is_published)

    def test_post_slug_uniqueness(self):
        Post.objects.create(
            category=self.category,
            title='Premier titre',
            slug='slug-unique',
            excerpt='Premier excerpt',
            content='Premier contenu',
            is_published=True,
        )

        with self.assertRaises(IntegrityError):
            Post.objects.create(
                category=self.category,
                title='Second titre',
                slug='slug-unique',
                excerpt='Second excerpt',
                content='Second contenu',
                is_published=True,
            )


class JournalViewTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Arts & Lettres', slug='arts-et-lettres')
        self.post = Post.objects.create(
            category=self.category,
            title='La Halle de la Machine réveille le Minotaure',
            slug='halle-machine-minotaure',
            excerpt='Le géant reprend du service.',
            content='Contenu complet du minotaure.',
            is_published=True,
        )

    def test_homepage_status_code_and_template(self):
        response = self.client.get(reverse('journal:home'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'journal/index.html')

    def test_detail_status_code_and_template(self):
        response = self.client.get(reverse('journal:post_detail', kwargs={'slug': self.post.slug}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'journal/detail.html')


    def test_detail_renders_html_and_linebreaks_in_content(self):
        self.post.content = 'Première ligne\nDeuxième ligne avec <a href="#ancre">un lien</a>'
        self.post.save(update_fields=['content'])

        response = self.client.get(reverse('journal:post_detail', kwargs={'slug': self.post.slug}))

        html = response.content.decode()
        self.assertIn('Première ligne<br>Deuxième ligne avec <a href="#ancre">un lien</a>', html)

    def test_category_status_code_and_template(self):
        response = self.client.get(reverse('journal:category_detail', kwargs={'slug': self.category.slug}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'journal/category_detail.html')
        self.assertContains(response, self.post.title)
