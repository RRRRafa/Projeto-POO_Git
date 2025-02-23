class Livro:
    def __init__(self, nome, autor, ano):
        self.nome = nome
        self.autor = autor
        self.ano = ano

class Revista(Livro):
    def __init__(self, nome, autor, ano, edicao):
        super().__init__(nome, autor, ano)
        self.edicao = edicao

class Usuario:
    def __init__(self, nome, cpf):
        self.nome = nome
        self.cpf = cpf

class Aluno(Usuario):
    def __init__(self, nome, cpf, matricula):
        super().__init__(nome, cpf)
        self.matricula = matricula
        self.emprestimo_ativo = False

class Professor(Usuario):
    def __init__(self, nome, cpf, disciplinas):
        super().__init__(nome, cpf)
        self.disciplinas = disciplinas

class Emprestimo:
    _id_counter = 1
    def __init__(self, usuario, livros, data_emprestimo, dias_limite):
        self.id = Emprestimo._id_counter
        Emprestimo._id_counter += 1
        self.usuario = usuario
        self.livros = livros
        self.data_emprestimo = data_emprestimo
        self.dias_limite = dias_limite

class Biblioteca:
    def __init__(self, nome, localizacao):
        self.nome = nome
        self.localizacao = localizacao
        self.livros = []
        self.revistas = []
        self.usuarios = []
        self.emprestimos = []

    def cadastrar_livro(self, livro):
        if any(l.nome == livro.nome for l in self.livros):
            return False
        self.livros.append(livro)
        return True

    def cadastrar_revista(self, revista):
        if any(r.nome == revista.nome for r in self.revistas):
            return False
        self.revistas.append(revista)
        return True

    def buscar_livro(self, nome):
        for livro in self.livros:
            if livro.nome == nome:
                return livro
        return None

    def buscar_revista(self, nome):
        for revista in self.revistas:
            if revista.nome == nome:
                return revista
        return None

    def atualizar_livro(self, nome, novo_autor, novo_ano):
        livro = self.buscar_livro(nome)
        if livro:
            livro.autor = novo_autor
            livro.ano = novo_ano
            return True
        return False

    def remover_livro(self, nome):
        livro = self.buscar_livro(nome)
        if livro:
            self.livros.remove(livro)
            return True
        return False

    def cadastrar_usuario(self, usuario):
        if any(u.cpf == usuario.cpf for u in self.usuarios):
            return False
        self.usuarios.append(usuario)
        return True

    def buscar_usuario(self, cpf):
        for usuario in self.usuarios:
            if usuario.cpf == cpf:
                return usuario
        return None

    def atualizar_usuario(self, cpf, novo_nome):
        usuario = self.buscar_usuario(cpf)
        if usuario:
            usuario.nome = novo_nome
            return True
        return False

    def remover_usuario(self, cpf):
        usuario = self.buscar_usuario(cpf)
        if usuario:
            self.usuarios.remove(usuario)
            return True
        return False

    def realizar_emprestimo(self, usuario_cpf, nomes_livros, data, dias):
        usuario = self.buscar_usuario(usuario_cpf)
        if not usuario:
            return None

        if isinstance(usuario, Aluno):
            if usuario.emprestimo_ativo:
                print("Aluno já possui um empréstimo ativo!")
                return None

        livros = []
        for nome in nomes_livros:
            livro = self.buscar_livro(nome)
            if not livro:
                revista = self.buscar_revista(nome)
                if not revista:
                    return None
                livros.append(revista)
            else:
                livros.append(livro)

        for item in livros:
            if item in self.livros:
                self.livros.remove(item)
            elif item in self.revistas:
                self.revistas.remove(item)

        emprestimo = Emprestimo(usuario, livros, data, dias)
        self.emprestimos.append(emprestimo)

        if isinstance(usuario, Aluno):
            usuario.emprestimo_ativo = True

        return emprestimo

    def buscar_emprestimo(self, emprestimo_id):
        for emprestimo in self.emprestimos:
            if emprestimo.id == emprestimo_id:
                return emprestimo
        return None

    def devolver_livros(self, emprestimo_id):
        emprestimo = self.buscar_emprestimo(emprestimo_id)
        if not emprestimo:
            return False

        for item in emprestimo.livros:
            if isinstance(item, Livro):
                self.livros.append(item)
            elif isinstance(item, Revista):
                self.revistas.append(item)

        if isinstance(emprestimo.usuario, Aluno):
            emprestimo.usuario.emprestimo_ativo = False

        self.emprestimos.remove(emprestimo)
        return True

def main():
    biblioteca = Biblioteca("Central", "Cidade")
    usuarios_logados = {}

    while True:
        print("\n1 - Cadastrar usuário\n2 - Login\n3 - Pesquisar livro\n4 - Pesquisar revista\n5 - Realizar empréstimo\n6 - Devolver livros\n7 - Sair")
        opcao = input("Escolha: ")

        if opcao == "1":
            tipo = input("Tipo (aluno/professor): ").lower()
            nome = input("Nome: ")
            cpf = input("CPF: ")
            if tipo == "aluno":
                matricula = input("Matrícula: ")
                usuario = Aluno(nome, cpf, matricula)
            elif tipo == "professor":
                disciplinas = input("Disciplinas (separadas por vírgula): ").split(",")
                usuario = Professor(nome, cpf, disciplinas)
            else:
                print("Tipo inválido!")
                continue
            if biblioteca.cadastrar_usuario(usuario):
                print("Usuário cadastrado!")
            else:
                print("CPF já existe!")

        elif opcao == "2":
            nome = input("Nome: ")
            cpf = input("CPF: ")
            usuario = biblioteca.buscar_usuario(cpf)
            if usuario and usuario.nome == nome:
                usuarios_logados[cpf] = usuario
                print("Login realizado!")
            else:
                print("Dados incorretos!")

        elif opcao == "3":
            termo = input("Nome do livro: ")
            livro = biblioteca.buscar_livro(termo)
            if livro:
                print(f"Livro encontrado: {livro.nome} ({livro.autor}, {livro.ano})")
            else:
                print("Livro não encontrado!")

        elif opcao == "4":
            termo = input("Nome da revista: ")
            revista = biblioteca.buscar_revista(termo)
            if revista:
                print(f"Revista encontrada: {revista.nome} (Edição {revista.edicao})")
            else:
                print("Revista não encontrada!")

        elif opcao == "5":
            cpf = input("CPF: ")
            if cpf not in usuarios_logados:
                print("Faça login primeiro!")
                continue
            livros = input("Livros/Revistas (separados por vírgula): ").split(",")
            data = input("Data (DD/MM/AAAA): ")
            dias = int(input("Dias para devolução: "))
            emprestimo = biblioteca.realizar_emprestimo(cpf, [l.strip() for l in livros], data, dias)
            if emprestimo:
                print(f"Empréstimo ID {emprestimo.id} realizado!")
            else:
                print("Erro ao realizar empréstimo!")

        elif opcao == "6":
            cpf = input("CPF: ")
            if cpf not in usuarios_logados:
                print("Faça login primeiro!")
                continue
            emprestimo_id = int(input("ID do empréstimo: "))
            if biblioteca.devolver_livros(emprestimo_id):
                print("Livros/Revistas devolvidos!")
            else:
                print("Empréstimo não encontrado!")

        elif opcao == "7":
            break

        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()