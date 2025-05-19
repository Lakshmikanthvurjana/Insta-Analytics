function analyze() {
    const username = document.getElementById('username').value.trim();
    const results = document.getElementById('results');
    if (!username) {
        results.innerHTML = "<p style='color:red;'>Please enter a username.</p>";
        return;
    }
    // Simulate analysis (replace with real API calls if available)
    results.innerHTML = `
        <h2>Results for @${username}</h2>
        <ul>
            <li>Followers: 1,234</li>
            <li>Following: 567</li>
            <li>Posts: 89</li>
            <li>Engagement Rate: 4.5%</li>
        </ul>
        <p><em>(This is a demo. Connect to Instagram API for real data.)</em></p>
    `;
}