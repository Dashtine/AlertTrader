let isRunning = false;

function toggleBot() {
    const button = document.getElementById('toggleButton');
    const status = document.getElementById('status');
    const logs = document.getElementById('logs');
    const isStarted = button.classList.contains('start');

    if (isStarted) {
        button.classList.remove('start');
        button.classList.add('stop');
        button.textContent = 'Stop';
        logs.innerHTML += `<p>[${new Date().toLocaleString()}] Bot started</p>`;
    } else {
        button.classList.remove('stop');
        button.classList.add('start');
        button.textContent = 'Start';
        logs.innerHTML += `<p>[${new Date().toLocaleString()}] Bot stopped</p>`;
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