"""
Inteligência Artificial aplicada à Visão Computacional
Capítulo 7: Visão Computacional aplicada ao rastreamento de objetos

Todos os direitos reservados à Facti, 2024

www.qualifacti.com.br

É importante esclarecer que estas atividades não compõem a avaliação e não haverá correção formal por parte dos instrutores;
o objetivo é a autoaprendizagem e prática.

-----------------------------------------------------------------------------------------------------------------------
ETAPA CONSOLIDAR

Recado importante
Olá,
Como parte do capítulo de rastreamento de objetos, gostaríamos de ressaltar a importância de realizar as atividades de
implementação fornecidas. Estas atividades são cuidadosamente desenhadas para reforçar o conteúdo apresentado. Lembre-se,
a implementação é uma habilidade que se aprimora com a prática. Ao aplicar os conceitos aprendidos, especialmente por meio
da escrita e execução de códigos, você ganhará uma compreensão mais profunda e prática dos modelos. Encorajamos todos a
dedicar tempo a essas atividades. Ao fazer isso, você não apenas reforçará o que foi ensinado, mas também desenvolverá
as habilidades essenciais de resolução de problemas e depuração de código.

Lembrem-se: não basta apenas aprender, é preciso codificar! O caminho para dominar os modelos começa com a experiência prática.

Atenciosamente,
Júlio e Marcelo

-----------------------------------------------------------------------------------------------------------------------
ORIENTAÇÕES:

#1 - Antes de iniciar e executar o código, abra a aba Terminal, localizada na parte inferior do PyCharm e execute, na
sequência, os seguintes comandos para instalar os recursos da biblioteca do OpenCV:

pip install opencv-python

pip install opencv-contrib-python

#2 - Para executar o código:
    * Clique em Run;
    * Visualize o rastreamento;
    * Pressione Enter para encerrar a qualquer momento.

-----------------------------------------------------------------------------------------------------------------------

Estudo de Caso

"""

# Importando bibliotecas
import cv2
import numpy as np

# Carrega um vídeo para análise do arquivo especificado
# cap = cv2.VideoCapture("./tracking_material/videos/walking.avi")
cap = cv2.VideoCapture(0)
ret, first_frame = cap.read() # Lê o primeiro frame do vídeo
frame_gray_init = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY) # Converte o primeiro frame para escala de cinza



# Cria uma matriz HSV (hue, saturation, value) com as mesmas dimensões e tipo do frame
hsv = np.zeros_like(first_frame)
hsv[..., 1] = 255

# Loop para processar cada frame do vídeo
while True:
    
    ret, frame = cap.read() # Lê o frame atual do vídeo
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Converte o frame atual para escala de cinza

    # Calcula o fluxo óptico denso usando o algoritmo de Farneback
    flow = cv2.calcOpticalFlowFarneback(frame_gray_init,
                                        frame_gray,
                                        None,
                                        0.5,  # Escala de pirâmide
                                        3,    # Níveis de pirâmide
                                        15,   # Tamanho da janela
                                        3,    # Iterações em cada nível de pirâmide
                                        5,    # Tamanho do pixel vizinho
                                        1.2,  # Constante de suavização
                                        0)    # Flags
    # Converte as componentes do fluxo (x, y) em magnitude e ângulo
    magnitude, angle = cv2.cartToPolar(flow[...,0], flow[...,1])
    # Ajusta o canal de matiz (hue) da matriz HSV com base no ângulo
    hsv[...,0] = angle * (180 / (np.pi / 2))
    # Normaliza a magnitude para o intervalo [0, 255] e ajusta o canal de valor da matriz HSV
    hsv[...,2] = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX)
    # Converte a matriz HSV de volta para o espaço de cores BGR para visualização
    final = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    # Exibe o resultado do fluxo óptico denso em uma janela
    cv2.imshow('Dense optical flow', final)
    # if cv2.waitKey(1) == 13:     # Aguarda por uma tecla ser pressionada; se a tecla 'Enter' for pressionada, interrompe o loop
        # break

    key = cv2.waitKey(1)
    if key == 27:
        break

    # Atualiza o frame inicial para o frame atual para a próxima iteração
    frame_gray_init = frame_gray

# Libera a captura de vídeo e fecha todas as janelas abertas
cap.release()
cv2.destroyAllWindows()