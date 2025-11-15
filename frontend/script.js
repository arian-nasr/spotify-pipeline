const apiUrl = 'http://spotify-grabber-docker:5000/tracks';

async function fetchTracks() {
    try {
        const response = await fetch(apiUrl);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const tracks = await response.json();
        return tracks;
    } catch (error) {
        console.error('Error fetching tracks:', error);
        return [];
    }
}

function displayTracks(tracks) {
    const trackList = document.getElementById('track-list');
    trackList.innerHTML = '';

    tracks.tracks.forEach(track => {
        const listItem = document.createElement('li');
        listItem.textContent = `${track.track_name} by ${track.artist_names}`;
        trackList.appendChild(listItem);
    });
}

document.addEventListener('DOMContentLoaded', async () => {
    const tracks = await fetchTracks();
    displayTracks(tracks);
});