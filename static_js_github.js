/**
 * GitHub integration for portfolio website
 */

document.addEventListener('DOMContentLoaded', function () {
    const reposContainer = document.getElementById('github-repos');
    const loadingSpinner = document.getElementById('github-loading');
    const errorMessage = document.getElementById('github-error');

    // Fetch GitHub repositories from our API endpoint
    fetch('/api/github/repos')
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch GitHub repositories');
            }
            return response.json();
        })
        .then(repos => {
            // Hide loading spinner
            if (loadingSpinner) {
                loadingSpinner.style.display = 'none';
            }

            // Display repositories
            displayRepositories(repos);
        })
        .catch(error => {
            console.error('Error fetching GitHub repositories:', error);

            // Hide loading spinner
            if (loadingSpinner) {
                loadingSpinner.style.display = 'none';
            }

            // Show error message
            if (errorMessage) {
                errorMessage.style.display = 'block';
                errorMessage.textContent = `Failed to load GitHub repositories: ${error.message}`;
            }
        });

    /**
     * Display GitHub repositories in a grid
     * @param {Array} repos - Array of GitHub repository objects
     */
    function displayRepositories(repos) {
        if (!reposContainer) return;

        // Create repository cards
        const reposHTML = repos.map(repo => {
            // Format dates
            const updatedAt = new Date(repo.updated_at);
            const formattedDate = updatedAt.toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'short',
                day: 'numeric'
            });

            // Create repository card
            return `
                <div class="col-md-6 col-lg-4 mb-4">
                    <div class="card repo-card h-100">
                        <div class="card-body">
                            <h5 class="card-title">
                                <i class="fas fa-code-branch me-2"></i>
                                ${repo.name}
                            </h5>
                            <p class="card-text">${repo.description || 'No description available'}</p>
                            <div class="repo-stats">
                                <div class="repo-stat">
                                    <i class="fas fa-star"></i>
                                    <span>${repo.stargazers_count}</span>
                                </div>
                                <div class="repo-stat">
                                    <i class="fas fa-code-branch"></i>
                                    <span>${repo.forks_count}</span>
                                </div>
                                <div class="repo-stat">
                                    <i class="fas fa-circle" style="color: ${getLanguageColor(repo.language)}"></i>
                                    <span>${repo.language || 'Unknown'}</span>
                                </div>
                            </div>
                        </div>
                        <div class="card-footer">
                            <small class="text-muted">Updated on ${formattedDate}</small>
                            <a href="${repo.html_url}" target="_blank" class="btn btn-sm btn-outline-primary float-end">
                                View Repository
                            </a>
                        </div>
                    </div>
                </div>
            `;
        }).join('');

        // Display repositories
        reposContainer.innerHTML = reposHTML;
    }

    /**
     * Get color for programming language
     * @param {string} language - Programming language name
     * @return {string} - CSS color value
     */
    function getLanguageColor(language) {
        const colors = {
            'JavaScript': '#f1e05a',
            'TypeScript': '#2b7489',
            'Python': '#3572A5',
            'Java': '#b07219',
            'C': '#555555',
            'C++': '#f34b7d',
            'C#': '#178600',
            'PHP': '#4F5D95',
            'Ruby': '#701516',
            'Go': '#00ADD8',
            'Swift': '#ffac45',
            'Kotlin': '#F18E33',
            'Rust': '#dea584',
            'HTML': '#e34c26',
            'CSS': '#563d7c',
            'Shell': '#89e051'
        };

        return colors[language] || '#858585';
    }
});
