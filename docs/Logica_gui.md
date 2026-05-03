## Gui

### Decisões

* AO iniciar o modo gui, deve aparecer um botão para adicionar mais videos
* Ao clicar no botão para adicionar mais videos, deve abrir uma janela que permita selecionar um ou mais videos
* Se quiser o pessoa pode clicar no botão novamente para adicionar mais videos, e o programa deve guarda o caminho de cada uma dos locais desse video para processamento
* os videos que foram selecionados aparece abaixo, com o caminho e ao lado uma opção para remove-lo da seleção
* no final dessa primeira janela deve ter um botão de proximo que vai guiar o usuario para uma proxima janela de configuração
* na janela de configuração o usuario tem todos os tipos de configuração que nos disponibilizamos para poder configurar os valores de acordo com o esperado
* no final dessa janela deve haver 3 botões voltar onde o usuario volta para a janela de seleção de videos, para deselecionar ou adicionar mais videos a lista. O outro botão é o de preview interativo e o ultimo botão é o botão de procesamento que vai processar cada video selecionado com os parametros definidos.
* ao decidir por preview interativo enquanto o programa estiver processando deve se abrir uma janela informando o processo dos processamento dos videos que ja tem o preview e os que ainda faltam e uma janela de loading, não deve se esquecer da opção de cancelar  para interroper o modo de preview
* ao carregar as informações do video o preview interativo deve abrir uma nova janela com o preview interativo, no preview interativo deve ter alem de um botão de processamento um botão de fechar para a pessoa volta a tela de parametrização caso decida fazer um ajuste
* ao clicar no botão de processar seja na janela de parametrização ou no preview interativo deve se abrir uma janela de loading informando para o usuario o andamanetodo processo e depois uma janela de conclusão
* apos concluido o processo o usuario volta a janela de seleção de video como se houver aberto o programa novamente. 


## Estrutura de 3 Painéis no Preview - layout preview interativo 
┌──────────────────────────────────────────────────────
│       VIDEO CLIP AUTOMATION - PREVIEW               │
├──────────┬───────────────────┬──────────────────────┤
│  VÍDEOS  │    PLAYER         │    CLIPS             │
│          │                   │                      │
│  □ vid1  │  ┌──────────┐     │  [1] 00:00-00:15     │
│  □ vid2  │  │          │     │  [2] 00:20-00:35     │
│  □ vid3  │  │  Video   │     │  [3] 00:45-01:10     │
│          │  │          │     │  [4] 01:20-01:50     │
│          │  └──────────┘     │                      │
│          ├───────────────────┤                      │
│          │ [◀]     [▶]       │ [Processar] [fechar] │
└──────────┴───────────────────┴──────────────────────┘