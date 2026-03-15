let tg = window.Telegram.WebApp;
tg.expand(); // развернуть на весь экран

const tempSlider = document.getElementById('temp');
const tempSpan = document.getElementById('tempValue');
const modeAuto = document.getElementById('modeAuto');
const modeManual = document.getElementById('modeManual');
const modeOff = document.getElementById('modeOff');
const sendBtn = document.getElementById('sendBtn');

let currentMode = 'auto';

tempSlider.addEventListener('input', () => {
    tempSpan.textContent = tempSlider.value;
});

function setMode(mode) {
    currentMode = mode;
    [modeAuto, modeManual, modeOff].forEach(btn => btn.classList.remove('active'));
    if (mode === 'auto') modeAuto.classList.add('active');
    if (mode === 'manual') modeManual.classList.add('active');
    if (mode === 'off') modeOff.classList.add('active');
}

modeAuto.addEventListener('click', () => setMode('auto'));
modeManual.addEventListener('click', () => setMode('manual'));
modeOff.addEventListener('click', () => setMode('off'));

sendBtn.addEventListener('click', () => {
    const data = {
        temperature: parseFloat(tempSlider.value),
        mode: currentMode
    };
    tg.sendData(JSON.stringify(data));
    tg.close(); // закрыть WebApp после отправки (опционально)
});