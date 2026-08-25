from django.shortcuts import render, redirect
from django.contrib import messages
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
    """Emails the founder when a new client inquiry comes in, using Resend's
    HTTP API (works on hosts like Render that block outbound SMTP ports).
    Never raises — a failed notification should never break the contact form."""
    api_key = getattr(settings, "RESEND_API_KEY", "")
    notify_email = getattr(settings, "CONTACT_NOTIFY_EMAIL", "")
    if not api_key or not notify_email:
        return
    try:
        import requests
        requests.post(
            "https://api.resend.com/emails",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "from": "Insightara <onboarding@resend.dev>",
                "to": [notify_email],
                "subject": f"New Insightara inquiry from {inquiry.name}",
                "text": (
                    f"Name: {inquiry.name}\n"
                    f"Email: {inquiry.email}\n"
                    f"Company: {inquiry.company or '-'}\n\n"
                    f"Message:\n{inquiry.message}\n\n"
                    f"View it in the admin panel."
                ),
            },
            timeout=8,
        )
    except Exception:
        pass


def projects_list(request):
    projects = Project.objects.filter(status="published")
    return render(request, "core/projects.html", {"projects": projects})