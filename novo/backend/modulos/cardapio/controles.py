from core.conexao_banco import ConexaoBanco
import mysql.connector
import logging

logger = logging.getLogger(__name__)

class CardapioControle:

    # ── Itens ────────────────────────────────────────────────────────────────

    @staticmethod
    def cadastrar_item(restaurante_id: int, dados: dict):
        conn = ConexaoBanco.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            # Verificar se o restaurante existe
            cursor.execute("SELECT id FROM restaurantes WHERE id = %s", (restaurante_id,))
            if not cursor.fetchone():
                return {"erro": "Restaurante não encontrado", "status_code": 404}

            # Validação de campos obrigatórios
            if not dados.get("nome"):
                return {"erro": "O nome do item é obrigatório", "status_code": 400}

            preco = dados.get("preco")
            if preco is None or float(preco) <= 0:
                return {"erro": "O preço deve ser maior que zero", "status_code": 400}

            query = """
                INSERT INTO itens_cardapio (nome, preco, descricao, id_restaurante)
                VALUES (%s, %s, %s, %s)
            """
            valores = (
                dados["nome"],
                float(preco),
                dados.get("descricao"),
                restaurante_id,
            )
            cursor.execute(query, valores)
            conn.commit()

            item_id = cursor.lastrowid
            return {"mensagem": "Item cadastrado com sucesso", "id": item_id, "status_code": 201}

        except mysql.connector.Error as err:
            logger.error(f"Erro no banco de dados: {err}")
            return {"erro": "Erro interno ao cadastrar item", "status_code": 500}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def listar_itens(restaurante_id: int):
        conn = ConexaoBanco.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT id FROM restaurantes WHERE id = %s", (restaurante_id,))
            if not cursor.fetchone():
                return {"erro": "Restaurante não encontrado", "status_code": 404}

            cursor.execute(
                "SELECT * FROM itens_cardapio WHERE id_restaurante = %s",
                (restaurante_id,)
            )
            itens = cursor.fetchall()
            return {"itens": itens, "status_code": 200}

        except mysql.connector.Error as err:
            logger.error(f"Erro ao listar itens: {err}")
            return {"erro": "Erro interno ao listar itens", "status_code": 500}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def buscar_item(restaurante_id: int, item_id: int):
        conn = ConexaoBanco.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT * FROM itens_cardapio WHERE id = %s AND id_restaurante = %s",
                (item_id, restaurante_id)
            )
            item = cursor.fetchone()
            if not item:
                return {"erro": "Item não encontrado", "status_code": 404}

            return {"item": item, "status_code": 200}

        except mysql.connector.Error as err:
            logger.error(f"Erro ao buscar item: {err}")
            return {"erro": "Erro interno ao buscar item", "status_code": 500}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def atualizar_item(restaurante_id: int, item_id: int, dados: dict):
        conn = ConexaoBanco.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT id FROM itens_cardapio WHERE id = %s AND id_restaurante = %s",
                (item_id, restaurante_id)
            )
            if not cursor.fetchone():
                return {"erro": "Item não encontrado", "status_code": 404}

            # Revalidar preço caso seja enviado na atualização
            if "preco" in dados and float(dados["preco"]) <= 0:
                return {"erro": "O preço deve ser maior que zero", "status_code": 400}

            campos = []
            valores = []
            for campo, valor in dados.items():
                if campo in ["nome", "preco", "descricao"]:
                    campos.append(f"{campo} = %s")
                    valores.append(valor)

            if not campos:
                return {"erro": "Nenhum campo válido para atualização fornecido", "status_code": 400}

            valores.append(item_id)
            query = f"UPDATE itens_cardapio SET {', '.join(campos)} WHERE id = %s"
            cursor.execute(query, tuple(valores))
            conn.commit()

            return {"mensagem": "Item atualizado com sucesso", "status_code": 200}

        except mysql.connector.Error as err:
            logger.error(f"Erro ao atualizar item: {err}")
            return {"erro": "Erro interno ao atualizar item", "status_code": 500}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def remover_item(restaurante_id: int, item_id: int):
        conn = ConexaoBanco.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT id FROM itens_cardapio WHERE id = %s AND id_restaurante = %s",
                (item_id, restaurante_id)
            )
            if not cursor.fetchone():
                return {"erro": "Item não encontrado", "status_code": 404}

            cursor.execute("DELETE FROM itens_cardapio WHERE id = %s", (item_id,))
            conn.commit()

            return {"mensagem": "Item removido com sucesso", "status_code": 200}

        except mysql.connector.Error as err:
            logger.error(f"Erro ao remover item: {err}")
            return {"erro": "Erro interno ao remover item", "status_code": 500}
        finally:
            cursor.close()
            conn.close()

    # ── Categorias ───────────────────────────────────────────────────────────

    @staticmethod
    def cadastrar_categoria(restaurante_id: int, dados: dict):
        conn = ConexaoBanco.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT id FROM restaurantes WHERE id = %s", (restaurante_id,))
            if not cursor.fetchone():
                return {"erro": "Restaurante não encontrado", "status_code": 404}

            if not dados.get("nome"):
                return {"erro": "O nome da categoria é obrigatório", "status_code": 400}

            # Impedir categoria duplicada no mesmo restaurante
            cursor.execute(
                "SELECT id FROM categorias WHERE nome = %s AND id_restaurante = %s",
                (dados["nome"], restaurante_id)
            )
            if cursor.fetchone():
                return {"erro": "Já existe uma categoria com este nome", "status_code": 400}

            cursor.execute(
                "INSERT INTO categorias (nome, id_restaurante) VALUES (%s, %s)",
                (dados["nome"], restaurante_id)
            )
            conn.commit()

            return {"mensagem": "Categoria criada com sucesso", "id": cursor.lastrowid, "status_code": 201}

        except mysql.connector.Error as err:
            logger.error(f"Erro ao cadastrar categoria: {err}")
            return {"erro": "Erro interno ao cadastrar categoria", "status_code": 500}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def listar_categorias(restaurante_id: int):
        conn = ConexaoBanco.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT id FROM restaurantes WHERE id = %s", (restaurante_id,))
            if not cursor.fetchone():
                return {"erro": "Restaurante não encontrado", "status_code": 404}

            # Retorna categorias com seus itens já agrupados
            cursor.execute(
                "SELECT * FROM categorias WHERE id_restaurante = %s",
                (restaurante_id,)
            )
            categorias = cursor.fetchall()

            for categoria in categorias:
                cursor.execute(
                    "SELECT * FROM itens_cardapio WHERE id_categoria = %s",
                    (categoria["id"],)
                )
                categoria["itens"] = cursor.fetchall()

            return {"categorias": categorias, "status_code": 200}

        except mysql.connector.Error as err:
            logger.error(f"Erro ao listar categorias: {err}")
            return {"erro": "Erro interno ao listar categorias", "status_code": 500}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def atualizar_categoria(restaurante_id: int, categoria_id: int, dados: dict):
        conn = ConexaoBanco.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT id FROM categorias WHERE id = %s AND id_restaurante = %s",
                (categoria_id, restaurante_id)
            )
            if not cursor.fetchone():
                return {"erro": "Categoria não encontrada", "status_code": 404}

            campos = []
            valores = []
            for campo, valor in dados.items():
                if campo in ["nome"]:
                    campos.append(f"{campo} = %s")
                    valores.append(valor)

            if not campos:
                return {"erro": "Nenhum campo válido para atualização fornecido", "status_code": 400}

            valores.append(categoria_id)
            query = f"UPDATE categorias SET {', '.join(campos)} WHERE id = %s"
            cursor.execute(query, tuple(valores))
            conn.commit()

            return {"mensagem": "Categoria atualizada com sucesso", "status_code": 200}

        except mysql.connector.Error as err:
            logger.error(f"Erro ao atualizar categoria: {err}")
            return {"erro": "Erro interno ao atualizar categoria", "status_code": 500}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def remover_categoria(restaurante_id: int, categoria_id: int):
        conn = ConexaoBanco.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT id FROM categorias WHERE id = %s AND id_restaurante = %s",
                (categoria_id, restaurante_id)
            )
            if not cursor.fetchone():
                return {"erro": "Categoria não encontrada", "status_code": 404}

            # Desvincula os itens antes de remover a categoria
            cursor.execute(
                "UPDATE itens_cardapio SET id_categoria = NULL WHERE id_categoria = %s",
                (categoria_id,)
            )
            cursor.execute("DELETE FROM categorias WHERE id = %s", (categoria_id,))
            conn.commit()

            return {"mensagem": "Categoria removida com sucesso", "status_code": 200}

        except mysql.connector.Error as err:
            logger.error(f"Erro ao remover categoria: {err}")
            return {"erro": "Erro interno ao remover categoria", "status_code": 500}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def associar_categoria(restaurante_id: int, item_id: int, categoria_id: int):
        conn = ConexaoBanco.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            # Verificar se o item pertence ao restaurante
            cursor.execute(
                "SELECT id, id_categoria FROM itens_cardapio WHERE id = %s AND id_restaurante = %s",
                (item_id, restaurante_id)
            )
            item = cursor.fetchone()
            if not item:
                return {"erro": "Item não encontrado", "status_code": 404}

            # Regra de exclusividade: item já possui categoria
            if item["id_categoria"] is not None:
                return {
                    "erro": "Este item já pertence a uma categoria e não pode ser associado a outra",
                    "status_code": 409
                }

            # Verificar se a categoria pertence ao mesmo restaurante
            cursor.execute(
                "SELECT id FROM categorias WHERE id = %s AND id_restaurante = %s",
                (categoria_id, restaurante_id)
            )
            if not cursor.fetchone():
                return {"erro": "Categoria não encontrada", "status_code": 404}

            cursor.execute(
                "UPDATE itens_cardapio SET id_categoria = %s WHERE id = %s",
                (categoria_id, item_id)
            )
            conn.commit()

            return {"mensagem": "Item associado à categoria com sucesso", "status_code": 200}

        except mysql.connector.Error as err:
            logger.error(f"Erro ao associar categoria: {err}")
            return {"erro": "Erro interno ao associar categoria", "status_code": 500}
        finally:
            cursor.close()
            conn.close()

    # ── Cardápio público ─────────────────────────────────────────────────────

    @staticmethod
    def gerar_link_publico(restaurante_id: int):
        conn = ConexaoBanco.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT id, slug_publico FROM restaurantes WHERE id = %s", (restaurante_id,))
            restaurante = cursor.fetchone()
            if not restaurante:
                return {"erro": "Restaurante não encontrado", "status_code": 404}

            # Idempotente: retorna o slug existente se já houver um
            if restaurante["slug_publico"]:
                return {"slug": restaurante["slug_publico"], "status_code": 200}

            import secrets
            slug = f"{restaurante_id}-cardapio-{secrets.token_urlsafe(6)}"
            cursor.execute(
                "UPDATE restaurantes SET slug_publico = %s WHERE id = %s",
                (slug, restaurante_id)
            )
            conn.commit()

            return {"slug": slug, "status_code": 201}

        except mysql.connector.Error as err:
            logger.error(f"Erro ao gerar link público: {err}")
            return {"erro": "Erro interno ao gerar link público", "status_code": 500}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def cardapio_publico(slug: str):
        conn = ConexaoBanco.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT id, nome FROM restaurantes WHERE slug_publico = %s",
                (slug,)
            )
            restaurante = cursor.fetchone()
            if not restaurante:
                return {"erro": "Cardápio não encontrado", "status_code": 404}

            restaurante_id = restaurante["id"]

            # Busca categorias com itens agrupados
            cursor.execute(
                "SELECT * FROM categorias WHERE id_restaurante = %s",
                (restaurante_id,)
            )
            categorias = cursor.fetchall()
            for categoria in categorias:
                cursor.execute(
                    "SELECT * FROM itens_cardapio WHERE id_categoria = %s",
                    (categoria["id"],)
                )
                categoria["itens"] = cursor.fetchall()

            # Itens sem categoria
            cursor.execute(
                "SELECT * FROM itens_cardapio WHERE id_restaurante = %s AND id_categoria IS NULL",
                (restaurante_id,)
            )
            itens_sem_categoria = cursor.fetchall()

            return {
                "restaurante": restaurante["nome"],
                "categorias": categorias,
                "itens_sem_categoria": itens_sem_categoria,
                "status_code": 200
            }

        except mysql.connector.Error as err:
            logger.error(f"Erro ao buscar cardápio público: {err}")
            return {"erro": "Erro interno ao buscar cardápio", "status_code": 500}
        finally:
            cursor.close()
            conn.close()