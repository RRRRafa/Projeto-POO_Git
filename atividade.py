class Livro:
    def __init__(self, nome, autor, ano):
        self.nome = nome
        self.autor = autor
        self.ano = ano

class Usuario:
    def __init__(self, nome, cpf):
        self.nome = nome
        self.cpf = cpf

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
        self.usuarios = []
        self.emprestimos = []

    def cadastrar_livro(self, livro):
        if any(l.nome == livro.nome for l in self.livros):
            return False
        self.livros.append(livro)
        return True

    def buscar_livro(self, nome):
        for livro in self.livros:
            if livro.nome == nome:
                return livro
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
        livros = []
        for nome in nomes_livros:
            livro = self.buscar_livro(nome)
            if not livro:
                return None
            livros.append(livro)
        for livro in livros:
            self.remover_livro(livro.nome)
        emprestimo = Emprestimo(usuario, livros, data, dias)
        self.emprestimos.append(emprestimo)
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
        for livro in emprestimo.livros:
            self.livros.append(livro)
        self.emprestimos.remove(emprestimo)
        return True

def main():
    biblioteca = Biblioteca("Central", "Cidade")
    usuarios_logados = {}

    while True:
        print("\n1 - Cadastrar usuário\n2 - Login\n3 - Pesquisar livro\n4 - Realizar empréstimo\n5 - Devolver livros\n6 - Sair")
        opcao = input("Escolha: ")

        if opcao == "1":
            nome = input("Nome: ")
            cpf = input("CPF: ")
            usuario = Usuario(nome, cpf)
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
            cpf = input("CPF: ")
            if cpf not in usuarios_logados:
                print("Faça login primeiro!")
                continue
            livros = input("Livros (separados por vírgula): ").split(",")
            data = input("Data (DD/MM/AAAA): ")
            dias = int(input("Dias para devolução: "))
            emprestimo = biblioteca.realizar_emprestimo(cpf, [l.strip() for l in livros], data, dias)
            if emprestimo:
                print(f"Empréstimo ID {emprestimo.id} realizado!")
            else:
                print("Erro ao realizar empréstimo!")

        elif opcao == "5":
            cpf = input("CPF: ")
            if cpf not in usuarios_logados:
                print("Faça login primeiro!")
                continue
            emprestimo_id = int(input("ID do empréstimo: "))
            if biblioteca.devolver_livros(emprestimo_id):
                print("Livros devolvidos!")
            else:
                print("Empréstimo não encontrado!")

        elif opcao == "6":
            break

        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()