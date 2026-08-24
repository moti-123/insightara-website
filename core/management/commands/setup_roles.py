"""
Run this once after your first deploy:
    python manage.py setup_roles

Creates two permission groups so the Founder can add new team members
to the admin without giving them full (superuser) access:

- "Co-Founder"  -> can manage team members, projects, and view inquiries
- "Team Member" -> can add/edit projects and their own team profile only

The Founder should always be a Django superuser (created via createsuperuser).
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from core.models import TeamMember, Project, ContactMessage


class Command(BaseCommand):
    help = "Creates Co-Founder and Team Member permission groups."

    def handle(self, *args, **options):
        cofounder_group, _ = Group.objects.get_or_create(name="Co-Founder")
        team_group, _ = Group.objects.get_or_create(name="Team Member")

        team_ct = ContentType.objects.get_for_model(TeamMember)
        project_ct = ContentType.objects.get_for_model(Project)
        contact_ct = ContentType.objects.get_for_model(ContactMessage)

        team_perms = Permission.objects.filter(content_type=team_ct)
        project_perms = Permission.objects.filter(content_type=project_ct)
        contact_view_perm = Permission.objects.filter(content_type=contact_ct, codename="view_contactmessage")

        # Co-Founder: full control over team + projects, can view inquiries
        cofounder_group.permissions.set(list(team_perms) + list(project_perms) + list(contact_view_perm))

        # Team Member: can add/change projects only (not delete, not team management)
        team_member_perms = Permission.objects.filter(
            content_type=project_ct, codename__in=["add_project", "change_project", "view_project"]
        )
        team_group.permissions.set(list(team_member_perms))

        self.stdout.write(self.style.SUCCESS("Roles created: 'Co-Founder' and 'Team Member'."))
        self.stdout.write("Next: in /admin/, open a user and tick 'Staff status' + add them to a group.")
