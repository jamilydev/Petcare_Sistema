from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from datetime import datetime, timedelta

# Imports dos DAOs
from app.dao.DonoDAO import DonoDAO
from app.dao.PetDAO import PetDAO
from app.dao.VeterinarioDAO import VeterinarioDAO
from app.dao.ConsultaDAO import ConsultaDAO
from app.dao.RecompensaDAO import RecompensaDAO
from app.dao.VacinaDAO import VacinaDAO
from app.dao.DisponibilidadeDAO import DisponibilidadeDAO

# Imports dos Models
from app.model.Dono import Dono
from app.model.Pet import Pet
from app.model.Veterinario import Veterinario
from app.model.Consulta import Consulta
from app.model.Recompensa import Recompensa
from app.model.Vacina import Vacina
from app.model.Disponibilidade import Disponibilidade

web_bp = Blueprint('web_bp', __name__)

# Instâncias
dono_dao = DonoDAO()
pet_dao = PetDAO()
vet_dao = VeterinarioDAO()
consulta_dao = ConsultaDAO()
recompensa_dao = RecompensaDAO()
vacina_dao = VacinaDAO()
disp_dao = DisponibilidadeDAO()

# ==============================================================================
# ÁREA PÚBLICA (LOGIN E LANDING)
# ==============================================================================

@web_bp.route('/')
def landing():
    return render_template('landing.html')

@web_bp.route('/login/<tipo>', methods=['GET', 'POST'])
def login(tipo):
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        usuario = None

        if tipo == 'tutor':
            usuario = dono_dao.autenticar(email, senha)
            if usuario:
                session['user_id'] = usuario.id
                session['tipo'] = 'tutor'
                session['nome'] = usuario._nome
                return redirect(url_for('web_bp.dashboard_tutor'))
        
        elif tipo == 'veterinario':
            usuario = vet_dao.autenticar(email, senha)
            if usuario:
                session['user_id'] = usuario.id
                session['tipo'] = 'veterinario'
                session['nome'] = usuario.nome
                return redirect(url_for('web_bp.dashboard_vet'))

        elif tipo == 'admin':
            if email == 'admin@petcare.com' and senha == 'admin123':
                session.permanent = True 
                session['tipo'] = 'admin'
                return redirect(url_for('web_bp.admin_panel'))

        flash('Email ou senha incorretos! Tente novamente.')
    
    return render_template('login.html', tipo=tipo)

@web_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('web_bp.landing'))

@web_bp.route('/recuperar-senha')
def recuperar_senha():
    return render_template('recuperar_senha.html')

# ==============================================================================
# ÁREA DE CADASTRO (TUTOR E VET)
# ==============================================================================

@web_bp.route('/register/tutor', methods=['GET', 'POST'])
def register_tutor():
    if request.method == 'POST':
        session['temp_dono'] = {
            'nome': request.form['nome'],
            'email': request.form['email'],
            'telefone': '00000000',
            'senha': request.form['senha']
        }
        return redirect(url_for('web_bp.register_pet'))
    return render_template('register_dono.html')

@web_bp.route('/register/pet', methods=['GET', 'POST'])
def register_pet():
    usuario_logado = 'user_id' in session and session.get('tipo') == 'tutor'

    if request.method == 'POST':
        # Pega os dados do form (incluindo os novos)
        nome = request.form['nome_pet']
        especie = request.form['tipo']
        raca = request.form['raca']
        idade = request.form.get('idade', 0)
        peso = request.form.get('peso', 0.0)
        data_nascimento = request.form.get('data_nascimento', '')

        # Define o dono_id
        if usuario_logado:
            dono_id = session['user_id']
        else:
            dados_dono = session.get('temp_dono')
            if not dados_dono: return redirect(url_for('web_bp.login', tipo='tutor'))
            try:
                novo_dono = Dono(dados_dono['nome'], dados_dono['email'], dados_dono['telefone'], dados_dono['senha'])
                dono_salvo = dono_dao.salvar(novo_dono)
                dono_id = dono_salvo.id
                session['user_id'] = dono_salvo.id
                session['tipo'] = 'tutor'
                session['nome'] = dono_salvo._nome 
                session.pop('temp_dono', None)
            except ValueError as e:
                flash(str(e), 'error')
                return redirect(url_for('web_bp.register_tutor'))
            except Exception as e:
                flash(f"Erro ao criar conta: {str(e)}", 'error')
                return redirect(url_for('web_bp.register_tutor'))

        # Salva o Pet Completo
        novo_pet = Pet(nome, dono_id, especie, raca, idade, peso, data_nascimento)
        pet_dao.salvar(novo_pet)
        
        return redirect(url_for('web_bp.dashboard_tutor'))

    return render_template('register_pet.html', logged_in=usuario_logado)

@web_bp.route('/register/veterinario', methods=['GET', 'POST'])
def register_vet():
    if request.method == 'POST':
        novo_vet = Veterinario(
            nome=request.form['nome'],
            crmv=request.form['crmv'],
            especialidade=request.form['especialidade'],
            telefone=request.form['telefone'],
            email=request.form['email'],
            senha=request.form['senha']
        )
        vet_salvo = vet_dao.salvar(novo_vet)
        
        session['user_id'] = vet_salvo.id
        session['tipo'] = 'veterinario'
        session['nome'] = vet_salvo.nome
        
        return redirect(url_for('web_bp.dashboard_vet'))

    return render_template('register_vet.html')

# ==============================================================================
# ÁREA DO TUTOR
# ==============================================================================

@web_bp.route('/tutor/dashboard')
def dashboard_tutor():
    if session.get('tipo') != 'tutor': return redirect(url_for('web_bp.landing'))
    
    dono_id = session['user_id']
    lista = dono_dao.listar()
    dono_encontrado = next((d for d in lista if d['id'] == dono_id), None)
    
    if not dono_encontrado:
        session.clear()
        flash("Sessão expirada. Faça login novamente.")
        return redirect(url_for('web_bp.login', tipo='tutor'))
            
    pets = [p for p in pet_dao.listar() if p['dono_id'] == dono_id]
    recompensa = recompensa_dao.buscar_por_dono(dono_id)
    
    pontos = recompensa['pontos'] if recompensa else 0
    progresso = (pontos % 500) / 500 * 100
    falta = 500 - (pontos % 500)

    consultas = [c for c in consulta_dao.listar() if c['pet_id'] in [p['id'] for p in pets]]

    return render_template('dashboard_tutor.html', 
                           dono=dono_encontrado, pets=pets, 
                           recompensa=recompensa, progresso=int(progresso), falta=falta, consultas=consultas)

@web_bp.route('/tutor/vacinas/<int:pet_id>')
def vacinas_pet(pet_id):
    if session.get('tipo') != 'tutor': return redirect(url_for('web_bp.landing'))
    
    todos_pets = pet_dao.listar()
    pet_encontrado = next((p for p in todos_pets if p['id'] == pet_id), None)
    
    if not pet_encontrado: return "Pet não encontrado", 404
    
    todas_vacinas = vacina_dao.listar()
    vacinas_do_pet = [v for v in todas_vacinas if v['pet_id'] == pet_id]
    
    return render_template('carteira_vacina.html', pet=pet_encontrado, vacinas=vacinas_do_pet)

@web_bp.route('/tutor/perfil')
def perfil_tutor():
    if session.get('tipo') != 'tutor': return redirect(url_for('web_bp.landing'))
    dono_id = session['user_id']
    lista = dono_dao.listar()
    dono = next((d for d in lista if d['id'] == dono_id), None)
    return render_template('perfil_tutor.html', dono=dono)

@web_bp.route('/tutor/perfil/atualizar', methods=['POST'])
def atualizar_perfil_tutor():
    if session.get('tipo') != 'tutor': return redirect(url_for('web_bp.landing'))
    
    dono_atualizado = Dono(
        nome=request.form['nome'],
        email=request.form['email'],
        telefone=request.form['telefone'],
        senha="" # Senha não muda aqui
    )
    dono_atualizado.id = session['user_id']
    dono_dao.atualizar(dono_atualizado)
    session['nome'] = dono_atualizado._nome
    return redirect(url_for('web_bp.perfil_tutor'))

@web_bp.route('/tutor/agendar', methods=['GET', 'POST'])
def agendar_tutor():
    if session.get('tipo') != 'tutor': return redirect(url_for('web_bp.landing'))
    dono_id = session['user_id']

    if request.method == 'POST':
        vaga_id = int(request.form['vaga_id'])
        todas_vagas = disp_dao.listar_livres()
        vaga_selecionada = next((v for v in todas_vagas if v.id == vaga_id), None)
        
        if vaga_selecionada:
            nova_consulta = Consulta(
                data=vaga_selecionada.data,
                hora=vaga_selecionada.hora,
                veterinario_id=vaga_selecionada.veterinario_id,
                pet_id=request.form['pet_id'],
                motivo=request.form['motivo']
            )
            consulta_dao.agendar(nova_consulta)
            disp_dao.ocupar_vaga(vaga_id)
            
        return redirect(url_for('web_bp.dashboard_tutor'))

    todos_pets = pet_dao.listar()
    meus_pets = [p for p in todos_pets if p['dono_id'] == dono_id]
    vagas_livres = disp_dao.listar_livres()
    lista_vets = vet_dao.listar()
    
    opcoes_agendamento = []
    for vaga in vagas_livres:
        nome_vet = next((v['nome'] for v in lista_vets if v['id'] == vaga.veterinario_id), 'Vet')
        opcoes_agendamento.append({'id': vaga.id, 'texto': f"{vaga.data} às {vaga.hora} - {nome_vet}"})
    
    return render_template('agendar.html', pets=meus_pets, vagas=opcoes_agendamento)

@web_bp.route('/deletar/pet/<int:id>', methods=['POST'])
def deletar_pet(id):
    if session.get('tipo') != 'tutor': return redirect(url_for('web_bp.landing'))
    pet_dao.excluir(id)
    return redirect(url_for('web_bp.dashboard_tutor'))

# --- EDITAR PET ---
@web_bp.route('/tutor/pet/editar/<int:id>', methods=['GET', 'POST'])
def editar_pet(id):
    if session.get('tipo') != 'tutor': return redirect(url_for('web_bp.landing'))
    
    # Busca o pet existente para preencher o formulário
    pet = pet_dao.buscar_por_id(id)
    if not pet or pet.dono_id != session['user_id']:
        return redirect(url_for('web_bp.dashboard_tutor'))

    if request.method == 'POST':
        # Atualiza os dados do objeto
        pet.nome = request.form['nome_pet']
        pet.especie = request.form['tipo']
        pet.raca = request.form['raca']
        pet.idade = request.form['idade']
        pet.peso = request.form['peso']
        pet.data_nascimento = request.form['data_nascimento']
        
        pet_dao.atualizar(pet)
        return redirect(url_for('web_bp.dashboard_tutor'))

    return render_template('editar_pet.html', pet=pet)
# ==============================================================================
# ÁREA DO VETERINÁRIO
# ==============================================================================

# --- DASHBOARD VETERINÁRIO (COM LÓGICA DE SEMANA) ---

@web_bp.route('/vet/dashboard')
def dashboard_vet():
    if session.get('tipo') != 'veterinario': return redirect(url_for('web_bp.landing'))
    
    # Busca consultas do banco
    consultas = consulta_dao.listar()
    
    # Prepara variáveis de data
    hoje = datetime.now().date()
    inicio_semana = hoje - timedelta(days=hoje.weekday()) # Segunda-feira
    fim_semana = inicio_semana + timedelta(days=6)        # Domingo
    
    agenda_completa = []
    pacientes_semana = 0 # Contador para "Esta Semana"

    for c in consultas:
        if c['veterinario_id'] == session['user_id']:
            # Converte a data string do banco para objeto data real
            data_consulta = datetime.strptime(c['data'], '%Y-%m-%d').date()
            
            # Lógica 1: Se for hoje, entra na agenda do dia
            if data_consulta == hoje:
                pet = next((p for p in pet_dao.listar() if p['id'] == c['pet_id']), None)
                dono = next((d for d in dono_dao.listar() if d['id'] == pet['dono_id']), None) if pet else None
                agenda_completa.append({
                    'hora': c['hora'],
                    'pet_nome': pet['nome'] if pet else 'Desconhecido',
                    'dono_nome': dono['nome'] if dono else 'Desconhecido',
                    'motivo': c['motivo']
                })
            
            # Lógica 2: Verifica se está na semana atual
            if inicio_semana <= data_consulta <= fim_semana:
                pacientes_semana += 1

    return render_template('dashboard_vet.html', 
                           nome_vet=session['nome'], 
                           agenda=agenda_completa, 
                           total_semana=pacientes_semana) # Passamos a nova variável

@web_bp.route('/vet/disponibilidade', methods=['GET', 'POST'])
def vet_disponibilidade():
    if session.get('tipo') != 'veterinario': return redirect(url_for('web_bp.landing'))
    vet_id = session['user_id']

    if request.method == 'POST':
        data_selecionada = request.form['data']
        hora_inicio_str = request.form['inicio']
        hora_fim_str = request.form['fim']
        intervalo_minutos = int(request.form['intervalo'])

        inicio = datetime.strptime(hora_inicio_str, '%H:%M')
        fim = datetime.strptime(hora_fim_str, '%H:%M')
        
        atual = inicio
        while atual < fim:
            hora_formatada = atual.strftime('%H:%M')
            nova_vaga = Disponibilidade(veterinario_id=vet_id, data=data_selecionada, hora=hora_formatada, status='livre')
            disp_dao.criar(nova_vaga)
            atual = atual + timedelta(minutes=intervalo_minutos)

        return redirect(url_for('web_bp.vet_disponibilidade'))
    
    if request.args.get('delete_id'):
        disp_dao.excluir(request.args.get('delete_id'))
        return redirect(url_for('web_bp.vet_disponibilidade'))

    minhas_vagas = disp_dao.listar_por_vet(vet_id)
    return render_template('gerenciar_disponibilidade.html', vagas=minhas_vagas)

@web_bp.route('/vet/prontuario', methods=['GET', 'POST'])
def prontuario_vet():
    if session.get('tipo') != 'veterinario': return redirect(url_for('web_bp.landing'))
    
    if request.method == 'POST':
        tipo = request.form['tipo']
        pet_id = int(request.form['pet_id'])
        
        if tipo == 'vacina':
            nova_vacina = Vacina(request.form['nome_vacina'], request.form['data'], request.form['validade'], pet_id)
            vacina_dao.aplicar(nova_vacina)
        elif tipo == 'consulta':
            nova_consulta = Consulta(request.form['data'], request.form['hora'], session['user_id'], pet_id, f"Realizada: {request.form['observacoes']}")
            consulta_dao.agendar(nova_consulta)
            
        return redirect(url_for('web_bp.dashboard_vet'))

    pets = pet_dao.listar()
    return render_template('prontuario_vet.html', pets=pets)

@web_bp.route('/vet/historico')
def historico_vet():
    if session.get('tipo') != 'veterinario': return redirect(url_for('web_bp.landing'))
    todas = consulta_dao.listar()
    vet_id = session['user_id']
    agendadas = []
    realizadas = []
    for c in todas:
        if c['veterinario_id'] == vet_id:
            pet = next((p for p in pet_dao.listar() if p['id'] == c['pet_id']), None)
            c['pet_nome'] = pet['nome'] if pet else 'Desconhecido'
            if "Realizada" in c.get('motivo', ''): realizadas.append(c)
            else: agendadas.append(c)
    return render_template('historico_vet.html', agendadas=agendadas, realizadas=realizadas)

@web_bp.route('/vet/perfil')
def perfil_vet():
    if session.get('tipo') != 'veterinario': return redirect(url_for('web_bp.landing'))
    vet_id = session['user_id']
    lista = vet_dao.listar()
    vet = next((v for v in lista if v['id'] == vet_id), None)
    return render_template('perfil_vet.html', vet=vet)

# ==============================================================================
# ÁREA ADMINISTRATIVA
# ==============================================================================

@web_bp.route('/admin')
def admin_panel():
    if session.get('tipo') != 'admin': return redirect(url_for('web_bp.landing'))
    donos = dono_dao.listar()
    vets = vet_dao.listar()
    pets = pet_dao.listar()
    mapa_pontos = {}
    for d in donos:
        rec = recompensa_dao.buscar_por_dono(d['id'])
        mapa_pontos[d['id']] = rec['pontos'] if rec else 0
    
    # O ERRO ESTAVA AQUI: Faltou fechar o parenteses na versão anterior
    return render_template('admin_panel.html', donos=donos, vets=vets, pets=pets, mapa_pontos=mapa_pontos)

@web_bp.route('/admin/dar_pontos', methods=['POST'])
def admin_dar_pontos():
    if session.get('tipo') != 'admin': return redirect(url_for('web_bp.landing'))
    dono_id = int(request.form['dono_id'])
    pontos_extras = int(request.form['pontos'])
    rec_atual = recompensa_dao.buscar_por_dono(dono_id)
    novos_pontos = (rec_atual['pontos'] + pontos_extras) if rec_atual else pontos_extras
    novo_nivel = (novos_pontos // 500) + 1
    recompensa_dao.salvar_ou_atualizar(Recompensa(novos_pontos, novo_nivel, dono_id))
    return redirect(url_for('web_bp.admin_panel'))

@web_bp.route('/deletar/vet/<int:id>', methods=['POST'])
def deletar_vet(id):
    if session.get('tipo') != 'admin': return redirect(url_for('web_bp.landing'))
    vet_dao.excluir(id)
    return redirect(url_for('web_bp.admin_panel'))

@web_bp.route('/deletar/dono/<int:id>', methods=['POST'])
def deletar_dono(id):
    if session.get('tipo') != 'admin': return redirect(url_for('web_bp.landing'))
    recompensa_dao.excluir_por_dono(id)
    todos_pets = pet_dao.listar()
    for pet in todos_pets:
        if pet['dono_id'] == id: pet_dao.excluir(pet['id'])
    dono_dao.excluir(id)
    return redirect(url_for('web_bp.admin_panel'))

@web_bp.route('/admin/deletar/pet/<int:id>', methods=['POST'])
def admin_deletar_pet(id):
    if session.get('tipo') != 'admin': return redirect(url_for('web_bp.landing'))
    pet_dao.excluir(id)
    return redirect(url_for('web_bp.admin_panel'))