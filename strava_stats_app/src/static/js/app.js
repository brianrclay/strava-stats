document.addEventListener('DOMContentLoaded', function() {
    console.log('Loading Strava stats...');
    
    // Conversion functions
    const kmToMiles = km => (km * 0.621371).toFixed(2);
    const metersToFeet = meters => Math.round(meters * 3.28084);
    
    fetch('/stats')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Received data:', data);
            
            if (data.error) {
                console.error('Error from server:', data.error);
                return;
            }

            // Update monthly stats
            const monthlyStats = data.monthly_stats;
            const monthlyStatsContainer = document.getElementById('monthly-stats');
            monthlyStatsContainer.innerHTML = ''; // Clear existing content
            
            monthlyStats.forEach(stat => {
                const date = new Date(stat.start_date).toLocaleDateString('en-US', { month: 'long', year: 'numeric' });
                const distance = kmToMiles(stat.distance / 1000); // Convert meters to miles
                const time = (stat.moving_time / 3600).toFixed(1); // Convert to hours
                const elevation = metersToFeet(stat.total_elevation_gain); // Convert to feet
                const rides = stat.name; // Number of activities
                
                const statElement = document.createElement('div');
                statElement.className = 'stat-item';
                statElement.innerHTML = `
                    <h3>${date}</h3>
                    <p><strong>${rides}</strong> ${rides === 1 ? 'ride' : 'rides'}</p>
                    <p>Distance: ${distance} miles</p>
                    <p>Time: ${time} hours</p>
                    <p>Elevation Gain: ${elevation} ft</p>
                `;
                monthlyStatsContainer.appendChild(statElement);
            });

            // Update yearly stats
            const yearlyStats = data.yearly_stats;
            const yearlyStatsContainer = document.getElementById('yearly-stats');
            yearlyStatsContainer.innerHTML = ''; // Clear existing content
            
            yearlyStats.forEach(stat => {
                const year = new Date(stat.start_date).getFullYear();
                const distance = kmToMiles(stat.distance / 1000); // Convert meters to miles
                const time = (stat.moving_time / 3600).toFixed(1); // Convert to hours
                const elevation = metersToFeet(stat.total_elevation_gain); // Convert to feet
                const rides = stat.name; // Number of activities
                
                const statElement = document.createElement('div');
                statElement.className = 'stat-item';
                statElement.innerHTML = `
                    <h3>${year}</h3>
                    <p><strong>${rides}</strong> ${rides === 1 ? 'ride' : 'rides'}</p>
                    <p>Distance: ${distance} miles</p>
                    <p>Time: ${time} hours</p>
                    <p>Elevation Gain: ${elevation} ft</p>
                `;
                yearlyStatsContainer.appendChild(statElement);
            });

            // Create charts with imperial units
            const monthlyDistanceChart = JSON.parse(data.monthly_distance_chart);
            monthlyDistanceChart.data[0].y = monthlyDistanceChart.data[0].y.map(d => kmToMiles(d/1000));
            monthlyDistanceChart.layout.yaxis = { title: 'Distance (miles)' };
            Plotly.newPlot('monthly-distance-chart', monthlyDistanceChart.data, monthlyDistanceChart.layout);

            const yearlyDistanceChart = JSON.parse(data.yearly_distance_chart);
            yearlyDistanceChart.data[0].y = yearlyDistanceChart.data[0].y.map(d => kmToMiles(d/1000));
            yearlyDistanceChart.layout.yaxis = { title: 'Distance (miles)' };
            Plotly.newPlot('yearly-distance-chart', yearlyDistanceChart.data, yearlyDistanceChart.layout);
        })
        .catch(error => {
            console.error('Error fetching Strava stats:', error);
            document.getElementById('error-message').textContent = 'Error loading Strava stats. Please try again later.';
        });
});
