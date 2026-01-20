// Global variables
let allProductsData = [];
let allNewsData = [];
let allData = null; // Store complete data object
let currentBrandFilter = 'all';
let currentNewsFilter = 'all';
let currentTab = 'price'; // Track current tab
let charts = {};

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    loadData();
    initializeCharts();
});

// Load data from JSON
async function loadData() {
    try {
        const response = await fetch('data/products.json');
        const data = await response.json();

        allProductsData = data.products;
        allNewsData = data.news;
        allData = data; // Store complete data

        updateSummaryStats(data);
        updateLastUpdateTime(data.lastUpdate);
        renderPriceTable(allProductsData);
        updateCharts(data);
        loadNews(data.news);
    } catch (error) {
        console.error('Error loading data:', error);
        document.getElementById('priceTableBody').innerHTML = `
            <tr>
                <td colspan="8" class="text-center text-danger">
                    Error loading data. Please try again later.
                </td>
            </tr>
        `;
    }
}

// Switch tab and update cards
function switchTab(tab) {
    currentTab = tab;

    // Show/hide brand filter buttons based on tab
    const brandButtons = document.getElementById('brandFilterButtons');
    if (tab === 'trends') {
        // Hide brand buttons for Price Trends
        brandButtons.parentElement.parentElement.style.display = 'none';
    } else {
        // Show brand buttons for other tabs
        brandButtons.parentElement.parentElement.style.display = 'block';
    }

    updateCardsForTab();
}

// Update cards based on current tab
function updateCardsForTab() {
    if (!allData) return;

    switch(currentTab) {
        case 'price':
            // Show price-related stats with current brand filter
            updateSummaryStats(allData, currentBrandFilter);
            break;
        case 'trends':
            // Always show all brands for trends
            updateTrendStats(allData, 'all');
            break;
        case 'news':
            // Show news-related stats with current brand filter
            updateNewsStats(allData, currentBrandFilter);
            break;
    }
}

// Update summary statistics (dynamic by brand filter)
function updateSummaryStats(data, brandFilter = 'all') {
    // Filter products by brand
    let products = brandFilter === 'all'
        ? data.products
        : data.products.filter(p => p.brand === brandFilter);

    // Update card title
    if (brandFilter === 'all') {
        document.getElementById('cardTitle1').textContent = 'Total Products';
    } else {
        document.getElementById('cardTitle1').textContent = brandFilter + ' Products';
    }

    // Total products
    document.getElementById('totalProducts').textContent = products.length;

    // Count price changes
    let priceChanges = 0;
    products.forEach(product => {
        Object.values(product.channels).forEach(channel => {
            if (channel.change && channel.change !== 0) {
                priceChanges++;
            }
        });
    });
    document.getElementById('priceChanges').textContent = priceChanges;

    // Calculate average price and lowest price
    let totalPrice = 0;
    let priceCount = 0;
    let allPrices = [];

    products.forEach(product => {
        Object.values(product.channels).forEach(channel => {
            if (channel.price && channel.price > 0) {
                totalPrice += channel.price;
                priceCount++;
                allPrices.push(channel.price);
            }
        });
    });

    const avgPrice = priceCount > 0 ? (totalPrice / priceCount).toFixed(2) : 0;
    const lowestPrice = allPrices.length > 0 ? Math.min(...allPrices).toFixed(2) : 0;

    document.getElementById('avgPrice').textContent = '$' + avgPrice;
    document.getElementById('lowestPrice').textContent = '$' + lowestPrice;
}

// Update last update time
function updateLastUpdateTime(timestamp) {
    const date = new Date(timestamp);
    const formatted = date.toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
    document.getElementById('lastUpdate').textContent = 'Last Update: ' + formatted;
}

// Render price comparison table
function renderPriceTable(products) {
    const tbody = document.getElementById('priceTableBody');
    tbody.innerHTML = '';

    // Filter by brand if needed
    let filteredProducts = currentBrandFilter === 'all'
        ? products
        : products.filter(p => p.brand === currentBrandFilter);

    if (filteredProducts.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="8" class="text-center">No products found for this brand.</td>
            </tr>
        `;
        return;
    }

    filteredProducts.forEach(product => {
        const row = document.createElement('tr');
        row.className = 'fade-in';

        // Brand
        const brandClass = 'brand-' + product.brand.toLowerCase();
        const brandCell = `<td><span class="brand-badge ${brandClass}">${product.brand}</span></td>`;

        // Product name with NEW badge
        const isNewProduct = product.note && (
            product.note.includes('CES 2026') ||
            product.note.includes('Launch Jan') ||
            product.note.includes('Pre-order')
        );
        const newBadge = isNewProduct ? '<span class="badge bg-danger ms-2">NEW</span>' : '';
        const productCell = `<td><strong>${product.name}</strong>${newBadge}</td>`;

        // MSRP cell
        const msrp = product.msrp || product.channels.official.msrp || null;
        let msrpCell = '';
        if (msrp && msrp > 0) {
            msrpCell = `<td class="price-cell text-muted"><small>$${msrp.toFixed(2)}</small></td>`;
        } else {
            msrpCell = '<td class="price-unavailable"><small>未公开</small></td>';
        }

        // Channels
        const officialCell = formatPriceCell(product.channels.official);
        const amazonCell = formatPriceCell(product.channels.amazon);
        const walmartCell = formatPriceCell(product.channels.walmart);
        const costcoCell = formatPriceCell(product.channels.costco);
        const ebayCell = formatPriceCell(product.channels.ebay);

        // 24h change - calculate overall trend
        const changeCell = formatChangeCell(product);

        row.innerHTML = brandCell + productCell + msrpCell + officialCell + amazonCell + walmartCell + costcoCell + ebayCell + changeCell;
        tbody.appendChild(row);
    });
}

// Format price cell with clickable link and confidence indicator
function formatPriceCell(channel) {
    if (!channel || !channel.price || channel.price === 0) {
        return '<td class="price-unavailable">N/A</td>';
    }

    const price = '$' + channel.price.toFixed(2);
    let priceClass = 'price-cell';

    if (channel.change) {
        if (channel.change > 0) priceClass += ' price-up';
        else if (channel.change < 0) priceClass += ' price-down';
    }

    // Check confidence level - Only VERIFIED or VERIFIED_SALE are accurate
    const confidence = channel.confidence || 'ESTIMATED';
    const isVerified = confidence === 'VERIFIED' || confidence === 'VERIFIED_SALE';

    // Add confidence indicator for all non-verified prices
    let confidenceTag = '';
    if (!isVerified) {
        const source = channel.price_source || 'Estimated from official MSRP';
        const shortSource = source.length > 50 ? source.substring(0, 47) + '...' : source;
        confidenceTag = ' <span class="price-estimated" title="' + shortSource + '">(估算)</span>';
    }

    // Add clickable link if URL is available
    if (channel.url) {
        return `<td class="${priceClass}"><a href="${channel.url}" target="_blank" rel="noopener noreferrer" class="price-link" title="Click to verify actual price">${price}</a>${confidenceTag}</td>`;
    }

    return `<td class="${priceClass}">${price}${confidenceTag}</td>`;
}

// Format change cell
function formatChangeCell(product) {
    // Calculate average change across all channels
    let totalChange = 0;
    let changeCount = 0;

    Object.values(product.channels).forEach(channel => {
        if (channel.change && channel.price > 0) {
            totalChange += channel.change;
            changeCount++;
        }
    });

    if (changeCount === 0) {
        return '<td><span class="change-indicator change-neutral">No change</span></td>';
    }

    const avgChange = totalChange / changeCount;
    const changePercent = avgChange.toFixed(1) + '%';

    if (avgChange > 0) {
        return `<td><span class="change-indicator change-up"><i class="bi bi-arrow-up"></i> ${changePercent}</span></td>`;
    } else if (avgChange < 0) {
        return `<td><span class="change-indicator change-down"><i class="bi bi-arrow-down"></i> ${changePercent}</span></td>`;
    } else {
        return '<td><span class="change-indicator change-neutral">0%</span></td>';
    }
}

// Filter by brand (unified for all tabs)
function filterBrand(brand) {
    currentBrandFilter = brand;
    currentNewsFilter = brand; // Sync news filter

    // Update content based on current tab
    renderPriceTable(allProductsData);
    loadNews(allNewsData);

    // Update cards based on current tab
    updateCardsForTab();

    // Update button states (global buttons)
    const buttons = document.querySelectorAll('#brandFilterButtons button');
    buttons.forEach(btn => {
        btn.classList.remove('active');
        if (btn.textContent.trim() === brand || (brand === 'all' && btn.textContent.trim() === 'All Brands')) {
            btn.classList.add('active');
        }
    });
}

// Initialize charts
function initializeCharts() {
    // Price Trend Chart
    const trendCtx = document.getElementById('priceTrendChart');
    if (trendCtx) {
        charts.priceTrend = new Chart(trendCtx, {
            type: 'line',
            data: {
                labels: [],
                datasets: []
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: false,
                        ticks: {
                            callback: function(value) {
                                return '$' + value;
                            }
                        }
                    }
                }
            }
        });
    }

    // Brand Comparison Chart
    const brandCtx = document.getElementById('brandComparisonChart');
    if (brandCtx) {
        charts.brandComparison = new Chart(brandCtx, {
            type: 'bar',
            data: {
                labels: [],
                datasets: [{
                    label: 'Average Price',
                    data: [],
                    backgroundColor: 'rgba(13, 110, 253, 0.5)',
                    borderColor: 'rgba(13, 110, 253, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return '$' + value;
                            }
                        }
                    }
                }
            }
        });
    }

    // Price Forecast Chart
    const forecastCtx = document.getElementById('priceForecastChart');
    if (forecastCtx) {
        charts.priceForecast = new Chart(forecastCtx, {
            type: 'line',
            data: {
                labels: [],
                datasets: []
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        position: 'top',
                    }
                },
                scales: {
                    y: {
                        beginAtZero: false,
                        ticks: {
                            callback: function(value) {
                                return '$' + value;
                            }
                        }
                    }
                }
            }
        });
    }
}

// Update charts with data
function updateCharts(data) {
    // Update price trend chart
    if (data.priceHistory && charts.priceTrend) {
        const brands = Object.keys(data.priceHistory);
        const datasets = brands.map((brand, index) => {
            const colors = [
                'rgb(255, 99, 132)',
                'rgb(54, 162, 235)',
                'rgb(75, 192, 192)',
                'rgb(255, 205, 86)',
                'rgb(153, 102, 255)',
                'rgb(255, 159, 64)',
                'rgb(199, 199, 199)',
                'rgb(83, 102, 255)'
            ];

            return {
                label: brand,
                data: data.priceHistory[brand].prices,
                borderColor: colors[index % colors.length],
                backgroundColor: colors[index % colors.length] + '33',
                tension: 0.3
            };
        });

        charts.priceTrend.data.labels = data.priceHistory[brands[0]].dates;
        charts.priceTrend.data.datasets = datasets;
        charts.priceTrend.update();
    }

    // Update brand comparison chart
    if (data.brandAverages && charts.brandComparison) {
        const brands = Object.keys(data.brandAverages);
        const prices = Object.values(data.brandAverages);

        charts.brandComparison.data.labels = brands;
        charts.brandComparison.data.datasets[0].data = prices;
        charts.brandComparison.update();
    }

    // Update forecast chart
    if (data.priceForecast && charts.priceForecast) {
        const brands = Object.keys(data.priceForecast);
        const datasets = brands.map((brand, index) => {
            const colors = [
                'rgb(255, 99, 132)',
                'rgb(54, 162, 235)',
                'rgb(75, 192, 192)',
                'rgb(255, 205, 86)',
                'rgb(153, 102, 255)',
                'rgb(255, 159, 64)',
                'rgb(199, 199, 199)',
                'rgb(83, 102, 255)'
            ];

            return {
                label: brand + ' (Forecast)',
                data: data.priceForecast[brand].prices,
                borderColor: colors[index % colors.length],
                backgroundColor: colors[index % colors.length] + '33',
                borderDash: [5, 5],
                tension: 0.3
            };
        });

        charts.priceForecast.data.labels = data.priceForecast[brands[0]].dates;
        charts.priceForecast.data.datasets = datasets;
        charts.priceForecast.update();
    }
}

// Load news (with brand filter support)
function loadNews(newsData) {
    const container = document.getElementById('newsContainer');
    container.innerHTML = '';

    if (!newsData || newsData.length === 0) {
        container.innerHTML = '<div class="col-12 text-center">No news available.</div>';
        return;
    }

    // Filter by brand if needed
    let filteredNews = currentNewsFilter === 'all'
        ? newsData
        : newsData.filter(n => n.brand === currentNewsFilter);

    if (filteredNews.length === 0) {
        container.innerHTML = '<div class="col-12 text-center">No news found for this brand.</div>';
        return;
    }

    filteredNews.forEach(newsItem => {
        const col = document.createElement('div');
        col.className = 'col-md-6 col-lg-4 mb-4 fade-in';

        const card = `
            <div class="card news-card h-100">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start mb-2">
                        <span class="brand-badge brand-${newsItem.brand.toLowerCase()}">${newsItem.brand}</span>
                        <span class="news-date">${formatDate(newsItem.date)}</span>
                    </div>
                    <h5 class="card-title">${newsItem.title}</h5>
                    <p class="card-text">${newsItem.summary}</p>
                    <a href="${newsItem.url}" target="_blank" class="btn btn-sm btn-outline-primary">Read More</a>
                    <div class="mt-2">
                        <span class="news-source">Source: ${newsItem.source}</span>
                    </div>
                </div>
            </div>
        `;

        col.innerHTML = card;
        container.appendChild(col);
    });
}

// Format date - Always show actual date in YYYY-MM-DD format
function formatDate(dateString) {
    const date = new Date(dateString);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

// Manual update function - Reloads latest data
async function manualUpdate() {
    const button = event.target.closest('button');
    const originalHTML = button.innerHTML;
    button.disabled = true;
    button.innerHTML = '<span class="spinner-border spinner-border-sm" role="status"></span> Updating...';

    try {
        // Reload data with cache-busting timestamp
        const timestamp = new Date().getTime();
        const response = await fetch(`data/products.json?t=${timestamp}`);

        if (!response.ok) {
            throw new Error('Failed to fetch data');
        }

        const data = await response.json();

        // Update all data
        allProductsData = data.products;
        allNewsData = data.news;

        // Refresh all components
        updateSummaryStats(data, currentBrandFilter);
        updateLastUpdateTime(data.lastUpdate);
        renderPriceTable(allProductsData);
        updateCharts(data);
        loadNews(allNewsData);

        // Show success message with current refresh time
        const dataGeneratedTime = new Date(data.lastUpdate).toLocaleString('en-US', {
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });

        const refreshTime = new Date().toLocaleString('en-US', {
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });

        // Update the last update display to current time
        updateLastUpdateTime(new Date().toISOString());

        alert(`✅ Interface refreshed successfully!\n\nData Generated: ${dataGeneratedTime}\nRefreshed At: ${refreshTime}\n\nProducts: ${data.products.length}\nNews: ${data.news.length}\n\nNote: For complete data update with latest prices,\nplease run the Python script:\ncd python && python generate_with_real_prices.py`);

        // Update allData
        allData = data;

        // Update cards for current tab
        updateCardsForTab();

    } catch (error) {
        console.error('Error updating data:', error);
        alert('❌ Failed to refresh data. Please try again.\n\nNote: For full data update, run:\ncd python && python generate_with_real_prices.py');
    } finally {
        button.disabled = false;
        button.innerHTML = originalHTML;
    }
}

// Update stats for Trends tab
function updateTrendStats(data, brandFilter = 'all') {
    // Filter products by brand
    let products = brandFilter === 'all'
        ? data.products
        : data.products.filter(p => p.brand === brandFilter);

    // Update title
    if (brandFilter === 'all') {
        document.getElementById('cardTitle1').textContent = 'Total Products';
    } else {
        document.getElementById('cardTitle1').textContent = brandFilter + ' Products';
    }

    // Product count
    document.getElementById('totalProducts').textContent = products.length;

    // Average trend (from price history)
    let avgTrend = 0;
    if (data.priceHistory) {
        if (brandFilter === 'all') {
            // Calculate overall trend
            let trendSum = 0;
            let brandCount = 0;
            for (let brand in data.priceHistory) {
                const prices = data.priceHistory[brand].prices;
                const trend = ((prices[prices.length - 1] - prices[0]) / prices[0]) * 100;
                trendSum += trend;
                brandCount++;
            }
            avgTrend = brandCount > 0 ? trendSum / brandCount : 0;
        } else if (data.priceHistory[brandFilter]) {
            const prices = data.priceHistory[brandFilter].prices;
            avgTrend = ((prices[prices.length - 1] - prices[0]) / prices[0]) * 100;
        }
    }
    const trendText = avgTrend >= 0 ? `+${avgTrend.toFixed(1)}%` : `${avgTrend.toFixed(1)}%`;
    document.getElementById('priceChanges').textContent = trendText;

    // Average price
    let totalPrice = 0;
    let priceCount = 0;
    let allPrices = [];
    products.forEach(product => {
        Object.values(product.channels).forEach(channel => {
            if (channel.price && channel.price > 0) {
                totalPrice += channel.price;
                priceCount++;
                allPrices.push(channel.price);
            }
        });
    });
    const avgPrice = priceCount > 0 ? (totalPrice / priceCount).toFixed(2) : 0;
    const lowestPrice = allPrices.length > 0 ? Math.min(...allPrices).toFixed(2) : 0;

    document.getElementById('avgPrice').textContent = '$' + avgPrice;
    document.getElementById('lowestPrice').textContent = '$' + lowestPrice;
}

// Update stats for News tab
function updateNewsStats(data, brandFilter = 'all') {
    // Filter news by brand
    let news = brandFilter === 'all'
        ? data.news
        : data.news.filter(n => n.brand === brandFilter);

    // Update title
    if (brandFilter === 'all') {
        document.getElementById('cardTitle1').textContent = 'Total News';
    } else {
        document.getElementById('cardTitle1').textContent = brandFilter + ' News';
    }

    // News count
    document.getElementById('totalProducts').textContent = news.length;

    // Count news by recency
    const now = new Date();
    let recentNews = 0; // Last 7 days
    news.forEach(item => {
        const newsDate = new Date(item.date);
        const daysDiff = (now - newsDate) / (1000 * 60 * 60 * 24);
        if (daysDiff <= 7) {
            recentNews++;
        }
    });
    document.getElementById('priceChanges').textContent = recentNews + ' (7d)';

    // Products mentioned in news
    let products = brandFilter === 'all'
        ? data.products
        : data.products.filter(p => p.brand === brandFilter);

    let totalPrice = 0;
    let priceCount = 0;
    let allPrices = [];
    products.forEach(product => {
        Object.values(product.channels).forEach(channel => {
            if (channel.price && channel.price > 0) {
                totalPrice += channel.price;
                priceCount++;
                allPrices.push(channel.price);
            }
        });
    });

    const avgPrice = priceCount > 0 ? (totalPrice / priceCount).toFixed(2) : 0;
    const lowestPrice = allPrices.length > 0 ? Math.min(...allPrices).toFixed(2) : 0;

    document.getElementById('avgPrice').textContent = '$' + avgPrice;
    document.getElementById('lowestPrice').textContent = '$' + lowestPrice;
}
