# Atividade 07 — Docker Compose | PequenoJim

**Disciplina:** Ferramentas Ágeis II  
**Aluno:** João Pedro Martinez Zambon (RA 219077)  
**Curso:** Análise e Desenvolvimento de Sistemas — 6º Termo A  
**Instituição:** UniSALESIANO — Araçatuba/SP

## Objetivo

Criar uma imagem Docker para uma aplicação web que exibe o wallpaper PequenoJim e executar seus serviços via Docker Compose no GitHub Codespaces. A página também mantém um contador de visitas, persistido pelo Redis.

## Estrutura

| Arquivo ou pasta | Finalidade |
| --- | --- |
| `Dockerfile` | Constrói a imagem Docker da aplicação Python/Flask. |
| `compose.yaml` | Define os serviços `web` e `redis`, rede, volume, reinicialização e monitoramento de saúde. |
| `compose.test.yaml` | Adiciona um serviço específico para executar testes automatizados. |
| `app.py` | Aplicação web e consulta ao contador no Redis. |
| `templates/index.html` | Interface HTML. |
| `static/` | Estilos da página e wallpaper original. |
| `tests/test_app.py` | Testes automatizados da página, imagem e saúde da aplicação. |
| `.github/workflows/ci.yaml` | Testes automáticos no GitHub Actions. |
| `.devcontainer/devcontainer.json` | Prepara o Codespaces para executar Docker e encaminhar a porta 8000. |

## Pré-requisito

Conta no GitHub com acesso ao Codespaces. Nenhuma instalação local de Docker é necessária para executar a atividade no Codespaces.

## Passo 1 — Subir para o GitHub

1. Extraia o arquivo ZIP no computador.
2. Acesse `https://github.com/new` e crie o repositório `atividade07-docker-compose-pequenojim`.
3. Se o repositório estiver vazio, clique em **uploading an existing file**; se já houver arquivos, escolha **Add file > Upload files**.
4. Arraste **todos os arquivos e as pastas de dentro da pasta extraída**, preservando `static`, `templates`, `tests`, `.github` e `.devcontainer`. Não envie apenas o ZIP e não crie uma pasta extra acima dos arquivos.
5. Confira se `compose.yaml` e `Dockerfile` estão na raiz do repositório.
6. Confirme em **Commit changes**.

## Passo 2 — Abrir no Codespaces

1. No repositório GitHub, selecione **Code > Codespaces > Create codespace on main**.
2. Aguarde o ambiente preparar as dependências. A configuração `.devcontainer` habilita Docker dentro do Codespaces.
3. Abra **Terminal > New Terminal**.
4. Confira as versões:

   ```bash
   docker --version
   docker compose version
   ```

## Passo 3 — Validar e executar

No terminal do Codespaces, com o diretório do projeto aberto:

```bash
docker compose config
```

Esse comando valida a sintaxe e a configuração final do Compose.

```bash
docker compose up -d --build
```

O Docker constrói `pequenojim-web:1.0` e inicia a aplicação e o Redis.

```bash
docker compose ps
```

Espere alguns segundos: ambos os serviços deverão aparecer como `Up` e, após a inicialização, `healthy`.

```bash
docker images
```

Confirme a presença da imagem `pequenojim-web` com a tag `1.0`.

```bash
docker compose exec redis redis-cli ping
```

A resposta esperada é `PONG`.

```bash
curl -i http://localhost:8000/health
```

A resposta esperada contém `HTTP/1.1 200 OK` e um JSON com `"status":"ok"`.

Na aba **PORTS** do Codespaces, escolha a porta `8000` e clique em **Open in Browser**. A página deve exibir o wallpaper e o total de visitas. Atualize a página e confira o aumento do contador.

## Passo 4 — Testar persistência do volume

Anote o total de visitas exibido na página. Em seguida, execute:

```bash
docker compose down
docker compose up -d
```

Abra novamente a página e confirme que a contagem **não voltou a zero**. O volume `dados_redis` mantém o valor salvo. Não utilize `docker compose down -v` na execução normal, pois `-v` remove o volume do projeto.

## Passo 5 — Testes automáticos com o Compose adicional

```bash
docker compose -f compose.yaml -f compose.test.yaml build tests
docker compose -f compose.yaml -f compose.test.yaml run --rm tests
```

O resultado esperado contém três testes concluídos e `OK`. O fluxo em `.github/workflows/ci.yaml` também executa os testes automaticamente em `push` e `pull_request` no GitHub Actions.

## Passo 6 — Capturar as evidências

Capture **prints reais do Codespaces**, preferencialmente contendo o terminal e os resultados:

1. `docker compose config` — configuração validada.
2. `docker compose up -d --build` — construção/inicialização dos serviços.
3. `docker compose ps` — `web` e `redis` ativos.
4. `docker images` — imagem `pequenojim-web:1.0` criada.
5. `docker compose exec redis redis-cli ping` — retorno `PONG`.
6. `curl -i http://localhost:8000/health` — HTTP 200.
7. Comandos de testes com retorno `OK`.
8. Opcional: página aberta na porta 8000, exibindo o wallpaper e o contador.

Para a entrega, o arquivo **`compose.yaml`** é o principal. É recomendável enviar também o repositório (ou o ZIP com os arquivos do projeto), `compose.test.yaml` e os prints, de acordo com o formulário da atividade.

## Passo 7 — Encerrar o ambiente

Desligue os serviços:

```bash
docker compose down
```

Depois entre em `https://github.com/codespaces`, clique no menu de três pontos do Codespace e escolha **Stop codespace**. Fechar a aba do navegador **não** o interrompe imediatamente. Se não for utilizá-lo novamente, considere **Delete** para evitar consumo de armazenamento; o código continua salvo no repositório GitHub.

## Explicação resumida da arquitetura

```text
Navegador -> Porta 8000 -> Contêiner web (Flask)
                                  |
                             rede_pequenojim
                                  |
                          Contêiner Redis
                                  |
                         Volume dados_redis
```

**Banco/cache:** Redis armazena e recupera o contador.  
**Rede:** `rede_pequenojim` permite a comunicação entre os serviços.  
**Volume:** `dados_redis` mantém os dados entre recriações normais dos contêineres.  
**Reinicialização:** `unless-stopped` reinicia os serviços em falhas, exceto após parada explícita.  
**Saúde:** ambos os serviços têm verificações `healthcheck`; a aplicação aguarda o Redis saudável.  
**CI:** o segundo Compose adiciona testes, executados automaticamente pelo GitHub Actions.
