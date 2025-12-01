from flask import Blueprint, render_template, request, redirect, url_for
from app.model.Dono import Dono
from app.model.Pet import Pet
from app.model.Veterinario import Veterinario
from app.model.Consulta import Consulta
from app.model.Recompensa import Recompensa
# Importando todos os DAOs necessários
from app.dao.DonoDAO import DonoDAO
from app.dao.PetDAO import PetDAO
from app.dao.VeterinarioDAO import VeterinarioDAO
from app.dao.ConsultaDAO import ConsultaDAO
from app.dao.RecompensaDAO import RecompensaDAO  # <--- Importante para os pontos

web_bp = Blueprint('web_bp', __name__)

# Instancia os DAOs para acessar o banco de dados
dono_dao = DonoDAO()
pet_dao = PetDAO()
vet_dao = VeterinarioDAO()
consulta_dao = ConsultaDAO()
recompensa_dao = RecompensaDAO() # <--- Instância da Recompensa

# --- PÁGINA INICIAL (Menu) ---
@web_bp.route('/')
def index():
    return render_template('index.html')

# --- LISTA DE CLIENTES (Para acessar os Dashboards) ---
@web_bp.route('/clientes')
def listar_clientes():
    lista_donos = dono_dao.listar()
    return render_template('lista_clientes.html', donos=lista_donos)

# --- DASHBOARD DO DONO (ATUALIZADO COM PROGRESSO) ---
@web_bp.route('/dashboard/<int:dono_id>')
def dashboard(dono_id):
    # 1. Busca Dono
    lista_donos = dono_dao.listar()
    dono_encontrado = None
    for d in lista_donos:
        if d['id'] == dono_id:
            dono_encontrado = d
            break
    
    if not dono_encontrado:
        return "<h1>Dono não encontrado!</h1>", 404

    # 2. Busca Pets
    todos_pets = pet_dao.listar()
    meus_pets = [p for p in todos_pets if p['dono_id'] == dono_id]

    # 3. Busca Recompensa e CALCULA O PROGRESSO
    minha_recompensa = recompensa_dao.buscar_por_dono(dono_id)
    
    if minha_recompensa:
        pontos_totais = minha_recompensa['pontos']
        # O operador % (módulo) pega o resto da divisão. 
        # Ex: 750 % 500 = 250 (pontos dentro do nível atual)
        pontos_no_nivel = pontos_totais % 500
        
        # Calcula a porcentagem (regra de 3)
        porcentagem = (pontos_no_nivel / 500) * 100
        
        # Calcula quanto falta para o próximo
        proximo_nivel_em = 500 - pontos_no_nivel
    else:
        pontos_totais = 0
        porcentagem = 0
        proximo_nivel_em = 500

    # 4. Renderiza enviando as novas variáveis (porcentagem e falta_quanto)
    return render_template(
        'dashboard.html', 
        dono=dono_encontrado, 
        pets=meus_pets, 
        recompensa=minha_recompensa,
        porcentagem=int(porcentagem), # Envia como número inteiro (sem vírgula)
        falta_pontos=proximo_nivel_em
    )

# --- CADASTRO DE DONO ---
@web_bp.route('/novo/dono', methods=['GET', 'POST'])
def novo_dono():
    if request.method == 'POST':
        dono = Dono(
            nome=request.form['nome'],
            email=request.form['email'],
            telefone=request.form['telefone']
        )
        dono_dao.salvar(dono)
        return redirect(url_for('web_bp.listar_clientes')) # Vai para a lista após salvar
    return render_template('form_dono.html')

# --- CADASTRO DE PET ---
@web_bp.route('/novo/pet', methods=['GET', 'POST'])
def novo_pet():
    if request.method == 'POST':
        pet = Pet(
            nome=request.form['nome'],
            dono_id=request.form['dono_id'],
            especie=request.form['especie'],
            raca=request.form['raca'],
            idade=request.form['idade'],
            peso=request.form['peso']
        )
        pet_dao.salvar(pet)
        return redirect(url_for('web_bp.index'))
    
    lista_donos = dono_dao.listar() 
    return render_template('form_pet.html', donos=lista_donos)

# --- CADASTRO DE VETERINÁRIO ---
@web_bp.route('/novo/veterinario', methods=['GET', 'POST'])
def novo_vet():
    if request.method == 'POST':
        vet = Veterinario(
            nome=request.form['nome'],
            crmv=request.form['crmv'],
            especialidade=request.form['especie'],
            telefone=request.form['telefone'],
            email=request.form['email']
        )
        vet_dao.salvar(vet)
        return redirect(url_for('web_bp.index'))
    return render_template('form_vet.html')

# --- AGENDAR CONSULTA ---
@web_bp.route('/nova/consulta', methods=['GET', 'POST'])
def nova_consulta():
    if request.method == 'POST':
        consulta = Consulta(
            data=request.form['data'],
            hora=request.form['hora'],
            veterinario_id=request.form['veterinario_id'],
            pet_id=request.form['pet_id'],
            motivo=request.form['motivo']
        )
        consulta_dao.agendar(consulta)
        return redirect(url_for('web_bp.index'))

    lista_vets = vet_dao.listar()
    lista_pets = pet_dao.listar()
    return render_template('form_consulta.html', vets=lista_vets, pets=lista_pets)
   
# --- DAR PONTOS (Gamificação) ---
@web_bp.route('/dar_pontos', methods=['POST'])
def dar_pontos():
    dono_id = int(request.form['dono_id'])
    pontos_extras = int(request.form['pontos'])

    # 1. Busca a recompensa atual (se existir)
    rec_atual = recompensa_dao.buscar_por_dono(dono_id)
    
    if rec_atual:
        # Se já tem, soma os pontos
        novos_pontos = rec_atual['pontos'] + pontos_extras
    else:
        # Se não tem, começa com o valor informado
        novos_pontos = pontos_extras

    # 2. Calcula o nível (Exemplo: A cada 500 pontos sobe 1 nível)
    novo_nivel = (novos_pontos // 500) + 1

    # 3. Cria o objeto e salva
    nova_recompensa = Recompensa(
        pontos=novos_pontos,
        nivel=novo_nivel,
        dono_id=dono_id
    )
    recompensa_dao.salvar_ou_atualizar(nova_recompensa)

    # 4. Recarrega a página do dashboard
    return redirect(url_for('web_bp.dashboard', dono_id=dono_id))

# --- EXCLUIR PET ---
@web_bp.route('/deletar/pet/<int:id>', methods=['POST'])
def deletar_pet(id):
    # Precisamos saber quem é o dono antes de apagar o pet, para voltar ao dashboard dele
    # Na prática, poderíamos buscar o pet pelo ID antes, mas vamos passar o dono_id no form
    dono_id = request.form['dono_id']
    pet_dao.excluir(id)
    return redirect(url_for('web_bp.dashboard', dono_id=dono_id))

# --- EXCLUIR DONO (Conta Completa) ---
@web_bp.route('/deletar/dono/<int:id>', methods=['POST'])
def deletar_dono(id):
    # 1. Apaga a pontuação (Recompensa)
    recompensa_dao.excluir_por_dono(id)
    
    # 2. Apaga TODOS os pets desse dono (busca manual)
    todos_pets = pet_dao.listar()
    for pet in todos_pets:
        if pet['dono_id'] == id:
            pet_dao.excluir(pet['id'])
            
    # 3. Finalmente, apaga o dono
    dono_dao.excluir(id)
    
    return redirect(url_for('web_bp.listar_clientes'))
