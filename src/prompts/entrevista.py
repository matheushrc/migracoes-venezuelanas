ENTREVISTA_PROMPT = """Analise a entrevista fornecida e extraia as informações a seguir:

- Motivações para Migrar da Venezuela:
    - motivos_migracao: Listar todos os motivos que levaram a pessoa entrevistada a migrar da Venezuela até exaurir todas as razões mencionadas. Forneça uma lista de palavras ou frases curtas que representem esses motivos.
- Movimentações Trabalhistas:
    Liste todas as movimentações trabalhistas da pessoa entrevistada, incluindo cargos ocupados, locais de trabalho, tipos de movimento (admissão, desligamento, transferência, etc.), motivos associados e datas. Para cada movimentação, forneça:
        - descricao_atividade: descrição da atividade ou cargo ocupado pela pessoa entrevistada.
        - localidade: local onde a pessoa entrevistada trabalhou.
        - setor_atividade: setor de atividade econômica do local de trabalho.
        - tipo_movimento: tipo de movimento trabalhista relacionado ao cargo e local de trabalho.
        - motivo_movimento: motivo associado ao movimento trabalhista.
        - ano: ano em que o movimento trabalhista ocorreu.
- Deslocamento:
    Liste as cidades ou locais por onde a pessoa entrevistada passou desde o local de origem até o destino final. Um deslocamento só acontece se ele sair de uma cidade a outra. Para cada local, forneça:
        - localidade: 
            - cidade: <nome da cidade>
            - estado_provincia: <nome do estado ou província, se aplicável>
            - pais: <sigla do país no formato ISO 3166-1 alpha-3>
        - motivo: motivo do deslocamento para esta localidade
"""
