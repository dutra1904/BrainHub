from flask import Blueprint, render_template, request, redirect, url_for, flash

# Inicialização do blueprint
quizzes_bp = Blueprint('quizzes', __name__)

# Dados temporários para simular quizzes no banco de dados
# (Substituir isso pelo acesso ao banco de dados)
quizzes_list = [
    {"id": 1, "title": "Quiz de História"},
    {"id": 2, "title": "Quiz de Matemática"},
    {"id": 3, "title": "Quiz de Ciência"},
]

# Rota para a página inicial dos quizzes
@quizzes_bp.route('/quizzes', methods=['GET'])
def list_quizzes():
    query = request.args.get('query', '')  # Obtém o termo de pesquisa (se existir)
    if query:
        filtered_quizzes = [quiz for quiz in quizzes_list if query.lower() in quiz['title'].lower()]
    else:
        filtered_quizzes = quizzes_list

    return render_template('quizzes.html', quizzes=filtered_quizzes)

# Rota para criar um novo quiz (somente redireciona por enquanto)
@quizzes_bp.route('/quizzes/create', methods=['GET'])
def create_quiz():
    # Redirecionar para uma página de criação (ainda a ser implementada)
    return redirect(url_for('quizzes.list_quizzes'))

# Rota para visualizar um quiz específico
@quizzes_bp.route('/quizzes/<int:quiz_id>', methods=['GET'])
def view_quiz(quiz_id):
    quiz = next((quiz for quiz in quizzes_list if quiz['id'] == quiz_id), None)
    if quiz is None:
        flash("Quiz não encontrado!", "error")
        return redirect(url_for('quizzes.list_quizzes'))

    # Renderizar uma página para mostrar os detalhes do quiz (ainda a ser implementada)
    return f"Detalhes do Quiz: {quiz['title']}"
