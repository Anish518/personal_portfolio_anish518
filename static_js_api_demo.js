/**
 * API Demo section functionality
 */

document.addEventListener('DOMContentLoaded', function () {
    // Skills API Demo
    const skillsApiBtn = document.getElementById('skills-api-btn');
    const skillsApiResult = document.getElementById('skills-api-result');

    if (skillsApiBtn && skillsApiResult) {
        skillsApiBtn.addEventListener('click', function () {
            // Show loading state
            skillsApiResult.innerHTML = '<div class="d-flex justify-content-center">' +
                '<div class="spinner-border text-primary" role="status">' +
                '<span class="visually-hidden">Loading...</span>' +
                '</div></div>';

            // Fetch skills data
            fetch('/api/data/skills')
                .then(response => response.json())
                .then(data => {
                    // Format JSON with syntax highlighting
                    const formattedJson = JSON.stringify(data, null, 2);
                    skillsApiResult.innerHTML = `<pre>${syntaxHighlight(formattedJson)}</pre>`;
                })
                .catch(error => {
                    console.error('Error fetching skills data:', error);
                    skillsApiResult.innerHTML = `<div class="alert alert-danger">Error: ${error.message}</div>`;
                });
        });
    }

    // Experience API Demo
    const experienceApiBtn = document.getElementById('experience-api-btn');
    const experienceApiResult = document.getElementById('experience-api-result');

    if (experienceApiBtn && experienceApiResult) {
        experienceApiBtn.addEventListener('click', function () {
            // Show loading state
            experienceApiResult.innerHTML = '<div class="d-flex justify-content-center">' +
                '<div class="spinner-border text-primary" role="status">' +
                '<span class="visually-hidden">Loading...</span>' +
                '</div></div>';

            // Fetch experience data
            fetch('/api/data/experience')
                .then(response => response.json())
                .then(data => {
                    // Format JSON with syntax highlighting
                    const formattedJson = JSON.stringify(data, null, 2);
                    experienceApiResult.innerHTML = `<pre>${syntaxHighlight(formattedJson)}</pre>`;
                })
                .catch(error => {
                    console.error('Error fetching experience data:', error);
                    experienceApiResult.innerHTML = `<div class="alert alert-danger">Error: ${error.message}</div>`;
                });
        });
    }

    // Weather API Demo
    const weatherApiForm = document.getElementById('weather-api-form');
    const weatherApiResult = document.getElementById('weather-api-result');

    if (weatherApiForm && weatherApiResult) {
        weatherApiForm.addEventListener('submit', function (event) {
            event.preventDefault();

            const cityInput = document.getElementById('weather-city-input');
            const city = cityInput.value.trim();

            if (!city) {
                weatherApiResult.innerHTML = '<div class="alert alert-warning">Please enter a city name</div>';
                return;
            }

            // Show loading state
            weatherApiResult.innerHTML = '<div class="d-flex justify-content-center">' +
                '<div class="spinner-border text-primary" role="status">' +
                '<span class="visually-hidden">Loading...</span>' +
                '</div></div>';

            // Fetch weather data
            fetch(`/api/demo/weather?city=${encodeURIComponent(city)}`)
                .then(response => response.json())
                .then(data => {
                    // Format weather data into a nice card
                    weatherApiResult.innerHTML = `
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">${data.city}</h5>
                                <p class="card-text">
                                    <strong>Temperature:</strong> ${data.temperature}°C<br>
                                    <strong>Weather:</strong> ${data.weather}<br>
                                    <strong>Humidity:</strong> ${data.humidity}%<br>
                                    <strong>Wind Speed:</strong> ${data.wind_speed} m/s<br>
                                    <strong>Timestamp:</strong> ${data.timestamp}
                                </p>
                            </div>
                        </div>
                        <div class="mt-3">
                            <h6>API Response (JSON):</h6>
                            <pre>${syntaxHighlight(JSON.stringify(data, null, 2))}</pre>
                        </div>
                    `;
                })
                .catch(error => {
                    console.error('Error fetching weather data:', error);
                    weatherApiResult.innerHTML = `<div class="alert alert-danger">Error: ${error.message}</div>`;
                });
        });
    }

    /**
     * Syntax highlighting for JSON
     * @param {string} json - JSON string to highlight
     * @return {string} - HTML with syntax highlighting
     */
    function syntaxHighlight(json) {
        json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
        return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, function (match) {
            let cls = 'text-number';
            if (/^"/.test(match)) {
                if (/:$/.test(match)) {
                    cls = 'text-key';
                } else {
                    cls = 'text-string';
                }
            } else if (/true|false/.test(match)) {
                cls = 'text-boolean';
            } else if (/null/.test(match)) {
                cls = 'text-null';
            }
            return '<span class="' + cls + '">' + match + '</span>';
        });
    }
});
