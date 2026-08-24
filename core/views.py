from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import TeamMember, Project
from .forms import ContactForm


def home(request):
    founder = TeamMember.objects.filter(role_category="founder", is_active=True).first()
    cofounder = TeamMember.objects.filter(role_category="cofounder", is_active=True).first()
    team = TeamMember.objects.filter(role_category="team", is_active=True)
    projects = Project.objects.filter(status="published")[:6]

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            inquiry = form.save()
            _notify_new_inquiry(inquiry)
            messages.success(request, "Thanks! Your message has been sent — we'll reply soon.")
            return redirect("home")
    else:
        form = ContactForm()

    return render(
        request,
        "core/home.html",
        {
            "founder": founder,
            "cofounder": cofounder,
            "team": team,
            "projects": projects,
            "form": form,
        },
    )


def _notify_new_inquiry(inquiry):
    """Emails the founder when a new client inquiry comes in. Fails silently
    if email isn't configured yet, so the form never breaks for the visitor."""
    if not settings.EMAIL_HOST_USER or not settings.CONTACT_NOTIFY_EMAIL:
        return
    try:
        send_mail(
            subject=f"New Insightara inquiry from {inquiry.name}",
            message=(
                f"Name: {inquiry.name}\n"
                f"Email: {inquiry.email}\n"
                f"Company: {inquiry.company or '-'}\n\n"
                f"Message:\n{inquiry.message}\n\n"
                f"Reply directly to this sender, or view it in the admin panel."
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CONTACT_NOTIFY_EMAIL],
            fail_silently=True,
        )
    except Exception:
        pass


def projects_list(request):
    projects = Project.objects.filter(status="published")
    return render(request, "core/projects.html", {"projects": projects})