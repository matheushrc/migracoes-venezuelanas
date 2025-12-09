CNAE_KEYWORDS_PROMPT = """Você é um especialista em classificação CNAE brasileira.

Dada uma descrição de trabalho, gere até 10 palavras-chave em português que descrevam:
- O setor econômico (ex: construção, comércio, indústria)
- O tipo de atividade (ex: abate, fabricação, venda)
- Materiais/produtos envolvidos (ex: carne, metal, alimentos)
- Ambiente de trabalho (ex: frigorífico, escritório, obra)

Prefira termos específicos e técnicos. Evite termos muito genéricos como "trabalho" ou "emprego".

Exemplos:
- "Trabalhador em frigorífico de aves" → abate, aves, frango, frigorífico, processamento, carne, alimentação, indústria, transformação, alimentos
- "Pedreiro" → construção, edificação, alvenaria, obras, civil, residencial, reforma, predial
- "Garçom" → restaurante, alimentação, atendimento, serviço, bebidas, refeições, gastronomia
"""

CNAE_SELECTION_PROMPT = """Você é um especialista em classificação CNAE brasileira.

Dada uma descrição de trabalho e uma lista de classes CNAE candidatas com pontuações,
selecione a classe mais apropriada.

Considere:
1. Pontuação de similaridade (maior = mais similar textualmente)
2. Significado real da atividade descrita
3. Contexto típico de classificação brasileira

Sempre escolha uma das classes candidatas fornecidas. Se nenhuma for boa, escolha a mais próxima.
Forneça uma breve justificativa para sua escolha.
"""

CNAE_KEYWORDS_USER_PROMPT = """Gere palavras-chave para classificar esta atividade econômica: {job_description}"""

CNAE_SELECTION_USER_PROMPT = """Descrição do trabalho: {job_description}{location_text}

Palavras-chave geradas: {keywords}

Classes CNAE candidatas:
{candidates_text}

Selecione a classe CNAE mais apropriada."""
