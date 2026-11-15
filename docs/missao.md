# Missão — RetroFPS Engine

Desenvolver uma engine de jogos 2.5D em Python como projeto universitário de estudo, utilizando Wolfenstein 3D como referência conceitual para a representação e a exploração de ambientes. O objetivo é aprender os fundamentos de computação gráfica e engenharia de software durante a implementação, sem pressupor conhecimento prévio de raycasting ou construção de engines.

A engine deverá carregar cenários definidos externamente, representar o ambiente em perspectiva e oferecer movimentação e colisões. Seu núcleo de renderização será implementado pelo próprio projeto, utilizando o Pygame para janela, entrada e apresentação gráfica.

A arquitetura deverá permitir que jogos diferentes utilizem os mesmos mecanismos de mundo, câmera, renderização e movimento. Objetivos, inventário, pontuação e condições de vitória pertencem aos jogos que utilizarem a engine. A reutilização será construída de forma incremental, com interfaces pequenas e compreensíveis.

A entrega mínima será uma engine funcional acompanhada de uma demonstração na qual seja possível explorar um pequeno mapa sem atravessar paredes. Texturas, objetos, portas, inimigos e combate são extensões opcionais. Não é necessário reproduzir todos os recursos de Wolfenstein 3D nem carregar seus arquivos originais.

O escopo inicial utiliza uma grade bidimensional, paredes verticais de altura uniforme, piso e teto planos e câmera com rotação horizontal. Desníveis, câmera inclinada e ambientes sobrepostos ficam fora desse recorte.

O sucesso será avaliado pelo funcionamento da solução e pelo aprendizado demonstrado: compreender os algoritmos, explicar decisões, reconhecer limitações e validar resultados. O uso de IA deverá apoiar esse processo com explicações, alterações revisáveis e registros das contribuições relevantes.
