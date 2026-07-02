# 🧠 FeynmanTutor AI: Democratizando o Aprendizado Através de GenAI Open-Source na Nuvem

🚀 **Conectando Educação, Inteligência Artificial e Infraestrutura Cloud de Alta Performance.**

---

## 💻 Link da Aplicação em Produção
* **Acesse o Chatbot aqui:** `http://<IP_DA_SUA_MAQUINA_ORACLE>:8501` *(Substitua pelo IP real fornecido pela Oracle Cloud)*

---

## 📝 Relatório Técnico do Projeto

### 1. Introdução
**Objetivo da Atividade:** O projeto consiste no desenvolvimento e implantação de um chatbot focado em engenharia pedagógica ativa, utilizando a arquitetura de IA Generativa. 
**Visão Geral da Solução:** Foi desenvolvido o **FeynmanTutor AI**, um assistente baseado no renomado *Método Feynman de Aprendizagem*. Em vez de fornecer respostas automáticas, o bot atua como um tutor socrático, desafiando o usuário a explicar conceitos complexos com linguagem simples (como se estivesse explicando para uma criança). O projeto une o framework Streamlit para interface de usuário, APIs da NVIDIA Cloud para inferência de modelos open-source e infraestrutura Oracle Cloud Infrastructure (OCI) para hospedagem de produção.

### 2. Infraestrutura Cloud
Para garantir a estabilidade e a acessibilidade global do assistente, a aplicação foi publicada em produção utilizando a seguinte arquitetura de nuvem:
* **Provedor:** Oracle Cloud Infrastructure (OCI)
* **Máquina Virtual:** VM.Standard.A1.Flex (Ampere) ou VM.Standard.E4.Flex *(Escolha a que você usou)*
* **Recursos Computacionais:** 1 a 4 OCPUs / 6GB a 24GB de RAM *(Ajuste conforme sua VM)*
* **Sistema Operacional:** Ubuntu 22.04 LTS / Oracle Linux *(Ajuste conforme sua VM)*
* **Rede:** Configuração de listas de segurança (Security Lists) liberando tráfego de entrada na porta ingress TCP `8501`.

### 3. Modelo Escolhido
* **Nome do Modelo:** `deepseek-ai/deepseek-v4-flash` (disponibilizado via NVIDIA NIM/Cloud)
* **Justificativa da Escolha:** O DeepSeek-V4-Flash destaca-se por sua altíssima eficiência computacional alinhada à capacidade nativa de raciocínio lógico avançado (*reasoning effort low*). Para um assistente socrático como o FeynmanTutor, o modelo precisa analisar e mapear lacunas lógicas e jargões ocultos na resposta do estudante antes de formular uma pergunta de acompanhamento. Essa inteligência analítica em tempo real viabiliza o método de ensino proposto sem onerar custos de infraestrutura local.

### 4. Desenvolvimento e Arquitetura
* **Arquitetura da Aplicação:** O software segue o padrão single-page reativo do Streamlit. O histórico de mensagens é gerenciado localmente via `st.session_state` e transmitido sequencialmente em formato estruturado (JSON) para a API da NVIDIA para manter o contexto.
* **Principais Bibliotecas:** 
  * `streamlit`: Construção da interface gráfica e componentes de chat.
  * `openai`: Cliente oficial utilizado para realizar requisições compatíveis ao padrão NVIDIA NIM.
  * `python-dotenv`: Gerenciamento seguro de variáveis globais de ambiente.
* **Gerenciamento de Credenciais:** Seguindo os pilares de segurança da informação, chaves de API cruciais não foram expostas no código fonte. Utilizou-se a abordagem de injeção via variáveis de ambiente localizadas em arquivo `.env` (devidamente protegido contra commits públicos via `.gitignore`).

### 5. Implantação e Desafios
O processo de publicação na Oracle Cloud envolveu a criação da instância, clonagem do repositório Git, configuração do ambiente Anaconda e execução em background através de gerenciadores de processo (como `nohup` ou `tmux`).
* **Principais Desafios:** O maior desafio técnico centrou-se na liberação do tráfego de rede na Oracle Cloud. Além de abrir a porta `8501` no painel web da OCI (VCN Security Lists), foi necessário configurar o firewall interno do Linux (`iptables` ou `ufw`) para permitir que requisições externas acessassem o servidor Streamlit.

### 6. Discussão e Lições Aprendidas
* **Lições Aprendidas:** A atividade consolidou conceitos práticos de engenharia de prompt avançada (System Prompts restritivos) e provou o valor de modelos open-source de reasoning para interações de alta complexidade conceitual. Além disso, reforçou a importância do DevOps básico na computação em nuvem.
* **Melhorias Futuras:** Como próximos passos para o produto, planeja-se a inclusão de arquitetura RAG (Geração Aumentada por Recuperação) para permitir que o usuário faça o upload de PDFs de livros texto específicos, além da implementação de análise de sentimento para ajustar o tom motivacional do tutor.

---

## 🛠️ Instruções de Instalação e Execução

### Pré-requisitos
* Ter o [Anaconda ou Miniconda](https://anaconda.com) instalado.
* Uma chave de API gerada na plataforma da NVIDIA.

### Passo a Passo

1. **Clone o Repositório:**
   ```bash
   git clone <LINK_DO_SEU_GITHUB>
   cd <NOME_DO_DIRETORIO>
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
   streamlit run app/main.py
   ```
