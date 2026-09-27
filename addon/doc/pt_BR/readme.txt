# ChatGPT Companion 0.1.2 — versão experimental

Por Fernando de Paula Zamboni. https://www.blog.fernandozamboni.com

Lê mensagens enviadas, respostas e avisos de andamento disponíveis à acessibilidade na conversa ativa do ChatGPT, sem mover o foco. Usa a voz e a saída braille do NVDA. Interface e documentação: português brasileiro, inglês, espanhol, francês e italiano.

## Alterações na versão 0.1.2

A opção Ignorar avisos e textos da interface fica ativada por padrão. Retira o bloco final conhecido “O ChatGPT pode cometer erros. Confira informações importantes.” seguido de “Resposta mais recente”, tanto da leitura automática quanto do atalho de repetir. Não faz substituição global: frases isoladas, exemplos entre aspas e referências no meio da resposta são preservados. O reconhecimento é textual; se uma resposta terminar literalmente com o mesmo bloco completo, desative a opção para ouvi-lo. Outros rodapés ainda não reconhecidos podem permanecer.

Também evita recolocar uma resposta antiga na fila quando surge um novo envio ou quando uma resposta já anunciada desaparece e reaparece na árvore de acessibilidade. A alternativa por silêncio agora começa em 3 segundos em instalações novas; suas configurações existentes são preservadas. A versão 0.1.1 teve leitura automática confirmada pelo usuário no Chrome e no aplicativo Windows, com essa alternativa. Esta atualização ainda deve ser testada nos dois ambientes antes da publicação.

## Alteração na versão 0.1.1

Corrigida a repetição da mensagem enviada enquanto a página atualizava o texto. Cada novo envio é anunciado uma vez; alterações do mesmo trecho e desaparecimentos temporários não geram outro anúncio. Um novo envio com texto idêntico continua sendo reconhecido. Para não ouvir nada ao enviar, desmarque Ler mensagens enviadas e Confirmar o envio. Editar uma mensagem já enviada, sem criar outra, não provoca nova leitura automática.

## Instalação e primeiro teste
Abra fzChatGPTCompanion-0.1.2.nvda-addon, confirme a instalação no NVDA e reinicie o leitor quando solicitado. A faixa de compatibilidade declarada é NVDA 2025.1 a 2026.2; ainda precisa ser confirmada em Windows real. O campo lastTestedNVDAVersion identifica o alvo de compatibilidade deste pacote experimental, não um teste de execução realizado.

Comece no Chrome, em https://chatgpt.com, com uma conversa curta. Aguarde cerca de dois segundos e envie uma pergunta simples. O complemento deve ler “Você disse”, os avisos reconhecidos e a resposta ao concluir. Não lê o histórico automaticamente. Ao mudar de aba, conversa ou aplicativo, estabelece uma nova referência e não anuncia o que ocorreu enquanto você estava fora. Mantenha a conversa ativa durante o teste.

Edge, Firefox, Brave e o aplicativo ChatGPT para Windows são alvos experimentais. O aplicativo precisa expor um documento com texto estruturado. Não há garantia de funcionamento antes do teste em cada ambiente. Este complemento não usa API do ChatGPT nem precisa de chave ou pagamento adicional de API.

## Configurações
No menu NVDA, abra Preferências, Configurações e ChatGPT Companion. Navegue com Tab, altere as opções com Espaço ou as setas e confirme em OK. Salve as configurações do NVDA caso o salvamento ao sair esteja desativado.

- Ativar leitura automática: liga ou desliga o monitoramento.
- Ler mensagens enviadas: lê o conteúdo depois que ele aparece na conversa, não apenas ao pressionar Enter.
- Confirmar o envio: quando a opção anterior está desativada, anuncia apenas “Mensagem enviada”. Desmarque ambas para silêncio no envio.
- Ler respostas e ler atualizações de andamento: opções independentes.
- Resposta completa: padrão; aguarda um controle de envio reconhecido e dois segundos sem alteração do texto.
- Novos parágrafos: experimental; lê parágrafos concluídos durante a geração. Uma revisão do texto pelo site pode causar repetição. Respostas sem parágrafos podem aguardar o final.
- Espera após a conclusão: de 1 a 10 segundos; padrão de 2 segundos.
- Alternativa por silêncio: de 0 a 60 segundos; 0 desativa e o padrão para novas instalações é 3. Se não houver controle de geração reconhecido, um valor como 8 permite inferir o final após silêncio. Pode antecipar a leitura durante uma pausa; não é garantia de conclusão.

## Atalhos
NVDA significa Insert ou Caps Lock, conforme sua configuração. Os atalhos podem ser alterados em Preferências, Gestos de entrada, ChatGPT Companion.

- NVDA+Control+Shift+G: ativar ou desativar a leitura automática.
- NVDA+Control+Shift+R: ler a última resposta disponível, inclusive parcial se ainda estiver sendo gerada. Funciona também com a leitura automática desativada.
- NVDA+Control+Shift+P: consultar o último aviso de andamento disponível.
- NVDA+Control+Shift+D: ouvir o diagnóstico: número de mensagens reconhecidas e estado do controle de geração.
- Control: interromper a fala atual, conforme o comportamento normal do NVDA. Para impedir os próximos anúncios, use o atalho G acima.

## Limitações e solução de problemas
“Pensamento” significa somente um aviso ou resumo exposto pela interface. O complemento não recupera raciocínio interno, textos ocultos ou conteúdo que o aplicativo não disponibilize ao NVDA. Reconhece cabeçalhos de autor e controles em cinco idiomas; mudanças da interface podem exigir atualização. Imagens, anexos e fórmulas não recebem interpretação especial.

Se o diagnóstico informar zero mensagens, confirme que a conversa contém uma mensagem enviada e experimente o modo de navegação com NVDA+Espaço. Se necessário, tente Chrome ou Edge. Se houver mensagens e o controle não for detectado, experimente a alternativa por silêncio ou a leitura manual. Conversas acima de 250 mil caracteres são ignoradas para limitar o processamento. Conversas longas abaixo desse limite ainda podem afetar o desempenho.

A página e o próprio NVDA podem anunciar regiões dinâmicas por conta própria; isso pode duplicar a fala. Desative a leitura de andamento do complemento se necessário. O complemento não suprime globalmente os anúncios nativos do leitor.

Para relatar um problema, informe navegador ou versão do aplicativo, versão do NVDA, idioma da interface e a mensagem do diagnóstico. Não é necessário enviar o conteúdo da conversa. Teste também mudança de aba, instalação, remoção, salvamento das opções e os quatro atalhos antes de publicar.

## Privacidade, licença e distribuição
Não acessa rede, cookies, senha, área de transferência ou arquivos das conversas. Processa o texto acessível em memória apenas enquanto a conversa está ativa, sem salvar ou enviar seu conteúdo. Funciona fora das telas seguras do Windows. As opções são guardadas pelo NVDA.

Software livre sob GNU GPL versão 2 ou posterior, sem garantia. Consulte COPYING.txt. Projeto independente, sem vínculo com OpenAI ou NV Access. O manifest.ini da raiz está em inglês; traduções ficam em locale. Antes do envio à Store, valide no Windows, confirme a compatibilidade declarada, publique código-fonte e um endereço HTTPS direto para o pacote. A estrutura do pacote não garante aprovação na Store.
