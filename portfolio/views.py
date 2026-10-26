import json
import random
import math
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse

from .models import (
    Profile, Education, SkillCategory, Skill,
    Project, Certification, Activity, ContactMessage
)

def home(request):
    profile = Profile.objects.first()
    education_list = Education.objects.all()
    categories = SkillCategory.objects.prefetch_related('skills').all()
    projects = Project.objects.all()
    certifications = Certification.objects.all()
    activities = Activity.objects.all()

    context = {
        'profile': profile,
        'education_list': education_list,
        'categories': categories,
        'projects': projects,
        'certifications': certifications,
        'activities': activities,
    }
    return render(request, 'portfolio/index.html', context)


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    related_projects = Project.objects.exclude(id=project.id)[:3]
    return render(request, 'portfolio/project_detail.html', {
        'project': project,
        'related_projects': related_projects,
    })


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()

        if name and email and message:
            ContactMessage.objects.create(
                name=name,
                email=email,
                subject=subject or 'Portfolio Inquiry',
                message=message
            )
            messages.success(request, f"Thank you, {name}! Your message has been sent successfully. Nisha will get back to you soon.")
        else:
            messages.error(request, "Please fill in all required fields before submitting.")
        
        return redirect('/#contact')

    return redirect('portfolio:home')


def run_kmeans_clustering(data_points, k=4, iterations=15):
    """
    K-Means clustering algorithm implementation for Customer RFM Segmentation.
    Works seamlessly without external OpenMP / heavy DLL dependencies.
    """
    random.seed(42)
    # Normalize features for distance computation (standard min-max or z-score)
    r_vals = [p['recency'] for p in data_points]
    f_vals = [p['frequency'] for p in data_points]
    m_vals = [p['monetary'] for p in data_points]

    r_min, r_max = min(r_vals), max(r_vals)
    f_min, f_max = min(f_vals), max(f_vals)
    m_min, m_max = min(m_vals), max(m_vals)

    def norm(r, f, m):
        nr = (r - r_min) / (r_max - r_min + 1e-9)
        nf = (f - f_min) / (f_max - f_min + 1e-9)
        nm = (m - m_min) / (m_max - m_min + 1e-9)
        return nr, nf, nm

    normalized_pts = [norm(p['recency'], p['frequency'], p['monetary']) for p in data_points]

    # Initialize k centroids
    centroids = [normalized_pts[i * (len(normalized_pts) // k)] for i in range(k)]

    for _ in range(iterations):
        clusters = [[] for _ in range(k)]
        for idx, pt in enumerate(normalized_pts):
            dists = [
                math.sqrt((pt[0]-c[0])**2 + (pt[1]-c[1])**2 + (pt[2]-c[2])**2)
                for c in centroids
            ]
            assigned_c = dists.index(min(dists))
            clusters[assigned_c].append(idx)

        # Update centroids
        new_centroids = []
        for c_idx in range(k):
            members = clusters[c_idx]
            if members:
                c_nr = sum(normalized_pts[m][0] for m in members) / len(members)
                c_nf = sum(normalized_pts[m][1] for m in members) / len(members)
                c_nm = sum(normalized_pts[m][2] for m in members) / len(members)
                new_centroids.append((c_nr, c_nf, c_nm))
            else:
                new_centroids.append(centroids[c_idx])
        centroids = new_centroids

    # Final assignment
    labels = [0] * len(data_points)
    for c_idx, members in enumerate(clusters):
        for m in members:
            labels[m] = c_idx

    return labels, centroids, (r_min, r_max, f_min, f_max, m_min, m_max)


def rfm_demo_api(request):
    """
    Live Machine Learning Demonstration:
    Performs Customer Segmentation Using RFM (Recency, Frequency, Monetary) & K-Means Clustering.
    """
    try:
        recency = float(request.GET.get('recency', 25))
        frequency = float(request.GET.get('frequency', 12))
        monetary = float(request.GET.get('monetary', 850))
    except (ValueError, TypeError):
        recency, frequency, monetary = 25.0, 12.0, 850.0

    random.seed(42)
    sample_customers = []

    # 1. Champions (Low Recency, High Frequency, High Spend)
    for _ in range(30):
        sample_customers.append({
            'recency': round(random.uniform(5, 40), 1),
            'frequency': round(random.uniform(20, 45), 1),
            'monetary': round(random.uniform(1800, 4800), 2),
        })

    # 2. Loyal Customers (Moderate Recency, Moderate Frequency, Moderate Spend)
    for _ in range(30):
        sample_customers.append({
            'recency': round(random.uniform(25, 75), 1),
            'frequency': round(random.uniform(9, 22), 1),
            'monetary': round(random.uniform(700, 1750), 2),
        })

    # 3. Potential / Emerging Customers (Low Recency, Low Frequency, Modest Spend)
    for _ in range(30):
        sample_customers.append({
            'recency': round(random.uniform(5, 55), 1),
            'frequency': round(random.uniform(1, 7), 1),
            'monetary': round(random.uniform(90, 550), 2),
        })

    # 4. At-Risk / Hibernating (High Recency, Low Frequency, Variable Spend)
    for _ in range(30):
        sample_customers.append({
            'recency': round(random.uniform(140, 360), 1),
            'frequency': round(random.uniform(1, 8), 1),
            'monetary': round(random.uniform(60, 650), 2),
        })

    labels, centroids, bounds = run_kmeans_clustering(sample_customers, k=4)

    # Compute cluster statistics
    cluster_stats = {}
    for c in range(4):
        indices = [i for i, lbl in enumerate(labels) if lbl == c]
        if indices:
            avg_r = sum(sample_customers[i]['recency'] for i in indices) / len(indices)
            avg_f = sum(sample_customers[i]['frequency'] for i in indices) / len(indices)
            avg_m = sum(sample_customers[i]['monetary'] for i in indices) / len(indices)
            cluster_stats[c] = {
                'avg_r': round(avg_r, 1),
                'avg_f': round(avg_f, 1),
                'avg_m': round(avg_m, 2),
                'count': len(indices)
            }
        else:
            cluster_stats[c] = {'avg_r': 0, 'avg_f': 0, 'avg_m': 0, 'count': 0}

    # Sort clusters by composite business score (frequency * monetary / recency)
    sorted_cluster_ids = sorted(
        cluster_stats.keys(),
        key=lambda c: (cluster_stats[c]['avg_m'] * cluster_stats[c]['avg_f']) / (cluster_stats[c]['avg_r'] + 1),
        reverse=True
    )

    segment_metadata = {
        sorted_cluster_ids[0]: {
            "name": "Champions (VIP)",
            "badge": "bg-success",
            "color": "#10b981",
            "advice": "High value and highly active. Reward with exclusive VIP perks and new releases."
        },
        sorted_cluster_ids[1]: {
            "name": "Loyal Customers",
            "badge": "bg-primary",
            "color": "#3b82f6",
            "advice": "Consistent purchase pattern. Upsell complementary services and maintain engagement."
        },
        sorted_cluster_ids[2]: {
            "name": "Potential Loyalists",
            "badge": "bg-info text-dark",
            "color": "#06b6d4",
            "advice": "Recent buyers with growth potential. Provide onboarding guides and discount incentives."
        },
        sorted_cluster_ids[3]: {
            "name": "At-Risk / Inactive",
            "badge": "bg-warning text-dark",
            "color": "#f59e0b",
            "advice": "Lapsed customers who haven't ordered recently. Launch win-back campaigns and re-engagement surveys."
        }
    }

    # Normalize user input point
    r_min, r_max, f_min, f_max, m_min, m_max = bounds
    u_nr = (recency - r_min) / (r_max - r_min + 1e-9)
    u_nf = (frequency - f_min) / (f_max - f_min + 1e-9)
    u_nm = (monetary - m_min) / (m_max - m_min + 1e-9)

    user_dists = [
        math.sqrt((u_nr - c[0])**2 + (u_nf - c[1])**2 + (u_nm - c[2])**2)
        for c in centroids
    ]
    pred_cluster = user_dists.index(min(user_dists))
    user_segment = segment_metadata.get(pred_cluster, segment_metadata[sorted_cluster_ids[0]])

    # Build chart data points
    points = []
    for i, cust in enumerate(sample_customers):
        c_id = labels[i]
        meta = segment_metadata[c_id]
        points.append({
            'x': cust['frequency'],
            'y': cust['monetary'],
            'recency': cust['recency'],
            'cluster_name': meta['name'],
            'color': meta['color'],
            'cluster_id': c_id,
        })

    return JsonResponse({
        'status': 'success',
        'prediction': {
            'cluster_id': pred_cluster,
            'segment_name': user_segment['name'],
            'badge': user_segment['badge'],
            'color': user_segment['color'],
            'advice': user_segment['advice'],
            'input': {
                'recency': recency,
                'frequency': frequency,
                'monetary': monetary,
            }
        },
        'clusters': [
            {
                'id': cid,
                'name': segment_metadata[cid]['name'],
                'badge': segment_metadata[cid]['badge'],
                'color': segment_metadata[cid]['color'],
                'avg_recency': cluster_stats[cid]['avg_r'],
                'avg_frequency': cluster_stats[cid]['avg_f'],
                'avg_monetary': cluster_stats[cid]['avg_m'],
                'count': cluster_stats[cid]['count']
            }
            for cid in sorted_cluster_ids
        ],
        'scatter_points': points
    })
