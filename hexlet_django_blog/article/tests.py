from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from hexlet_django_blog.article.models import Article


class ArticleIndexViewTests(TestCase):
    def test_index_lists_articles(self):
        Article.objects.create(name="Первая", body="Тело первой")
        Article.objects.create(name="Вторая", body="Тело второй")

        response = self.client.get(reverse("article:articles"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "articles/index.html")
        self.assertEqual(len(response.context["articles"]), 2)

    def test_index_is_limited_to_15_articles(self):
        for i in range(20):
            Article.objects.create(name=f"Статья {i}", body="Тело")

        response = self.client.get(reverse("article:articles"))

        self.assertEqual(len(response.context["articles"]), 15)

    def test_index_is_ok_without_articles(self):
        response = self.client.get(reverse("article:articles"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["articles"]), [])


class ArticleShowViewTests(TestCase):
    def setUp(self):
        self.article = Article.objects.create(name="Первая", body="Тело первой")

    def test_show_renders_article(self):
        response = self.client.get(
            reverse("article:articles_show", args=[self.article.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "articles/show.html")
        self.assertEqual(response.context["article"], self.article)
        self.assertContains(response, "Первая")

    def test_show_returns_404_for_missing_article(self):
        response = self.client.get(reverse("article:articles_show", args=[99999]))

        self.assertEqual(response.status_code, 404)


class ArticleCreateViewTests(TestCase):
    def test_get_renders_empty_form(self):
        response = self.client.get(reverse("article:articles_create"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "articles/create.html")
        self.assertFalse(response.context["form"].is_bound)

    def test_post_creates_article_and_redirects(self):
        response = self.client.post(
            reverse("article:articles_create"),
            data={"name": "Новая статья", "body": "Тело новой статьи"},
        )

        self.assertRedirects(response, reverse("article:articles"))
        article = Article.objects.get(name="Новая статья")
        self.assertEqual(article.body, "Тело новой статьи")

    def test_post_sets_success_message(self):
        response = self.client.post(
            reverse("article:articles_create"),
            data={"name": "Новая статья", "body": "Тело"},
            follow=True,
        )

        messages = [str(m) for m in get_messages(response.wsgi_request)]
        self.assertEqual(messages, ['Статья "Новая статья" успешно создана!'])

    def test_post_sets_timestamps(self):
        self.client.post(
            reverse("article:articles_create"),
            data={"name": "Новая статья", "body": "Тело"},
        )

        article = Article.objects.get(name="Новая статья")
        self.assertIsNotNone(article.created_at)
        self.assertIsNotNone(article.updated_at)

    def test_post_with_invalid_data_does_not_create_article(self):
        response = self.client.post(
            reverse("article:articles_create"),
            data={"name": "", "body": "Тело"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors)
        self.assertEqual(Article.objects.count(), 0)

    def test_post_with_too_long_name_is_rejected(self):
        response = self.client.post(
            reverse("article:articles_create"),
            data={"name": "x" * 201, "body": "Тело"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("name", response.context["form"].errors)
        self.assertEqual(Article.objects.count(), 0)


class ArticleUpdateViewTests(TestCase):
    def setUp(self):
        self.article = Article.objects.create(name="Старая", body="Старое тело")

    def test_get_renders_form_with_instance(self):
        response = self.client.get(
            reverse("article:articles_update", args=[self.article.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "articles/update.html")
        self.assertEqual(response.context["article_id"], self.article.id)
        self.assertEqual(response.context["form"].instance, self.article)

    def test_get_returns_404_for_missing_article(self):
        response = self.client.get(reverse("article:articles_update", args=[99999]))

        self.assertEqual(response.status_code, 404)

    def test_post_updates_article_and_redirects(self):
        response = self.client.post(
            reverse("article:articles_update", args=[self.article.id]),
            data={"name": "Новая", "body": "Новое тело"},
        )

        self.assertRedirects(response, reverse("article:articles"))
        self.article.refresh_from_db()
        self.assertEqual(self.article.name, "Новая")
        self.assertEqual(self.article.body, "Новое тело")

    def test_post_with_invalid_data_keeps_article(self):
        response = self.client.post(
            reverse("article:articles_update", args=[self.article.id]),
            data={"name": "", "body": "Новое тело"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors)
        self.article.refresh_from_db()
        self.assertEqual(self.article.name, "Старая")


class ArticleDeleteViewTests(TestCase):
    def setUp(self):
        self.article = Article.objects.create(name="Удаляемая", body="Тело")

    def test_post_deletes_article_and_redirects(self):
        response = self.client.post(
            reverse("article:articles_delete", args=[self.article.id])
        )

        self.assertRedirects(response, reverse("article:articles"))
        self.assertFalse(Article.objects.filter(id=self.article.id).exists())

    def test_post_returns_404_for_missing_article(self):
        response = self.client.post(reverse("article:articles_delete", args=[99999]))

        self.assertEqual(response.status_code, 404)

    def test_get_is_not_allowed(self):
        response = self.client.get(
            reverse("article:articles_delete", args=[self.article.id])
        )

        self.assertEqual(response.status_code, 405)
        self.assertTrue(Article.objects.filter(id=self.article.id).exists())


class ProjectViewTests(TestCase):
    def test_index_page(self):
        response = self.client.get(reverse("index"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

    def test_about_page(self):
        response = self.client.get(reverse("about"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "about.html")

    def test_admin_requires_login(self):
        response = self.client.get("/admin/")

        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin/login/", response.url)
