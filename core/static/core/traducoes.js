const traducoes = {
    pt: {
        // HOME
        'ola': 'Olá,',
        'por_onde': 'Por onde vamos começar?',
        'registo_humor': 'Registo de humor',
        'diario_digital': 'Diário digital',
        'exercicios': 'Exercícios',
        'album': 'Álbum',
        'frases_motivacao': 'Frases de motivação',
        'estatisticas': 'Estatísticas',
        'perfil': 'Perfil',
        'sair': 'Sair',
        'frase_label': '💬 Frase do dia',
        'frase_label_humor': '💬 Frase do dia — para o teu humor de hoje',
        'quero_mais': '✨ Quero mais frases',

        // LOGIN
        'bem_vindo': 'Bem-vindo(a) de volta!',
        'entrar': 'Entrar',
        'criar_conta': 'Criar conta',
        'username': 'Username',
        'password': 'Password',

        // REGISTO
        'criar_conta_titulo': 'Cria a tua conta',
        'ja_tens_conta': 'Já tens conta? Entra aqui',
    },
    en: {
        // HOME
        'ola': 'Hello,',
        'por_onde': 'Where shall we start?',
        'registo_humor': 'Mood tracker',
        'diario_digital': 'Digital diary',
        'exercicios': 'Exercises',
        'album': 'Album',
        'frases_motivacao': 'Motivational quotes',
        'estatisticas': 'Statistics',
        'perfil': 'Profile',
        'sair': 'Sign out',
        'frase_label': '💬 Quote of the day',
        'frase_label_humor': '💬 Quote of the day — based on your mood',
        'quero_mais': '✨ I want more quotes',

        // LOGIN
        'bem_vindo': 'Welcome back!',
        'entrar': 'Sign in',
        'criar_conta': 'Create account',
        'username': 'Username',
        'password': 'Password',

        // REGISTO
        'criar_conta_titulo': 'Create your account',
        'ja_tens_conta': 'Already have an account? Sign in',
    }
};

// obtém idioma guardado (default: pt)
function getIdioma() {
    return localStorage.getItem('mindly_idioma') || 'pt';
}

// guarda idioma
function setIdioma(idioma) {
    localStorage.setItem('mindly_idioma', idioma);
}

// traduz todos os elementos com data-i18n
function aplicarTraducoes() {
    const idioma = getIdioma();
    const t = traducoes[idioma];

    document.querySelectorAll('[data-i18n]').forEach(el => {
        const chave = el.getAttribute('data-i18n');
        if (t[chave]) {
            el.textContent = t[chave];
        }
    });

    // atualiza botões PT/EN
    document.querySelectorAll('.btn-idioma-pt').forEach(btn => {
        btn.classList.toggle('ativo', idioma === 'pt');
    });
    document.querySelectorAll('.btn-idioma-en').forEach(btn => {
        btn.classList.toggle('ativo', idioma === 'en');
    });
}

// troca idioma
function trocarIdioma(idioma) {
    setIdioma(idioma);
    aplicarTraducoes();
}

// aplica ao carregar a página
document.addEventListener('DOMContentLoaded', aplicarTraducoes);