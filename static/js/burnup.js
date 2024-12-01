document.addEventListener('DOMContentLoaded', function () {
    const ctx = document.getElementById('burnupChart').getContext('2d');
    if (!ctx) {
        console.error('Canvas element not found');
        return;
    }

    // 데이터 검증
    if (!chartData.labels || !chartData.totalTasks || !chartData.completedTasks) {
        console.error('Chart data is incomplete or incorrectly formatted');
        return;
    }

    // 차트 인스턴스 생성
    const burnupChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: chartData.labels,
            datasets: [{
                label: 'Total Tasks',
                data: chartData.totalTasks,
                borderColor: 'rgb(75, 192, 192)',
                backgroundColor: 'rgba(75, 192, 192, 0.5)',
                fill: true
            }, {
                label: 'Completed Tasks',
                data: chartData.completedTasks,
                borderColor: 'rgb(255, 99, 132)',
                backgroundColor: 'rgba(255, 99, 132, 0.5)',
                fill: true
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Number of Tasks'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Project Period'
                    }
                }
            },
            plugins: {
                legend: {
                    position: 'top'
                },
                tooltip: {
                    mode: 'index',
                    intersect: false
                }
            }
        }
    });
});
