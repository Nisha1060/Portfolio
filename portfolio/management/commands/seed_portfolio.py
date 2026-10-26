from django.core.management.base import BaseCommand
from portfolio.models import (
    Profile, Education, SkillCategory, Skill, 
    Project, Certification, Activity
)

class Command(BaseCommand):
    help = "Seed database with initial portfolio data from Nisha Rani Singha's CV"

    def handle(self, *args, **options):
        self.stdout.write("Seeding portfolio data...")

        # 1. Profile
        profile, created = Profile.objects.get_or_create(id=1)
        profile.name = "Nisha Rani Singha"
        profile.tagline = "Computer Science & Engineering Student | Aspiring Data Scientist & ML Enthusiast"
        profile.bio = (
            "Computer Science and Engineering student with introductory knowledge of data science "
            "and machine learning. Completed an Ostad Data Science course and building foundational "
            "skills in Python, statistics, probability, data analysis, and machine learning. "
            "Interested in learning, practical projects, and entry-level opportunities."
        )
        profile.location = "Dhaka, Bangladesh"
        profile.email = "nishasingha277@gmail.com"
        profile.phone = "01609439468"
        profile.avatar = "profile/profile.jpg"
        profile.github = "https://github.com"
        profile.linkedin = "https://linkedin.com"
        profile.save()
        self.stdout.write(self.style.SUCCESS("  [OK] Profile created/updated"))

        # 2. Education
        Education.objects.all().delete()
        Education.objects.create(
            degree="Bachelor of Computer Science and Engineering",
            institution="Northern University Bangladesh",
            duration="DEC_2024 – DEC_2027",
            cgpa="3.75",
            description=(
                "Undergraduate student in Computer Science and Engineering with an outstanding CGPA of 3.75. "
                "Active coursework covering Object-Oriented Programming, Data Structures, Algorithms, "
                "Database Systems, Probability & Statistics, and Discrete Mathematics."
            ),
            order=1
        )
        self.stdout.write(self.style.SUCCESS("  [OK] Education created"))

        # 3. Skill Categories and Skills
        Skill.objects.all().delete()
        SkillCategory.objects.all().delete()

        cat_prog = SkillCategory.objects.create(name="Programming", icon="fas fa-code", order=1)
        cat_data = SkillCategory.objects.create(name="Data Analysis", icon="fas fa-chart-line", order=2)
        cat_ml = SkillCategory.objects.create(name="Machine Learning", icon="fas fa-brain", order=3)
        cat_stats = SkillCategory.objects.create(name="Statistics & Math", icon="fas fa-square-root-alt", order=4)
        cat_core = SkillCategory.objects.create(name="Core Competencies & Tools", icon="fas fa-tools", order=5)

        skills_data = [
            (cat_prog, "Python", 90, "Proficient", "fab fa-python", 1),
            (cat_prog, "Django", 78, "Intermediate", "fab fa-python", 2),
            (cat_data, "Pandas", 88, "Proficient", "fas fa-table", 1),
            (cat_data, "NumPy", 85, "Proficient", "fas fa-calculator", 2),
            (cat_data, "Exploratory Data Analysis (EDA)", 85, "Proficient", "fas fa-search-plus", 3),
            (cat_data, "Data Preprocessing", 82, "Intermediate", "fas fa-filter", 4),
            (cat_ml, "Scikit-learn", 80, "Intermediate", "fas fa-cogs", 1),
            (cat_ml, "Model Training Concepts", 75, "Foundational / Beginner", "fas fa-project-diagram", 2),
            (cat_ml, "K-Means Clustering & RFM", 85, "Proficient", "fas fa-cubes", 3),
            (cat_stats, "Statistics and Probability", 85, "Proficient", "fas fa-percentage", 1),
            (cat_stats, "Hypothesis Testing & Variance", 78, "Intermediate", "fas fa-chart-bar", 2),
            (cat_core, "Jupyter Notebook", 88, "Proficient", "fas fa-book", 1),
            (cat_core, "Git & GitHub", 80, "Intermediate", "fab fa-git-alt", 2),
            (cat_core, "Data Visualization (Matplotlib/Seaborn)", 82, "Intermediate", "fas fa-chart-pie", 3),
        ]

        for cat, name, prof, level, icon, order in skills_data:
            Skill.objects.create(
                category=cat,
                name=name,
                proficiency=prof,
                level=level,
                icon=icon,
                order=order
            )
        self.stdout.write(self.style.SUCCESS("  [OK] Skills and categories created"))

        # 4. Projects
        Project.objects.all().delete()
        Project.objects.create(
            title="Customer Segmentation Using RFM & K-Means Clustering",
            slug="customer-segmentation-rfm-kmeans",
            category="ml",
            short_description="Behavioral customer segmentation using Recency, Frequency, and Monetary (RFM) modeling and Scikit-learn K-Means unsupervised clustering.",
            description=(
                "Architected an unsupervised machine learning clustering model to partition e-commerce / retail customers "
                "into distinct behavioral cohorts based on their transaction patterns (Recency, Frequency, and Monetary value). "
                "Calculated RFM metrics, normalized features with StandardScaler, determined the optimal cluster count using the Elbow Method "
                "and Silhouette score, and trained a Scikit-learn KMeans algorithm. Generated meaningful actionable segments (Champions, "
                "Loyal Customers, Potential Loyalists, and At-Risk customers) to assist targeted marketing and customer retention."
            ),
            technologies="Python, Scikit-learn, Pandas, NumPy, Matplotlib, Seaborn, RFM Modeling, K-Means Clustering",
            featured=True,
            github_url="https://github.com",
            live_demo_url="/#demo",
            order=1
        )

        Project.objects.create(
            title="Exploratory Data Analysis (EDA)",
            slug="exploratory-data-analysis-eda",
            category="eda",
            short_description="In-depth statistical investigation, distribution analysis, correlation matrices, and anomaly detection across complex datasets.",
            description=(
                "Conducted end-to-end Exploratory Data Analysis (EDA) on real-world datasets to uncover hidden patterns, trends, "
                "and relationships before model building. Performed thorough data hygiene, including missing value imputation, "
                "outlier identification using Interquartile Range (IQR) and Z-score methods, univariate and bivariate distributions, "
                "and Pearson/Spearman correlation heatmaps. Visualized key business drivers through rich graphical representations."
            ),
            technologies="Python, Pandas, NumPy, Matplotlib, Seaborn, Statistical Summaries, IQR Outlier Detection",
            featured=True,
            github_url="https://github.com",
            order=2
        )

        Project.objects.create(
            title="Data Analysis Using Pandas",
            slug="data-analysis-using-pandas",
            category="da",
            short_description="High-performance data manipulation, multi-dimensional grouping, aggregations, and cleaning pipelines using the Pandas library.",
            description=(
                "Engineered robust data analysis and wrangling pipelines using Python and Pandas. Implemented advanced filtering, "
                "multi-index hierarchical data grouping, customized aggregation functions, date-time transformations, and pivot tables. "
                "Processed large datasets, cleaned inconsistencies, and generated analytical reports that provide key quantitative indicators."
            ),
            technologies="Python, Pandas, Data Cleaning, Wrangling, GroupBy Aggregations, NumPy",
            featured=True,
            github_url="https://github.com",
            order=3
        )
        self.stdout.write(self.style.SUCCESS("  [OK] Projects created"))

        # 5. Certification
        Certification.objects.all().delete()
        Certification.objects.create(
            title="Ostad Data Science Course",
            issuer="Ostad",
            issue_date="Completed",
            description=(
                "Completed intensive Data Science training through Ostad. Acquired strong foundational skills in Python programming, "
                "descriptive and inferential statistics, probability distributions, data wrangling and transformation using Pandas and NumPy, "
                "exploratory data analysis (EDA), and machine learning workflow fundamentals with Scikit-learn."
            )
        )
        self.stdout.write(self.style.SUCCESS("  [OK] Certification created"))

        # 6. Activities
        Activity.objects.all().delete()
        Activity.objects.create(
            title="Participation in Programming Contests",
            category="Competitive Programming & Algorithmic Problem Solving",
            icon="fas fa-laptop-code",
            description=(
                "Actively engaged in programming competitions and problem-solving platforms. Regularly solves algorithmic challenges "
                "involving arrays, search algorithms, sorting, recursion, and dynamic logic to hone analytical speed and precision."
            ),
            order=1
        )
        Activity.objects.create(
            title="Research Interest in Collective Behaviour",
            category="Academic & Scientific Research",
            icon="fas fa-network-wired",
            description=(
                "Deep curiosity and ongoing exploratory research into Collective Behaviour -- how simple local rules in multi-agent "
                "systems give rise to complex emergent macroscopic phenomena, inspired by biological swarms, crowd dynamics, "
                "and distributed algorithmic consensus."
            ),
            order=2
        )
        self.stdout.write(self.style.SUCCESS("  [OK] Activities created"))
        self.stdout.write(self.style.SUCCESS("Portfolio seeding finished successfully!"))
