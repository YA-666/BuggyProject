const labels = {
    en: { send: 'Send', placeholder: 'Type here...' },
    nl: { send: 'Verstuur', placeholder: 'Typ hier...' },
    fr: { send: 'Envoyer', placeholder: 'Tapez ici...' },
    de: { send: 'Senden', placeholder: 'Hier eingeben...' },
};

function updateLabels(lang) {
    const l = labels[lang] || labels.en;
    document.getElementById('send-btn').textContent = l.send;
    document.getElementById('user-input').placeholder = l.placeholder;
}

document.getElementById('lang-select').addEventListener('change', (e) => {
    updateLabels(e.target.value);
});

updateLabels('en');

// Live2D avatar example using pixi-live2d-display
const app = new PIXI.Application({ view: document.getElementById('avatar'), width: 300, height: 400, transparent: true });
PIXI.live2d.Live2DModel.from('https://unpkg.com/@cubism/ecl@latest/Hiyori/Hiyori.model3.json').then(model => {
    model.scale.set(0.2);
    model.x = app.renderer.width / 2;
    model.y = app.renderer.height * 0.95;
    model.anchor.set(0.5, 1);
    app.stage.addChild(model);
});

document.getElementById('send-btn').addEventListener('click', () => {
    const text = document.getElementById('user-input').value;
    fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById('output').textContent = data.text;
    })
    .catch(err => {
        document.getElementById('output').textContent = 'Error: ' + err;
    });
});
