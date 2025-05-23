/**
 * Charts.js script for skills visualization
 */

document.addEventListener('DOMContentLoaded', function () {
    // Fetch skills data from API
    fetch('/api/data/skills')
        .then(response => response.json())
        .then(data => {
            createProgrammingLanguagesChart(data.programming_languages);
            createDatabasesChart(data.databases);
            createCloudPlatformsChart(data.cloud_platforms);
            createDevOpsToolsChart(data.devops_tools);
            createWebFrameworksChart(data.web_frameworks);
        })
        .catch(error => {
            console.error('Error fetching skills data:', error);
            document.getElementById('skills-charts-container').innerHTML =
                '<div class="alert alert-danger">Failed to load skills data. Please try refreshing the page.</div>';
        });

    // Create Programming Languages Chart
    function createProgrammingLanguagesChart(skills) {
        const ctx = document.getElementById('programmingLanguagesChart').getContext('2d');

        const names = skills.map(skill => skill.name);
        const proficiencies = skills.map(skill => skill.proficiency);

        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: names,
                datasets: [{
                    label: 'Proficiency',
                    data: proficiencies,
                    backgroundColor: 'rgba(54, 162, 235, 0.7)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function (context) {
                                return `Proficiency: ${context.raw}%`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            callback: function (value) {
                                return `${value}%`;
                            }
                        }
                    }
                }
            }
        });
    }

    // Create Databases Chart
    function createDatabasesChart(skills) {
        const ctx = document.getElementById('databasesChart').getContext('2d');

        const names = skills.map(skill => skill.name);
        const proficiencies = skills.map(skill => skill.proficiency);

        new Chart(ctx, {
            type: 'polarArea',
            data: {
                labels: names,
                datasets: [{
                    data: proficiencies,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.7)',
                        'rgba(54, 162, 235, 0.7)',
                        'rgba(255, 206, 86, 0.7)',
                        'rgba(75, 192, 192, 0.7)',
                        'rgba(153, 102, 255, 0.7)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'right'
                    },
                    tooltip: {
                        callbacks: {
                            label: function (context) {
                                return `${context.label}: ${context.raw}%`;
                            }
                        }
                    }
                },
                scales: {
                    r: {
                        max: 100,
                        ticks: {
                            display: false
                        }
                    }
                }
            }
        });
    }

    // Create Cloud Platforms Chart
    function createCloudPlatformsChart(skills) {
        const ctx = document.getElementById('cloudPlatformsChart').getContext('2d');

        const names = skills.map(skill => skill.name);
        const proficiencies = skills.map(skill => skill.proficiency);

        new Chart(ctx, {
            type: 'radar',
            data: {
                labels: names,
                datasets: [{
                    label: 'Cloud Platforms',
                    data: proficiencies,
                    backgroundColor: 'rgba(75, 192, 192, 0.3)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 2,
                    pointBackgroundColor: 'rgba(75, 192, 192, 1)',
                    pointHoverRadius: 5
                }]
            },
            options: {
                responsive: true,
                scales: {
                    r: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            display: false
                        }
                    }
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function (context) {
                                return `${context.label}: ${context.raw}%`;
                            }
                        }
                    }
                }
            }
        });
    }

    // Create DevOps Tools Chart
    function createDevOpsToolsChart(skills) {
        const ctx = document.getElementById('devOpsToolsChart').getContext('2d');

        const names = skills.map(skill => skill.name);
        const proficiencies = skills.map(skill => skill.proficiency);

        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: names,
                datasets: [{
                    label: 'Proficiency',
                    data: proficiencies,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.7)',
                        'rgba(54, 162, 235, 0.7)',
                        'rgba(255, 206, 86, 0.7)',
                        'rgba(75, 192, 192, 0.7)',
                        'rgba(153, 102, 255, 0.7)',
                        'rgba(255, 159, 64, 0.7)',
                        'rgba(201, 203, 207, 0.7)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function (context) {
                                return `Proficiency: ${context.raw}%`;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            callback: function (value) {
                                return `${value}%`;
                            }
                        }
                    }
                }
            }
        });
    }

    // Create Web Frameworks Chart
    function createWebFrameworksChart(skills) {
        const ctx = document.getElementById('webFrameworksChart').getContext('2d');

        const names = skills.map(skill => skill.name);
        const proficiencies = skills.map(skill => skill.proficiency);

        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: names,
                datasets: [{
                    data: proficiencies,
                    backgroundColor: [
                        'rgba(153, 102, 255, 0.7)',
                        'rgba(54, 162, 235, 0.7)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function (context) {
                                return `${context.label}: ${context.raw}%`;
                            }
                        }
                    }
                }
            }
        });
    }
});
