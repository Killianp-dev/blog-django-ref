from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from blog.models import BlogPost

User = get_user_model()


class BlogPostModelTests(TestCase):
    def test_slug_is_generated_from_title(self):
        post = BlogPost.objects.create(title="Hello World", content="body")
        self.assertEqual(post.slug, "hello-world")

    def test_str_returns_title(self):
        post = BlogPost.objects.create(title="Un article")
        self.assertEqual(str(post), "Un article")

    def test_author_or_default_without_author(self):
        post = BlogPost.objects.create(title="Sans auteur")
        self.assertEqual(post.author_or_default, "auteur inconnu")

    def test_author_or_default_with_author(self):
        author = User.objects.create_user(username="killian", password="pass")
        post = BlogPost.objects.create(title="Avec auteur", author=author)
        self.assertEqual(post.author_or_default, "killian")


class BlogViewTests(TestCase):
    def setUp(self):
        self.staff = User.objects.create_user(
            username="staff", password="pass", is_staff=True
        )
        self.published = BlogPost.objects.create(
            title="Article publié",
            content="Contenu public",
            published=True,
        )
        self.draft = BlogPost.objects.create(
            title="Brouillon secret",
            content="Contenu privé",
            published=False,
        )

    def test_home_anonymous_sees_published_only(self):
        response = self.client.get(reverse("blog:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Article publié")
        self.assertNotContains(response, "Brouillon secret")

    def test_home_staff_sees_drafts(self):
        self.client.force_login(self.staff)
        response = self.client.get(reverse("blog:home"))
        self.assertContains(response, "Article publié")
        self.assertContains(response, "Brouillon secret")

    def test_detail_published_is_public(self):
        response = self.client.get(
            reverse("blog:detail", kwargs={"slug": self.published.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Article publié")

    def test_detail_draft_hidden_from_anonymous(self):
        response = self.client.get(
            reverse("blog:detail", kwargs={"slug": self.draft.slug})
        )
        self.assertEqual(response.status_code, 404)

    def test_detail_draft_visible_to_staff(self):
        self.client.force_login(self.staff)
        response = self.client.get(
            reverse("blog:detail", kwargs={"slug": self.draft.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Brouillon secret")

    def test_create_requires_staff(self):
        response = self.client.get(reverse("blog:create"))
        self.assertEqual(response.status_code, 302)

    def test_create_accessible_to_staff(self):
        self.client.force_login(self.staff)
        response = self.client.get(reverse("blog:create"))
        self.assertEqual(response.status_code, 200)

    def test_edit_requires_staff(self):
        response = self.client.get(
            reverse("blog:edit", kwargs={"slug": self.published.slug})
        )
        self.assertEqual(response.status_code, 302)

    def test_delete_requires_staff(self):
        response = self.client.get(
            reverse("blog:delete", kwargs={"slug": self.published.slug})
        )
        self.assertEqual(response.status_code, 302)
