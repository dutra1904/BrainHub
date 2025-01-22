from flask import Blueprint, render_template, request, redirect, url_for, flash
from extensions import db
from models import Quiz, Pergunta


quizzes_bp = Blueprint('quizzes', __name__)

# Lista temporária de quizzes
quizzes_list = [
    
]

# Rota para a página inicial dos quizzes
@quizzes_bp.route('/quizzes', methods=['GET'])
def list_quizzes():
    query = request.args.get('query', '') 
    if query:
        filtered_quizzes = [quiz for quiz in quizzes_list if query.lower() in quiz['title'].lower()]
    else:
        filtered_quizzes = quizzes_list

    return render_template('quizzes.html', quizzes=filtered_quizzes)

# Rota para criar um novo quiz
@quizzes_bp.route('/quizzes/create', methods=['GET', 'POST'], endpoint='quizzes_create')
def create_quiz():
    if request.method == 'POST':
        title = request.form['title']
        perguntas_data = request.form.getlist('perguntas')  # Lista de perguntas do formulário

        new_quiz = Quiz(title=title)
        db.session.add(new_quiz)
        db.session.flush()

        for pergunta in perguntas_data:
            texto = pergunta.get('texto')
            tipo = pergunta.get('tipo')
            resposta_correta = pergunta.get('resposta_correta')
            opcoes = ','.join(pergunta.get('opcoes', []))  # Junta as opções com vírgulas
            nova_pergunta = Pergunta(texto=texto, tipo=tipo, resposta_correta=resposta_correta, opcoes=opcoes, quiz_id=new_quiz.id)
            db.session.add(nova_pergunta)

        db.session.commit()
        flash('Quiz criado com sucesso!', 'success')
        return redirect(url_for('quizzes.list_quizzes'))

    return render_template('criar_quizz.html')


# Rota para visualizar um quiz específico
@quizzes_bp.route('/quizzes/<int:quiz_id>', methods=['GET'])
def view_quiz(quiz_id):
    quiz = next((quiz for quiz in quizzes_list if quiz['id'] == quiz_id), None)
    if quiz is None:
        flash("Quiz não encontrado!", "error")
        return redirect(url_for('quizzes.list_quizzes'))

    return render_template('view_quizz.html', quiz=quiz)

@quizzes_bp.route('/quizzes/create', methods=['GET', 'POST'])
def create_quiz():
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        descricao = request.form.get('descricao')
        perguntas = request.form.getlist('pergunta')  # Lista de perguntas
        tipos_perguntas = request.form.getlist('tipo_pergunta')  # Lista de tipos de perguntas
        opcoes = request.form.getlist('opcoes')  # Lista de opções (para perguntas de marcar)

        if not titulo:
            flash("O título é obrigatório!", "error")
            return render_template('criar_quizz.html')

        # Validação para verificar se há perguntas
        if not perguntas or len(perguntas) == 0:
            flash("Adicione ao menos uma pergunta!", "error")
            return render_template('criar_quizz.html', titulo=titulo, descricao=descricao)

        # Criação do quiz
        new_id = len(quizzes_list) + 1
        perguntas_formatadas = [
            {
                "texto": pergunta,
                "tipo": tipo,
                "opcoes": opcao.split(';') if tipo == 'marcar' else None
            }
            for pergunta, tipo, opcao in zip(perguntas, tipos_perguntas, opcoes)
        ]
        quizzes_list.append({
            "id": new_id,
            "title": titulo,
            "description": descricao,
            "perguntas": perguntas_formatadas
        })

        flash("Quiz criado com sucesso!", "success")
        return redirect(url_for('quizzes.list_quizzes'))

    return render_template('criar_quizz.html')

@quizzes_bp.route('/quizzes/<int:quiz_id>/play', methods=['GET', 'POST'])
def play_quiz(quiz_id):
    # Encontra o quiz pelo ID
    quiz = next((quiz for quiz in quizzes_list if quiz['id'] == quiz_id), None)
    if quiz is None:
        flash("Quiz não encontrado!", "error")
        return redirect(url_for('quizzes.list_quizzes'))

    # Lógica de verificação das respostas
    if request.method == 'POST':
        respostas = request.form.to_dict()  # Obtem as respostas enviadas
        resultado = []
        acertos = 0

        # Valida as respostas
        for index, pergunta in enumerate(quiz.get('perguntas', [])):
            resposta_correta = pergunta.get('resposta_correta', '').strip().lower()
            resposta_usuario = respostas.get(f'resposta_{index}', '').strip().lower()

            if resposta_usuario == resposta_correta:
                resultado.append({'pergunta': pergunta['texto'], 'correto': True})
                acertos += 1
            else:
                resultado.append({'pergunta': pergunta['texto'], 'correto': False})

        return render_template('resultado_quizz.html', quiz=quiz, resultado=resultado, acertos=acertos)

    return render_template('jogar_quizz.html', quiz=quiz)
