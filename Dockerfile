# Derivando da imagem oficial do MySQL
FROM mysql:latest
# Adicionando os scripts SQL para serem executados na criação do banco
COPY ./src/database/scripts/ /docker-entrypoint-initdb.d/