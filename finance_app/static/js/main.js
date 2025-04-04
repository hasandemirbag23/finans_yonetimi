// Ana JavaScript Dosyası

document.addEventListener('DOMContentLoaded', function() {
    // Tooltips aktifleştirme
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Grafikler için renk paleti
    const chartColors = [
        '#3498db', // mavi
        '#e74c3c', // kırmızı
        '#2ecc71', // yeşil
        '#f39c12', // turuncu
        '#9b59b6', // mor
        '#1abc9c', // turkuaz
        '#34495e', // lacivert
        '#d35400', // koyu turuncu
        '#7f8c8d', // gri
        '#27ae60', // koyu yeşil
        '#2980b9', // koyu mavi
        '#8e44ad'  // koyu mor
    ];
    
    // Tarih formatlama fonksiyonu
    function formatCurrency(amount) {
        return new Intl.NumberFormat('tr-TR', { style: 'currency', currency: 'TRY' }).format(amount);
    }
    
    // Dashboard sayfa kontrolü - Gelir/Gider pasta grafiği
    if (document.getElementById('income-category-chart')) {
        renderIncomeChart();
    }
    
    if (document.getElementById('expense-category-chart')) {
        renderExpenseChart();
    }
    
    // Rapor sayfası kontrolü
    if (document.getElementById('monthly-income-expense-chart')) {
        renderMonthlyComparisonChart();
    }
    
    if (document.getElementById('category-expense-chart')) {
        renderCategoryExpenseChart();
    }
    
    // Form alanları için tarih seçici
    const dateInputs = document.querySelectorAll('input[type="date"]');
    dateInputs.forEach(function(input) {
        if (!input.value) {
            input.valueAsDate = new Date();
        }
    });
    
    // Gelir kategorilerine göre pasta grafik oluştur
    function renderIncomeChart() {
        const ctx = document.getElementById('income-category-chart').getContext('2d');
        
        // Data element'inden veri çek
        const dataElement = document.getElementById('income-category-data');
        if (!dataElement) return;
        
        const categoryData = JSON.parse(dataElement.dataset.categories);
        const labels = categoryData.map(item => item.category);
        const data = categoryData.map(item => item.amount);
        
        new Chart(ctx, {
            type: 'pie',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: chartColors.slice(0, data.length),
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'right',
                    },
                    title: {
                        display: true,
                        text: 'Gelir Dağılımı'
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                let label = context.label || '';
                                if (label) {
                                    label += ': ';
                                }
                                label += formatCurrency(context.raw);
                                return label;
                            }
                        }
                    }
                }
            }
        });
    }
    
    // Gider kategorilerine göre pasta grafik oluştur
    function renderExpenseChart() {
        const ctx = document.getElementById('expense-category-chart').getContext('2d');
        
        // Data element'inden veri çek
        const dataElement = document.getElementById('expense-category-data');
        if (!dataElement) return;
        
        const categoryData = JSON.parse(dataElement.dataset.categories);
        const labels = categoryData.map(item => item.category);
        const data = categoryData.map(item => item.amount);
        
        new Chart(ctx, {
            type: 'pie',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: chartColors.slice(0, data.length),
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'right',
                    },
                    title: {
                        display: true,
                        text: 'Gider Dağılımı'
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                let label = context.label || '';
                                if (label) {
                                    label += ': ';
                                }
                                label += formatCurrency(context.raw);
                                return label;
                            }
                        }
                    }
                }
            }
        });
    }
    
    // Aylık gelir-gider karşılaştırma grafiği
    function renderMonthlyComparisonChart() {
        const ctx = document.getElementById('monthly-income-expense-chart').getContext('2d');
        
        // Data element'inden veri çek
        const dataElement = document.getElementById('monthly-comparison-data');
        if (!dataElement) return;
        
        const monthlyData = JSON.parse(dataElement.dataset.monthly);
        const labels = monthlyData.map(item => item.month);
        const incomeData = monthlyData.map(item => item.income);
        const expenseData = monthlyData.map(item => item.expense);
        
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Gelir',
                        data: incomeData,
                        backgroundColor: '#2ecc71',
                        borderColor: '#27ae60',
                        borderWidth: 1
                    },
                    {
                        label: 'Gider',
                        data: expenseData,
                        backgroundColor: '#e74c3c',
                        borderColor: '#c0392b',
                        borderWidth: 1
                    }
                ]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return formatCurrency(value);
                            }
                        }
                    }
                },
                plugins: {
                    title: {
                        display: true,
                        text: 'Aylık Gelir-Gider Karşılaştırması'
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                let label = context.dataset.label || '';
                                if (label) {
                                    label += ': ';
                                }
                                label += formatCurrency(context.raw);
                                return label;
                            }
                        }
                    }
                }
            }
        });
    }
    
    // Kategori bazlı gider dağılımı grafiği
    function renderCategoryExpenseChart() {
        const ctx = document.getElementById('category-expense-chart').getContext('2d');
        
        // Data element'inden veri çek
        const dataElement = document.getElementById('category-expense-data');
        if (!dataElement) return;
        
        const categoryData = JSON.parse(dataElement.dataset.categories);
        const labels = categoryData.map(item => item.category);
        const data = categoryData.map(item => item.percentage);
        
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: chartColors.slice(0, data.length),
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'right',
                    },
                    title: {
                        display: true,
                        text: 'Kategori Bazlı Gider Yüzdeleri'
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                let label = context.label || '';
                                if (label) {
                                    label += ': ';
                                }
                                label += context.raw.toFixed(2) + '%';
                                return label;
                            }
                        }
                    }
                }
            }
        });
    }
    
    // Silme işlemleri için onay kutusu
    const deleteButtons = document.querySelectorAll('.delete-btn');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            if (!confirm('Bu kaydı silmek istediğinizden emin misiniz?')) {
                e.preventDefault();
            }
        });
    });
}); 