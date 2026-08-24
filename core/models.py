from django.db import models
from django.core.validators import FileExtensionValidator


class TeamMember(models.Model):
    """
    Every person shown on the site: Founder, Co-Founder, and Team members.
    ROLE controls which section of the homepage they appear in and the
    display order within that section.
    """

    class RoleCategory(models.TextChoices):
        FOUNDER = "founder", "Founder"
        COFOUNDER = "cofounder", "Co-Founder"
        TEAM = "team", "Team Member"

    full_name = models.CharField(max_length=120)
    role_category = models.CharField(max_length=20, choices=RoleCategory.choices)
    job_title = models.CharField(
        max_length=120,
        help_text="e.g. 'Founder & Data Analyst', 'Power BI Developer'",
    )
    bio = models.TextField(help_text="Short 2-4 sentence bio shown on the site.")
    photo = models.ImageField(
        upload_to="team_photos/",
        validators=[FileExtensionValidator(["jpg", "jpeg", "png", "webp"])],
        help_text="Square photo recommended (min 500x500px).",
    )
    linkedin_url = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    display_order = models.PositiveIntegerField(
        default=0, help_text="Lower numbers appear first within their section."
    )
    is_active = models.BooleanField(
        default=True, help_text="Uncheck to hide this person from the live site without deleting them."
    )
    date_joined = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["role_category", "display_order", "full_name"]
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"

    def __str__(self):
        return f"{self.full_name} ({self.get_role_category_display()})"


class Project(models.Model):
    """Portfolio / case-study items shown on the site, addable by any team member."""

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft (hidden from site)"
        PUBLISHED = "published", "Published (visible on site)"

    title = models.CharField(max_length=150)
    client_name = models.CharField(max_length=120, blank=True, help_text="Optional - leave blank if confidential.")
    summary = models.TextField(help_text="What the project was about and the outcome.")
    tools_used = models.CharField(
        max_length=200, help_text="Comma-separated, e.g. 'Python, Pandas, Power BI'"
    )
    cover_image = models.ImageField(upload_to="project_covers/", blank=True, null=True)
    project_url = models.URLField(blank=True, help_text="Link to GitHub repo, dashboard, or live demo.")
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PUBLISHED)
    added_by = models.ForeignKey(
        "auth.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="projects_added"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    """Messages submitted by prospective clients through the public contact form."""

    name = models.CharField(max_length=120)
    email = models.EmailField()
    company = models.CharField(max_length=120, blank=True)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-submitted_at"]
        verbose_name = "Client Inquiry"
        verbose_name_plural = "Client Inquiries"

    def __str__(self):
        return f"{self.name} - {self.submitted_at.strftime('%Y-%m-%d')}"
