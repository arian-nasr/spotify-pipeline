const apiUrl = 'http://spotify-grabber-docker:5000';

async function fetchTracks() {
    try {
        const response = await fetch(`${apiUrl}/tracks`);
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

    tracks.tracks.forEach((track, index) => {
        const listItem = document.createElement('li');
        listItem.textContent = `${track.track_name} by ${track.artist_names}`;
        
        // Add click event to delete track
        listItem.addEventListener('click', function() {
            fetch(`${apiUrl}/tracks/delete/${encodeURIComponent(track.track_name)}/${encodeURIComponent(track.artist_names)}`)
                .then(response => {
                    if (!response.ok) { 
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    console.log(data.message);
                    fetchTracks().then(tracks => {
                        displayTracks(tracks);
                    });
                })
                .catch(error => {
                    console.error('Error deleting track:', error);
                });
        });
        
        trackList.appendChild(listItem);
    });
}


document.addEventListener('DOMContentLoaded', async () => {
    const tracks = await fetchTracks();
    displayTracks(tracks);
});