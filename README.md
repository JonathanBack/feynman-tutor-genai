# FeynmanTutor AI: Democratizando o Aprendizado Através de GenAI

**Conectando Educação, Inteligência Artificial e Infraestrutura Cloud.**

---

## Link da Aplicação em Produção
* **Acesse o Chatbot aqui:** `http://64.181.174.184:8501`

---

## Relatório Técnico do Projeto

### 1. Introdução
**Objetivo da Atividade:** O projeto consiste no desenvolvimento e implantação de um chatbot focado em engenharia pedagógica ativa, utilizando a arquitetura de IA Generativa. 
**Visão Geral da Solução:** Foi desenvolvido o **FeynmanTutor AI**, um assistente baseado no renomado *Método Feynman de Aprendizagem*. Em vez de fornecer respostas automáticas, o bot atua como um tutor socrático, desafiando o usuário a explicar conceitos complexos com linguagem simples (como se estivesse explicando para uma criança). O projeto une o framework Streamlit para interface de usuário, APIs da NVIDIA Cloud para inferência de modelos open-source e infraestrutura Oracle Cloud Infrastructure (OCI) para hospedagem de produção.

### 2. Infraestrutura Cloud
Para garantir a estabilidade e a acessibilidade global do assistente, a aplicação foi publicada em produção utilizando a seguinte arquitetura de nuvem:
* **Provedor:** Oracle Cloud Infrastructure (OCI)
* **Máquina Virtual:** VM.Standard.E2.1.Micro
* **Recursos Computacionais:** 1 OCPUs / 1GB de RAM 
* **Sistema Operacional:** Ubuntu 22.04 
* **Rede:** Configuração de listas de segurança (Security Lists) liberando tráfego de entrada na porta ingress TCP `8501`.

### 3. Modelo Escolhido
* **Nome do Modelo:** `mistralai/ministral-14b-instruct-2512` (disponibilizado via NVIDIA NIM/Cloud)
* **Justificativa da Escolha:** O Ministral-14B-Instruct é um modelo instrutivo focado em baixa latência e respostas curtas, sem cadeia de raciocínio explícita. Para um tutor socrático como o FeynmanTutor, a velocidade de resposta é o fator crítico de usabilidade pois uma resposta lenta quebra o ritmo do método. Por ser não-reasoning, o modelo entrega feedback imediato em linguagem natural, viabilizando a interação conversacional exigida pelo Método Feynman sem o ônus de custo por tokens de raciocínio.

### 4. Desenvolvimento e Arquitetura
* **Arquitetura da Aplicação:** O software segue o padrão single-page reativo do Streamlit. O histórico de mensagens é gerenciado localmente via `st.session_state` e transmitido sequencialmente em formato estruturado (JSON) para a API da NVIDIA para manter o contexto.
* **Principais Bibliotecas:** 
  * `streamlit`: Construção da interface gráfica e componentes de chat.
  * `openai`: Cliente oficial utilizado para realizar requisições compatíveis ao padrão NVIDIA NIM.
  * `python-dotenv`: Gerenciamento seguro de variáveis globais de ambiente.
* **Gerenciamento de Credenciais:** Seguindo os pilares de segurança da informação, chaves de API cruciais não foram expostas no código fonte. Utilizou-se a abordagem de injeção via variáveis de ambiente localizadas em arquivo `.env.

### 5. Implantação e Desafios
O processo de publicação na Oracle Cloud envolveu a criação da instância, clonagem do repositório Git, configuração do ambiente conda e execução em background através de gerenciadores de processo (como `nohup` ou `tmux`).
* **Principais Desafios:** O maior desafio técnico centrou-se na liberação do tráfego de rede na Oracle Cloud. Além de abrir a porta `8501` no painel web da OCI (VCN Security Lists), foi necessário configurar o firewall interno do Linux para permitir que requisições externas acessassem o servidor Streamlit.

### 6. Discussão e Lições Aprendidas
* **Lições Aprendidas:** A atividade consolidou conceitos práticos de engenharia de prompt avançada (System Prompts restritivos) e provou o valor de modelos open-source para interações com usuários. Além disso, reforçou a importância do DevOps básico na computação em nuvem.
* **Melhorias Futuras:** Como próximos passos para o produto, planeja-se a inclusão de arquitetura RAG (Geração Aumentada por Recuperação) para permitir que o usuário faça o upload de PDFs de livros texto específicos.

---

## Instruções de Instalação e Execução

### Pré-requisitos
* Ter o [Anaconda ou Miniconda](https://anaconda.com) instalado.
* Uma chave de API gerada na plataforma da NVIDIA.

### Passo a Passo

1. **Clone o Repositório:**
   ```bash
   git clone https://github.com/JonathanBack/feynman-tutor-genai.git
   cd feynman-tutor-genai
   ```

2. **Crie e Ative o Ambiente Conda:**
   ```bash
   conda create --name feynman-tutor python=3.10 -y
   conda activate feynman-tutor
   ```

3. **Instale as Dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as Variáveis de Ambiente:**
   * Crie um arquivo chamado `.env` na raiz do projeto.
   * Adicione sua chave da NVIDIA conforme o exemplo:
   ```text
   NVIDIA_API_KEY="sua_chave_aqui"
   ```

5. **Execute a Aplicação:**
   ```bash
   streamlit run app.py
   ```