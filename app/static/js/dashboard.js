document.addEventListener('DOMContentLoaded', function() {
    var ctx = document.getElementById('visitsChart');
    if (ctx) {
        var visitChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: JSON.parse('{{ visit_data.labels|tojson|safe }}'),
                datasets: [{
                    label: 'Pengunjung',
                    data: JSON.parse('{{ visit_data.data|tojson|safe }}'),
                    backgroundColor: 'rgba(78, 115, 223, 0.05)',
                    borderColor: 'rgba(78, 115, 223, 1)',
                    pointBackgroundColor: 'rgba(78, 115, 223, 1)',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: 'rgba(78, 115, 223, 1)',
                    pointRadius: 3,
                    pointHoverRadius: 3,
                    borderWidth: 2,
                    fill: true
                }]
            },
            options: {
                maintainAspectRatio: false,
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                if (value % 1 === 0) {
                                    return value;
                                }
                            }
                        }
                    }
                }
            }
        });
    }
});