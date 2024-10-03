document.getElementById('sendButton').addEventListener('click', function() {
    const userInput = document.getElementById('userInput').value;
    const chatBox = document.getElementById('chatBox');

    if (userInput) {
        // Display user message
        chatBox.innerHTML += `<div class="user-message"><span>${userInput}</span></div>`;
        document.getElementById('userInput').value = ''; // Clear input

        // Generate a bot response after a delay
        setTimeout(() => {
            const botResponse = getBotResponse(userInput);
            chatBox.innerHTML += `<div class="bot-message"><span>${botResponse}</span></div>`;
            chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll to the bottom
        }, 1000);
    }
});

// Simple bot response function
function getBotResponse(input) {
    const responses = {
        "hi": "Hello! How can I help you?",
        "how are you?": "I'm just a bot, but thanks for asking!",
        "what's your name?": "I'm your friendly chatbot!",
        "bye": "Goodbye! Have a great day!",
    };

    return responses[input.toLowerCase()] || "I'm not sure how to respond to that.";
}

document.getElementById('sendButton').addEventListener('click', function() {
    const eye = document.getElementById('eye');
  eye.classList.add('after'); // Add the animation class
;
    // Optional: Remove the animation class after some time (to reset)
    setTimeout(function() {
      eye.classList.remove('after');
    }, 300);  // Match this time to the transition duration in CSS
  });

  document.getElementById('sendButton').addEventListener('click', function() {
    const handl = document.getElementById('handl');
  handl.classList.add('after'); // Add the animation class
;
    // Optional: Remove the animation class after some time (to reset)
    setTimeout(function() {
      handl.classList.remove('after');
    }, 300);  // Match this time to the transition duration in CSS
  });
  

  document.getElementById('sendButton').addEventListener('click', function() {
    const handr = document.getElementById('handr');
  handr.classList.add('after'); // Add the animation class
;
    // Optional: Remove the animation class after some time (to reset)
    setTimeout(function() {
      handr.classList.remove('after');
    }, 300);  // Match this time to the transition duration in CSS
  });


  document.getElementById('sendButton').addEventListener('click', function() {
    const mouth = document.getElementById('mouth');
  mouth.classList.add('after'); // Add the animation class
;
    // Optional: Remove the animation class after some time (to reset)
    setTimeout(function() {
      handr.classList.remove('after');
    }, 300);  // Match this time to the transition duration in CSS
  });

  let map;

  // Function to display the map and show user's current location
  function showLocation() {
      if (navigator.geolocation) {
          navigator.geolocation.getCurrentPosition(position => {
              const lat = position.coords.latitude;
              const lon = position.coords.longitude;

              // Show the map and the close button
              document.getElementById('map').style.display = 'block';
              document.getElementById('closeBtn').style.display = 'block';

              // Initialize the map and set it to the user's location
              if (!map) {
                  map = L.map('map').setView([lat, lon], 13);

                  // Load OpenStreetMap tiles
                  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                  }).addTo(map);

                  // Add a marker at the user's location
                  L.marker([lat, lon]).addTo(map)
                      .bindPopup('You are here!')
                      .openPopup();
                  
                  // Initialize the geocoder
                  const geocoder = L.Control.geocoder({
                      defaultMarkGeocode: true
                  }).addTo(map);

                  // Handle geocode results
                  geocoder.on('markgeocode', function(e) {
                      const marker = e.geocode;
                      L.marker(marker.center).addTo(map)
                          .bindPopup(marker.name)
                          .openPopup();
                      map.setView(marker.center, 13);
                  });
              } else {
                  // If the map already exists, just pan to the new location
                  map.setView([lat, lon], 13);
              }

          }, error => {
              alert('Unable to retrieve your location');
          });
      } else {
          alert('Geolocation is not supported by your browser');
      }
  }

  // Function to close the map
  function closeMap() {
      document.getElementById('map').style.display = 'none';
      document.getElementById('closeBtn').style.display = 'none';
  }