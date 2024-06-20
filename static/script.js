let isRunning = false;

function toggleBot(){
    const button = document.getElementById('toggleButton');
    if(isRunning){
        fetch('/stop', {method: 'POST'})
            .then(response => response.text())
            .then(data => {
                button.textContent = 'Start';
                button.classList.remove('stop');
                button.classList.add('start');
                document.getElementById('status').innerText = data;
                isRunning = false;
            })
            .catch(error => console.error('Error:', error));
    } else {
        fetch('/start', {method: 'POST'})
            .then(response => response.text())
            .then(data => {
                button.textContent = 'Stop';
                button.classList.remove('start');
                button.classList.add('stop');
                document.getElementById('status').innerText = data;
                isRunning = true;
            })
            .catch(error => console.error('Error', error));
    }
}

function startLogStream(){
    const eventSource = new EventSource('/logs');
    eventSource.onmessage = function(event){
        const logContainer = document.getElementById('logs');
        logContainer.innerHTML += event.data + '<br>';
        logContainer.scrollTop = logContainer.scrollHeight;
    };
}

window.onload = startLogStream;