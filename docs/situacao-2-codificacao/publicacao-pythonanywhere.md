# Publicação gratuita no PythonAnywhere

O PythonAnywhere hospeda aplicações Flask de graça e mantém o arquivo do banco SQLite entre os acessos.

## Passo a passo

1. Crie uma conta gratuita (plano **Beginner**) em https://www.pythonanywhere.com.
2. No painel, abra **Consoles → Bash** e rode:
   ```bash
   git clone https://github.com/SEU-USUARIO/agendafacil.git
   cd agendafacil
   pip3 install --user -r requirements.txt
   ```
3. Vá em **Web → Add a new web app → Manual configuration → Python 3.10** (ou a versão mais nova oferecida).
4. Na página do web app:
   - **Source code:** `/home/SEU-USUARIO/agendafacil`
   - **Working directory:** `/home/SEU-USUARIO/agendafacil`
5. Clique no link do **WSGI configuration file**, apague o conteúdo e cole:
   ```python
   import sys, os
   caminho = '/home/SEU-USUARIO/agendafacil'
   if caminho not in sys.path:
       sys.path.insert(0, caminho)
   os.environ['SECRET_KEY'] = 'coloque-aqui-uma-frase-longa-e-secreta'
   from run import app as application
   ```
6. Em **Static files**, adicione: URL `/static/` → Directory `/home/SEU-USUARIO/agendafacil/app/static`.
7. Clique em **Reload** (botão verde). O sistema fica em `https://SEU-USUARIO.pythonanywhere.com`.

## Atualizar depois de uma correção

```bash
cd ~/agendafacil && git pull
```
Depois clique em **Reload** na aba Web.

> No plano gratuito, o PythonAnywhere pede que você entre no painel e clique em "Run until 3 months from today" a cada 3 meses para manter o site no ar.
