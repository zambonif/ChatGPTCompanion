# ChatGPT Companion

Por Fernando de Paula Zamboni. Versão 0.1.3 (beta).

ChatGPT Companion é um complemento do NVDA para acompanhar novas mensagens no site e no aplicativo Windows do ChatGPT. Pode ler respostas automaticamente, ler ou confirmar suas mensagens enviadas e anunciar avisos acessíveis de andamento, sem mover o foco do teclado.

## Para que serve?

O objetivo é acompanhar a conversa sem precisar sair repetidamente do campo de mensagem para procurar a resposta mais recente. Você continua usando sua conta e a interface habitual do ChatGPT. Não é preciso outro cliente, chave de API ou pagamento adicional de API. A fala e o braille seguem a configuração do NVDA.

Outros complementos podem oferecer recursos semelhantes. Este projeto se concentra em anúncios automáticos na interface existente, com opções independentes para mensagens enviadas, respostas e andamento. É um auxílio opcional à acessibilidade, não substitui melhorias de acessibilidade no próprio ChatGPT.

## Instalação

Baixe ChatGPTCompanion-0.1.3.nvda-addon, abra com o NVDA funcionando, confirme a instalação e reinicie o leitor. Requer NVDA 2026.2 ou posterior; a versão de API declarada como testada é 2026.2. Versões futuras do NVDA podem exigir revisão de compatibilidade.

Downloads: https://github.com/zambonif/ChatGPTCompanion/releases

Código-fonte e relatos de problemas: https://github.com/zambonif/ChatGPTCompanion

## Começando

Abra o ChatGPT no Chrome ou no aplicativo Windows, deixe a conversa ativa por um momento e envie uma pergunta. O autor confirmou a leitura nos dois ambientes em testes de versões anteriores. A versão 0.1.3 traz novas correções que ainda precisam ser testadas no uso real. Edge, Firefox e Brave são alvos experimentais adicionais.

Ao abrir uma conversa existente, o histórico não é anunciado. O complemento monitora somente a conversa ativa e lembra até oito contextos visitados durante a sessão do NVDA. Se você sair de uma conversa já reconhecida e voltar após a resposta chegar, poderá ouvir essa nova resposta ao retornar. Não há leitura em segundo plano. Reiniciar o NVDA ou alternar o monitoramento pelo atalho limpa essa memória.

## Configurações

Abra o menu NVDA, Preferências, Configurações, ChatGPT Companion. A atualização preserva suas opções. Salve a configuração do NVDA se o salvamento automático estiver desativado.

- Ativar leitura automática: liga ou desliga o monitoramento.
- Ler mensagens enviadas: lê sua mensagem depois que ela aparece na conversa.
- Confirmar o envio: anuncia apenas “Mensagem enviada” quando a leitura das próprias mensagens está desativada. Desative as duas opções para silêncio no envio.
- Ler respostas e Ler atualizações de andamento: opções independentes.
- Ignorar avisos e textos da interface: ativada por padrão; remove blocos de rodapé reconhecidos no fim do texto. Desative se um exemplo literal desse rodapé no final da resposta for removido.
- Resposta completa: aguarda um controle de conclusão reconhecido e texto estável. Novos parágrafos é uma alternativa experimental para leitura durante a geração.
- Espera após a conclusão: de 1 a 10 segundos; padrão 2.
- Alternativa por silêncio: de 0 a 60 segundos; padrão 3 em instalações novas. É usada quando o controle de geração não é reconhecido. Uma pausa longa pode parecer o final; aumente o valor se a leitura começar cedo demais. O valor 0 desativa essa alternativa.

## Atalhos

NVDA significa Insert ou Caps Lock, conforme sua configuração. Altere os atalhos em Preferências, Gestos de entrada, ChatGPT Companion.

- NVDA+Control+Shift+G: ativar ou desativar a leitura automática.
- NVDA+Control+Shift+R: ler a última resposta disponível. Quando uma pergunta mais recente aguarda resposta, a anterior não é usada em seu lugar. Uma resposta ainda em geração pode estar incompleta.
- NVDA+Control+Shift+P: ler o último aviso acessível de andamento.
- NVDA+Control+Shift+D: atualizar e informar o diagnóstico das mensagens recentes e do controle de geração.
- Control: interromper a fala atual conforme o comportamento normal do NVDA. Use o atalho G para impedir os próximos anúncios automáticos.

## Problemas e limitações

Se nada for lido, confira Ler respostas, teste os atalhos R e D e verifique a alternativa por silêncio. A contagem do diagnóstico corresponde ao trecho recente examinado, não à conversa inteira. Experimente o modo de navegação com NVDA+Espaço se a conversa não for reconhecida.

O complemento lê cabeçalhos de autor e texto acessível. Não recupera conteúdo que o ChatGPT não disponibiliza ao NVDA. Quando não consegue obter a resposta atual, informa que não há resposta disponível em vez de usar deliberadamente uma resposta antiga em cache. Mudanças da interface ainda podem afetar a detecção. Não interpreta imagens, anexos ou fórmulas de maneira especial. Andamento significa avisos acessíveis da interface, não raciocínio interno.

A versão 0.1.3 busca mensagens recentes a partir do fim do documento, em vez de rejeitar históricos acima de 250 mil caracteres. Respostas individuais enormes ou interfaces sem navegação por cabeçalhos ainda podem causar lentidão ou leitura incompleta. A busca alternativa alcança até 2.560 linhas a partir do fim.

Anúncios nativos da página podem duplicar a fala; desativar a leitura de andamento do complemento pode ajudar. Ao relatar problemas, informe versão do NVDA, navegador/aplicativo, idioma da interface, diagnóstico e passos para reproduzir. Não é necessário compartilhar o conteúdo privado da conversa.

## Novidades da versão 0.1.3

Melhorias na leitura de conversas longas e históricos com campos de edição. O atalho de repetição consulta texto atualizado. O estado das conversas recentes é preservado nas trocas temporárias de foco. A documentação de uso foi separada dos documentos de desenvolvimento e testes. O manifesto aponta para o repositório do projeto e exige NVDA 2026.2 como versão mínima.

## Privacidade e licença

O complemento não faz conexões de rede nem acessa senhas, cookies ou a área de transferência. Mantém temporariamente texto acessível em memória, sem salvá-lo ou enviá-lo. As preferências são guardadas pelo NVDA. Não funciona nas telas seguras do Windows.

Software livre sob GNU GPL versão 2 ou posterior, sem garantia. Projeto independente, sem vínculo com OpenAI ou NV Access. Interface e ajuda disponíveis em português brasileiro, inglês, espanhol, francês e italiano.
