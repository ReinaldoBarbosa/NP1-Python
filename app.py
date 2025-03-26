import json
import time
import re
import hashlib

usuario_logado = False 
status_usuario = '' 

def informar_senha(senha):
    """Função para validar e criptografar a senha"""
    padrao = re.compile("[@#$%^&+=!]")
    
    if len(senha) < 6:
        print("A senha deve ter pelo menos 6 caracteres.")
        return cadastrar_usuario()
    
    if not re.search(padrao, senha):
        print("A senha deve conter pelo menos um caractere especial (ex: @, #, $, %, ^, &, +, =, !).")
        return cadastrar_usuario()

    return hashlib.sha256(senha.encode()).hexdigest()

def cadastrar_usuario(status):
    try:
        with open('dados.json', 'r', encoding='utf-8') as arq:
            dados = json.load(arq)
    except (FileNotFoundError, json.JSONDecodeError):
        dados = {'Usuario': []}

    print("\n==== Cadastro de Usuário ====")
    
    while True:  # Agora ele pergunta até que um nome válido seja informado
        usuario = input("Digite o nome de usuário: ").strip()
        if usuario:
            break
        print("Nome não informado. Por favor, tente novamente.")

    # Verifica se o usuário já existe
    for user in dados['Usuario']:
        if user['nome'] == usuario:
            print("Usuário já cadastrado!")
            return cadastrar_usuario()

    while True:  # Loop para garantir que a senha seja válida
        senha = input("Digite a senha: ").strip()
        if senha:
            break
        print("Senha não informada. Por favor, tente novamente.")

    while True:  # Loop para garantir que a senha seja confirmada corretamente
        senha_confirmada = input("Confirme a senha: ").strip()
        if senha_confirmada == senha:
            break
        print("As senhas são diferentes! Tente novamente.")

    senha_hash = informar_senha(senha)

    if senha_hash is None:
        return  # Volta ao menu se a senha não atender aos critérios

    dados['Usuario'].append({
        'nome': usuario,
        'senha': senha_hash,
        'status' : status
    })

    with open('dados.json', 'w', encoding='utf-8') as arq:
        json.dump(dados, arq, indent=4, ensure_ascii=False)

    print(f"Usuário '{usuario}' cadastrado com sucesso!")

def login():
    global usuario_logado  # Torna a variável global para alterar o estado
    global status_usuario # Torna a variável global para alterar o estado

    try:
        with open('dados.json', 'r', encoding='utf-8') as arq:
            dados = json.load(arq)
    except (FileNotFoundError, json.JSONDecodeError):
        dados = {'Usuario': []} 

    print("\n==== Login ====")
    usuario = input("Digite o nome de usuário: ").strip()

    for user in dados['Usuario']:
        if user['nome'] == usuario:
            senha = input("Digite a senha: ").strip()
            if user['senha'] == hashlib.sha256(senha.encode()).hexdigest():
                print("Acesso Autorizado!")
                usuario_logado = True
                status_usuario = user['status']
                time.sleep(1)
                return  # Volta ao menu sem chamar `menu()` de novo
    
    print("Usuário ou senha incorretos. Tente novamente!")

def cadastrar_curso():
    try:
        with open('dados.json', 'r', encoding='utf-8') as arq:
            dados = json.load(arq)
    except (FileNotFoundError, json.JSONDecodeError):
        dados = {'Cursos': []}

    print("\n==== Cadastro de Curso ====")
    curso_nome = input("Digite o nome do curso: ")
    
    for curso in dados['Cursos']:
        if curso['nome'] == curso_nome:
            print("Esse curso já existe!")
            return
    
    conteudo = input("Digite o conteúdo do curso: ")

    dados['Cursos'].append({
        'nome': curso_nome,
        'conteudo': conteudo,
        'questoes':[

        ]
    })

    with open('dados.json', 'w', encoding='utf-8') as arq:
            json.dump(dados, arq, indent=4, ensure_ascii=False)

    print(f"Curso {curso_nome} cadastrado com sucesso!")
    menu()

def adicionar_questoes():
    try:
        with open('dados.json', 'r', encoding='utf-8') as arq:
            dados = json.load(arq)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Nenhum curso cadastrado ainda!")
        return

    print("\n==== Adicionar Questões ====")
    curso_nome = input("Digite o nome do curso ao qual deseja adicionar questões: ").strip()

    for curso in dados['Cursos']:
        if curso['nome'].lower() == curso_nome.lower():
            while True:
                enunciado = input("\nDigite o enunciado da questão (ou pressione Enter para sair): ").strip()
                if not enunciado:
                    break  # Sai do loop se o usuário pressionar Enter
                
                alternativa_a = input("Alternativa A: ").strip()
                alternativa_b = input("Alternativa B: ").strip()
                alternativa_c = input("Alternativa C: ").strip()
                resposta = input("Digite a resposta correta (A, B ou C): ").strip().upper()

                 

                if resposta not in ('A', 'B', 'C'):
                    print("Resposta inválida! Escolha entre A, B ou C.")
                    continue  # Volta para repetir a entrada da questão
                
                resposta = 'alternativa_' + resposta.lower() 

                curso['questoes'].append({
                    'enunciado': enunciado,
                    'alternativa_a': alternativa_a,
                    'alternativa_b': alternativa_b,
                    'alternativa_c': alternativa_c,
                    'resposta': resposta
                })
                print("Questão adicionada com sucesso!")

            # Salvar no JSON
            with open('dados.json', 'w', encoding='utf-8') as arq:
                json.dump(dados, arq, indent=4, ensure_ascii=False)
            print(f"\nAs questões foram salvas no curso '{curso_nome}' com sucesso!")
            return
    
    print("Curso não encontrado!")

def exibe_curso(curso):
    print(f'\n==== {curso['nome']} ====')
    print('1. Conteudo')
    print('2. Questões')
    print('3. Voltar')

    escolha = input("\nEscolha um número correspondente ao curso: ").strip()

    if escolha == '1':
        conteudo_curso(curso)
    elif escolha == '2':
        abrir_questoes(curso)
    elif escolha == '3':
        curso_disponivel()
    else:
       print("Opção inválida. Tente novamente!")

def conteudo_curso(curso):
    print(f'\n==== {curso['nome']} ====')

    print('')
    print('CONTEÚDO')
    print('')

    print(curso['conteudo'])


    escolha = input("\nPresione Enter para Voltar... ").strip()
    if not escolha:
        exibe_curso(curso)
    
def abrir_questoes(materia):
    global questoes, indice_questao, pontuacao

    questoes = materia['questoes']
    indice_questao = 0
    pontuacao = 0    

    exibir_questao()

def exibir_questao():
    global indice_questao

    if indice_questao < len(questoes):
        questao_atual = questoes[indice_questao]

        print(questao_atual['enunciado'])
        print(questao_atual['alternativa_a'])
        print(questao_atual['alternativa_b'])
        print(questao_atual['alternativa_c'])
          
    else:
        print(f"Você acertou {pontuacao} de {len(questoes)} questões!")

    if indice_questao < len(questoes):
        escolha = input("\nResposta: ").strip()

        if escolha.lower() == 'a':  
            verificar_resposta('alternativa_a')
        elif escolha.lower() == 'b':      
            verificar_resposta('alternativa_b')
        elif escolha.lower() == 'c':     
            verificar_resposta('alternativa_c')  
        else:
            print('Opção Invalida')    
    else:
        escolha = input("\nPresione Enter para Voltar... ").strip()
        if not escolha:
            curso_disponivel()    

def verificar_resposta(resposta):
    global indice_questao, pontuacao

    if resposta == questoes[indice_questao]['resposta']:
        print("Correto ✅")
        pontuacao += 1
    else:
        print("Incorreto ❌")

    time.sleep(2)  # Delay de 2 segundos
    
    indice_questao += 1
    exibir_questao()

def curso_disponivel():
    try:
        with open('dados.json', 'r', encoding='utf-8') as arq:
            dados = json.load(arq)
    except (FileNotFoundError, json.JSONDecodeError):
        dados = {'Cursos': []} 

    if not dados['Cursos']:
        print("\nNenhum curso disponível no momento.")
        return  

    print("\n==== Cursos Disponíveis ====")
    for i, materia in enumerate(dados['Cursos'], start=1):
        print(f"{i}. {materia['nome']}")

    while True:
        escolha = input("\nEscolha um número correspondente ao curso, ou pressione Enter para Voltar: ").strip()

        if escolha == "":
            menu()  # Volta para o menu se o usuário apenas pressionar Enter
            break
        
        if not escolha.isdigit():
            print("Entrada inválida! Digite um número correspondente ao curso.")
            continue  # Volta para o início do loop
        
        escolha = int(escolha)

        if 1 <= escolha <= len(dados['Cursos']):
            curso_escolhido = dados['Cursos'][escolha - 1]
            exibe_curso(curso_escolhido)
            break
        else:
            print("Opção inválida. Escolha um número dentro da lista.")

def informacao_seguranca():

    print('===== Informações de Segurança =====')
    print('- Use senhas fortes e únicas para cada plataforma.')
    print('- Nunca compartilhe suas credenciais com terceiros.')
    print('- Mantenha seu software sempre atualizado.')

    escolha = input("\nPressione Enter para voltar ao menu principal.").strip()
    if not escolha:
        menu()

def menu():
    global usuario_logado  
    global status_usuario

    while True:
        if usuario_logado:
            if status_usuario == 'Professor':
                print("\n==== Menu ====")
                print("1. Cadastrar Curso")
                print("2. Adicionar Questões")
                print("3. Cursos Disponíveis")
                print("4. Sair")
            
                escolha = input("Escolha uma opção: ").strip()

                if escolha == '1':
                    cadastrar_curso()
                elif escolha == '2':
                    adicionar_questoes()
                elif escolha == '3':
                    curso_disponivel()
                elif escolha == '4':
                    print("Saindo...")
                    usuario_logado = False 
                    status_usuario = '' 
                    time.sleep(1)
                    menu()
                else:
                    print("Opção inválida. Tente novamente!")

            elif status_usuario == 'Aluno':
                print("\n==== Menu ====")
                print("1. Cursos Disponíveis")                                
                print("2. Sair")

                escolha = input("Escolha uma opção: ").strip()

                if escolha == '1':
                    curso_disponivel()                   
                elif escolha == '2':
                    print("Saindo...")
                    usuario_logado = False 
                    status_usuario = '' 
                    time.sleep(1)
                    menu()
        else:
            print("\n==== Menu ====")
            print("1. Fazer Cadastro")
            print("2. Fazer Login")
            print("3. Informações de Segurança")  
            print("4. Sair")
            
            escolha = input("Escolha uma opção: ").strip()

            if escolha == '1':
                print("\n==== Menu ====")
                print("1. Aluno")
                print("2. Professor")
                print("3. Sair")

                escolha = input("Escolha uma opção: ").strip()

                if escolha == '1':
                    cadastrar_usuario("Aluno")
                elif escolha == '2':
                    cadastrar_usuario("Professor")
                elif escolha == '3':
                    print("Saindo...")
                    time.sleep(1)
                    menu()        
            
            elif escolha == '2':
                login()
            elif escolha == '3':
                informacao_seguranca()    
            elif escolha == '4':
                print("Saindo...")
                return
            else:
                print("Opção inválida. Tente novamente!")

menu()