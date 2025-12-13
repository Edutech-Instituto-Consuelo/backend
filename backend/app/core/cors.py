from fastapi.middleware.cors import CORSMiddleware

def setup_cors(app):
	"""Função que configura o CORS, ou seja, define quais rotas podem acessar a api
	Configuração passa pelo middleware para verificação

	em origins, deve adicionar as rotas permitidas, em desenvolvimento, colocar '*' para tudos
	"""

	origins = [
		"http://localhost:5173",  # O local que confirmaram no chat (Vite)
		"http://localhost:3000",  # Deixei o 3000 caso alguém rode nesse também
		"https://plataforma-instituto-consuelo.vercel.app" # A URL de produção (sem a barra / no final)
	]

	app.add_middleware(
		CORSMiddleware,
		allow_origins=origins,
		allow_credentials=True,
		allow_methods=["*"],
		allow_headers=["*"],
	)
