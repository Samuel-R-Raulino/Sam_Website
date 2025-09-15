// ---- Animação das bolhas ---- //
const canvas = document.getElementById('bolhasCanvas');
const ctx = canvas?.getContext('2d');

let bolhas = [];
const numBolhas = 15;

function resizeCanvas() {
    if (!canvas) return;
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}

resizeCanvas();
window.addEventListener('resize', resizeCanvas);

if (canvas && ctx) {
    for (let i = 0; i < numBolhas; i++) {
        bolhas.push(criarBolha());
    }

    function criarBolha() {
        return {
            x: Math.random() * canvas.width,
            y: window.innerHeight + Math.random() * 200,
            size: Math.random() * 100 + 50,
            speed: Math.random() * 1 + 0.5,
            drift: Math.random() * 2 - 1,
            opacity: Math.random() * 0.5 + 0.5
        };
    }

    function desenharBolhas() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        bolhas.forEach(bolha => {
            ctx.globalAlpha = bolha.opacity;
            const img = new Image();
            img.src = 'static/img/bolha.png';
            ctx.drawImage(img, bolha.x, bolha.y, bolha.size, bolha.size);
        });
        ctx.globalAlpha = 1;
    }

    function atualizarBolhas() {
        bolhas.forEach(bolha => {
            bolha.y -= bolha.speed;
            bolha.x += bolha.drift;
            if (bolha.y + bolha.size < 0) {
                Object.assign(bolha, criarBolha());
            }
        });
    }

    function animar() {
        atualizarBolhas();
        desenharBolhas();
        requestAnimationFrame(animar);
    }

    animar();
}

// ---- Configuração de Tema ---- //
const botaoTema = document.getElementById('botaoTema');
const transitionOverlay = document.getElementById('transitionOverlay');
const iconeSwitch = document.getElementById('iconeSwitch');

const logoOragame = document.getElementById('logoOragame');
const logoOragameGrande = document.getElementById('logoOragameGrande');

const imgSol = "/static/img/sol.png";
const imgLua = "/static/img/lua.png";

const logoClaro = "/static/img/oragame.png";
const logoEscuro = "/static/img/oradark.png";

let transitionDuration = 800;
let switchCooldown = 2000;

function atualizarIcone() {
    if (iconeSwitch && botaoTema) {
        iconeSwitch.style.backgroundImage = botaoTema.checked ? `url('${imgLua}')` : `url('${imgSol}')`;
    }
}

function atualizarFundoParaTema() {
    const fundo = document.getElementById('fundo');
    if (!fundo) return;
    const isDark = document.body.classList.contains('dark-theme');
    fundo.src = isDark ? "/static/img/fundo2.gif" : "/static/img/fundo.gif";
}

function atualizarLogo() {
    const isDark = document.body.classList.contains('dark-theme');
    const novaSrc = isDark ? logoEscuro : logoClaro;

    if (logoOragame) logoOragame.src = novaSrc;
    if (logoOragameGrande) logoOragameGrande.src = novaSrc;
}

function atualizarBolhasCanvas() {
    if (!canvas) return;
    canvas.style.display = document.body.classList.contains('dark-theme') ? 'none' : 'block';
}

function salvarTema() {
    const temaAtual = document.body.classList.contains('dark-theme') ? 'dark' : 'light';
    localStorage.setItem('tema', temaAtual);
}
document.body.classList.add('dark-theme');
localStorage.setItem('tema', 'dark');

function carregarTema() {
    const temaSalvo = localStorage.getItem('tema');
    if (temaSalvo === 'dark') {
        document.body.classList.add('dark-theme');
        if (botaoTema) botaoTema.checked = true;
    } else {
        document.body.classList.remove('dark-theme');
        if (botaoTema) botaoTema.checked = false;
    }
}

function initTema() {
    carregarTema();
    atualizarIcone();
    atualizarLogo();
    atualizarFundoParaTema();
    atualizarBolhasCanvas();
}

// ---- Troca de Tema ---- //
if (botaoTema) {
    botaoTema.addEventListener('change', () => {
        const isDark = document.body.classList.contains('dark-theme');
        botaoTema.disabled = true;

        atualizarIcone();

        if (transitionOverlay) {
            transitionOverlay.style.background = isDark ? 'white' : 'black';
            transitionOverlay.style.transition = `opacity ${transitionDuration}ms ease-in-out`;
            transitionOverlay.style.opacity = '1';
        }

        setTimeout(() => {
            document.body.classList.toggle('dark-theme');

            atualizarLogo();
            atualizarFundoParaTema();
            atualizarBolhasCanvas();
            salvarTema();

            if (transitionOverlay) {
                setTimeout(() => {
                    transitionOverlay.style.opacity = '0';
                }, 50);
            }

        }, transitionDuration);

        setTimeout(() => {
            botaoTema.disabled = false;
        }, switchCooldown);
    });
}

// ---- Atualização dos Peixes ---- //
function atualizarPeixesParaTema() {
    if (typeof peixesCriados === 'undefined') return;

    const usandoDark = document.body.classList.contains('dark-theme');
    peixesCriados.forEach(peixe => {
        const index = peixe.dataset.index;
        const novaConfig = usandoDark ? imagensNaves[index] : imagensPeixe[index];
        peixe.style.backgroundImage = `url("${novaConfig.src}")`;
        peixe.style.width = `${novaConfig.width}px`;
        peixe.style.height = `${novaConfig.height}px`;
    });
}

initTema();