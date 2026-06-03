# Mini Shell Linux em Python

## Descrição

Este projeto consiste na implementação de uma **Mini Shell Linux em Python**, desenvolvida como atividade da disciplina **Computação Distribuída e Paralela**.

O objetivo do trabalho é aplicar, na prática, conceitos fundamentais de **Sistemas Operacionais**, especialmente aqueles relacionados ao gerenciamento de processos, threads, espaço de endereçamento de memória e chamadas de sistema abordados no Capítulo 7 do material teórico.

A Mini Shell permite a execução de comandos básicos do sistema, gerenciamento de diretórios e arquivos, criação de processos para execução de comandos externos e utilização de threads para execução concorrente de tarefas de backup.

---

# Objetivos do Projeto

- Implementar uma interface de linha de comando semelhante às shells Unix/Linux.
- Aplicar os conceitos de:
  - Processos
  - Threads
  - Espaço de Endereçamento
  - Copy-On-Write (COW)
  - Chamadas de Sistema
  - Concorrência
- Demonstrar o funcionamento de:
  - `fork()`
  - `execvp()`
  - `wait()`
  - `threading.Thread()`
- Comparar teoricamente e experimentalmente processos e threads.

---

# Estrutura do Projeto

```text
miniShellProject/
│
├── main.py
│
├── shell/
│   ├── prompt.py
│   └── parser.py
│
├── managers/
│   ├── process_manager.py
│   ├── thread_manager.py
│   ├── file_manager.py
│   └── timer_manager.py
│
└── README.md
```

---

# Arquitetura Geral

```text
Usuário
   │
   ▼
Mini Shell
   │
   ▼
Parser
   │
   ├─────────────► FileManager
   │
   ├─────────────► ProcessManager
   │
   └─────────────► ThreadManager
```

Cada módulo possui uma responsabilidade específica.

---

# Módulos do Sistema

## Prompt

Responsável pela interface principal da shell.

### Funções

- Exibir o prompt ao usuário.
- Receber comandos.
- Encaminhar comandos para o parser.
- Controlar o ciclo de execução da shell.

### Exemplo

```bash
mini-shell>
```

---

## Parser

Responsável por identificar qual comando foi digitado e encaminhá-lo para o módulo adequado.

### Exemplo

```bash
mkdir teste
```

Encaminhado para:

```python
FileManager.mkdir()
```

---

## FileManager

Responsável pelos comandos internos da shell.

### Comandos implementados

| Comando | Descrição |
|----------|------------|
| mkdir | Cria diretório |
| rmdir | Remove diretório vazio |
| rmdir -rf | Remove diretório recursivamente |
| cp | Copia arquivos |
| cd | Altera diretório atual |
| echo | Cria/escreve arquivos |

---

## ProcessManager

Responsável pela execução de comandos externos utilizando processos.

### Exemplo

```bash
ls
```

### Fluxo

```text
Shell
 │
 ▼
fork()
 │
 ├──── Processo Pai
 │
 └──── Processo Filho
           │
           ▼
       execvp()
           │
           ▼
      Executa comando
```

---

## ThreadManager

Responsável pelo comando:

```bash
backup-dir
```

Utiliza threads para executar cópias de arquivos em paralelo.

### Exemplo

```bash
backup-dir managers
```

### Resultado

```text
Backup started for directory: managers
Backup completed: managers_backup
```

---

## TimerManager

Responsável pela medição de desempenho.

Utiliza:

```python
time.perf_counter()
```

para medir o tempo de execução dos comandos.

---

# Conceitos de Sistemas Operacionais Aplicados

## Processos

Um processo representa uma instância de um programa em execução.

Na Mini Shell, comandos externos são executados por meio da criação de novos processos.

### Exemplo

```bash
ls -lah
```

---

## fork()

A chamada:

```python
os.fork()
```

cria um processo filho a partir do processo atual.

Após a execução:

```text
Shell
   │
fork()
   │
 ┌─┴─┐
 │   │
Pai Filho
```

### Retornos

```python
pid > 0
```

Processo pai.

```python
pid == 0
```

Processo filho.

---

## execvp()

Após o `fork()`, o processo filho executa:

```python
os.execvp()
```

Essa função substitui completamente o espaço de endereçamento do processo pelo programa solicitado.

### Exemplo

Antes:

```text
Processo Filho
└── Código da Shell
```

Depois:

```text
Processo Filho
└── Programa ls
```

O PID permanece o mesmo.

---

## wait()

O processo pai executa:

```python
os.wait()
```

para aguardar a finalização do processo filho.

Isso impede que o prompt retorne antes da conclusão do comando.

---

# Espaço de Endereçamento

O espaço de endereçamento corresponde à memória utilizada por um processo.

Após um `fork()`, pai e filho compartilham inicialmente as mesmas páginas físicas de memória.

---

## Copy-On-Write (COW)

Sistemas modernos utilizam a técnica de Copy-On-Write.

Inicialmente:

```text
Pai ----+
         |
         +---- Página Compartilhada
         |
Filho ---+
```

Nenhuma cópia real é realizada.

Quando ocorre uma escrita:

```python
x = 20
```

o sistema cria uma cópia privada da página modificada.

### Resultado

```text
Pai
x = 10

Filho
x = 20
```

Isso reduz significativamente o custo de criação de processos.

---

# Threads

Threads representam fluxos de execução dentro de um mesmo processo.

No projeto, são utilizadas para executar backups de diretórios.

### Exemplo

```bash
backup-dir managers
```

---

## Compartilhamento de Memória

As threads compartilham:

- Heap
- Variáveis globais
- Arquivos abertos
- Recursos do processo

Cada thread possui:

- Stack própria
- Registradores próprios
- Program Counter próprio

---

## Importante

Threads **não utilizam Copy-On-Write**.

Diferentemente dos processos criados por `fork()`, as threads compartilham diretamente o mesmo espaço de endereçamento.

---

# Comando time

O comando:

```bash
time comando
```

mede o tempo de execução utilizando:

```python
time.perf_counter()
```

### Exemplo

```bash
mini-shell> time rmdir -rf managers_backup
Execution time: 0.011305 seconds
```

---

# Benchmark

### Resultados Obtidos

```bash
mini-shell> time rmdir -rf managers_backup
Execution time: 0.011305 seconds

mini-shell> time backup-dir managers
Execution time: 0.001304 seconds
```

### Observação

O tempo medido para `backup-dir` representa apenas o tempo necessário para criar e iniciar a thread.

O backup continua executando em paralelo após o retorno do comando.

Portanto, esse valor **não representa o tempo total da cópia dos arquivos**.

---

# Como Executar

## Requisitos

- Python 3.10+
- Linux ou WSL

### Observação

O projeto utiliza:

```python
os.fork()
```

que não está disponível no Windows nativo.

Recomenda-se utilizar:

- Ubuntu
- Debian
- Fedora
- WSL Ubuntu

---

## Executando

Entrar no diretório do projeto:

```bash
cd miniShellProject
```

Executar:

```bash
python3 main.py
```

Prompt:

```bash
mini-shell>
```

---

# Exemplos de Uso

### Criar diretório

```bash
mkdir teste
```

### Entrar no diretório

```bash
cd teste
```

### Criar arquivo

```bash
echo "Olá Mundo" > arquivo.txt
```

### Listar conteúdo

```bash
ls
```

### Executar backup

```bash
backup-dir managers
```

### Medir desempenho

```bash
time ls
```

### Sair

```bash
exit
```

---

# Aprendizados Obtidos

Durante o desenvolvimento deste projeto foi possível aplicar na prática conceitos fundamentais de Sistemas Operacionais:

- Criação e gerenciamento de processos.
- Execução de programas utilizando `fork()` e `execvp()`.
- Sincronização com `wait()`.
- Concorrência utilizando threads.
- Compartilhamento de memória.
- Espaço de endereçamento.
- Copy-On-Write.
- Medição de desempenho.

A Mini Shell permitiu transformar conceitos teóricos do Capítulo 7 em uma implementação prática, demonstrando como sistemas operacionais modernos gerenciam processos, threads e memória durante a execução de aplicações.