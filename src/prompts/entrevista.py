ENTREVISTA_PROMPT: str = """Você é um pesquisador especializado em migrações venezuelanas.
Analise a entrevista fornecida e extraia as informações estruturadas descritas no schema de saída.

## Motivações para migrar

Classifique cada motivação em uma das seis subdivisões abaixo.
O campo `motivo` deve conter exatamente a string indicada entre aspas — não use paráfrases.

### Motivos Fatuais / Econômicos — dimensão da Realidade
Condições tangíveis, objetivas e materiais que tornaram a migração necessária ou viável.

- **"Apoio Institucional e Humanitário"** — suporte logístico, material ou estrutural fornecido por
  organizações (ONGs, governos, igrejas) que objetivamente viabilizou a migração. O tom do trecho é
  prático e operacional (ex.: transporte, abrigo, documentação, rotas organizadas).
- **"Busca por Oportunidades Financeiras"** — relatos de procura de emprego, fuga da hiperinflação,
  necessidade de renda ou busca por estabilidade econômica.
- **"Escassez e Condições Básicas de Sobrevivência"** — fuga da falta de alimentos, medicamentos ou
  infraestrutura básica no país de origem.

### Motivos Políticos / Afetivos — dimensão da Percepção/Afeto
Percepções subjetivas, emoções, crenças e perseguição política que motivaram a migração.

- **"Reunificação e Laços Familiares"** — peso emocional de reconstituir o núcleo familiar ou buscar
  amparo de parentes que já migraram (ex.: cônjuge que partiu meses antes, tias já estabelecidas no
  destino).
- **"Redes de Apoio Comunitário e Religioso"** — senso de pertencimento, segurança emocional e
  acolhimento proporcionado por grupos sociais ou religiosos. O tom do trecho é afetivo: fraternidade,
  identidade coletiva, sensação de ser recebido.
- **"Clima Político e Insegurança"** — desejo de fugir de polarização política, perseguição ideológica
  ou sensação de opressão pelo Estado.

### Regras de classificação

- Um mesmo trecho pode mapear para subdivisões de **categorias diferentes** quando ambas as dimensões
  estiverem presentes. Nesse caso, inclua-o nas duas listas com formulações distintas que capturem
  cada dimensão separadamente.
  Exemplo típico: uma passagem sobre organização religiosa pode ser
  "Apoio Institucional e Humanitário" (tom prático) **e** "Redes de Apoio Comunitário e Religioso"
  (tom afetivo) ao mesmo tempo.
- Se nenhuma motivação de determinada categoria for mencionada, retorne uma lista vazia para ela.

## Movimentações trabalhistas

Registre todos os vínculos de emprego ou atividade econômica mencionados.
Deixe `setor_atividade` como `null` — este campo é preenchido por uma etapa posterior do pipeline.
Se o ano de um vínculo não for mencionado nem puder ser inferido com segurança, use `null`.

## Deslocamento

Registre cada cidade distinta por onde a pessoa passou, incluindo a cidade de origem e o destino final.
Omita menções a localidades que não representem uma parada real na trajetória (ex.: cidades citadas
apenas como referência geográfica ou contexto histórico).
Se apenas o mês e ano forem conhecidos, use o primeiro dia do mês (ex.: 2019-06-01).
Se somente o ano for conhecido, use 1º de janeiro daquele ano (ex.: 2020-01-01) e registre a
incerteza no campo `motivo` quando relevante.
"""
