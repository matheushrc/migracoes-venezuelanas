ENTREVISTA_PROMPT: str = """Analise a entrevista fornecida e extraia e categorize as informações a seguir:

- Motivações para Migrar da Venezuela: Dividir os motivos de migração em duas categorias principais, baseando-se na distinção entre o que é "factual/econômico" (ligado a dados e condições objetivas ou de "Realidade") e o que é "político/afetivo" (ligado a ideologia, emoção, crenças ou circunstâncias de polarização e perseguição, baseados em "Percepção").
    - motivos_fatuais_economicos: Listar todas as razões mencionadas que se referem a condições objetivas ou materiais (a "realidade" de mercado, pobreza, escassez ou a busca por estabilidade econômica). Forneça uma lista de palavras ou frases curtas.
    - motivos_politicos_afetivos: Listar todas as razões mencionadas que se referem a percepções subjetivas, apelos à emoção, crenças pessoais, ressentimento social ou questões de perseguição política. Incluir motivações ligadas à polarização e ao alinhamento ou antagonismo ideológico/partidário. Forneça uma lista de palavras ou frases curtas.
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
