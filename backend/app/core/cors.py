from fastapi.middleware.cors import CORSMiddleware

def setup_cors(app):
	"""Função que configura o CORS, ou seja, define quais rotas podem acessar a api
	Configuração passa pelo middleware para verificação

	em origins, deve adicionar as rotas permitidas, em desenvolvimento, colocar '*' para tudos
	"""

	origins = ["*"]

	app.add_middleware(
		CORSMiddleware,
		allow_origins=origins,
		allow_credentials=True,
		allow_methods=["*"],
		allow_headers=["*"],
	)
