document.addEventListener('DOMContentLoaded', function () {
    // 1. Initialize Navbar Scroll Behavior
    const nav = document.getElementById('mainNav');
    window.addEventListener('scroll', function () {
        if (window.scrollY > 50) {
            nav.classList.add('shadow-lg');
            nav.style.padding = '0.75rem 0';
        } else {
            nav.classList.remove('shadow-lg');
            nav.style.padding = '1rem 0';
        }
    });

    // 2. Interactive Machine Learning Demo (RFM & K-Means)
    const recencySlider = document.getElementById('recencySlider');
    const frequencySlider = document.getElementById('frequencySlider');
    const monetarySlider = document.getElementById('monetarySlider');

    const recencyVal = document.getElementById('recencyVal');
    const frequencyVal = document.getElementById('frequencyVal');
    const monetaryVal = document.getElementById('monetaryVal');

    const runMlBtn = document.getElementById('runMlBtn');
    const clusterChartCanvas = document.getElementById('clusterChart');
    let clusterChart = null;

    if (recencySlider && frequencySlider && monetarySlider) {
        // Sync slider badges
        recencySlider.addEventListener('input', () => recencyVal.textContent = recencySlider.value + ' days');
        frequencySlider.addEventListener('input', () => frequencyVal.textContent = frequencySlider.value + ' orders');
        monetarySlider.addEventListener('input', () => monetaryVal.textContent = '$' + Number(monetarySlider.value).toLocaleString());

        // Preset buttons
        document.querySelectorAll('.preset-btn').forEach(btn => {
            btn.addEventListener('click', function () {
                const r = this.dataset.recency;
                const f = this.dataset.frequency;
                const m = this.dataset.monetary;

                recencySlider.value = r;
                frequencySlider.value = f;
                monetarySlider.value = m;

                recencyVal.textContent = r + ' days';
                frequencyVal.textContent = f + ' orders';
                monetaryVal.textContent = '$' + Number(m).toLocaleString();

                runClusteringPrediction();
            });
        });

        // Run ML Prediction Button
        if (runMlBtn) {
            runMlBtn.addEventListener('click', runClusteringPrediction);
        }

        // Run initial prediction on page load
        runClusteringPrediction();
    }

    function runClusteringPrediction() {
        const r = recencySlider.value;
        const f = frequencySlider.value;
        const m = monetarySlider.value;

        if (runMlBtn) {
            runMlBtn.disabled = true;
            runMlBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Clustering Data...';
        }

        fetch(`/api/rfm-cluster/?recency=${r}&frequency=${f}&monetary=${m}`)
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    updatePredictionUI(data.prediction);
                    updateClusterBreakdown(data.clusters);
                    renderClusterScatterPlot(data.scatter_points, data.prediction);
                }
            })
            .catch(err => {
                console.error('Error fetching cluster prediction:', err);
            })
            .finally(() => {
                if (runMlBtn) {
                    runMlBtn.disabled = false;
                    runMlBtn.innerHTML = '<i class="fas fa-play me-2"></i>Run Real-Time ML Segmentation';
                }
            });
    }

    function updatePredictionUI(prediction) {
        const segmentBadge = document.getElementById('predSegmentBadge');
        const segmentName = document.getElementById('predSegmentName');
        const adviceText = document.getElementById('predAdvice');
        const inputEcho = document.getElementById('predInputEcho');

        if (segmentBadge) {
            segmentBadge.className = `badge ${prediction.badge} px-3 py-2 fs-6 rounded-pill`;
            segmentBadge.textContent = prediction.segment_name;
        }

        if (segmentName) {
            segmentName.textContent = prediction.segment_name;
            segmentName.style.color = prediction.color;
        }

        if (adviceText) {
            adviceText.textContent = prediction.advice;
        }

        if (inputEcho) {
            inputEcho.innerHTML = `Customer Metrics: <strong>${prediction.input_data ? prediction.input_data.recency : prediction.input.recency} days</strong> recency &bull; <strong>${prediction.input_data ? prediction.input_data.frequency : prediction.input.frequency} orders</strong> &bull; <strong>$${Number(prediction.input_data ? prediction.input_data.monetary : prediction.input.monetary).toLocaleString()} spend</strong>`;
        }
    }

    function updateClusterBreakdown(clusters) {
        const container = document.getElementById('clusterStatsContainer');
        if (!container) return;

        container.innerHTML = clusters.map(c => `
            <div class="col-6 col-md-3">
                <div class="p-3 rounded-3" style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07);">
                    <div class="d-flex align-items-center justify-content-between mb-2">
                        <span class="badge ${c.badge} rounded-pill">${c.name}</span>
                        <small class="text-secondary font-mono">${c.count} clients</small>
                    </div>
                    <div class="small text-secondary">
                        <div>Avg Recency: <span class="text-light fw-medium">${c.avg_recency}d</span></div>
                        <div>Avg Orders: <span class="text-light fw-medium">${c.avg_frequency}</span></div>
                        <div>Avg Spend: <span class="text-light fw-medium">$${Number(c.avg_monetary).toLocaleString()}</span></div>
                    </div>
                </div>
            </div>
        `).join('');
    }

    function renderClusterScatterPlot(points, prediction) {
        if (!clusterChartCanvas) return;

        // Group points by cluster
        const datasets = [];
        const clusterMap = {};

        points.forEach(p => {
            if (!clusterMap[p.cluster_name]) {
                clusterMap[p.cluster_name] = {
                    label: p.cluster_name,
                    data: [],
                    backgroundColor: p.color + 'aa',
                    borderColor: p.color,
                    borderWidth: 1,
                    pointRadius: 5,
                    pointHoverRadius: 7
                };
            }
            clusterMap[p.cluster_name].data.push({ x: p.x, y: p.y, recency: p.recency });
        });

        for (const key in clusterMap) {
            datasets.push(clusterMap[key]);
        }

        // Add user point
        const userPoint = prediction.input_data || prediction.input;
        datasets.push({
            label: 'Your Current Input Customer',
            data: [{ x: userPoint.frequency, y: userPoint.monetary, recency: userPoint.recency }],
            backgroundColor: '#ffffff',
            borderColor: '#f43f5e',
            borderWidth: 3,
            pointRadius: 10,
            pointHoverRadius: 12,
            pointStyle: 'crossRot'
        });

        if (clusterChart) {
            clusterChart.destroy();
        }

        const ctx = clusterChartCanvas.getContext('2d');
        clusterChart = new Chart(ctx, {
            type: 'scatter',
            data: { datasets: datasets },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                        labels: {
                            color: '#94a3b8',
                            font: { family: 'Plus Jakarta Sans', size: 12 },
                            usePointStyle: true,
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function (context) {
                                const pt = context.raw;
                                return `${context.dataset.label}: ${pt.x} orders, $${Number(pt.y).toLocaleString()} (Recency: ${pt.recency}d)`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        title: { display: true, text: 'Purchase Frequency (Orders)', color: '#94a3b8' },
                        grid: { color: 'rgba(255,255,255,0.06)' },
                        ticks: { color: '#94a3b8' }
                    },
                    y: {
                        title: { display: true, text: 'Monetary Spend ($)', color: '#94a3b8' },
                        grid: { color: 'rgba(255,255,255,0.06)' },
                        ticks: { color: '#94a3b8' }
                    }
                }
            }
        });
    }

    // 3. Quick Copy helper for email/phone
    window.copyText = function (text, elementId) {
        navigator.clipboard.writeText(text).then(() => {
            const el = document.getElementById(elementId);
            if (el) {
                const originalHtml = el.innerHTML;
                el.innerHTML = '<i class="fas fa-check text-success me-1"></i>Copied!';
                setTimeout(() => {
                    el.innerHTML = originalHtml;
                }, 2000);
            }
        });
    };
});
