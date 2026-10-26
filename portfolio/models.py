from django.db import models

class Profile(models.Model):
    name = models.CharField(max_length=150, default="Nisha Rani Singha")
    tagline = models.CharField(
        max_length=255, 
        default="Computer Science & Engineering Student | Aspiring Data Scientist & ML Enthusiast"
    )
    bio = models.TextField(
        default=(
            "Computer Science and Engineering student with introductory knowledge of data science "
            "and machine learning. Completed an Ostad Data Science course and building foundational "
            "skills in Python, statistics, probability, data analysis, and machine learning. "
            "Interested in learning, practical projects, and entry-level opportunities."
        )
    )
    location = models.CharField(max_length=120, default="Dhaka, Bangladesh")
    email = models.EmailField(default="nishasingha277@gmail.com")
    phone = models.CharField(max_length=50, default="01609439468")
    avatar = models.ImageField(upload_to="profile/", blank=True, null=True)
    github = models.URLField(blank=True, default="https://github.com")
    linkedin = models.URLField(blank=True, default="https://linkedin.com")
    resume = models.FileField(upload_to="resume/", blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Profile Information"
        verbose_name_plural = "Profile Information"


class Education(models.Model):
    degree = models.CharField(max_length=200, default="Bachelor of Computer Science and Engineering")
    institution = models.CharField(max_length=200, default="Northern University Bangladesh")
    duration = models.CharField(max_length=100, default="Dec 2024 – Dec 2027")
    cgpa = models.CharField(max_length=20, default="3.75")
    description = models.TextField(
        blank=True,
        default="Pursuing undergraduate studies focused on software engineering, algorithm design, data structures, and computer science foundations with strong academic excellence."
    )
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order']
        verbose_name_plural = "Education"

    def __str__(self):
        return f"{self.degree} - {self.institution}"


class SkillCategory(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, default="fas fa-code", help_text="FontAwesome icon class")
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order']
        verbose_name_plural = "Skill Categories"

    def __str__(self):
        return self.name


class Skill(models.Model):
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE, related_name="skills")
    name = models.CharField(max_length=100)
    proficiency = models.PositiveIntegerField(default=80, help_text="Percentage 1-100")
    level = models.CharField(max_length=50, default="Proficient")
    icon = models.CharField(max_length=50, blank=True, help_text="FontAwesome icon class")
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.name} ({self.category.name})"


class Project(models.Model):
    CATEGORY_CHOICES = [
        ('ml', 'Machine Learning'),
        ('da', 'Data Analysis'),
        ('eda', 'Exploratory Data Analysis'),
        ('dev', 'Web Development'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='da')
    short_description = models.CharField(max_length=300)
    description = models.TextField()
    technologies = models.CharField(max_length=255, help_text="Comma-separated technologies e.g. Python, Pandas, Scikit-learn")
    image = models.ImageField(upload_to="projects/", blank=True, null=True)
    featured = models.BooleanField(default=True)
    github_url = models.URLField(blank=True, default="https://github.com")
    live_demo_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=1)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

    def get_tech_list(self):
        return [t.strip() for t in self.technologies.split(',') if t.strip()]


class Certification(models.Model):
    title = models.CharField(max_length=200, default="Ostad Data Science Course")
    issuer = models.CharField(max_length=150, default="Ostad")
    issue_date = models.CharField(max_length=50, default="2024")
    description = models.TextField(
        default="Comprehensive foundational coursework covering Python programming, statistics and probability, data wrangling with Pandas/NumPy, exploratory data analysis, and machine learning model training with Scikit-learn."
    )
    certificate_url = models.URLField(blank=True)

    def __str__(self):
        return f"{self.title} - {self.issuer}"


class Activity(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100, default="Extracurricular")
    icon = models.CharField(max_length=50, default="fas fa-trophy")
    description = models.TextField()
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order']
        verbose_name_plural = "Extracurricular Activities & Interests"

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"
