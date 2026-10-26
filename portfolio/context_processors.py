from .models import Profile

def portfolio_context(request):
    profile = Profile.objects.first()
    if not profile:
        profile = Profile(
            name="Nisha Rani Singha",
            tagline="Computer Science & Engineering Student | Aspiring Data Scientist & ML Enthusiast",
            email="nishasingha277@gmail.com",
            phone="01609439468",
            location="Dhaka, Bangladesh"
        )
    return {
        'site_profile': profile
    }
