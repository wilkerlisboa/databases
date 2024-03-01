import cv2
import mysql.connector

# Conectar ao banco de dados MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="lIsboa123*",
    database="empresa"
)
cursor = conn.cursor()

# Inicializando a captura de vídeo da câmera do notebook
video_capture = cv2.VideoCapture(0)

while True:
    # Capturando frame a frame
    ret, frame = video_capture.read()

    # Verificando se a leitura do frame foi bem-sucedida
    if not ret:
        print("Erro na leitura do frame. Verifique a conexão com a câmera.")
        break

    # Convertendo a imagem para escala de cinza para a detecção facial
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Utilizando um classificador de face pré-treinado do OpenCV
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # ID do aluno que queremos buscar no banco de dados
    n_id = 1

    # Iterando sobre cada rosto encontrado
    for (x, y, w, h) in faces:
        # Desenhando um retângulo roxo mais forte ao redor do rosto
        cv2.rectangle(frame, (x, y), (x+w, y+h), (148, 0, 211), 2)

        # Consultando informações no banco de dados para o aluno com ID 1
        cursor.execute("SELECT N_ID, NOME, CPF, RG, CURSO FROM alunos WHERE N_ID = %s", (n_id,))
        aluno_info = cursor.fetchone()

        # Verificando se a consulta retornou resultados
        if aluno_info is not None:
            # Criando uma lista com as linhas de informações
            info_lines = [
                f"ID: {aluno_info[0]}",
                f"Nome: {aluno_info[1]}",
                f"CPF: {aluno_info[2]}",
                f"RG: {aluno_info[3]}",
                f"Curso: {aluno_info[4]}"
            ]

            # Posicionando o texto dentro do retângulo
            font = cv2.FONT_HERSHEY_DUPLEX
            for i, line in enumerate(info_lines):
                cv2.putText(frame, line, (x + 150, y + 20 * (i+1)), font, 0.4, (255, 255, 255), 1, cv2.LINE_AA)

        else:
            print(f"Aluno com ID {n_id} não encontrado no banco de dados")

    # Exibindo o resultado
    cv2.imshow('ODIN', frame)

    # Encerrando o loop ao pressionar a tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberando os recursos
video_capture.release()
cv2.destroyAllWindows()

# Fechando a conexão com o banco de dados
conn.close()
